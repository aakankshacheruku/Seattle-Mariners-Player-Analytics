from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def plot_top_hitters_by_ops(df: pd.DataFrame, out_path: str | Path, n: int = 10) -> None:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    top = df[['Name','OPS']].dropna().sort_values('OPS', ascending=False).head(n)
    plt.figure()
    plt.barh(top['Name'][::-1], top['OPS'][::-1])
    plt.xlabel('OPS')
    plt.title('Top Hitters by OPS')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
