"""
API Endpoints for the AI Beauty Concierge.
"""

import logging
import json
from typing import List, Dict, Any
import httpx
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.salon import Salon
from app.models.service import Service
from app.models.user import User
from app.models.recommendation import SavedRecommendation
from app.schemas.recommendation import SavedRecommendationCreate, SavedRecommendationOut
from app.schemas.concierge import (
    ConciergeRequest,
    ConciergeResponse,
    HairstyleRecommendation,
    ServiceRecommendation,
    SalonRecommendation,
    FaceAnalysisResponse,
    MakeupRecommendation,
    DressAnalysisResponse,
)
from app.core.config import settings

router = APIRouter(prefix="/api/concierge", tags=["AI Concierge"])
logger = logging.getLogger(__name__)


# ── Gemini Response Schema ───────────────────────────────────────
# Define the expected JSON Schema for Gemini's structured response.
GEMINI_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "recommended_hairstyles": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "description": {"type": "STRING"}
                },
                "required": ["name", "description"]
            }
        },
        "recommended_services": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "description": {"type": "STRING"},
                    "price_estimate": {"type": "NUMBER"},
                    "salon_id": {"type": "INTEGER"},
                    "service_id": {"type": "INTEGER"}
                },
                "required": ["name", "description", "price_estimate", "salon_id"]
            }
        },
        "recommended_salons": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "reason": {"type": "STRING"},
                    "salon_id": {"type": "INTEGER"}
                },
                "required": ["name", "reason", "salon_id"]
            }
        },
        "estimated_budget": {"type": "NUMBER"},
        "explanation": {"type": "STRING"}
    },
    "required": [
        "recommended_hairstyles",
        "recommended_services",
        "recommended_salons",
        "estimated_budget",
        "explanation"
    ]
}


# ── POST /api/concierge/recommend ────────────────────────────────

