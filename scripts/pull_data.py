#!/usr/bin/env python
import argparse
from pathlib import Path
import pandas as pd

from src.utils.io import load_config, ensure_dir
from src.data.loaders import (
    get_team_batting, get_team_pitching,
    get_player_batting, get_player_pitching,
    save
)

def main():
    parser = argparse.ArgumentParser(description="Pull Mariners data via pybaseball")
    parser.add_argument("--start", type=int, required=True, help="Start season (e.g., 2019)")
    parser.add_argument("--end", type=int, required=True, help="End season (e.g., 2024)")
    parser.add_argument("--team", type=str, default="SEA", help="Team code (e.g., SEA)")
    args = parser.parse_args()

    cfg = load_config()
    raw_dir = Path(cfg['paths']['raw'])

    for season in range(args.start, args.end + 1):
        tb = get_team_batting(args.team, season)
        tp = get_team_pitching(args.team, season)
        pb = get_player_batting(season)
        pp = get_player_pitching(season)

        save(tb, raw_dir / f"team_batting_{args.team}_{season}.csv")
        save(tp, raw_dir / f"team_pitching_{args.team}_{season}.csv")
        save(pb, raw_dir / f"player_batting_{season}.csv")
        save(pp, raw_dir / f"player_pitching_{season}.csv")

if __name__ == "__main__":
    main()
