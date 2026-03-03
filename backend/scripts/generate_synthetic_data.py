import os
import sys
import uuid
import datetime
import random
import numpy as np
from sqlalchemy.orm import Session

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, Base, SessionLocal
from models import Bank, User, Applicant, LoanApplication, RiskAssessment, ActiveLoan, EwsAlert
from ml.inference import ScoringService

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Mock Bank
    bank_id = "mock_bank_id"
    if not db.query(Bank).filter(Bank.id == bank_id).first():
        bank = Bank(id=bank_id, name="Vision Bank", code="VIS_MFI", tier="NBFC")
        db.add(bank)
        db.commit()

    # Mock User
    if not db.query(User).filter(User.email == "officer@bank.com").first():
        user = User(
            id=str(uuid.uuid4()),
            bank_id=bank_id,
            email="officer@bank.com",
            hashed_password="hashed_securepassword",
            full_name="Priya Sharma",
            role="loan_officer",
            branch_code="DEL-001"
        )
        db.add(user)
        db.commit()

    # Generate Mock Data
    if db.query(Applicant).count() < 10:
        print("Generating mock portfolio data...")
        scoring_svc = ScoringService() # Mock scoring behavior
        
        for i in range(50): # Generate 50 applications
            app_rec = Applicant(
                bank_id=bank_id,
                full_name=f"Applicant {i}",
                phone=f"987654{i:04d}",
                age=random.randint(22, 55),
                gender=random.choice(["Male", "Female"]),
                marital_status=random.choice(["Single", "Married"]),
                education_level="Undergraduate",
                city="Mumbai",
                state="Maharashtra",
                geo_risk_zone="Tier-1",
                residential_status=random.choice(["Rented", "Owned"]),
                years_at_current_address=random.uniform(1.0, 10.0),
                family_size=random.randint(1, 6),
                dependents=random.randint(0, 3)
            )
            db.add(app_rec)
            db.commit()
            db.refresh(app_rec)
            
            income = random.uniform(30000, 150000)
            
            loan_app = LoanApplication(
                applicant_id=app_rec.id,
                bank_id=bank_id,
                application_ref=f"APP_{2026}_{random.randint(1000, 9999)}",
                status="scored",
                loan_type="Personal",
                loan_amount=random.uniform(50000, 1000000),
                loan_tenure_months=random.choice([12, 24, 36, 48, 60]),
                purpose_of_loan="Home Renovation",
                employment_type="Salaried",
                employment_years=random.uniform(1.0, 15.0),
                monthly_income=income,
                annual_income=income * 12,
                monthly_expense=income * random.uniform(0.3, 0.8),
                savings_balance=income * random.uniform(0.5, 5.0),
                average_monthly_balance=income * random.uniform(0.2, 1.5),
                total_assets_value=random.uniform(100000, 5000000),
                owns_car=random.choice([True, False]),
                owns_bike=random.choice([True, False]),
            )
            db.add(loan_app)
            db.commit()
            db.refresh(loan_app)
            
            raw_dict = {
                c.name: getattr(loan_app, c.name) for c in loan_app.__table__.columns if getattr(loan_app, c.name) is not None
            }
            raw_dict.update({
                c.name: getattr(loan_app.applicant, c.name) for c in loan_app.applicant.__table__.columns if getattr(loan_app.applicant, c.name) is not None
            })
            
            for k, v in raw_dict.items():
                if isinstance(v, datetime.datetime):
                    raw_dict[k] = v.isoformat()
            
            res = scoring_svc.score(raw_dict)
            
            risk = RiskAssessment(
                application_id=loan_app.id,
                bank_id=bank_id,
                pd_score=res.pd_score,
                risk_rating=res.risk_rating,
                recommended_rate_band=res.recommended_rate_band,
                recommended_action=res.recommended_action,
                confidence_score=res.confidence_score,
                feature_snapshot=res.feature_snapshot,
                top_risk_factors=res.top_risk_factors,
                assessed_at=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))
            )
            db.add(risk)
            db.commit()
            
            # Form active loans for approved A/B
            if risk.risk_rating in ["A", "B", "C"] and random.choice([True, True, False]):
                loan_app.status = "disbursed"
                active = ActiveLoan(
                    application_id=loan_app.id,
                    bank_id=bank_id,
                    disbursed_at=risk.assessed_at,
                    disbursed_amount=loan_app.loan_amount,
                    emi_amount=loan_app.loan_amount * 0.05,
                    interest_rate=12.5 if risk.risk_rating == "B" else 9.0,
                    outstanding_amount=loan_app.loan_amount * random.uniform(0.5, 0.9),
                    remaining_emis=loan_app.loan_tenure_months - 5,
                    baseline_pd_score=risk.pd_score,
                    current_pd_score=risk.pd_score + random.uniform(-0.02, 0.15),
                    current_risk_rating=risk.risk_rating
                )
                db.add(active)
                db.commit()
                db.refresh(active)
                
                # Create Alerts
                pd_delta = active.current_pd_score - active.baseline_pd_score
                if pd_delta > 0.1:
                    alert = EwsAlert(
                        active_loan_id=active.id,
                        bank_id=bank_id,
                        severity="warning" if pd_delta > 0.2 else "watch",
                        pd_at_alert=active.current_pd_score,
                        pd_delta=pd_delta,
                        trigger_signals={"emi_delay_days": random.randint(0, 15)},
                        recommended_action="Call borrower immediately"
                    )
                    db.add(alert)
                    db.commit()
                    
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