@router.post(
    "/recommend",
    response_model=ConciergeResponse,
    summary="Get bespoke AI beauty & salon recommendations",
)
async def get_beauty_recommendations(
    payload: ConciergeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get bespoke beauty, hairstyle, and salon recommendations using Gemini.
    If GEMINI_API_KEY is not set, a realistic mock recommendation is returned.
    """
    # 1. Fetch salons and services database context
    db_salons = db.query(Salon).all()
    db_services = db.query(Service).all()

    if not db_salons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No salons available in database to recommend.",
        )

    # 2. Check for Gemini API Key; if missing, generate mock response
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not configured. Falling back to mock recommendations.")
        return generate_mock_recommendations(payload, db_salons, db_services)

    # 3. Format database data for LLM context
    salons_context = []
    for s in db_salons:
        salons_context.append({
            "id": s.id,
            "name": s.name,
            "area": s.area,
            "price_range": s.price_range,
            "description": s.description,
            "rating": s.rating
        })

    services_context = []
    for s in db_services:
        services_context.append({
            "id": s.id,
            "salon_id": s.salon_id,
            "service_name": s.service_name,
            "category": s.category,
            "price": s.price,
            "duration": s.duration_minutes,
            "description": s.description
        })

    # 4. Build prompt
    prompt = f"""
You are the AI Luxury Style Director & Concierge for "Aura Elite", a luxury salon portal in Bangalore.
Provide bespoke beauty and styling recommendations for the following user:

USER PROFILE:
- Occasion: {payload.occasion}
- Budget (Max INR): {payload.budget} INR
- Preferred Location: {payload.location} (if "All Locations", search all areas)
- Hair Type / Texture: {payload.hair_type}

AVAILABLE SALONS (You MUST only recommend from these salons):
{json.dumps(salons_context, indent=2)}

AVAILABLE SERVICES (You MUST only recommend services that match these, linking them using `salon_id` and `service_id`):
{json.dumps(services_context, indent=2)}

INSTRUCTIONS:
1. Suggest 2-3 suitable hairstyles for the occasion and hair type.
2. Select 1-2 salons and corresponding actual services from the provided lists that fit the location preference and total budget.
3. Calculate the estimated budget based on the exact services recommended. Ensure the total is under the user's budget if possible.
4. Fill in the correct `salon_id` and `service_id` for every recommended service.
5. Write a personalized, premium explanation in an elegant, sophisticated concierge tone. Show expertise about hair care and Bangalore locations.
"""

    # 5. Call Gemini API
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": GEMINI_RESPONSE_SCHEMA,
            "temperature": 0.2
        }
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(api_url, json=request_body)
            
            if res.status_code != 200:
                logger.error(f"Gemini API error: {res.status_code} - {res.text}")
                # Fallback to mock on API error
                return generate_mock_recommendations(payload, db_salons, db_services)

            response_data = res.json()
            # Extract generated text
            generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
            recommendations_dict = json.loads(generated_text)

            # Map the parsed JSON back to ConciergeResponse pydantic model
            return ConciergeResponse(
                recommended_hairstyles=[
                    HairstyleRecommendation(**h) for h in recommendations_dict.get("recommended_hairstyles", [])
                ],
                recommended_services=[
                    ServiceRecommendation(**s) for s in recommendations_dict.get("recommended_services", [])
                ],
                recommended_salons=[
                    SalonRecommendation(**s) for s in recommendations_dict.get("recommended_salons", [])
                ],
                estimated_budget=recommendations_dict.get("estimated_budget", 0.0),
                explanation=recommendations_dict.get("explanation", ""),
                is_mock=False
            )

    except Exception as e:
        logger.error(f"Failed to get Gemini recommendation: {str(e)}")
        # Return fallback mock response on exception
        return generate_mock_recommendations(payload, db_salons, db_services)


# ── Mock Generator Fallback ──────────────────────────────────────

def generate_mock_recommendations(
    payload: ConciergeRequest,
    salons: List[Salon],
    services: List[Service]
) -> ConciergeResponse:
    """
    Generates realistic, context-aware mock recommendations based on DB data.
    Ensures correct structure and ID matching for testing and demo purposes.
    """
    # 1. Filter salons matching location if possible
    matched_salons = salons
    if payload.location.lower() != "all locations":
        matched_salons = [s for s in salons if payload.location.lower() in s.area.lower()]
        if not matched_salons:  # Fallback
            matched_salons = salons

    # 2. Pick a salon and a service that fits within budget
    selected_salon = matched_salons[0]
    selected_service = None

    # Try to find a service in the budget
    salon_services = [s for s in services if s.salon_id == selected_salon.id]
    if not salon_services:
        salon_services = services

    for s in salon_services:
        if s.price <= payload.budget:
            selected_service = s
            break

    # If no service fits, just pick the cheapest one
    if not selected_service:
        selected_service = min(salon_services, key=lambda s: s.price)

    # 3. Generate visual hairstyle suggestions based on hair type and occasion
    hair_type = payload.hair_type.lower()
    occasion = payload.occasion.lower()

    hairstyles = []
    if "curly" in hair_type or "coily" in hair_type:
        hairstyles = [
            HairstyleRecommendation(
                name="Defined Deva Cut Layers",
                description=f"A layered cut tailored specifically for your beautiful natural curls to add structure and prevent the 'triangle' shape, perfect for a {payload.occasion}."
            ),
            HairstyleRecommendation(
                name="Luxury Hollywood Wave Updo",
                description="Glamorous, structured pinned-up curls styled with high-shine serum to withstand humidity and keep you looking elegant throughout the evening."
            )
        ]
    else:  # Straight or wavy
        hairstyles = [
            HairstyleRecommendation(
                name="Bespoke Sleek Parisian Blowout",
                description="Ultra-smooth, glossy blowout with gentle inward-curving ends for a sophisticated look that highlights hair health."
            ),
            HairstyleRecommendation(
                name="Textured Crown Chignon",
                description=f"An elegant, low bun with soft face-framing waves, combining classic poise with contemporary ease, fitting for a {payload.occasion}."
            )
        ]

    # 4. Build recommendations
    rec_services = [
        ServiceRecommendation(
            name=selected_service.service_name,
            description=selected_service.description or "Elite beauty therapy.",
            price_estimate=selected_service.price,
            salon_id=selected_salon.id,
            service_id=selected_service.id
        )
    ]

    rec_salons = [
        SalonRecommendation(
            name=selected_salon.name,
            reason=f"Selected for its proximity in {selected_salon.area} and exceptional {selected_service.category} expertise. Fits your budget with premium styling services starting from {selected_salon.price_range}.",
            salon_id=selected_salon.id
        )
    ]

    # Add a second service if budget allows
    remaining_budget = payload.budget - selected_service.price
    if remaining_budget > 1500:
        # Find another cheap service in the same salon or different salon
        other_svcs = [s for s in services if s.id != selected_service.id and s.price <= remaining_budget]
        if other_svcs:
            second_svc = other_svcs[0]
            second_salon = next((s for s in salons if s.id == second_svc.salon_id), selected_salon)
            
            rec_services.append(
                ServiceRecommendation(
                    name=second_svc.service_name,
                    description=second_svc.description or "Premium grooming ritual.",
                    price_estimate=second_svc.price,
                    salon_id=second_salon.id,
                    service_id=second_svc.id
                )
            )

            # Add second salon if it's different
            if second_salon.id != selected_salon.id:
                rec_salons.append(
                    SalonRecommendation(
                        name=second_salon.name,
                        reason=f"Recommended for additional {second_svc.category} treatments that fit within your remaining budget.",
                        salon_id=second_salon.id
                    )
                )

    total_est = sum(s.price_estimate for s in rec_services)

    explanation = (
        f"For your upcoming {payload.occasion}, we recommend focusing on defining your {payload.hair_type} hair "
        f"with high-end treatments at {selected_salon.name} in {selected_salon.area}. "
        f"Their {selected_service.service_name} will perfectly complement your style while respecting "
        f"your maximum budget constraint of ₹{payload.budget:,.2f}. "
        f"Our curated choices ensure you receive the finest standard of Bangalore grooming."
    )

    return ConciergeResponse(
        recommended_hairstyles=hairstyles,
        recommended_services=rec_services,
        recommended_salons=rec_salons,
        estimated_budget=total_est,
        explanation=explanation,
        is_mock=True
    )


# ── Gemini Face Response Schema ──────────────────────────────────
GEMINI_FACE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "face_shape": {"type": "STRING"},
        "recommended_hairstyles": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "description": {"type": "STRING"}
                },
                "required": ["name", "description"]
            }
        },
        "explanation": {"type": "STRING"}
    },
    "required": ["face_shape", "recommended_hairstyles", "explanation"]
}


# ── POST /api/concierge/analyze-face ─────────────────────────────

@router.post(
    "/analyze-face",
    response_model=FaceAnalysisResponse,
    summary="Analyze face shape from selfie using Gemini Vision",
)
async def analyze_face_shape(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze the user's face shape from a selfie image and recommend hairstyles.
    If GEMINI_API_KEY is not set, a high-fidelity mock face analysis is returned.
    """
    # Verify file type is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a valid image.",
        )

    # Check for Gemini API Key; if missing, generate mock response
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not configured. Falling back to mock face shape analysis.")
        return generate_mock_face_analysis(file.filename)

    try:
        # Read file contents and encode to base64
        image_bytes = await file.read()
        import base64
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        prompt = """
        You are an expert AI Esthetician and Luxury Style Director for "Aura Elite".
        Analyze the provided selfie image and identify the user's face shape (Oval, Round, Square, Heart, or Diamond).
        Provide a structured analysis including:
        1. The detected face shape (choose one of: Oval, Round, Square, Heart, Diamond).
        2. A list of 3 recommended hairstyles that perfectly complement this face shape and enhance their features.
        3. A detailed, elegant, and sophisticated explanation of the analysis (why this face shape was selected and how the recommended hairstyles balance their features).

        Write a personalized explanation in an elegant concierge tone. Show expertise about style.
        """

        # Call Gemini API
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        request_body = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inlineData": {
                                "mimeType": file.content_type,
                                "data": base64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": GEMINI_FACE_SCHEMA,
                "temperature": 0.2
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(api_url, json=request_body)
            
            if res.status_code != 200:
                logger.error(f"Gemini API error during face analysis: {res.status_code} - {res.text}")
                return generate_mock_face_analysis(file.filename)

            response_data = res.json()
            generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
            analysis_dict = json.loads(generated_text)

            return FaceAnalysisResponse(
                face_shape=analysis_dict.get("face_shape", "Oval"),
                recommended_hairstyles=[
                    HairstyleRecommendation(**h) for h in analysis_dict.get("recommended_hairstyles", [])
                ],
                explanation=analysis_dict.get("explanation", ""),
                is_mock=False
            )

    except Exception as e:
        logger.error(f"Failed to get Gemini face analysis: {str(e)}")
        return generate_mock_face_analysis(file.filename)


