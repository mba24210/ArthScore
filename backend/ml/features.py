def compute_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    if annual_rate == 0:
        return principal / tenure_months
    
    monthly_rate = annual_rate / 12
    emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months
    emi /= ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)

def get_rating(pd_score: float, collateral_value: float, loan_amount: float):
    if pd_score < 0.10:
        rating = "A"
        rate_band = "8-10%"
        action = "approve"
    elif pd_score < 0.25:
        rating = "B"
        rate_band = "11-14%"
        action = "approve"
    elif pd_score < 0.45:
        rating = "C"
        rate_band = "15-20%"
        action = "approve_with_collateral"
        if collateral_value >= loan_amount:
            action = "approve"
    else:
        rating = "D"
        rate_band = "N/A"
        action = "reject"
    return rating, rate_band, action

def engineer_features(raw: dict) -> dict:
    features = raw.copy()
    
    features['lifestyle_asset_score'] = sum([
        raw.get('owns_house', False),
        raw.get('owns_car', False),
        raw.get('owns_bike', False),
        raw.get('owns_refrigerator', False),
        raw.get('owns_washing_machine', False),
        raw.get('owns_ac', False),
        raw.get('owns_tv', False),
    ])
    
    dependents = raw.get('dependents', 0)
    family_size = max(raw.get('family_size', 1), 1)
    features['dependency_ratio'] = dependents / family_size
    
    total_assets_value = raw.get('total_assets_value', 0)
    total_liabilities_value = raw.get('total_liabilities_value', 0)
    features['asset_to_liability_ratio'] = min(total_assets_value / max(total_liabilities_value, 1), 50.0)
    
    monthly_income = raw.get('monthly_income', 0)
    features['income_per_dependent'] = monthly_income / (dependents + 1)
    
    savings_balance = raw.get('savings_balance', 0)
    features['savings_to_income_ratio'] = min(savings_balance / max(monthly_income, 1), 100.0)
    
    loan_amount = raw.get('loan_amount', 0)
    annual_income = raw.get('annual_income', 0)
    features['loan_to_income_ratio'] = loan_amount / max(annual_income, 1)
    
    features['net_worth'] = total_assets_value - total_liabilities_value
    features['net_worth_to_loan'] = max(-10.0, min(features['net_worth'] / max(loan_amount, 1), 50.0))
    
    monthly_expense = raw.get('monthly_expense', 0)
    features['expense_income_gap'] = monthly_income - monthly_expense
    
    # Pre-approval EMI proxy
    # We don't have final rate, so we approximate
    emi_amount = compute_emi(loan_amount, 0.125, raw.get('loan_tenure_months', 12))
    features['emi_burden_ratio'] = emi_amount / max(monthly_income, 1)
    features['emi_amount'] = emi_amount
    
    employment_years = raw.get('employment_years', 0)
    job_switch_frequency = raw.get('job_switch_frequency', 0)
    employer_category = raw.get('employer_category', '')
    
    base_score = min(employment_years * 0.5, 5.0)
    switch_penalty = job_switch_frequency * 0.5
    category_bonus = {'Government': 2.0, 'MNC': 1.5, 'Private': 0.5, 'Own Business': 0.0}.get(employer_category, 0.0)
    features['employment_stability_score'] = max(0.0, min(10.0, base_score - switch_penalty + category_bonus))
    
    features['debt_to_income_ratio'] = min(total_liabilities_value / max(annual_income, 1), 20.0)
    
    return features
