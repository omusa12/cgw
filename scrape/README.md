# Warranty Management System

A comprehensive system for managing vehicle warranty contracts, GAP insurance, and protection products.

## Project Overview

This system manages the full lifecycle of automotive warranty contracts, including:
- Contract creation and management
- Claims processing
- Customer management
- Vehicle information tracking
- Reporting and analytics

## Data Analysis Insights

Based on analysis of 200,000+ contracts:

### Warranty Products
- Most popular: Principal (46,498), Pinnacle (22,709)
- Common terms: 24 month (43,834), No Time Limit (20,591)
- Average dealer cost: $832.11

### GAP Insurance
- Total contracts: 56,160
- Most common term: 84 months (39,822 contracts)
- Average dealer cost: $454.45

### Vehicle Coverage
- Top makes: Hyundai, Ford, Nissan
- Years: 2003-2025
- Usage: Personal and Commercial

## Project Structure

```
src/
├── models/             # Database models
│   ├── base.py        # Base model classes
│   ├── vehicle.py     # Vehicle models
│   ├── product.py     # Product models
│   ├── contract.py    # Contract models
│   └── __init__.py    # Model exports
├── schemas/           # Pydantic schemas
│   ├── base.py       # Base schemas
│   ├── vehicle.py    # Vehicle schemas
│   ├── product.py    # Product schemas
│   ├── contract.py   # Contract schemas
│   ├── customer.py   # Customer schemas
│   ├── claim.py      # Claim schemas
│   ├── reports.py    # Reporting schemas
│   └── __init__.py   # Schema exports
├── database.py       # Database configuration
└── main.py          # FastAPI application
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/warranty_db"
```

4. Run the application:
```bash
uvicorn src.main:app --reload
```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Contracts
- POST /contracts/ - Create new contract
- GET /contracts/ - List contracts
- GET /contracts/{id} - Get contract details
- PUT /contracts/{id} - Update contract
- DELETE /contracts/{id} - Delete contract

#### Claims
- POST /contracts/{id}/claims/ - Create claim
- GET /contracts/{id}/claims/ - List claims
- PUT /claims/{id} - Update claim

#### Products
- GET /products/warranty/ - List warranty products
- GET /products/gap/ - List GAP products
- GET /products/protection/ - List protection products

#### Reports
- GET /reports/sales/ - Generate sales report
- GET /reports/claims/ - Generate claims report

## Data Models

### Contract Types
1. Warranty Contracts
   - Principal, Pinnacle, Powertrain variants
   - Configurable terms and coverage limits
   - Claims tracking

2. GAP Insurance
   - Standard and Double GAP options
   - Term-based coverage
   - Finance amount tracking

3. Protection Products
   - Paint/Interior/Rust protection
   - Theft protection
   - Tire and wheel coverage

### Vehicle Information
- Comprehensive vehicle details
- Mileage tracking
- Usage type (personal/commercial)
- Service history

### Customer Management
- Customer profiles
- Contact information
- Contract history
- Claims history

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
alembic upgrade head
```

## License

This project is proprietary and confidential.
