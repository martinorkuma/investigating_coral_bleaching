from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_raw_data(path: str | Path) -> pd.DataFrame:
    """Load raw Florida Keys coral bleaching data."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame, columns: dict[str, str], date_format: str) -> pd.DataFrame:
    """Clean raw data and derive temporal features used for analysis."""
    df = df.copy()

    date_col = columns["date"]
    numeric_cols = [
        columns["latitude"],
        columns["longitude"],
        columns["sst"],
        columns["hotspots"],
        columns["dhw"],
        columns["bleaching_alert"],
    ]

    df[date_col] = pd.to_datetime(df[date_col], format=date_format, errors="coerce")
    df = df.dropna(subset=[date_col]).copy()

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols).copy()
    df = df.sort_values(date_col).reset_index(drop=True)

    df["Year"] = df[date_col].dt.year
    df["Month"] = df[date_col].dt.month
    df["Month_Name"] = df[date_col].dt.month_name().str[:3]
    df["Season"] = df["Month"].map(
        {
            12: "Winter", 1: "Winter", 2: "Winter",
            3: "Spring", 4: "Spring", 5: "Spring",
            6: "Summer", 7: "Summer", 8: "Summer",
            9: "Fall", 10: "Fall", 11: "Fall",
        }
    )

    return df


def save_processed_data(df: pd.DataFrame, path: str | Path) -> None:
    """Save cleaned analysis-ready data."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
