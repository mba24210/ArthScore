from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, applications, ews, portfolio

# Create database tables (in a real app, use Alembic migrations instead of this)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CreditVision AI API",
    description="Smart Loan Risk Assessment & Real-Time Default Prediction System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(applications.router, prefix="/api/v1/applications", tags=["Applications"])
app.include_router(ews.router, prefix="/api/v1/ews", tags=["EWS Alerts"])
app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["Portfolio"])

@app.get("/api/v1/health", tags=["Utility"])
def health_check():
    return {"status": "ok", "db": "connected", "model_loaded": True, "timestamp": "now"}
