#!/usr/bin/env python
import argparse
from pathlib import Path
import pandas as pd

from src.utils.io import load_config
from scripts.pull_data import main as pull_main
from scripts.build_features import main as feat_main
from scripts.make_figures import main as figs_main
from src.models.value_model import hitter_value_table, pitcher_value_table

def main():
    parser = argparse.ArgumentParser(description="Run full Mariners pipeline")
    parser.add_argument("--start", type=int, default=None)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--team", type=str, default=None)
    args = parser.parse_args()

    cfg = load_config()
    if args.start: cfg['project']['start_season'] = args.start
    if args.end: cfg['project']['end_season'] = args.end
    if args.team: cfg['project']['team'] = args.team

    # Pull data
    pull_main()

    # Build features
    feat_main()

    # Figures
    figs_main()

    # Value tables
    proc = Path(cfg['paths']['processed'])
    tables = Path(cfg['paths']['tables']); tables.mkdir(parents=True, exist_ok=True)
    bat = pd.read_csv(proc / "player_batting_features.csv") if (proc / "player_batting_features.csv").exists() else None
    pit = pd.read_csv(proc / "player_pitching_features.csv") if (proc / "player_pitching_features.csv").exists() else None

    if bat is not None:
        hv = hitter_value_table(bat, top_n=25)
        hv.to_csv(tables / "hitter_value_top25.csv", index=False)
    if pit is not None:
        pv = pitcher_value_table(pit, top_n=25)
        pv.to_csv(tables / "pitcher_value_top25.csv", index=False)

if __name__ == "__main__":
    main()
