from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from .base import BaseSchema

class SalesReportItem(BaseSchema):
    contract_id: int
    contract_number: str
    contract_type: str
    customer_name: str
    vehicle_info: str  # e.g., "2023 Honda Accord"
    dealership: str
    salesperson: str
    contract_price: int  # Amount in cents
    tax: int            # Amount in cents
    total: int          # Amount in cents
    created_at: datetime
    status: str

class SalesReport(BaseSchema):
    start_date: datetime
    end_date: datetime
    total_contracts: int
    total_value: int  # Amount in cents
    total_tax: int    # Amount in cents
    contracts_by_type: Dict[str, int]
    contracts_by_dealership: Dict[str, int]
    contracts_by_salesperson: Dict[str, int]
    monthly_totals: Dict[str, int]  # Key: "YYYY-MM", Value: amount in cents
    items: List[SalesReportItem]

    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-01-31T23:59:59Z",
                "total_contracts": 150,
                "total_value": 15000000,
                "total_tax": 1950000,
                "contracts_by_type": {
                    "Warranty": 100,
                    "GAP": 35,
                    "Protection": 15
                },
                "contracts_by_dealership": {
                    "ABC Motors": 50,
                    "XYZ Auto": 45,
                    "123 Cars": 55
                },
                "contracts_by_salesperson": {
                    "John Smith": 30,
                    "Jane Doe": 25,
                    "Bob Wilson": 20
                },
                "monthly_totals": {
                    "2024-01": 15000000
                }
            }
        }

class ClaimsReportItem(BaseSchema):
    claim_id: int
    contract_id: int
    contract_number: str
    customer_name: str
    vehicle_info: str
    repair_facility: str
    labour_price: int     # Amount in cents
    parts_price: int      # Amount in cents
    tax_price: int        # Amount in cents
    other_price: int      # Amount in cents
    total_amount: int     # Amount in cents
    status: str
    type: str
    opened_at: Optional[datetime]
    closed_at: Optional[datetime]

class ClaimsReport(BaseSchema):
    start_date: datetime
    end_date: datetime
    total_claims: int
    open_claims: int
    closed_claims: int
    total_amount: int  # Amount in cents
    average_amount: float
    claims_by_type: Dict[str, int]
    claims_by_status: Dict[str, int]
    claims_by_vehicle_make: Dict[str, int]
    monthly_totals: Dict[str, int]  # Key: "YYYY-MM", Value: amount in cents
    items: List[ClaimsReportItem]

    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-01-31T23:59:59Z",
                "total_claims": 50,
                "open_claims": 10,
                "closed_claims": 35,
                "total_amount": 5000000,
                "average_amount": 100000.0,
                "claims_by_type": {
                    "regular": 40,
                    "stretch": 10
                },
                "claims_by_status": {
                    "pending": 5,
                    "open": 10,
                    "closed": 35
                },
                "claims_by_vehicle_make": {
                    "Honda": 15,
                    "Toyota": 12,
                    "Ford": 8
                },
                "monthly_totals": {
                    "2024-01": 5000000
                }
            }
        }

class ReportDateRange(BaseSchema):
    start_date: datetime = Field(..., description="Start date in ISO format")
    end_date: datetime = Field(..., description="End date in ISO format")
    include_void: bool = False

class ReportFilters(BaseSchema):
    dealership_ids: Optional[List[int]] = None
    contract_types: Optional[List[str]] = None
    salesperson_ids: Optional[List[int]] = None
    vehicle_makes: Optional[List[str]] = None
    claim_types: Optional[List[str]] = None
    claim_statuses: Optional[List[str]] = None
