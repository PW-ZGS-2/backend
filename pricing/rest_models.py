from pydantic import BaseModel

class TelescopePricing(BaseModel):
    usage_time: float
    telescope_id: str
    price: float


class UserPricing(BaseModel):
    total_cost: float
    user_id: str
    telescopes: list[TelescopePricing]



class SharerEarnigs(BaseModel):
    total_earn: float
    user_id: str
    telescopes: list[TelescopePricing]