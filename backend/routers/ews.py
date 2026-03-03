from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import EwsAlert, ActiveLoan
from schemas import AlertUpdateReq

router = APIRouter()

@router.get("/alerts")
def get_alerts(severity: str = None, status: str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db)):
    query = db.query(EwsAlert)
    if severity:
        query = query.filter(EwsAlert.severity == severity)
    if status:
        query = query.filter(EwsAlert.status == status)
        
    alerts = query.offset((page - 1) * limit).limit(limit).all()
    results = []
    
    for alert in alerts:
        results.append({
            "id": alert.id,
            "active_loan_id": alert.active_loan_id,
            "application_ref": alert.active_loan.application.application_ref if alert.active_loan else "UNKNOWN",
            "borrower_name": alert.active_loan.application.applicant.full_name if alert.active_loan else "UNKNOWN",
            "loan_amount": alert.active_loan.disbursed_amount if alert.active_loan else 0,
            "severity": alert.severity,
            "current_pd": alert.pd_at_alert,
            "baseline_pd": alert.pd_at_alert - alert.pd_delta,
            "pd_delta": alert.pd_delta,
            "trigger_signals": alert.trigger_signals,
            "recommended_action": alert.recommended_action,
            "assigned_to_name": "Priya Sharma",
            "status": alert.status,
            "generated_at": alert.generated_at
        })
        
    counts = {
        "open": db.query(EwsAlert).filter(EwsAlert.status == "open").count(),
        "critical": db.query(EwsAlert).filter(EwsAlert.status == "open", EwsAlert.severity == "critical").count(),
        "warning": db.query(EwsAlert).filter(EwsAlert.status == "open", EwsAlert.severity == "warning").count(),
        "watch": db.query(EwsAlert).filter(EwsAlert.status == "open", EwsAlert.severity == "watch").count(),
    }
        
    return {
        "success": True,
        "data": {
            "alerts": results,
            "counts": counts,
            "pagination": {
                "total": query.count(),
                "page": page,
                "limit": limit,
                "total_pages": (query.count() // limit) + 1
            }
        }
    }

@router.patch("/alerts/{id}")
def update_alert(id: str, req: AlertUpdateReq, db: Session = Depends(get_db)):
    alert = db.query(EwsAlert).filter(EwsAlert.id == id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
        
    alert.status = req.status
    alert.resolution_notes = req.resolution_notes
    db.commit()
    return {"success": True, "data": None}
