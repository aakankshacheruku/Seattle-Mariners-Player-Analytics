#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from glob import glob

from src.utils.io import load_config, ensure_dir
from src.features.engineering import hitters_basic_features, pitchers_basic_features

def main():
    cfg = load_config()
    raw = Path(cfg['paths']['raw'])
    proc = Path(cfg['paths']['processed'])
    proc.mkdir(parents=True, exist_ok=True)

    # Combine player batting across seasons, then compute features
    batting_files = sorted(glob(str(raw / "player_batting_*.csv")))
    if batting_files:
        df_bat = pd.concat([pd.read_csv(f) for f in batting_files], ignore_index=True)
        df_bat = hitters_basic_features(df_bat)
        df_bat.to_csv(proc / "player_batting_features.csv", index=False)

    pitching_files = sorted(glob(str(raw / "player_pitching_*.csv")))
    if pitching_files:
        df_pit = pd.concat([pd.read_csv(f) for f in pitching_files], ignore_index=True)
        df_pit = pitchers_basic_features(df_pit)
        df_pit.to_csv(proc / "player_pitching_features.csv", index=False)

if __name__ == "__main__":
    main()
