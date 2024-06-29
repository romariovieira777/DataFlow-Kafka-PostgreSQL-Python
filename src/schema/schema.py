from typing import Optional, TypeVar, Dict

from pydantic import BaseModel, Field

T = TypeVar('T')

""""
    General
"""


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    parameter: Parameter = Field(...)


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    headers: Optional[T] = None
    result: Optional[T] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenVerify(BaseModel):
    token: str


"""
    User
"""


class LoginSchema(BaseModel):
    username: str
    password: str


"""
    Pricing
"""


class PricingSchema(BaseModel):
    ammount: float
    currency: str


"""
    Availability
"""


class AvailabilitySchema(BaseModel):
    quantity: float


"""
    Product
"""


class ProductSchema(BaseModel):
    name: str
    description: str
    category: str
    pricing: PricingSchema
    availability: AvailabilitySchema

