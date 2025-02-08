from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, constr
from .base import BaseSchema, TimestampedSchema
from ..models.vehicle import VehicleUsage

class VehicleBase(BaseSchema):
    vin: constr(min_length=17, max_length=17)
    make: str
    model: str
    year: int = Field(..., ge=1900, le=datetime.now().year + 1)
    trim: Optional[str] = None
    delivery_date: datetime
    in_service_date: datetime
    odometer: int = Field(..., ge=0)
    odometer_unit: str = Field(..., pattern="^(km|mi)$")
    transmission: str
    num_cylinders: int = Field(..., ge=0)
    drivetrain: Optional[str] = None
    fuel_type: Optional[str] = None
    vehicle_usage: VehicleUsage
    lienholder: Optional[str] = None
    price: Optional[float] = None
    hybrid_electric: Optional[bool] = False

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseSchema):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=datetime.now().year + 1)
    trim: Optional[str] = None
    delivery_date: Optional[datetime] = None
    in_service_date: Optional[datetime] = None
    odometer: Optional[int] = Field(None, ge=0)
    odometer_unit: Optional[str] = Field(None, pattern="^(km|mi)$")
    transmission: Optional[str] = None
    num_cylinders: Optional[int] = Field(None, ge=0)
    drivetrain: Optional[str] = None
    fuel_type: Optional[str] = None
    vehicle_usage: Optional[VehicleUsage] = None
    lienholder: Optional[str] = None
    price: Optional[float] = None
    hybrid_electric: Optional[bool] = None

class Vehicle(VehicleBase):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "vin": "1HGCM82633A123456",
                "make": "Honda",
                "model": "Accord",
                "year": 2023,
                "trim": "Sport",
                "delivery_date": "2023-01-15T00:00:00Z",
                "in_service_date": "2023-01-15T00:00:00Z",
                "odometer": 0,
                "odometer_unit": "km",
                "transmission": "Automatic",
                "num_cylinders": 4,
                "drivetrain": "FWD",
                "fuel_type": "Gas",
                "vehicle_usage": "personal",
                "hybrid_electric": False
            }
        }

class VehicleInDB(Vehicle, TimestampedSchema):
    pass

class VehicleValidation(BaseSchema):
    is_valid: bool
    eligible_products: list[str]
    validation_messages: list[str]
    max_coverage_amount: Optional[int] = None
    restrictions: Optional[list[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "is_valid": True,
                "eligible_products": ["Principal", "Pinnacle", "GAP"],
                "validation_messages": ["Vehicle age within acceptable range", "Mileage within limits"],
                "max_coverage_amount": 2500000,
                "restrictions": ["Commercial use requires additional documentation"]
            }
        }
