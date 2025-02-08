from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from .base import BaseSchema, TimestampedSchema
from .customer import CustomerBase
from .vehicle import VehicleBase
from .product import WarrantyProductBase, GAPProductBase, ProtectionProductBase
from .claim import Claim

class ContractBase(BaseSchema):
    contract_number: str
    prefixed_contract_number: str
    status: str = "pending"  # pending, active, void
    contract_price: float
    tax: float
    total: float
    creator: str
    salesperson: str
    account_admin: str
    dealership: str
    dealership_id: Optional[int] = None
    ready_for_completion: Optional[bool] = None
    contract_type: str
    pdf_url: str
    claims_url: str
    subtotal: int  # Amount in cents
    tax_exempt: bool = False
    is_void_eligible: bool = False
    has_exception: bool = False

class ContractCreate(BaseSchema):
    customer: CustomerBase
    vehicle: VehicleBase
    product: Union[WarrantyProductBase, GAPProductBase, ProtectionProductBase]
    contract_price: float
    tax: float
    creator: str
    salesperson: str
    account_admin: str
    dealership: str
    dealership_id: Optional[int] = None
    tax_exempt: bool = False

class ContractUpdate(BaseSchema):
    status: Optional[str] = None
    contract_price: Optional[float] = None
    tax: Optional[float] = None
    salesperson: Optional[str] = None
    account_admin: Optional[str] = None
    ready_for_completion: Optional[bool] = None
    tax_exempt: Optional[bool] = None

class Contract(ContractBase, TimestampedSchema):
    id: int
    customer: CustomerBase
    vehicle: VehicleBase
    product: Union[WarrantyProductBase, GAPProductBase, ProtectionProductBase]
    claims: List[Claim] = []
    completed_at: Optional[datetime] = None
    alert_notes: List[Dict[str, Any]] = []
    void: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "contract_number": "123456",
                "prefixed_contract_number": "W-123456",
                "status": "active",
                "contract_price": 699.00,
                "tax": 90.87,
                "total": 789.87,
                "creator": "John Smith",
                "salesperson": "Jane Doe",
                "account_admin": "Admin User",
                "dealership": "ABC Motors",
                "dealership_id": 123,
                "contract_type": "Warranty",
                "pdf_url": "/warranty-contracts/123456/pdf",
                "claims_url": "warranty-contracts/123456/claims",
                "subtotal": 69900,
                "tax_exempt": False,
                "is_void_eligible": False,
                "has_exception": False,
                "created_at": "2024-01-28T12:00:00Z"
            }
        }

class ContractInDB(Contract):
    pass

# Additional schemas for contract-related operations
class ContractVoid(BaseSchema):
    reason: str = Field(..., description="Reason for voiding the contract")
    detail: Optional[str] = None
    voided_at: datetime = Field(default_factory=datetime.utcnow)

class ContractStatusUpdate(BaseSchema):
    status: str = Field(..., pattern="^(pending|active|void)$")
    reason: Optional[str] = None
    notes: Optional[str] = None

class ContractSummary(BaseSchema):
    total_contracts: int
    active_contracts: int
    void_contracts: int
    total_value: int  # Amount in cents
    total_claims: int
    total_claim_amount: int  # Amount in cents
    contracts_by_type: Dict[str, int]  # e.g., {"Warranty": 10, "GAP": 5}
    contracts_by_status: Dict[str, int]  # e.g., {"active": 12, "void": 3}

    class Config:
        json_schema_extra = {
            "example": {
                "total_contracts": 15,
                "active_contracts": 12,
                "void_contracts": 3,
                "total_value": 1500000,
                "total_claims": 5,
                "total_claim_amount": 250000,
                "contracts_by_type": {
                    "Warranty": 10,
                    "GAP": 5
                },
                "contracts_by_status": {
                    "active": 12,
                    "void": 3
                }
            }
        }
