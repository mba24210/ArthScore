from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import LoanApplication, ActiveLoan, EwsAlert, RiskAssessment

router = APIRouter()

@router.get("/summary")
def get_portfolio_summary(db: Session = Depends(get_db)):
    total_apps = db.query(LoanApplication).count()
    total_loans = db.query(ActiveLoan).filter(ActiveLoan.is_closed == False).count()
    
    total_value = db.query(func.sum(ActiveLoan.outstanding_amount)).filter(ActiveLoan.is_closed == False).scalar() or 0
    avg_pd = db.query(func.avg(ActiveLoan.current_pd_score)).filter(ActiveLoan.is_closed == False).scalar() or 0
    
    open_alerts = db.query(EwsAlert).filter(EwsAlert.status == "open").count()
    critical_alerts = db.query(EwsAlert).filter(EwsAlert.status == "open", EwsAlert.severity == "critical").count()
    
    rating_distribution = {
        "A": db.query(RiskAssessment).filter(RiskAssessment.risk_rating == "A").count(),
        "B": db.query(RiskAssessment).filter(RiskAssessment.risk_rating == "B").count(),
        "C": db.query(RiskAssessment).filter(RiskAssessment.risk_rating == "C").count(),
        "D": db.query(RiskAssessment).filter(RiskAssessment.risk_rating == "D").count(),
    }
    
    # Mock trend
    import datetime
    pd_trend = []
    base_date = datetime.datetime.now() - datetime.timedelta(days=30)
    for i in range(30):
        pd_trend.append({
            "date": (base_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"),
            "avg_pd": round(0.15 + (i * 0.001), 3) # Mock increasing trend
        })
        
    return {
        "success": True,
        "data": {
            "total_applications": total_apps,
            "total_disbursed_loans": total_loans,
            "total_portfolio_value": total_value,
            "avg_pd_score": float(avg_pd),
            "open_alerts": open_alerts,
            "critical_alerts": critical_alerts,
            "rating_distribution": rating_distribution,
            "pd_trend_30d": pd_trend
        }
    }
