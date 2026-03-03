import numpy as np
import os
import joblib
from dataclasses import dataclass
from ml.features import engineer_features, get_rating

MEDIAN_VALUES = {
    'loan_repayment_history_score': 7.5,
    'credit_card_utilization_ratio': 0.50,
    'past_default_count': 0,
    'digital_payment_ratio': 0.64,
    'cash_withdrawal_ratio': 0.29,
    'transaction_volatility_score': 0.50,
    'income_growth_rate': 0.0,
    'days_past_due_avg': 0.0,
}

@dataclass
class ScoringResult:
    pd_score: float
    risk_rating: str
    recommended_rate_band: str
    recommended_action: str
    confidence_score: float
    top_risk_factors: list
    feature_snapshot: dict
    is_new_to_credit: bool

class ScoringService:
    def __init__(self, model_path: str = None):
        if model_path and os.path.exists(model_path):
            self.artifact = joblib.load(model_path)
            self.model = self.artifact.get("model")
            self.feature_list = self.artifact.get("feature_list", [])
            self.feature_medians = self.artifact.get("feature_medians", MEDIAN_VALUES)
            self.label_encoders = self.artifact.get("label_encoders", {})
        else:
            self.model = None

    def transform_input(self, features: dict):
        if not self.model:
            return features
        
        # In a real setup, we would apply imputation and encoding.
        for k, v in self.feature_medians.items():
            if features.get(k) is None:
                features[k] = v

        encoded_features = []
        for feat in self.feature_list:
            val = features.get(feat, 0)
            if feat in self.label_encoders:
                encoder = self.label_encoders[feat]
                try:
                    val = encoder.transform([val])[0]
                except Exception:
                    val = -1
            encoded_features.append(val)
        return encoded_features

    def score(self, raw_input: dict) -> ScoringResult:
        features = engineer_features(raw_input)
        
        is_new_to_credit = raw_input.get('loan_repayment_history_score') is None
        
        # Base mock scoring if no model found
        if not self.model:
            pd_score = 0.18  # mock base score
            # A mock bump based on DTI
            pd_score += min((features.get('debt_to_income_ratio', 0) / 10.0) * 0.2, 0.4)
            # Clip between 0.02 and 0.8
            pd_score = max(0.02, min(0.8, pd_score))
            
            rating, rate_band, action = get_rating(pd_score, raw_input.get("collateral_value", 0), raw_input.get("loan_amount", 1))
            
            top_factors = [
                {"feature": "debt_to_income_ratio", "value": features.get('debt_to_income_ratio', 0), "impact": "moderate_risk", "percentile": 60},
                {"feature": "emi_burden_ratio", "value": features.get('emi_burden_ratio', 0), "impact": "low_risk", "percentile": 40}
            ]
            confidence_score = 0.85
        else:
            encoded_features = self.transform_input(features)
            X = np.array([encoded_features])
            
            try:
                pd_score = float(self.model.predict_proba(X)[0][1])
            except Exception:
                pd_score = float(self.model.predict(X)[0])
                
            rating, rate_band, action = get_rating(pd_score, raw_input.get("collateral_value", 0), raw_input.get("loan_amount", 1))
            top_factors = self.get_top_risk_factors(features, pd_score)
            confidence_score = self.compute_confidence(pd_score)

        return ScoringResult(
            pd_score=round(pd_score, 4),
            risk_rating=rating,
            recommended_rate_band=rate_band,
            recommended_action=action,
            confidence_score=round(confidence_score, 3),
            top_risk_factors=top_factors,
            feature_snapshot=features,
            is_new_to_credit=is_new_to_credit
        )

    def get_top_risk_factors(self, features: dict, pd_score: float) -> list:
        # Mock logic as exact importances need scikit-learn model with feature_importances_
        return [
            {"feature": "debt_to_income_ratio", "value": features.get('debt_to_income_ratio', 0), "impact": "moderate_risk", "percentile": 60},
            {"feature": "emi_burden_ratio", "value": features.get('emi_burden_ratio', 0), "impact": "low_risk", "percentile": 40}
        ]

    def compute_confidence(self, pd_score: float) -> float:
        boundaries = [0.10, 0.25, 0.45]
        min_dist = min(abs(pd_score - b) for b in boundaries)
        return min(1.0, min_dist / 0.10)
