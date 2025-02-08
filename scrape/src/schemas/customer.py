from typing import Optional, Dict
from pydantic import BaseModel, EmailStr, Field, constr
from .base import BaseSchema, TimestampedSchema

class CustomerBase(BaseSchema):
    first_name: str
    last_name: str
    address1: str
    address2: Optional[str] = None
    city: str
    province: str = Field(..., min_length=2, max_length=2)  # Province/State code
    postal_code: constr(pattern=r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$')  # Canadian postal code
    phone: constr(pattern=r'^\d{3}-\d{3}-\d{4}$')
    email: EmailStr
    birthdate: Optional[Dict[str, str]] = None  # {"month": "01", "day": "01", "year": "1990"}
    native_status_number: Optional[str] = None
    mail_in_signature_expected: Optional[bool] = False

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "address1": "123 Main St",
                "address2": "Apt 4B",
                "city": "Toronto",
                "province": "ON",
                "postal_code": "M5V 2T6",
                "phone": "416-555-1234",
                "email": "john.doe@example.com",
                "birthdate": {
                    "month": "01",
                    "day": "15",
                    "year": "1985"
                }
            }
        }

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = Field(None, min_length=2, max_length=2)
    postal_code: Optional[constr(pattern=r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$')] = None
    phone: Optional[constr(pattern=r'^\d{3}-\d{3}-\d{4}$')] = None
    email: Optional[EmailStr] = None
    birthdate: Optional[Dict[str, str]] = None
    native_status_number: Optional[str] = None
    mail_in_signature_expected: Optional[bool] = None

class Customer(CustomerBase, TimestampedSchema):
    id: int

class CustomerInDB(Customer):
    pass

# Additional schemas for customer-related operations
class CustomerSearch(BaseSchema):
    query: str = Field(..., min_length=2, description="Search term (name, email, phone)")
    include_inactive: bool = False

class CustomerContractSummary(BaseSchema):
    customer_id: int
    total_contracts: int
    active_contracts: int
    total_claims: int
    total_claim_amount: int  # Amount in cents
    contracts_by_type: Dict[str, int]  # e.g., {"Warranty": 2, "GAP": 1}

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "total_contracts": 3,
                "active_contracts": 2,
                "total_claims": 1,
                "total_claim_amount": 150000,
                "contracts_by_type": {
                    "Warranty": 2,
                    "GAP": 1
                }
            }
        }
