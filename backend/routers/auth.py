from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserLoginReq, SuccessResponse, ErrorResponse, UserProfile
from typing import Any
import uuid

router = APIRouter()

# Mock for MVP
@router.post("/login")
def login(req: UserLoginReq, response: Response, db: Session = Depends(get_db)):
    if req.email == "officer@bank.com" and req.password == "securepassword":
        response.set_cookie(key="access_token", value="mock_access_token", httponly=True)
        response.set_cookie(key="refresh_token", value="mock_refresh_token", httponly=True)
        return {
            "success": True, 
            "data": {
                "user": {
                    "id": str(uuid.uuid4()),
                    "email": req.email,
                    "full_name": "Priya Sharma",
                    "role": "loan_officer",
                    "bank_id": str(uuid.uuid4()),
                    "branch_code": "DEL-001"
                }
            }
        }
    return {"success": False, "error": {"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"success": True, "data": None}

@router.get("/me")
def me(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="SESSION_EXPIRED")
    return {
        "success": True, 
        "data": {
            "user": {
                "id": str(uuid.uuid4()),
                "email": "officer@bank.com",
                "full_name": "Priya Sharma",
                "role": "loan_officer",
                "bank_id": str(uuid.uuid4()),
                "branch_code": "DEL-001"
            }
        }
    }
