#!/usr/bin/env python
from pathlib import Path
import pandas as pd

from src.utils.io import load_config, ensure_dir
from src.visualization.plots import plot_top_hitters_by_ops

def main():
    cfg = load_config()
    proc = Path(cfg['paths']['processed'])
    figs = Path(cfg['paths']['figures'])
    figs.mkdir(parents=True, exist_ok=True)

    batting_path = proc / "player_batting_features.csv"
    if batting_path.exists():
        df = pd.read_csv(batting_path)
        # Column names vary by pybaseball version; adapt common name fields
        name_col = 'Name' if 'Name' in df.columns else ('name' if 'name' in df.columns else None)
        if name_col and 'OPS' in df.columns:
            df = df.rename(columns={name_col: 'Name'})
            plot_top_hitters_by_ops(df, figs / "top_hitters_ops.png", n=10)

if __name__ == "__main__":
    main()