# ── Mock Face Analysis Generator Fallback ────────────────────────

def generate_mock_face_analysis(filename: str) -> FaceAnalysisResponse:
    """
    Generates high-fidelity mock face shape analysis recommendations.
    Uses filename or simple hash-based routing to ensure deterministic styling.
    """
    # Basic deterministic choice using filename length
    shapes = ["Oval", "Round", "Square", "Heart", "Diamond"]
    idx = len(filename) % len(shapes)
    selected_shape = shapes[idx]

    # Predefined recommendations for each shape
    recommendations_db = {
        "Oval": {
            "hairstyles": [
                {"name": "Sleek Lob with Face-Framing Layers", "description": "A long bob hitting right at the collarbone. Subtle face-framing layers highlight your symmetrical oval structure without elongating it."},
                {"name": "Soft Wavy Shag with Curtain Bangs", "description": "Textured shaggy waves with curtain bangs. Curtains break up the vertical line of the face, drawing attention to your eyes."},
                {"name": "Deep Side-Parted Waves", "description": "Classic Hollywood glamour waves parted deeply. This adds volume to one side, adding drama and highlighting your cheekbones."}
            ],
            "explanation": "Oval face shapes are highly versatile and balanced. The French-trained stylists at Warren Tricomi recommend choosing cuts that maintain this natural symmetry. A collarbone-length lob or textured waves with curtain bangs are excellent selections that will accentuate your high cheekbones and soft jawline."
        },
        "Round": {
            "hairstyles": [
                {"name": "Asymmetrical Long Bob", "description": "An uneven cut that is longer in the front. This draws the eye downward, creating the illusion of length and minimizing roundness."},
                {"name": "Voluminous Pixie Cut with Side Bangs", "description": "Short textured top with clean sides. Elevating the height at the crown elongates the face and adds modern architectural lines."},
                {"name": "Long Shaggy Layers", "description": "Long textured layers starting past the chin. Avoid bulk at the cheeks and create length while providing natural movement."}
            ],
            "explanation": "Round face shapes benefit from styles that introduce structure, height, and length. Play Salon UB City stylists suggest an asymmetrical lob or a pixie cut with crown volume. These techniques create flattering angles, elongating the silhouette and framing your cheeks with elegant, lengthening shadows."
        },
        "Square": {
            "hairstyles": [
                {"name": "Wispy Layered Shoulder Cut", "description": "Feathery layers starting from the collarbone. Soft, wispy texture breaks the sharp angles of a strong jawline."},
                {"name": "Side-Swept Soft Fringe", "description": "A long, sweeping side fringe. This softens the forehead and draws attention diagonally rather than horizontally."},
                {"name": "Tousled Beachy Waves", "description": "Textured, loose waves. Curved texture offsets the straight lines of the forehead and jaw, creating a harmonious, romantic look."}
            ],
            "explanation": "Square face shapes boast strong, gorgeous jawlines and broad foreheads. The Method Precision Haircut at Rossano Ferretti is designed to soften these striking angles. By creating soft, wispy layers and long side-swept fringes, our directors neutralize horizontal lines, surrounding your face in a frame of gentle, rounded waves."
        },
        "Heart": {
            "hairstyles": [
                {"name": "Chin-Length Textured Bob", "description": "A classic bob landing right at the chin. This adds volume at the jawline, balancing the wider forehead and narrower chin."},
                {"name": "Side-Swept Wispy Bangs with Long Waves", "description": "Long, flowing waves with a diagonal fringe. Side-swept bangs reduce the width of the forehead while keeping the focus on the eyes."},
                {"name": "Layered Collarbone Shag", "description": "Shaggy layers focused from the chin down. Creates texture and fullness where the face is narrowest, balancing your overall profile."}
            ],
            "explanation": "Heart face shapes feature a wider forehead and a delicate, pointed chin. To balance this silhouette, JCB Lavelle Road stylists recommend adding volume and width around the jawline. A chin-length textured bob or collarbone-length shag with side-swept bangs achieves a stunning proportions, softening the forehead and framing the chin."
        },
        "Diamond": {
            "hairstyles": [
                {"name": "Chin-Length Classic Bob", "description": "A bob ending right at the chin. Fills in the space around the jaw, balancing the prominent cheekbones and narrow chin."},
                {"name": "Deep Side-Part with Voluminous Waves", "description": "A dramatic side part with fullness. Draws attention to one side while softening the diamond angles with wavy movement."},
                {"name": "Soft Curtain Bangs with Layers", "description": "Wispy curtain bangs paired with long layers. Curtain bangs cover part of the narrow forehead, while layers frame the jaw beautifully."}
            ],
            "explanation": "Diamond face shapes are defined by a narrow forehead and jawline with dramatic, wide cheekbones. The directors at Warren Tricomi advise choosing hairstyles that add width to the forehead and jaw while keeping the cheekbones clear. Wispy curtain bangs and a chin-length bob or deep side-parted waves will frame your natural elegance."
        }
    }

    data = recommendations_db.get(selected_shape, recommendations_db["Oval"])

    return FaceAnalysisResponse(
        face_shape=selected_shape,
        recommended_hairstyles=[
            HairstyleRecommendation(**h) for h in data["hairstyles"]
        ],
        explanation=data["explanation"],
        is_mock=True
    )


