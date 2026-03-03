from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ApplicationCreateReq
from models import LoanApplication, RiskAssessment, Applicant
from ml.inference import ScoringService
import datetime
import uuid

router = APIRouter()

@router.post("")
def create_application(req: ApplicationCreateReq, db: Session = Depends(get_db)):
    # Simple duplicate check
    applicant_record = db.query(Applicant).filter(Applicant.phone == req.applicant.phone).first()
    if not applicant_record:
        applicant_record = Applicant(
            bank_id="mock_bank_id",
            **req.applicant.model_dump()
        )
        db.add(applicant_record)
        db.commit()
        db.refresh(applicant_record)
        
    app_ref = f"APP_{datetime.datetime.now().year}_{uuid.uuid4().hex[:6].upper()}"
    
    loan_app = LoanApplication(
        applicant_id=applicant_record.id,
        bank_id="mock_bank_id",
        application_ref=app_ref,
        status="pending_score",
        **req.employment.model_dump(),
        **req.assets.model_dump(),
        **req.loan.model_dump(),
        **(req.credit_history.model_dump() if req.credit_history else {})
    )
    db.add(loan_app)
    db.commit()
    db.refresh(loan_app)
    
    # Automatically score
    return _score_application(loan_app.id, db)

def _score_application(app_id: str, db: Session):
    loan_app = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not loan_app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    # Convert ORM to dict for scoring
    # Exclude system fields
    raw_dict = {
        c.name: getattr(loan_app, c.name) for c in loan_app.__table__.columns
        if getattr(loan_app, c.name) is not None
    }
    raw_dict.update({
        c.name: getattr(loan_app.applicant, c.name) for c in loan_app.applicant.__table__.columns
        if getattr(loan_app.applicant, c.name) is not None
    })
    
    scoring_svc = ScoringService("backend/models/latest.pkl")
    result = scoring_svc.score(raw_dict)
    
    assessment = RiskAssessment(
        application_id=loan_app.id,
        bank_id="mock_bank_id",
        pd_score=result.pd_score,
        risk_rating=result.risk_rating,
        recommended_rate_band=result.recommended_rate_band,
        recommended_action=result.recommended_action,
        confidence_score=result.confidence_score,
        feature_snapshot=result.feature_snapshot,
        top_risk_factors=result.top_risk_factors
    )
    db.add(assessment)
    loan_app.status = "scored"
    db.commit()
    db.refresh(assessment)
    
    return {
        "success": True,
        "data": {
            "application_id": loan_app.id,
            "application_ref": loan_app.application_ref,
            "assessment": {
                "id": assessment.id,
                "pd_score": assessment.pd_score,
                "risk_rating": assessment.risk_rating,
                "recommended_rate_band": assessment.recommended_rate_band,
                "recommended_action": assessment.recommended_action,
                "confidence_score": assessment.confidence_score,
                "top_risk_factors": assessment.top_risk_factors,
                "is_new_to_credit": result.is_new_to_credit,
                "assessed_at": assessment.assessed_at
            }
        }
    }

@router.get("")
def list_applications(submitted_by: str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db)):
    query = db.query(LoanApplication, RiskAssessment, Applicant).outerjoin(
        RiskAssessment, RiskAssessment.application_id == LoanApplication.id
    ).join(
        Applicant, Applicant.id == LoanApplication.applicant_id
    )
    
    apps = query.offset((page - 1) * limit).limit(limit).all()
    
    results = []
    for app, risk, app_rec in apps:
        results.append({
            "id": app.id,
            "application_ref": app.application_ref,
            "applicant_name": app_rec.full_name,
            "loan_type": app.loan_type,
            "loan_amount": app.loan_amount,
            "risk_rating": risk.risk_rating if risk else "N/A",
            "pd_score": risk.pd_score if risk else 0.0,
            "status": app.status,
            "submitted_at": app.submitted_at,
            "submitted_by_name": "Priya Sharma"
        })
        
    return {
        "success": True,
        "data": {
            "applications": results,
            "pagination": {
                "total": query.count(),
                "page": page,
                "limit": limit,
                "total_pages": (query.count() // limit) + 1
            }
        }
    }
