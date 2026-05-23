from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


@dataclass(frozen=True)
class TrendResult:
    slope_c_per_year: float
    intercept: float
    r_value: float
    p_value: float
    stderr: float
    total_change_c: float


def annual_sst_summary(df: pd.DataFrame, columns: dict[str, str]) -> pd.DataFrame:
    """Annual SST and thermal-stress summary table."""
    return (
        df.groupby("Year")
        .agg(
            mean_sst=(columns["sst"], "mean"),
            median_sst=(columns["sst"], "median"),
            max_sst=(columns["sst"], "max"),
            mean_hotspots=(columns["hotspots"], "mean"),
            max_hotspots=(columns["hotspots"], "max"),
            mean_dhw=(columns["dhw"], "mean"),
            max_dhw=(columns["dhw"], "max"),
            mean_bleaching_alert=(columns["bleaching_alert"], "mean"),
            max_bleaching_alert=(columns["bleaching_alert"], "max"),
            n_days=(columns["sst"], "size"),
        )
        .reset_index()
    )


def monthly_summary(df: pd.DataFrame, columns: dict[str, str]) -> pd.DataFrame:
    """Monthly SST and thermal-stress summary table."""
    return (
        df.groupby(["Month", "Month_Name"])
        .agg(
            mean_sst=(columns["sst"], "mean"),
            median_sst=(columns["sst"], "median"),
            max_sst=(columns["sst"], "max"),
            mean_hotspots=(columns["hotspots"], "mean"),
            max_hotspots=(columns["hotspots"], "max"),
            mean_dhw=(columns["dhw"], "mean"),
            max_dhw=(columns["dhw"], "max"),
            mean_bleaching_alert=(columns["bleaching_alert"], "mean"),
            max_bleaching_alert=(columns["bleaching_alert"], "max"),
            n_days=(columns["sst"], "size"),
        )
        .reset_index()
        .sort_values("Month")
    )


def correlation_matrix(df: pd.DataFrame, columns: dict[str, str]) -> pd.DataFrame:
    """Correlation matrix for SST, HotSpots, DHW, and bleaching alert area."""
    corr_cols = [
        columns["sst"],
        columns["hotspots"],
        columns["dhw"],
        columns["bleaching_alert"],
    ]
    return df[corr_cols].corr()


def fit_annual_sst_trend(annual_df: pd.DataFrame) -> TrendResult:
    """Fit a linear trend to annual mean SST."""
    result = stats.linregress(annual_df["Year"], annual_df["mean_sst"])
    years = annual_df["Year"].max() - annual_df["Year"].min()
    return TrendResult(
        slope_c_per_year=float(result.slope),
        intercept=float(result.intercept),
        r_value=float(result.rvalue),
        p_value=float(result.pvalue),
        stderr=float(result.stderr),
        total_change_c=float(result.slope * years),
    )


def top_thermal_stress_days(
    df: pd.DataFrame,
    columns: dict[str, str],
    n: int = 25,
) -> pd.DataFrame:
    """Return days with the highest combined thermal stress indicators."""
    ranked = df.copy()
    ranked["thermal_stress_score"] = (
        ranked[columns["sst"]].rank(pct=True)
        + ranked[columns["hotspots"]].rank(pct=True)
        + ranked[columns["dhw"]].rank(pct=True)
        + ranked[columns["bleaching_alert"]].rank(pct=True)
    )
    keep_cols = [
        columns["date"],
        "Year",
        "Month",
        columns["sst"],
        columns["hotspots"],
        columns["dhw"],
        columns["bleaching_alert"],
        "thermal_stress_score",
    ]
    return ranked.sort_values("thermal_stress_score", ascending=False)[keep_cols].head(n)


def build_summary_metrics(
    df: pd.DataFrame,
    annual_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    corr_df: pd.DataFrame,
    trend: TrendResult,
    columns: dict[str, str],
) -> dict[str, object]:
    """Create a compact dictionary of headline metrics for README/reporting."""
    date_col = columns["date"]
    sst_col = columns["sst"]
    dhw_col = columns["dhw"]
    alert_col = columns["bleaching_alert"]
    hotspot_col = columns["hotspots"]

    hottest_year = annual_df.loc[annual_df["mean_sst"].idxmax()]
    peak_month = monthly_df.loc[monthly_df["mean_sst"].idxmax()]
    peak_dhw_month = monthly_df.loc[monthly_df["mean_dhw"].idxmax()]

    return {
        "record_count": int(len(df)),
        "date_min": str(df[date_col].min().date()),
        "date_max": str(df[date_col].max().date()),
        "unique_locations": int(df[[columns["latitude"], columns["longitude"]]].drop_duplicates().shape[0]),
        "latitude": float(df[columns["latitude"]].iloc[0]),
        "longitude": float(df[columns["longitude"]].iloc[0]),
        "sst_mean_c": round(float(df[sst_col].mean()), 3),
        "sst_min_c": round(float(df[sst_col].min()), 3),
        "sst_max_c": round(float(df[sst_col].max()), 3),
        "annual_sst_slope_c_per_year": round(trend.slope_c_per_year, 5),
        "annual_sst_total_change_c": round(trend.total_change_c, 3),
        "annual_sst_trend_p_value": float(trend.p_value),
        "hottest_year_by_mean_sst": int(hottest_year["Year"]),
        "hottest_year_mean_sst_c": round(float(hottest_year["mean_sst"]), 3),
        "peak_month_by_mean_sst": str(peak_month["Month_Name"]),
        "peak_month_mean_sst_c": round(float(peak_month["mean_sst"]), 3),
        "peak_month_by_mean_dhw": str(peak_dhw_month["Month_Name"]),
        "peak_month_mean_dhw": round(float(peak_dhw_month["mean_dhw"]), 3),
        "corr_sst_hotspots": round(float(corr_df.loc[sst_col, hotspot_col]), 3),
        "corr_sst_dhw": round(float(corr_df.loc[sst_col, dhw_col]), 3),
        "corr_sst_bleaching_alert": round(float(corr_df.loc[sst_col, alert_col]), 3),
        "corr_dhw_bleaching_alert": round(float(corr_df.loc[dhw_col, alert_col]), 3),
        "max_bleaching_alert_area": int(df[alert_col].max()),
    }