# ── Gemini Dress Response Schema ─────────────────────────────────
GEMINI_DRESS_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "dress_color": {"type": "STRING"},
        "occasion_type": {"type": "STRING"},
        "makeup_recommendations": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "description": {"type": "STRING"}
                },
                "required": ["name", "description"]
            }
        },
        "explanation": {"type": "STRING"}
    },
    "required": ["dress_color", "occasion_type", "makeup_recommendations", "explanation"]
}


# ── POST /api/concierge/analyze-dress ────────────────────────────

@router.post(
    "/analyze-dress",
    response_model=DressAnalysisResponse,
    summary="Analyze dress details and recommend makeup using Gemini Vision",
)
async def analyze_dress(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze the uploaded dress photo to detect its color and style,
    and suggest complementary luxury makeup looks and occasions.
    If GEMINI_API_KEY is not set, a high-fidelity mock dress analysis is returned.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a valid image.",
        )

    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not configured. Falling back to mock dress analysis.")
        return generate_mock_dress_analysis(file.filename)

    try:
        image_bytes = await file.read()
        import base64
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        prompt = """
        You are an expert AI Makeup Artist and Luxury Style Director for "Aura Elite".
        Analyze the provided dress image and identify:
        1. The dominant or key color of the dress (e.g. Emerald Green, Royal Blue, Pastel Pink).
        2. The most suitable luxury occasion type for this dress (e.g. Wedding Gala, Romantic Date Night, Cocktail Party, Festive Celebration).
        3. A list of 3 specific makeup recommendations (Lips, Eyes, and Complexion) that perfectly coordinate with the dress color and style.
        4. A detailed, elegant, and sophisticated explanation of the styling rationale.

        Write a personalized explanation in an elegant concierge tone.
        """

        # Call Gemini API
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        request_body = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inlineData": {
                                "mimeType": file.content_type,
                                "data": base64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": GEMINI_DRESS_SCHEMA,
                "temperature": 0.2
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(api_url, json=request_body)
            
            if res.status_code != 200:
                logger.error(f"Gemini API error during dress analysis: {res.status_code} - {res.text}")
                return generate_mock_dress_analysis(file.filename)

            response_data = res.json()
            generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
            analysis_dict = json.loads(generated_text)

            return DressAnalysisResponse(
                dress_color=analysis_dict.get("dress_color", "Royal Blue"),
                occasion_type=analysis_dict.get("occasion_type", "Cocktail Party"),
                makeup_recommendations=[
                    MakeupRecommendation(**m) for m in analysis_dict.get("makeup_recommendations", [])
                ],
                explanation=analysis_dict.get("explanation", ""),
                is_mock=False
            )

    except Exception as e:
        logger.error(f"Failed to get Gemini dress analysis: {str(e)}")
        return generate_mock_dress_analysis(file.filename)


