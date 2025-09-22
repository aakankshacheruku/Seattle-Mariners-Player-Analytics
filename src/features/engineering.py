import pandas as pd
"""
Feature engineering utilities for hitters/pitchers.
Design notes:
- Use NA-safe division for all rate stats.
- Keep formulas transparent (OPS first, wOBA in v0.2).
"""
import numpy as np
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

def safe_div(numer, denom):
    """Return numer/denom with div-by-zero -> NaN."""
    return np.where(denom == 0, np.nan, numer / denom)

def hitters_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute core hitter features with NA-safe rate math.
    Expected cols: H, AB, 2B, 3B, HR, BB, HBP, SF
    """
    out = df.copy()
    singles = out["H"] - (out["2B"] + out["3B"] + out["HR"])
    tb = singles + 2*out["2B"] + 3*out["3B"] + 4*out["HR"]

    out["AVG"] = safe_div(out["H"], out["AB"])
    out["SLG"] = safe_div(tb, out["AB"])
    denom_obp = out["AB"] + out["BB"] + out["HBP"] + out["SF"]
    out["OBP"] = safe_div(out["H"] + out["BB"] + out["HBP"], denom_obp)
    out["OPS"] = out["OBP"] + out["SLG"]
    return out

def ip_to_decimal(ip_series: pd.Series) -> pd.Series:
    """
    Convert baseball IP notation (e.g., 45.2 == 45 and 2/3) to decimal innings.
    Assumes .0, .1, .2 map to 0, 1/3, 2/3.
    """
    whole = np.floor(ip_series)
    frac = (ip_series - whole).round(1)
    frac_dec = np.select(
        [frac == 0.0, frac == 0.1, frac == 0.2],
        [0.0, 1.0/3.0, 2.0/3.0],
        default=np.nan
    )
    return whole + frac_dec

def pitchers_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute core pitcher features (ERA_calc, K/BB) with NA-safe math.
    Expected cols: IP, ER, SO, BB
    """
    out = df.copy()
    ip_dec = ip_to_decimal(out["IP"]) if out["IP"].dtype != float else out["IP"]
    out["ERA_calc"] = safe_div(out["ER"] * 9.0, ip_dec)
    out["KBB"] = safe_div(out["SO"], out["BB"])
    return out

