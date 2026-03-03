import uuid
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Bank(Base):
    __tablename__ = "banks"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    tier = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    settings = Column(JSON, default={})

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    bank_id = Column(String, ForeignKey("banks.id"), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(30), nullable=False)
    branch_code = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(String, primary_key=True, default=generate_uuid)
    bank_id = Column(String, ForeignKey("banks.id"), nullable=False)
    external_id = Column(String(100), nullable=True)
    full_name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    marital_status = Column(String(30), nullable=False)
    education_level = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    geo_risk_zone = Column(String(20), nullable=False)
    residential_status = Column(String(30), nullable=False)
    years_at_current_address = Column(Float, nullable=False)
    family_size = Column(Integer, nullable=False)
    dependents = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_duplicate_flagged = Column(Boolean, default=False)

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(String, primary_key=True, default=generate_uuid)
    applicant_id = Column(String, ForeignKey("applicants.id"), nullable=False)
    bank_id = Column(String, ForeignKey("banks.id"), nullable=False)
    application_ref = Column(String(50), unique=True, nullable=False)
    submitted_by = Column(String, ForeignKey("users.id"), nullable=True)
    status = Column(String(30), nullable=False)
    loan_type = Column(String(30), nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_tenure_months = Column(Integer, nullable=False)
    purpose_of_loan = Column(String(100), nullable=True)
    collateral_provided = Column(Boolean, default=False)
    collateral_value = Column(Float, default=0.0)
    
    employment_type = Column(String(30), nullable=False)
    industry_type = Column(String(50), nullable=True)
    employer_category = Column(String(30), nullable=True)
    employment_years = Column(Float, nullable=False)
    job_switch_frequency = Column(Integer, default=0)
    monthly_income = Column(Float, nullable=False)
    annual_income = Column(Float, nullable=False)
    monthly_expense = Column(Float, nullable=False)
    
    savings_balance = Column(Float, nullable=False)
    average_monthly_balance = Column(Float, nullable=False)
    investment_portfolio_value = Column(Float, default=0.0)
    total_assets_value = Column(Float, nullable=False)
    total_liabilities_value = Column(Float, default=0.0)
    existing_loans = Column(Integer, default=0)
    credit_card_utilization_ratio = Column(Float, nullable=True)
    insurance_coverage = Column(Boolean, default=False)
    salary_account_with_bank = Column(Boolean, default=False)
    
    owns_house = Column(Boolean, default=False)
    property_market_value = Column(Float, default=0.0)
    owns_car = Column(Boolean, default=False)
    vehicle_market_value = Column(Float, default=0.0)
    owns_bike = Column(Boolean, default=False)
    owns_refrigerator = Column(Boolean, default=False)
    owns_washing_machine = Column(Boolean, default=False)
    owns_ac = Column(Boolean, default=False)
    owns_tv = Column(Boolean, default=False)
    gold_value_estimate = Column(Float, default=0.0)
    has_ongoing_loan = Column(Boolean, default=False)
    
    past_default_count = Column(Integer, default=0)
    loan_repayment_history_score = Column(Float, nullable=True)
    prepayment_history = Column(Boolean, default=False)
    income_growth_rate = Column(Float, nullable=True)
    transaction_volatility_score = Column(Float, nullable=True)
    digital_payment_ratio = Column(Float, nullable=True)
    cash_withdrawal_ratio = Column(Float, nullable=True)
    
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
    
    applicant = relationship("Applicant")
    submitter = relationship("User")

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    id = Column(String, primary_key=True, default=generate_uuid)
    application_id = Column(String, ForeignKey("loan_applications.id"), unique=True)
    bank_id = Column(String, ForeignKey("banks.id"))
    model_version_id = Column(String, nullable=True) # Optional FK for MVP
    pd_score = Column(Float, nullable=False)
    risk_rating = Column(String(1), nullable=False)
    recommended_rate_band = Column(String(30), nullable=False)
    recommended_action = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)
    feature_snapshot = Column(JSON, nullable=False)
    top_risk_factors = Column(JSON, nullable=False)
    assessed_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_by = Column(String, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    final_decision = Column(String(20), nullable=True)
    override_reason = Column(Text, nullable=True)
    
    application = relationship("LoanApplication")

class ActiveLoan(Base):
    __tablename__ = "active_loans"
    id = Column(String, primary_key=True, default=generate_uuid)
    application_id = Column(String, ForeignKey("loan_applications.id"), unique=True)
    bank_id = Column(String, ForeignKey("banks.id"))
    disbursed_at = Column(DateTime(timezone=True), nullable=False)
    disbursed_amount = Column(Float, nullable=False)
    emi_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    outstanding_amount = Column(Float, nullable=False)
    remaining_emis = Column(Integer, nullable=False)
    baseline_pd_score = Column(Float, nullable=False)
    current_pd_score = Column(Float, nullable=False)
    current_risk_rating = Column(String(1), nullable=False)
    emi_delay_count = Column(Integer, default=0)
    last_emi_paid_at = Column(DateTime(timezone=True), nullable=True)
    salary_missed_months = Column(Integer, default=0)
    sudden_balance_drop_count = Column(Integer, default=0)
    ews_status = Column(String(20), default="green")
    last_monitored_at = Column(DateTime(timezone=True), nullable=True)
    is_closed = Column(Boolean, default=False)
    closed_at = Column(DateTime(timezone=True), nullable=True)

class EwsAlert(Base):
    __tablename__ = "ews_alerts"
    id = Column(String, primary_key=True, default=generate_uuid)
    active_loan_id = Column(String, ForeignKey("active_loans.id"))
    bank_id = Column(String, ForeignKey("banks.id"))
    severity = Column(String(20), nullable=False)
    pd_at_alert = Column(Float, nullable=False)
    pd_delta = Column(Float, nullable=False)
    trigger_signals = Column(JSON, nullable=False)
    recommended_action = Column(Text, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="open")
    reviewed_by = Column(String, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    active_loan = relationship("ActiveLoan")

class ModelVersion(Base):
    __tablename__ = "model_versions"
    id = Column(String, primary_key=True, default=generate_uuid)
    bank_id = Column(String, ForeignKey("banks.id"), nullable=True)
    version_tag = Column(String(50), nullable=False)
    algorithm = Column(String(50), nullable=False)
    roc_auc = Column(Float, nullable=False)
    ks_statistic = Column(Float, nullable=False)
    gini_coefficient = Column(Float, nullable=False)
    training_records = Column(Integer, nullable=False)
    default_rate_in_training = Column(Float, nullable=False)
    artifact_path = Column(String(500), nullable=False)
    feature_list = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=False)
    trained_at = Column(DateTime(timezone=True), server_default=func.now())
    trained_by = Column(String, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
