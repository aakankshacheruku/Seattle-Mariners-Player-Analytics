from typing import Optional
from pathlib import Path
from pybaseball import batting_stats, pitching_stats, team_batting, team_pitching
import pandas as pd

def get_team_batting(team: str, season: int) -> pd.DataFrame:
    df = team_batting(season)
    return df[df['Team'] == team].reset_index(drop=True)

def get_team_pitching(team: str, season: int) -> pd.DataFrame:
    df = team_pitching(season)
    return df[df['Team'] == team].reset_index(drop=True)

def get_player_batting(season: int) -> pd.DataFrame:
    return batting_stats(season)

def get_player_pitching(season: int) -> pd.DataFrame:
    return pitching_stats(season)

def save(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