# ── Mock Dress Analysis Generator Fallback ────────────────────────

def generate_mock_dress_analysis(filename: str) -> DressAnalysisResponse:
    """
    Generates high-fidelity mock dress color and makeup recommendations.
    Uses filename or simple hash-based routing to ensure deterministic styling.
    """
    colors = ["Royal Crimson", "Emerald Green", "Midnight Obsidian", "Champagne Gold", "Blush Rose"]
    occasions = ["Wedding Gala / Bridal", "Cocktail Party / Evening Reception", "Romantic Date Night", "Elite Corporate Meet", "Festive Celebration"]
    
    idx = len(filename) % len(colors)
    selected_color = colors[idx]
    selected_occasion = occasions[idx]

    recommendations_db = {
        "Royal Crimson": {
            "makeup": [
                {"name": "Eyes", "description": "Soft matte brown transition with subtle champagne shimmer on the lid, paired with a clean, classic black winged eyeliner to define the eyes without competing with the dress."},
                {"name": "Lips", "description": "A classic satin-finish true red lip color that matches the intensity and undertone of your crimson gown, lined precisely for an elite definition."},
                {"name": "Complexion", "description": "Velvet matte finish with a soft contour. Use a neutral dusty rose blush applied high on the cheekbones to pull the look together harmoniously."}
            ],
            "explanation": "A striking Crimson dress makes a powerful, elegant statement. To complement this, Rossano Ferretti beauty experts suggest a classic Hollywood look. Pairing a structured matte complexion with a matching crimson lip and understated warm eyes creates a timeless, high-contrast silhouette perfect for a Gala."
        },
        "Emerald Green": {
            "makeup": [
                {"name": "Eyes", "description": "Sophisticated warm bronze and copper smokey eyes with rich brown smudged eyeliner. This warm-toned contrast beautifully makes the cool emerald shade pop."},
                {"name": "Lips", "description": "A sophisticated warm nude or creamy peach lip with a touch of gloss, keeping the focus entirely on your striking eyes and dress."},
                {"name": "Complexion", "description": "Dewy, luminous skin with a warm gold highlighter. A peach blush swept across the apples of the cheeks gives a fresh, sun-kissed contrast."}
            ],
            "explanation": "Emerald Green is a rich, regal color. To balance its depth, JCB Lavelle Road styling directors advise choosing a warm bronze eyeshadow palette and a peach-toned nude lip. This gold-accented color harmony adds an air of modern Parisian elegance, perfect for a high-end Cocktail Party."
        },
        "Midnight Obsidian": {
            "makeup": [
                {"name": "Eyes", "description": "A sultry charcoal and silver smokey eye with heavy kohl along the waterlines, blended outwards for a bold, dramatic evening look."},
                {"name": "Lips", "description": "A sophisticated deep berry or cool-toned mauve lip with a matte finish, adding depth and mystery to your look."},
                {"name": "Complexion", "description": "Flawless satin finish with sharp contouring to highlight facial structure. Use a cool-toned plum highlighter for a futuristic metallic glow."}
            ],
            "explanation": "A classic Black dress is a blank canvas for high-drama styling. Warren Tricomi makeup artists recommend a bold charcoal smokey eye paired with deep plum or berry lip tones. This high-fidelity evening look emphasizes structural definition and looks magnificent under luxury lighting."
        },
        "Champagne Gold": {
            "makeup": [
                {"name": "Eyes", "description": "Gilded metallic gold eyeshadow on the inner half of the lid, blending into a warm chocolate brown outer V, finished with volumizing mascara."},
                {"name": "Lips", "description": "A glossed warm brick red or spiced terracotta lip color, adding a beautiful pop of color that enlivens the metallic dress."},
                {"name": "Complexion", "description": "Golden-hour glowing skin. Use a champagne powder highlighter on the high points of the face and a warm terracotta blush."}
            ],
            "explanation": "Champagne Gold exudes absolute opulence. To enhance this metallic luster, Play Salon stylists suggest matching the look with gilded eyes and a rich terracotta or brick red lip. This warm monochromatic glow provides a cohesive and luxurious look for elite evening receptions."
        },
        "Blush Rose": {
            "makeup": [
                {"name": "Eyes", "description": "Rose gold shimmer on the lids, blended with a soft mauve in the crease and finished with chocolate brown liner for a romantic, soft look."},
                {"name": "Lips", "description": "A soft rosebud pink lip balm or cream lipstick that mirrors the gentle, romantic hue of your dress."},
                {"name": "Complexion", "description": "Fresh, youthful glass skin with a pink liquid blush blended upwards, and a pearlescent highlighter for a natural, ethereal glow."}
            ],
            "explanation": "Blush Rose is soft, romantic, and ethereal. BBlunt Premium style directors recommend keeping the makeup soft and radiant. Using rose gold, mauve, and soft rosebud pinks creates a romantic, monochromatic harmony that accentuates your features with subtle, natural beauty."
        }
    }

    data = recommendations_db.get(selected_color, recommendations_db["Royal Crimson"])

    return DressAnalysisResponse(
        dress_color=selected_color,
        occasion_type=selected_occasion,
        makeup_recommendations=[
            MakeupRecommendation(**m) for m in data["makeup"]
        ],
        explanation=data["explanation"],
        is_mock=True
    )


