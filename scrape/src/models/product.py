from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from .base import TimestampedModel

class ProductType(str, Enum):
    PRINCIPAL = "Principal"
    PINNACLE = "Pinnacle"
    POWERTRAIN = "Powertrain"
    PLATINUM = "Platinum"
    PREMIUM = "Premium"
    GAP = "GAP"
    PROTECTION = "Protection"

class WarrantyProduct(TimestampedModel):
    name: str
    type: ProductType
    term: Optional[str] = None  # e.g., "24 month", "No Time Limit"
    distance: Optional[str] = None  # e.g., "Unlimited km", "40000 km"
    dealer_cost: int = Field(..., ge=0)  # Amount in cents
    claim_amount: Optional[int] = None  # Maximum claim amount in cents
    max_model_years: Optional[int] = Field(None, ge=0)
    max_model_km: Optional[int] = Field(None, ge=0)
    commercial_eligible: bool = False
    description: Optional[str] = None
    sku: str
    sku_type: str = "App\\Products\\Warranty\\CGWWarrantyProduct"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "PRINCIPAL - 24 month / Unlimited km",
                "type": "Principal",
                "term": "24 month",
                "distance": "Unlimited km",
                "dealer_cost": 65900,
                "claim_amount": 250000,
                "max_model_years": 15,
                "max_model_km": 210000,
                "commercial_eligible": False,
                "sku": "1PL24UNL",
                "sku_type": "App\\Products\\Warranty\\CGWWarrantyProduct"
            }
        }

class GAPProduct(TimestampedModel):
    name: str
    type: str = "GAP"
    term_months: int = Field(..., ge=1, le=120)
    dealer_cost: int = Field(..., ge=0)  # Amount in cents
    double_gap: bool = False
    max_model_years: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    sku: str
    sku_type: str = "App\\Products\\GAP\\CGWGAPProduct"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Standard GAP 84 months",
                "term_months": 84,
                "dealer_cost": 74900,
                "double_gap": False,
                "max_model_years": 7,
                "sku": "DGAP84",
                "sku_type": "App\\Products\\GAP\\CGWGAPProduct"
            }
        }

class ProtectionProduct(TimestampedModel):
    name: str
    type: str
    dealer_cost: int = Field(..., ge=0)  # Amount in cents
    max_model_years: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    sku: str
    sku_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Paint Protection",
                "type": "Paint/Interior/Rust",
                "dealer_cost": 49900,
                "max_model_years": 7,
                "sku": "CAPP-C",
                "sku_type": "App\\Products\\Protection\\PaintInteriorRustProduct"
            }
        }
