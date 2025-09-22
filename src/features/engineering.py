import pandas as pd

def hitters_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if {'H','AB'}.issubset(out.columns):
        out['AVG'] = out['H'] / out['AB'].replace(0, pd.NA)
    if {'H','2B','3B','HR','AB'}.issubset(out.columns):
        singles = out['H'] - out.get('2B',0) - out.get('3B',0) - out.get('HR',0)
        tb = singles + 2*out.get('2B',0) + 3*out.get('3B',0) + 4*out.get('HR',0)
        out['SLG'] = tb / out['AB'].replace(0, pd.NA)
    if {'H','BB','HBP','AB','SF'}.issubset(out.columns):
        out['OBP'] = (out['H'] + out['BB'] + out.get('HBP',0)) / (out['AB'] + out['BB'] + out.get('HBP',0) + out.get('SF',0)).replace(0, pd.NA)
    if {'OBP','SLG'}.issubset(out.columns):
        out['OPS'] = out['OBP'] + out['SLG']
    return out

def pitchers_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if {'ER','IP'}.issubset(out.columns):
        out['ERA_calc'] = (9 * out['ER']) / out['IP'].replace(0, pd.NA)
    return out
