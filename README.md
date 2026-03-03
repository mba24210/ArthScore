# CreditVision AI

A Smart Loan Risk Assessment & Real-Time Default Prediction System built with FastAPI and React.

## System Architecture

- **Backend:** Python 3.11+, FastAPI, SQLite, Scikit-learn
- **Frontend:** React 18, Vite, Tailwind CSS, React Router

## Setup Instructions

### Backend (API & Model)

The backend handles AI inference, API routes, and database storage.

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Generate the DB and ML synthetic data:
   ```bash
   python scripts/generate_synthetic_data.py
   ```
5. Run the FastAPI dev server:
   ```bash
   fastapi dev main.py
   ```
   > The API will be available at `http://localhost:8000`

### Frontend (React Dashboard)

The frontend provides the Dashboard, New Application form, and EWS alerts visualizer.

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   > The Web App will be available at `http://localhost:5173`

## Features Matrix

- **MVP Phase:** Comprehensive assessment APIs, Dashboard layout, Application Wizard, Synthetic Training features.
- **Future:** Live EWS automated push jobs using Celery.
