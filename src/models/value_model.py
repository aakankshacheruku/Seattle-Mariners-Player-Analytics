import pandas as pd
from pathlib import Path

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
