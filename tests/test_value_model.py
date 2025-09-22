import pandas as pd
from src.models.value_model import hitter_value_table

def test_hitter_value_table_shapes():
    df = pd.DataFrame({
        'Name': ['A','B','C'],
        'H': [100,120,90],
        'AB': [300,380,310],
        '2B': [20,30,25],
        '3B': [5,2,3],
        'HR': [15,25,12],
        'BB': [40,50,35],
        'HBP': [3,1,2],
        'SF': [5,6,4],
        'SO': [80, 70, 85]
    })
    from src.features.engineering import hitters_basic_features
    df = hitters_basic_features(df)
    out = hitter_value_table(df, top_n=2)
    assert len(out) == 2
    assert 'score' in out.columns
