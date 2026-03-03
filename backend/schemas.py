from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class SuccessResponse(BaseModel):
    success: bool = True
    data: Any = None

class ErrorDetail(BaseModel):
    code: str
    message: str
    fields: Optional[List[Dict[str, str]]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


class UserLoginReq(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    bank_id: str
    branch_code: Optional[str] = None
    
    class Config:
        from_attributes = True

class ApplicantSchema(BaseModel):
    full_name: str
    phone: str
    age: int
    gender: str
    marital_status: str
    education_level: str
    city: str
    state: str
    geo_risk_zone: str
    residential_status: str
    years_at_current_address: float
    family_size: int
    dependents: int

class EmploymentSchema(BaseModel):
    employment_type: str
    industry_type: Optional[str] = None
    employer_category: Optional[str] = None
    employment_years: float
    job_switch_frequency: int = 0
    monthly_income: float
    annual_income: float
    monthly_expense: float
    salary_account_with_bank: bool = False

class AssetsSchema(BaseModel):
    savings_balance: float
    average_monthly_balance: float
    investment_portfolio_value: float = 0.0
    total_assets_value: float
    total_liabilities_value: float = 0.0
    insurance_coverage: bool = False
    owns_house: bool = False
    property_market_value: float = 0.0
    owns_car: bool = False
    vehicle_market_value: float = 0.0
    owns_bike: bool = False
    owns_refrigerator: bool = False
    owns_washing_machine: bool = False
    owns_ac: bool = False
    owns_tv: bool = False
    gold_value_estimate: float = 0.0

class LoanSchema(BaseModel):
    loan_type: str
    loan_amount: float
    loan_tenure_months: int
    purpose_of_loan: Optional[str] = None
    collateral_provided: bool = False
    collateral_value: float = 0.0
    existing_loans: int = 0
    has_ongoing_loan: bool = False

class CreditHistorySchema(BaseModel):
    past_default_count: int = 0
    loan_repayment_history_score: Optional[float] = None
    prepayment_history: bool = False
    credit_card_utilization_ratio: Optional[float] = None
    digital_payment_ratio: Optional[float] = None
    cash_withdrawal_ratio: Optional[float] = None
    transaction_volatility_score: Optional[float] = None
    income_growth_rate: Optional[float] = None

class ApplicationCreateReq(BaseModel):
    applicant: ApplicantSchema
    employment: EmploymentSchema
    assets: AssetsSchema
    loan: LoanSchema
    credit_history: Optional[CreditHistorySchema] = None

class RiskFactor(BaseModel):
    feature: str
    value: float
    impact: str
    percentile: int

class AssessmentRes(BaseModel):
    id: str
    pd_score: float
    risk_rating: str
    recommended_rate_band: str
    recommended_action: str
    confidence_score: float
    top_risk_factors: List[RiskFactor]
    is_new_to_credit: bool
    assessed_at: datetime

class DecisionUpdateReq(BaseModel):
    final_decision: str
    conditions: Optional[str] = None
    override_reason: Optional[str] = None

class SignalUpdateReq(BaseModel):
    emi_delay_days: int
    balance_change_pct: float
    salary_credited: bool
    new_loan_detected: bool
    
class AlertUpdateReq(BaseModel):
    status: str
    resolution_notes: str
