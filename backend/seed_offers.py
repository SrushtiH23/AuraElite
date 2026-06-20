"""
Seed script for active offers.
Run from the backend directory:
    python seed_offers.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.salon import Salon
from app.models.service import Service
from app.models.booking import Booking
from app.models.review import Review
from app.models.favorite import FavoriteSalon
from app.models.recommendation import SavedRecommendation
from app.models.offer import Offer



def seed_offers():
    db = SessionLocal()

    # Check if offers already exist
    existing = db.query(Offer).count()
    if existing > 0:
        print(f"[INFO] Offers table already contains {existing} entries. Skipping seeding.")
        db.close()
        return

    # Seed list
    offers_data = [
        {
            "salon_id": 1,
            "title": "30% OFF Royal Scalp Therapy",
            "description": "Nourish your scalp with organic essential oils and luxurious steam therapy. Perfect for weekend relaxation.",
            "discount_percentage": 30,
            "original_price": 4500.0,
            "offer_price": 3150.0,
            "category": "Spa Treatments",
            "valid_until": "2026-08-31",
            "is_active": True,
        },
        {
            "salon_id": 2,
            "title": "25% OFF French Balayage Premium",
            "description": "Multi-dimensional hand-painted highlights by award-winning senior artists. Includes luxury hair wash.",
            "discount_percentage": 25,
            "original_price": 9500.0,
            "offer_price": 7125.0,
            "category": "Hair Care",
            "valid_until": "2026-07-15",
            "is_active": True,
        },
        {
            "salon_id": 5,
            "title": "50% OFF Express Blowout & Style",
            "description": "Get ready for date night with our professional creative blowout and custom heat styling finish.",
            "discount_percentage": 50,
            "original_price": 1500.0,
            "offer_price": 750.0,
            "category": "Hair Care",
            "valid_until": "2026-06-30",
            "is_active": True,
        },
        {
            "salon_id": 6,
            "title": "20% OFF Diamond Dust Facial",
            "description": "Luxe 90-minute facial utilizing genuine diamond dust exfoliation and royal 24K gold peptide infusion.",
            "discount_percentage": 20,
            "original_price": 12000.0,
            "offer_price": 9600.0,
            "category": "Skin Care",
            "valid_until": "2026-09-15",
            "is_active": True,
        },
        {
            "salon_id": 12,
            "title": "35% OFF Champagne Pedicure Spa",
            "description": "Indulge in a premium nail shaping, relaxing massage, and grooming package with complimentary champagne.",
            "discount_percentage": 35,
            "original_price": 3200.0,
            "offer_price": 2080.0,
            "category": "Nails & Grooming",
            "valid_until": "2026-07-05",
            "is_active": True,
        },
    ]

    for data in offers_data:
        # Find salon name
        salon = db.query(Salon).filter(Salon.id == data["salon_id"]).first()
        if salon:
            offer = Offer(
                salon_id=data["salon_id"],
                salon_name=salon.name,
                title=data["title"],
                description=data["description"],
                discount_percentage=data["discount_percentage"],
                original_price=data["original_price"],
                offer_price=data["offer_price"],
                category=data["category"],
                valid_until=data["valid_until"],
                is_active=data["is_active"],
            )
            db.add(offer)

    db.commit()
    db.close()
    print("[SUCCESS] Seeded active offers.")


if __name__ == "__main__":
    seed_offers()
