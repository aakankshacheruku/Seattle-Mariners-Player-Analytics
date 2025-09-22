import pandas as pd
from src.features.engineering import pitchers_basic_features

def test_zero_ip_safe_era():
    df = pd.DataFrame({'IP':[0.0], 'ER':[0], 'SO':[0], 'BB':[0]})
    out = pitchers_basic_features(df)
    assert 'ERA_calc' in out.columns
    # Should be NaN or finite, but must not error or be inf
    val = out['ERA_calc'].iloc[0]
    assert (pd.isna(val)) or (val >= 0 and val != float('inf'))
