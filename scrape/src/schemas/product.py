from typing import Optional
from pydantic import BaseModel, Field
from .base import BaseSchema, TimestampedSchema
from ..models.product import ProductType

class ProductBase(BaseSchema):
    name: str
    dealer_cost: int = Field(..., ge=0)  # Amount in cents
    max_model_years: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    sku: str

class WarrantyProductBase(ProductBase):
    type: ProductType
    term: Optional[str] = None  # e.g., "24 month", "No Time Limit"
    distance: Optional[str] = None  # e.g., "Unlimited km", "40000 km"
    claim_amount: Optional[int] = None  # Maximum claim amount in cents
    max_model_km: Optional[int] = Field(None, ge=0)
    commercial_eligible: bool = False
    sku_type: str = "App\\Products\\Warranty\\CGWWarrantyProduct"

class WarrantyProduct(WarrantyProductBase, TimestampedSchema):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
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
                "sku_type": "App\\Products\\Warranty\\CGWWarrantyProduct",
                "created_at": "2024-01-28T12:00:00Z"
            }
        }

class GAPProductBase(ProductBase):
    type: str = "GAP"
    term_months: int = Field(..., ge=1, le=120)
    double_gap: bool = False
    sku_type: str = "App\\Products\\GAP\\CGWGAPProduct"

class GAPProduct(GAPProductBase, TimestampedSchema):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Standard GAP 84 months",
                "term_months": 84,
                "dealer_cost": 74900,
                "double_gap": False,
                "max_model_years": 7,
                "sku": "DGAP84",
                "sku_type": "App\\Products\\GAP\\CGWGAPProduct",
                "created_at": "2024-01-28T12:00:00Z"
            }
        }

class ProtectionProductBase(ProductBase):
    type: str
    sku_type: str = "App\\Products\\Protection\\PaintInteriorRustProduct"

class ProtectionProduct(ProtectionProductBase, TimestampedSchema):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Paint Protection",
                "type": "Paint/Interior/Rust",
                "dealer_cost": 49900,
                "max_model_years": 7,
                "sku": "CAPP-C",
                "sku_type": "App\\Products\\Protection\\PaintInteriorRustProduct",
                "created_at": "2024-01-28T12:00:00Z"
            }
        }

# Request/Response schemas for product operations
class ProductCreate(BaseSchema):
    product_type: str = Field(..., description="Type of product to create: warranty, gap, or protection")
    data: dict = Field(..., description="Product data matching the appropriate product type schema")

class ProductUpdate(BaseSchema):
    dealer_cost: Optional[int] = Field(None, ge=0)
    max_model_years: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow additional fields based on product type
