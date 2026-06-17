"""
Seed script — Populates the database with 500 Bangalore luxury & premium salons.

Run from the backend directory:
    python seed.py
"""

import sys
import os
import random

# Ensure the backend package is importable
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import Base, engine, SessionLocal
from app.models.salon import Salon
from app.models.service import Service
from app.models.user import User
from app.models.booking import Booking
from app.models.review import Review
from app.models.favorite import FavoriteSalon
from app.models.recommendation import SavedRecommendation

# Neighborhood coordinate centers in Bangalore
NEIGHBORHOODS = {
    "Indiranagar": (12.9719, 77.6412),
    "UB City": (12.9715, 77.6012),
    "Ashok Nagar": (12.9723, 77.5997),
    "Koramangala": (12.9340, 77.6190),
    "HSR Layout": (12.9100, 77.6410),
    "Jayanagar": (12.9250, 77.5900),
    "Whitefield": (12.9690, 77.7500),
    "Sadashivanagar": (13.0070, 77.5800),
    "Malleshwaram": (12.9980, 77.5720),
    "JP Nagar": (12.9070, 77.5850),
    "Electronic City": (12.8450, 77.6650),
    "Bellandur": (12.9280, 77.6780),
    "Marathahalli": (12.9560, 77.6970),
    "MG Road": (12.9740, 77.6070),
    "Brigade Road": (12.9710, 77.6070),
    "Cunningham Road": (12.9820, 77.5980),
}

PREFIXES = ["The", "Elite", "Luxury", "Royal", "Signature", "Classic", "Studio", "Atelier", "Glow", "Aura", "Gold", "Urban", "Vibe"]
BRANDS = [
    "Bounce", "Bodycraft", "Vurve", "Mirrors", "Page 3", "Toni & Guy", "Lakme", "Naturals", 
    "Green Trends", "Jawed Habib", "BBlunt", "Play", "Blown", "Limelite", "Envi", "Dessange", 
    "Truefitt", "Pinkfox", "Scissors", "Stylz", "Artistry", "Gloss", "Crown", "Locks & Lashes", 
    "Trends", "Kaya", "Looks", "Enigma", "Glamour", "Orane", "Chic", "Grace", "Aesthetic", "Zenith"
]
SUFFIXES = ["Salon", "Salon & Spa", "Style Lounge", "Hair Spa", "Beauty Lounge", "Atelier", "Studio", "Grooming Lounge", "Boutique"]

FIRST_NAMES = [
    "Amit", "Rahul", "Priya", "Sunita", "Anjali", "Rohan", "Vikram", "Sneha", "Karan", "Meera", 
    "Siddharth", "Kriti", "Varun", "Nehal", "Deepak", "Aishwarya", "Rajesh", "Sanjay", "Anand", 
    "Divya", "Swati", "Arjun", "Neha", "Manish", "Gaurav", "Pooja", "Ritu", "Akash", "Aditya", 
    "Preeti", "Kunal", "Tanvi", "Kabir", "Deepa", "Nisha", "Sandeep", "Jyoti", "Raj", "Vijay"
]
LAST_NAMES = [
    "Sharma", "Patel", "Sen", "Malhotra", "Reddy", "Rao", "Das", "Nair", "Bose", "Akhtar", 
    "Sanon", "Dhawan", "Gupta", "Malik", "Karhal", "Joshi", "Verma", "Patil", "Roy", "Kapoor",
    "Nair", "Babu", "Menon", "Shenoy", "Kamath", "Hegde", "Shetty", "Pai", "Prabhu", "Gowda"
]

SERVICE_TEMPLATES = [
    {"name": "Precision Haircut & Style", "category": "Hair Care", "desc": "Signature styling cut with deep wash and blowdry", "base_price": 2500, "duration": 45},
    {"name": "Global Hair Color & Glazing", "category": "Hair Care", "desc": "Multi-dimensional rich global coloring protection", "base_price": 7500, "duration": 120},
    {"name": "Keratin Smoothing Therapy", "category": "Hair Care", "desc": "Premium protein treatment for frizz-free alignment", "base_price": 6000, "duration": 150},
    {"name": "Rehydrating Botanical Hair Spa", "category": "Hair Care", "desc": "Intensive argan-oil nourishing scalp ritual", "base_price": 3000, "duration": 60},
    {"name": "Anti-Pollution Hydra Facial", "category": "Skin Care", "desc": "Deep clinical skin hydration and glow peptide peel", "base_price": 4000, "duration": 75},
    {"name": "Deep Tissue Stress Relief Spa", "category": "Spa Treatments", "desc": "Full body relaxation massage with organic essential oils", "base_price": 4500, "duration": 90},
    {"name": "Spa Manicure & Pedicure Duo", "category": "Nails & Grooming", "desc": "Complete nail shaping, massage, and grooming", "base_price": 2200, "duration": 75},
    {"name": "Classic Beard Shave & Sculpt", "category": "Nails & Grooming", "desc": "Hot towel precision shave and beard conditioning", "base_price": 1200, "duration": 30},
]

