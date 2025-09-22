import pandas as pd
from src.features.engineering import hitters_basic_features

def test_hitters_basic_features_ops():
    df = pd.DataFrame({
        'H': [100, 120],
        'AB': [300, 400],
        '2B': [20, 30],
        '3B': [5, 2],
        'HR': [15, 25],
        'BB': [40, 50],
        'HBP': [3, 1],
        'SF': [5, 6]
    })
    out = hitters_basic_features(df)
    assert 'OPS' in out.columns
    assert out['OPS'].notna().all()
