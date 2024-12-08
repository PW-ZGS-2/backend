import os
from fastapi import APIRouter

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session

from pricing.rest_models import TelescopePricing, UserPricing

pricing_router = APIRouter(prefix="/pricing")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pricing_router.get(
    "/client/{user_id}", response_model=UserPricing
)
async def user_pricing(
    user_id: str,
    db: Session = Depends(get_db),
):
    return UserPricing(total_cost="20.7$",
user_id="123",
telescopes = [TelescopePricing(usage_time="20m",
telescope_id="8bf5a669-2f7d-455b-89d6-dc4ea47ddb4b",
price=14.3), TelescopePricing(usage_time="9m",
telescope_id="c101179a-554a-48ac-9a0e-1397c13ff66b",
price=6.4)])

@pricing_router.get(
    "/sharer/{user_id}", response_model=UserPricing
)
async def sharer_pricing(
    user_id: str,
    db: Session = Depends(get_db),
):
    return UserPricing(total_earn="20.7$",
user_id="123",
telescopes = [TelescopePricing(usage_time="20m",
telescope_id="8bf5a669-2f7d-455b-89d6-dc4ea47ddb4b",
price=14.3), TelescopePricing(usage_time="9m",
telescope_id="c101179a-554a-48ac-9a0e-1397c13ff66b",
price=6.4)])