REVIEW_TEMPLATES = {
    5: [
        "Absolutely amazing experience! The service was excellent and the staff was super friendly.",
        "Best haircut I've ever had. Highly recommend the stylists here.",
        "Very clean, luxurious environment. Total value for money if you appreciate high quality.",
        "Stellar balayage color job! Exceeded my expectations.",
        "Top-notch hygiene and world-class products. Simply outstanding."
    ],
    4: [
        "Great service, though it is a bit expensive. The styling was exactly what I wanted.",
        "Clean place and nice staff. Had to wait 10 minutes past my slot, but the treatment was very relaxing.",
        "Overall a very good experience. Will visit again for color highlights.",
        "Very courteous therapists and clean rooms. Worth the price.",
        "Professional stylists, but make sure to book ahead since weekends are super busy."
    ],
    3: [
        "Decent place, but nothing extraordinary. The wait time was too long.",
        "Service was okay but felt a bit rushed. The prices are high for the quality of care.",
        "Standard salon experience. Stylists are okay, but parking in the area is difficult.",
        "Average services. Cleanliness was good but the music was way too loud."
    ]
}

def generate_reviews(salon_name: str, rating: float) -> list[dict]:
    # Determine star category
    star = 5 if rating >= 4.7 else (4 if rating >= 4.3 else 3)
    templates = REVIEW_TEMPLATES[star]
    
    # Generate 2 to 3 reviews
    count = random.randint(2, 3)
    reviews = []
    chosen_templates = random.sample(templates, min(count, len(templates)))
    
    for template in chosen_templates:
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        reviews.append({
            "user_name": f"{first} {last}",
            "rating": random.choice([star, min(star + 1, 5)]),
            "comment": template
        })
    return reviews


