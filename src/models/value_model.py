import pandas as pd
from pathlib import Path
"""
Simple value scoring for hitters/pitchers.
v0.1 priorities:
- Hitters: OPS as first-pass production proxy.
- Pitchers: blend K/BB (command) and 1/ERA (run prevention).
Known gaps: park factors, FIP/xwOBA; planned in v0.2.
"""
import numpy as np
import pandas as pd


def hitter_value_table(bat_features: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    df = bat_features.copy()
    # Plate discipline proxy if available
    bb = df['BB'] if 'BB' in df.columns else 0
    so = df['SO'] if 'SO' in df.columns else 1
    df['KBB'] = (so.replace(0, 1)) / (bb.replace(0, 1))
    for c in ['OPS','OBP','SLG']:
        if c not in df.columns:
            df[c] = pd.NA
    # Lower KBB is better, so invert rank
    df['score'] = df['OPS'].fillna(0)*0.6 + df['OBP'].fillna(0)*0.25 + df['SLG'].fillna(0)*0.15 - (df['KBB'].fillna(1)*0.02)
    keep = [c for c in ['Name','Team','OPS','OBP','SLG','KBB','score'] if c in df.columns]
    out = df[keep].sort_values('score', ascending=False).head(top_n).reset_index(drop=True)
    return out

def pitcher_value_table(pit_features: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    df = pit_features.copy()
    # K/BB if available
    k = df['SO'] if 'SO' in df.columns else 0
    bb = df['BB'] if 'BB' in df.columns else 1
    df['K_per_BB'] = (k) / (bb.replace(0, 1))
    era = df['ERA_calc'] if 'ERA_calc' in df.columns else df.get('ERA', pd.Series([None]*len(df)))
    # Lower ERA better; K/BB higher better
    df['score'] = (df['K_per_BB'].fillna(0)*0.5) + (1.0 / (era.replace(0, 1)).fillna(5))*0.5
    keep = [c for c in ['Name','Team','ERA_calc','K_per_BB','score'] if c in df.columns]
    out = df[keep].sort_values('score', ascending=False).head(top_n).reset_index(drop=True)
    return out

def hitter_score(df: pd.DataFrame) -> pd.Series:
    """
    Composite score for hitters:
    - Start with OPS (OBP + SLG) for transparency.
    - Scale by reliability ~ sqrt(plate appearances), small effect to reduce tiny-sample spikes.
    """
    ops = df["OPS"].replace([np.inf, -np.inf], np.nan).fillna(0)
    # if you have PA, use it; else approximate with AB + BB + HBP + SF
    pa = (df.get("PA") 
          or (df.get("AB", 0) + df.get("BB", 0) + df.get("HBP", 0) + df.get("SF", 0)))
    rel = np.sqrt(pd.Series(pa)).replace([np.inf, -np.inf], np.nan).fillna(0)
    return ops * (1 + 0.05 * (rel / (rel.max() or 1)))

def pitcher_score(df: pd.DataFrame) -> pd.Series:
    """
    Composite score for pitchers:
    - 50/50 blend of K/BB (command) and 1/ERA_calc (run prevention).
    - Add small reliability weight ~ sqrt(IP) to downweight tiny samples.
    """
    kbb = (df["KBB"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    run_prev = (1.0 / df["ERA_calc"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    base = 0.5 * kbb + 0.5 * run_prev
    rel = np.sqrt(df.get("IP", 0)).replace([np.inf, -np.inf], np.nan).fillna(0)
    return base * (1 + 0.05 * (rel / (rel.max() or 1)))

