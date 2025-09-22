from datetime import date
from typing import Iterable, Tuple
from pathlib import Path
import pandas as pd
from pybaseball import statcast
from src.utils.io import load_config
from src.data.loaders import save

TEAM_ABBR = {
    "SEA": "SEA"
}

def season_dates(year: int) -> Tuple[str, str]:
    # MLB regular season approx (adjust per year if needed)
    start = f"{year}-03-15"
    end = f"{year}-11-10"
    return start, end

def pull_team_statcast(team: str, start_year: int, end_year: int, out_dir: str | Path) -> None:
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    for yr in range(start_year, end_year + 1):
        start, end = season_dates(yr)
        df = statcast(start_dt=start, end_dt=end)
        # Filter by team involvement (home or away) where available
        for col in ("home_team", "away_team", "home_team_name", "away_team_name", "team"):
            if col in df.columns:
                # match common 'SEA' abbreviation or 'Mariners' strings
                if col.endswith("_team"):
                    mask = (df[col] == team)
                else:
                    mask = df[col].astype(str).str.contains("Mariner", case=False, na=False) | (df[col] == team)
                df = df[mask | (df.get('home_team') == team) | (df.get('away_team') == team)]
        save(df, out_dir / f"statcast_{team}_{yr}.csv")