def seed():
    """Insert salon, service, and review seed data."""
    # Wipe the database to ensure we get a clean seed
    print("[INFO] Re-creating database tables for 500 salons...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    # Core 12 anchor salons
    salons_data = [
        {
            "name": "Rossano Ferretti Hair Spa",
            "area": "Ashok Nagar",
            "address": "The Ritz-Carlton, Residency Road, Ashok Nagar, Bangalore 560025",
            "rating": 4.9,
            "description": "The legendary Italian 'Method' haircut by Rossano Ferretti, exclusively at The Ritz-Carlton Bangalore. Ultra-premium styling with world-class hair diagnostics.",
            "image_url": "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹₹",
            "latitude": 12.9723,
            "longitude": 77.5997,
            "services": [
                {"service_name": "The Method Precision Haircut", "category": "Hair Care", "description": "Rossano Ferretti's signature invisible haircut technique", "price": 5500, "duration_minutes": 60},
                {"service_name": "Italian Luxury Color Treatment", "category": "Hair Care", "description": "Custom blended Italian hair color with keratin infusion", "price": 12000, "duration_minutes": 120},
                {"service_name": "Royal Scalp Therapy", "category": "Spa Treatments", "description": "Deep conditioning scalp treatment with rare botanical oils", "price": 4500, "duration_minutes": 45},
                {"service_name": "24K Gold Facial", "category": "Skin Care", "description": "Premium 24-karat gold leaf facial with diamond microdermabrasion", "price": 8000, "duration_minutes": 90},
                {"service_name": "Bridal Styling Package", "category": "Hair Care", "description": "Complete bridal hair and makeup with trial session included", "price": 25000, "duration_minutes": 180},
            ],
            "reviews": generate_reviews("Rossano Ferretti Hair Spa", 4.9)
        },
        {
            "name": "Play Salon",
            "area": "UB City",
            "address": "UB City Mall, Vittal Mallya Road, Bangalore 560001",
            "rating": 4.7,
            "description": "Fashion-forward styling hub in the heart of UB City. Known for celebrity stylists, Balayage mastery, and champagne-service experience.",
            "image_url": "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹",
            "latitude": 12.9715,
            "longitude": 77.6012,
            "services": [
                {"service_name": "Celebrity Signature Haircut", "category": "Hair Care", "description": "Precision cut by award-winning stylists", "price": 3500, "duration_minutes": 45},
                {"service_name": "French Balayage Premium", "category": "Hair Care", "description": "Hand-painted highlights using imported French techniques", "price": 9500, "duration_minutes": 150},
                {"service_name": "Luxury Keratin Smoothing", "category": "Hair Care", "description": "Brazilian keratin treatment for silky smooth hair", "price": 7000, "duration_minutes": 120},
                {"service_name": "Express VIP Grooming", "category": "Nails & Grooming", "description": "Quick luxury grooming: beard trim, facial, and styling", "price": 2500, "duration_minutes": 60},
                {"service_name": "Champagne Mani-Pedi", "category": "Nails & Grooming", "description": "Premium nail care with complimentary champagne", "price": 3000, "duration_minutes": 75},
            ],
            "reviews": generate_reviews("Play Salon", 4.7)
        },
        {
            "name": "Warren Tricomi",
            "area": "Ashok Nagar",
            "address": "JW Marriott Hotel, Vittal Mallya Road, Ashok Nagar, Bangalore 560001",
            "rating": 4.8,
            "description": "New York's famed Warren Tricomi salon, housed in the JW Marriott. World-class hair artistry with a focus on precision cutting and color.",
            "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹₹",
            "latitude": 12.9720,
            "longitude": 77.5991,
            "services": [
                {"service_name": "New York Precision Cut", "category": "Hair Care", "description": "The signature Warren Tricomi precision layering technique", "price": 4500, "duration_minutes": 60},
                {"service_name": "Global Color Artistry", "category": "Hair Care", "description": "Multi-dimensional color with foiling and glazing", "price": 11000, "duration_minutes": 150},
                {"service_name": "Organic Hydrafacial", "category": "Skin Care", "description": "Medical-grade hydrafacial with organic serums", "price": 6500, "duration_minutes": 75},
                {"service_name": "Deep Tissue Body Massage", "category": "Spa Treatments", "description": "Full body deep tissue massage with aromatic oils", "price": 5000, "duration_minutes": 90},
                {"service_name": "Men's Executive Grooming", "category": "Nails & Grooming", "description": "Premium men's package: cut, shave, facial, and scalp massage", "price": 4000, "duration_minutes": 90},
            ],
            "reviews": generate_reviews("Warren Tricomi", 4.8)
        },
        {
            "name": "Jean-Claude Biguine",
            "area": "UB City",
            "address": "1 MG Road, Lavelle Road Junction, Bangalore 560001",
            "rating": 4.6,
            "description": "Parisian elegance meets Bangalore luxury. Jean-Claude Biguine offers French-trained stylists and exclusive imported product lines.",
            "image_url": "https://images.unsplash.com/photo-1633681926022-84c23e8cb2d6?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹",
            "latitude": 12.9732,
            "longitude": 77.6006,
            "services": [
                {"service_name": "Parisian Chic Haircut", "category": "Hair Care", "description": "French cutting technique for effortless style", "price": 3000, "duration_minutes": 45},
                {"service_name": "French Ombré Color", "category": "Hair Care", "description": "Seamless ombré gradient using French coloring methods", "price": 8500, "duration_minutes": 120},
                {"service_name": "Crème de la Mer Facial", "category": "Skin Care", "description": "Ultra-luxe facial using La Mer skincare products", "price": 7500, "duration_minutes": 90},
                {"service_name": "Aromatherapy Full Body Spa", "category": "Spa Treatments", "description": "Complete body ritual with French lavender and essential oils", "price": 6000, "duration_minutes": 120},
                {"service_name": "Nail Artistry & Spa Pedicure", "category": "Nails & Grooming", "description": "Custom nail art with luxury spa pedicure treatment", "price": 2800, "duration_minutes": 90},
            ],
            "reviews": generate_reviews("Jean-Claude Biguine", 4.6)
        },
        {
            "name": "BBlunt Premium",
            "area": "Indiranagar",
            "address": "100 Feet Road, Indiranagar, Bangalore 560038",
            "rating": 4.5,
            "description": "Bollywood's go-to brand BBlunt brings creative hair artistry to Indiranagar. Known for trendy cuts, vivid colors, and expert styling.",
            "image_url": "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹",
            "latitude": 12.9719,
            "longitude": 77.6398,
            "services": [
                {"service_name": "Trendsetter Haircut", "category": "Hair Care", "description": "Modern creative cut with personalized consultation", "price": 2000, "duration_minutes": 45},
                {"service_name": "Vivid Fantasy Color", "category": "Hair Care", "description": "Bold fashion colors — pastels, neons, and custom blends", "price": 6500, "duration_minutes": 120},
                {"service_name": "Express Blowout & Style", "category": "Hair Care", "description": "Quick professional blowout with heat styling", "price": 1500, "duration_minutes": 30},
                {"service_name": "Classic Clean-Up Facial", "category": "Skin Care", "description": "Deep cleansing facial for radiant skin", "price": 2500, "duration_minutes": 45},
                {"service_name": "Hair Spa Rejuvenation", "category": "Spa Treatments", "description": "Intensive hair spa with protein mask and steam therapy", "price": 3000, "duration_minutes": 60},
            ],
            "reviews": generate_reviews("BBlunt Premium", 4.5)
        },
        {
            "name": "The Spa & Salon - Leela Palace",
            "area": "Old Airport Road",
            "address": "The Leela Palace, Old Airport Road, Bangalore 560008",
            "rating": 4.9,
            "description": "The epitome of five-star luxury wellness. The Leela Palace's in-house salon and spa offers royal treatments with imported products and master therapists.",
            "image_url": "https://images.unsplash.com/photo-1600948836101-f9ffda59d250?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹₹₹",
            "latitude": 12.9610,
            "longitude": 77.6483,
            "services": [
                {"service_name": "Royal Heritage Haircut", "category": "Hair Care", "description": "Personalized styling consultation with senior master stylist", "price": 6000, "duration_minutes": 60},
                {"service_name": "Platinum Hair Restoration", "category": "Hair Care", "description": "Advanced hair repair with stem-cell technology", "price": 15000, "duration_minutes": 120},
                {"service_name": "Diamond Dust Facial", "category": "Skin Care", "description": "Exclusive facial with real diamond dust exfoliation and 24k gold serum", "price": 12000, "duration_minutes": 90},
                {"service_name": "Royal Thai Massage", "category": "Spa Treatments", "description": "Traditional Thai massage by certified therapists from Bangkok", "price": 8000, "duration_minutes": 90},
                {"service_name": "Ayurvedic Abhyanga Ritual", "category": "Spa Treatments", "description": "Ancient Ayurvedic full-body oil massage with herbal steam bath", "price": 9500, "duration_minutes": 120},
            ],
            "reviews": generate_reviews("The Spa & Salon - Leela Palace", 4.9)
        },
        {
            "name": "Franck Provost Paris",
            "area": "Indiranagar",
            "address": "1151, 12th Main Rd, HAL 2nd Stage, Indiranagar, Bengaluru, Karnataka 560008",
            "rating": 4.8,
            "description": "High-end French hair care, balayage, and personalized styling consultations by internationally trained hair experts.",
            "image_url": "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹",
            "latitude": 12.9719,
            "longitude": 77.6412,
            "services": [
                {"service_name": "French Balayage Signature", "category": "Hair Care", "description": "Classic Parisian hand-painted highlighting technique", "price": 8500, "duration_minutes": 120},
                {"service_name": "Provost Precision Haircut", "category": "Hair Care", "description": "Style haircut custom suited for your hair texture", "price": 3000, "duration_minutes": 45},
                {"service_name": "Luxury Olaplex Treatment", "category": "Hair Care", "description": "Intensive bond rebuilding treatment for chemical damage", "price": 4000, "duration_minutes": 60},
            ],
            "reviews": generate_reviews("Franck Provost Paris", 4.8)
        },
        {
            "name": "Vurve Signature Salon",
            "area": "Indiranagar",
            "address": "No. 2981, 1st Floor, Icon Mall, 12th Main Road, Indiranagar, Bangalore, Karnataka 560008",
            "rating": 4.7,
            "description": "Luxury destination for bespoke hair transformations, clinical skincare, and wedding makeups in a refined atmosphere.",
            "image_url": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹",
            "latitude": 12.9722,
            "longitude": 77.6415,
            "services": [
                {"service_name": "Vurve Bespoke Haircut", "category": "Hair Care", "description": "Creative hair styling by Vurve senior art directors", "price": 2800, "duration_minutes": 45},
                {"service_name": "Global Keratin Infusion", "category": "Hair Care", "description": "Deep nourishment and frizz-free hair alignment", "price": 7500, "duration_minutes": 150},
                {"service_name": "Anti-Aging Glow Facial", "category": "Skin Care", "description": "Customized clinical hydration and peptide treatment", "price": 4500, "duration_minutes": 75},
            ],
            "reviews": generate_reviews("Vurve Signature Salon", 4.7)
        },
        {
            "name": "Bodycraft Salon & Spa",
            "area": "Indiranagar",
            "address": "#653, 100 Feet Road, Defence Colony, Indiranagar, Bangalore 560038",
            "rating": 4.6,
            "description": "A well-established premium wellness brand offering a wide range of expert hair care, massages, and skincare therapies.",
            "image_url": "https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹",
            "latitude": 12.9712,
            "longitude": 77.6405,
            "services": [
                {"service_name": "Bodycraft Classic Haircut", "category": "Hair Care", "description": "Standard fashion haircut and wash", "price": 1800, "duration_minutes": 45},
                {"service_name": "L'Oreal Power Mix Treatment", "category": "Hair Care", "description": "Personalized hair care mask treatment", "price": 2500, "duration_minutes": 40},
                {"service_name": "Stress Relief Aromatherapy", "category": "Spa Treatments", "description": "Full body wellness therapy with soothing oils", "price": 4000, "duration_minutes": 90},
            ],
            "reviews": generate_reviews("Bodycraft Salon & Spa", 4.6)
        },
        {
            "name": "Bounce Style Lounge",
            "area": "Lavelle Road",
            "address": "First Floor, Magnolia, No. 36, Vittal Mallya Road, Bengaluru 560001",
            "rating": 4.8,
            "description": "Bespoke styling lounge popular for trendy haircuts, advanced fashion colors, and high-end French product lines.",
            "image_url": "https://images.unsplash.com/photo-1582095133179-bfd08e2fc6b3?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹",
            "latitude": 12.9720,
            "longitude": 77.5957,
            "services": [
                {"service_name": "Bounce Signature Haircut", "category": "Hair Care", "description": "Precision haircut by senior Bounce stylists", "price": 3200, "duration_minutes": 45},
                {"service_name": "Fashion Streaks & Glazing", "category": "Hair Care", "description": "Multi-dimensional hair locks color highlighting", "price": 8000, "duration_minutes": 120},
                {"service_name": "Moroccanoil Rejuvenating Spa", "category": "Hair Care", "description": "Argan-oil infused deep hydration styling treatment", "price": 3500, "duration_minutes": 60},
            ],
            "reviews": generate_reviews("Bounce Style Lounge", 4.8)
        },
        {
            "name": "Page 3 Luxury Salon",
            "area": "HSR Layout",
            "address": "No. 2734, Ground Floor, Sector 1, HSR Layout, Opposite NIFT, Bengaluru, Karnataka 560102",
            "rating": 4.7,
            "description": "Elite luxury salon offering master haircuts, advanced skin treatments, and complete corporate grooming services.",
            "image_url": "https://images.unsplash.com/photo-1605497746444-05dac3e8b04e?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹",
            "latitude": 12.9115,
            "longitude": 77.6408,
            "services": [
                {"service_name": "Page 3 Art Director Cut", "category": "Hair Care", "description": "Precision luxury haircut by style directors", "price": 3000, "duration_minutes": 50},
                {"service_name": "Charcoal Detox Facial", "category": "Skin Care", "description": "Deep pore cleansing and carbon peel mask", "price": 3800, "duration_minutes": 60},
                {"service_name": "Executive Spa Manicure", "category": "Nails & Grooming", "description": "Luxury hands grooming with collagen treatment", "price": 2000, "duration_minutes": 45},
            ],
            "reviews": generate_reviews("Page 3 Luxury Salon", 4.7)
        },
        {
            "name": "Blown",
            "area": "UB City",
            "address": "No. 23, 1st Floor, Lavelle Road, Bangalore 560001",
            "rating": 4.7,
            "description": "A premium styling blow-dry bar lounge. Ideal for quick styles, pampering body care, and relaxing with custom refreshments.",
            "image_url": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=600&auto=format&fit=crop&q=80",
            "price_range": "₹₹₹",
            "latitude": 12.9718,
            "longitude": 77.5985,
            "services": [
                {"service_name": "Blown Signature Blowout", "category": "Hair Care", "description": "Volumizing professional blowout and heat finish", "price": 2200, "duration_minutes": 40},
                {"service_name": "Luxe Caviar Hydration Treatment", "category": "Hair Care", "description": "Elite hair restoration using real caviar extracts", "price": 9000, "duration_minutes": 90},
                {"service_name": "Champagne Pedicure Spa", "category": "Nails & Grooming", "description": "Relaxing feet spa treatment with bubbly luxury drink", "price": 3200, "duration_minutes": 60},
            ],
            "reviews": generate_reviews("Blown", 4.7)
        }
    ]

    # Programmatically generate remaining 490+ salons to reach at least 500
    generated_names = set(s["name"] for s in salons_data)
    neighborhood_keys = list(NEIGHBORHOODS.keys())
    
    # Image URLs list to choose from for programmatically generated salons
    image_pool = [
        "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1633681926022-84c23e8cb2d6?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1600948836101-f9ffda59d250?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1582095133179-bfd08e2fc6b3?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1605497746444-05dac3e8b04e?w=600&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=600&auto=format&fit=crop&q=80"
    ]

    target_count = 505
    attempts = 0
    
    while len(salons_data) < target_count and attempts < 10000:
        attempts += 1
        prefix = random.choice(PREFIXES) if random.random() > 0.4 else ""
        brand = random.choice(BRANDS)
        suffix = random.choice(SUFFIXES)
        
        name = f"{prefix} {brand} {suffix}".strip()
        if name in generated_names:
            continue
            
        generated_names.add(name)
        area = random.choice(neighborhood_keys)
        center_lat, center_lon = NEIGHBORHOODS[area]
        
        # Add random offset to cluster salons realistically around neighborhood hubs
        lat = center_lat + random.uniform(-0.015, 0.015)
        lon = center_lon + random.uniform(-0.015, 0.015)
        
        rating = round(random.uniform(3.7, 4.9), 1)
        price_range = random.choice(["₹", "₹₹", "₹₹₹", "₹₹₹₹", "₹₹₹₹₹"])
        
        # Price multiplier mapping
        price_mult = {
            "₹": 0.4,
            "₹₹": 0.8,
            "₹₹₹": 1.2,
            "₹₹₹₹": 1.8,
            "₹₹₹₹₹": 2.5
        }[price_range]
        
        desc = f"Discover styling excellence at {name} in {area}. Known for its premium ambiance, friendly staff, and expert styling therapists."
        address = f"No. {random.randint(10, 999)}, {random.randint(1, 19)}th Cross, {random.randint(1, 7)}th Block, {area}, Bangalore 5600{random.randint(10, 99)}"
        image_url = random.choice(image_pool)
        
        # Programmatic services scaling
        services = []
        chosen_templates = random.sample(SERVICE_TEMPLATES, random.randint(3, 5))
        for t in chosen_templates:
            scaled_price = int(t["base_price"] * price_mult)
            # Round to nearest 50 INR
            scaled_price = max(scaled_price - (scaled_price % 50), 300)
            services.append({
                "service_name": t["name"],
                "category": t["category"],
                "description": t["desc"],
                "price": scaled_price,
                "duration_minutes": t["duration"]
            })
            
        salons_data.append({
            "name": name,
            "area": area,
            "address": address,
            "rating": rating,
            "description": desc,
            "image_url": image_url,
            "price_range": price_range,
            "latitude": lat,
            "longitude": lon,
            "services": services,
            "reviews": generate_reviews(name, rating)
        })

    for salon_data in salons_data:
        services_data = salon_data.pop("services")
        reviews_data = salon_data.pop("reviews", [])

        salon = Salon(**salon_data)
        db.add(salon)
        db.flush()

        for svc in services_data:
            service = Service(salon_id=salon.id, **svc)
            db.add(service)

        for rev in reviews_data:
            review = Review(salon_id=salon.id, **rev)
            db.add(review)

    db.commit()
    db.close()
    print(f"[SUCCESS] Seeded {len(salons_data)} real & premium Bangalore luxury salons with coordinates, services, and reviews.")


if __name__ == "__main__":
    seed()
