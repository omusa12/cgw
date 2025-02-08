from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, constr

class VehicleUsage(str, Enum):
    PERSONAL = "personal"
    COMMERCIAL = "commercial"

class Vehicle(BaseModel):
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

    class Config:
        json_schema_extra = {
            "example": {
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
