import pytest
import pandas as pd
from project import clean_data, calculate_data, risk_report

def test_clean_data():
    mask_raw_data = {
        'chart': {'result': [{'timestamp': [1718026200, 1718112600],'indicators': {'quote': [{"close": [100.5, 105.2]}]}}]}}

    df = clean_data(mask_raw_data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df["Close"].iloc[0] == 100.5

    with pytest.raises(ValueError):
        clean_data({'bad_data': 'none'})


def test_calculate_data():
    mask_cf = pd.DataFrame({'Close': [100.0, 150.0, 50.0, 200.0] })
    metrics = calculate_data(mask_cf)
    assert metrics['max_price'] == 200.0
    assert metrics['min_price'] == 50.0
    assert metrics['price_change_pct'] == 100.0


def test_risk_report():
    assert '高风险' in risk_report(12.5)
    assert '成本大跌' in risk_report(-9.0)
    assert '风险稳定' in risk_report(2.3)
