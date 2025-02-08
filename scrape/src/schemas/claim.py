from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .base import BaseSchema, TimestampedSchema

class ClaimNoteBase(BaseSchema):
    note: str
    content: str

class ClaimNoteCreate(ClaimNoteBase):
    pass

class ClaimNote(ClaimNoteBase, TimestampedSchema):
    id: int
    claim_id: int
    deleted_by: Optional[str] = None

class ClaimBase(BaseSchema):
    authorization_number: Optional[str] = None
    repair_facility_name: Optional[str] = None
    km_at_claim_time: Optional[int] = Field(None, ge=0)
    date_of_repair: Optional[datetime] = None
    labour_price: Optional[int] = Field(None, ge=0)  # Amount in cents
    parts_price: Optional[int] = Field(None, ge=0)   # Amount in cents
    tax_price: Optional[int] = Field(None, ge=0)     # Amount in cents
    other_price: Optional[int] = Field(None, ge=0)   # Amount in cents
    status: str = "pending"  # pending, open, closed
    type: Optional[str] = None  # regular, stretch
    reason: Optional[str] = None
    pre_tax_price: Optional[int] = Field(None, ge=0)
    adjusting_cost: Optional[int] = Field(None, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "repair_facility_name": "AutoFix Shop",
                "km_at_claim_time": 50000,
                "date_of_repair": "2024-01-28T10:00:00Z",
                "labour_price": 15000,
                "parts_price": 25000,
                "tax_price": 5200,
                "status": "pending",
                "type": "regular"
            }
        }

class ClaimCreate(ClaimBase):
    contract_id: int
    notes: Optional[List[ClaimNoteCreate]] = None

class ClaimUpdate(BaseSchema):
    authorization_number: Optional[str] = None
    repair_facility_name: Optional[str] = None
    km_at_claim_time: Optional[int] = Field(None, ge=0)
    date_of_repair: Optional[datetime] = None
    labour_price: Optional[int] = Field(None, ge=0)
    parts_price: Optional[int] = Field(None, ge=0)
    tax_price: Optional[int] = Field(None, ge=0)
    other_price: Optional[int] = Field(None, ge=0)
    status: Optional[str] = None
    type: Optional[str] = None
    reason: Optional[str] = None
    pre_tax_price: Optional[int] = Field(None, ge=0)
    adjusting_cost: Optional[int] = Field(None, ge=0)

class Claim(ClaimBase, TimestampedSchema):
    id: int
    contract_id: int
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    notes: List[ClaimNote] = []
    uploads: List[Any] = []

    @property
    def total_amount(self) -> int:
        """Calculate total claim amount in cents."""
        return (self.labour_price or 0) + \
               (self.parts_price or 0) + \
               (self.tax_price or 0) + \
               (self.other_price or 0)

class ClaimInDB(Claim):
    pass

# Additional schemas for claim-related operations
class ClaimStatusUpdate(BaseSchema):
    status: str = Field(..., pattern="^(pending|open|closed)$")
    reason: Optional[str] = None
    notes: Optional[str] = None

class ClaimSummary(BaseSchema):
    total_claims: int
    open_claims: int
    closed_claims: int
    total_amount: int  # Amount in cents
    average_amount: float
    claims_by_type: Dict[str, int]  # e.g., {"regular": 5, "stretch": 2}
    claims_by_status: Dict[str, int]  # e.g., {"pending": 1, "open": 2, "closed": 4}

    class Config:
        json_schema_extra = {
            "example": {
                "total_claims": 7,
                "open_claims": 2,
                "closed_claims": 4,
                "total_amount": 450000,
                "average_amount": 64285.71,
                "claims_by_type": {
                    "regular": 5,
                    "stretch": 2
                },
                "claims_by_status": {
                    "pending": 1,
                    "open": 2,
                    "closed": 4
                }
            }
        }
