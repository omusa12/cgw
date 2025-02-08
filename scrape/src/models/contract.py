from datetime import datetime
from enum import Enum
from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field
from .base import TimestampedModel
from .vehicle import Vehicle
from .product import WarrantyProduct, GAPProduct, ProtectionProduct

class ContractStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    VOID = "void"

class ClaimStatus(str, Enum):
    PENDING = "pending"
    OPEN = "open"
    CLOSED = "closed"

class ClaimType(str, Enum):
    REGULAR = "regular"
    STRETCH = "stretch"

class Customer(BaseModel):
    first_name: str
    last_name: str
    address1: str
    address2: Optional[str] = None
    city: str
    province: str
    postal_code: str
    phone: str
    email: str
    birthdate: Optional[Dict[str, str]] = None
    native_status_number: Optional[str] = None
    mail_in_signature_expected: Optional[bool] = False

class ClaimNote(TimestampedModel):
    id: int
    claim_id: int
    note: str
    deleted_by: Optional[str] = None
    content: str

class Claim(TimestampedModel):
    id: int
    contract_id: int
    authorization_number: Optional[str] = None
    repair_facility_name: Optional[str] = None
    km_at_claim_time: Optional[int] = None
    date_of_repair: Optional[datetime] = None
    labour_price: Optional[int] = None  # Amount in cents
    parts_price: Optional[int] = None   # Amount in cents
    tax_price: Optional[int] = None     # Amount in cents
    other_price: Optional[int] = None   # Amount in cents
    status: ClaimStatus
    type: Optional[ClaimType] = None
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    pre_tax_price: Optional[int] = None
    adjusting_cost: Optional[int] = None
    reason: Optional[str] = None
    notes: List[ClaimNote] = []
    uploads: List[Any] = []

class Contract(TimestampedModel):
    id: int
    contract_number: str
    prefixed_contract_number: str
    status: ContractStatus
    product: Union[WarrantyProduct, GAPProduct, ProtectionProduct]
    customer: Customer
    vehicle: Vehicle
    contract_price: float
    tax: float
    total: float
    claims: List[Claim] = []
    completed_at: Optional[datetime] = None
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
                "has_exception": False
            }
        }

    @property
    def total_claim_amount(self) -> int:
        """Calculate total amount of all closed claims in cents."""
        if not self.claims:
            return 0
            
        total = 0
        for claim in self.claims:
            if claim.status == ClaimStatus.CLOSED:
                total += (claim.labour_price or 0) + \
                        (claim.parts_price or 0) + \
                        (claim.tax_price or 0) + \
                        (claim.other_price or 0)
        return total

    @property
    def is_active(self) -> bool:
        """Check if contract is active."""
        return self.status == ContractStatus.ACTIVE

    @property
    def has_claims(self) -> bool:
        """Check if contract has any claims."""
        return len(self.claims) > 0