# ── GET /api/concierge/saved ──────────────────────────────────────


@router.get(
    "/saved",
    response_model=List[SavedRecommendationOut],
    summary="Get user's saved concierge recommendations",
)
def get_saved_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all saved lookbooks for the authenticated user, newest first."""
    saved = (
        db.query(SavedRecommendation)
        .filter(SavedRecommendation.user_id == current_user.id)
        .order_by(SavedRecommendation.created_at.desc())
        .all()
    )
    
    # We must deserialize the JSON strings back to objects for the response
    res = []
    for r in saved:
        res.append(
            SavedRecommendationOut(
                id=r.id,
                user_id=r.user_id,
                occasion=r.occasion,
                budget=r.budget,
                location=r.location,
                hair_type=r.hair_type,
                explanation=r.explanation,
                recommended_hairstyles=json.loads(r.recommended_hairstyles),
                recommended_services=json.loads(r.recommended_services),
                recommended_salons=json.loads(r.recommended_salons),
                estimated_budget=r.estimated_budget,
                created_at=r.created_at
            )
        )
    return res


# ── POST /api/concierge/save ──────────────────────────────────────


@router.post(
    "/save",
    response_model=SavedRecommendationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Save a concierge recommendation lookbook",
)
def save_recommendation(
    payload: SavedRecommendationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save an AI styling recommendation lookbook to the user profile."""
    db_rec = SavedRecommendation(
        user_id=current_user.id,
        occasion=payload.occasion,
        budget=payload.budget,
        location=payload.location,
        hair_type=payload.hair_type,
        explanation=payload.explanation,
        recommended_hairstyles=json.dumps(payload.recommended_hairstyles),
        recommended_services=json.dumps(payload.recommended_services),
        recommended_salons=json.dumps(payload.recommended_salons),
        estimated_budget=payload.estimated_budget
    )
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)

    return SavedRecommendationOut(
        id=db_rec.id,
        user_id=db_rec.user_id,
        occasion=db_rec.occasion,
        budget=db_rec.budget,
        location=db_rec.location,
        hair_type=db_rec.hair_type,
        explanation=db_rec.explanation,
        recommended_hairstyles=payload.recommended_hairstyles,
        recommended_services=payload.recommended_services,
        recommended_salons=payload.recommended_salons,
        estimated_budget=db_rec.estimated_budget,
        created_at=db_rec.created_at
    )


# ── DELETE /api/concierge/saved/{id} ──────────────────────────────


@router.delete(
    "/saved/{id}",
    summary="Delete a saved concierge recommendation",
)
def delete_saved_recommendation(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a saved AI lookbook by ID."""
    rec = db.query(SavedRecommendation).filter(SavedRecommendation.id == id).first()
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Saved recommendation with ID {id} not found."
        )

    if rec.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this saved recommendation."
        )

    db.delete(rec)
    db.commit()
    return {"id": id, "deleted": True}
