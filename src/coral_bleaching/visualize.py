from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


sns.set_theme(style="whitegrid")


def _savefig(path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_sst_time_series(df: pd.DataFrame, columns: dict[str, str], out_path: str | Path) -> None:
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x=columns["date"], y=columns["sst"], linewidth=1)
    plt.xlabel("Year")
    plt.ylabel("Sea Surface Temperature (°C)")
    plt.title("Daily Sea Surface Temperature in the Florida Keys")
    _savefig(out_path)


def plot_annual_sst_trend(annual_df: pd.DataFrame, out_path: str | Path) -> None:
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=annual_df, x="Year", y="mean_sst", s=45)
    sns.regplot(data=annual_df, x="Year", y="mean_sst", scatter=False, ci=95)
    plt.xlabel("Year")
    plt.ylabel("Annual Mean SST (°C)")
    plt.title("Long-Term Annual SST Trend in the Florida Keys")
    _savefig(out_path)


def plot_seasonal_sst_boxplot(df: pd.DataFrame, columns: dict[str, str], out_path: str | Path) -> None:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="Month_Name", y=columns["sst"], order=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    plt.xlabel("Month")
    plt.ylabel("Sea Surface Temperature (°C)")
    plt.title("Seasonal Distribution of Sea Surface Temperature")
    _savefig(out_path)


def plot_monthly_thermal_stress(monthly_df: pd.DataFrame, out_path: str | Path) -> None:
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_df, x="Month_Name", y="mean_dhw", marker="o", label="Mean DHW")
    sns.lineplot(data=monthly_df, x="Month_Name", y="mean_hotspots", marker="o", label="Mean HotSpots")
    plt.xlabel("Month")
    plt.ylabel("Mean thermal stress metric")
    plt.title("Monthly Thermal Stress Patterns")
    plt.legend()
    _savefig(out_path)


def plot_station_hotspot_summary(df: pd.DataFrame, columns: dict[str, str], out_path: str | Path) -> None:
    summary = (
        df.groupby([columns["latitude"], columns["longitude"]])
        .agg(mean_sst=(columns["sst"], "mean"), max_hotspots=(columns["hotspots"], "max"), max_dhw=(columns["dhw"], "max"))
        .reset_index()
    )
    plt.figure(figsize=(8, 6))
    sc = plt.scatter(
        summary[columns["longitude"]],
        summary[columns["latitude"]],
        c=summary["mean_sst"],
        s=(summary["max_dhw"] + 1) * 35,
        alpha=0.8,
    )
    plt.colorbar(sc, label="Mean SST (°C)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Florida Keys Virtual Station: SST and Thermal Stress Summary")
    if len(summary) == 1:
        plt.annotate(
            "Single NOAA virtual station",
            xy=(summary[columns["longitude"]].iloc[0], summary[columns["latitude"]].iloc[0]),
            xytext=(10, 10),
            textcoords="offset points",
        )
    _savefig(out_path)


def plot_correlation_matrix(corr_df: pd.DataFrame, out_path: str | Path) -> None:
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_df, annot=True, fmt=".2f", linewidths=0.5, square=True)
    plt.title("Correlation Matrix: SST, HotSpots, DHW, and Bleaching Alerts")
    plt.xticks(rotation=45, ha="right")
    _savefig(out_path)


def plot_dhw_vs_bleaching(df: pd.DataFrame, columns: dict[str, str], out_path: str | Path) -> None:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=columns["dhw"], y=columns["bleaching_alert"], alpha=0.25)
    sns.regplot(data=df, x=columns["dhw"], y=columns["bleaching_alert"], scatter=False, ci=95)
    plt.xlabel("Degree Heating Weeks (DHW)")
    plt.ylabel("Bleaching Alert Area")
    plt.title("Relationship Between DHW and Bleaching Alert Area")
    _savefig(out_path)


def plot_sst_vs_bleaching(df: pd.DataFrame, columns: dict[str, str], out_path: str | Path) -> None:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=columns["sst"], y=columns["bleaching_alert"], alpha=0.25)
    sns.regplot(data=df, x=columns["sst"], y=columns["bleaching_alert"], scatter=False, ci=95)
    plt.xlabel("Sea Surface Temperature (°C)")
    plt.ylabel("Bleaching Alert Area")
    plt.title("Relationship Between SST and Bleaching Alert Area")
    _savefig(out_path)
