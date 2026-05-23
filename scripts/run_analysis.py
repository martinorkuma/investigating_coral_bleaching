#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from coral_bleaching.analysis import (  # noqa: E402
    annual_sst_summary,
    build_summary_metrics,
    correlation_matrix,
    fit_annual_sst_trend,
    monthly_summary,
    top_thermal_stress_days,
)
from coral_bleaching.config import load_config  # noqa: E402
from coral_bleaching.data import clean_data, load_raw_data, save_processed_data  # noqa: E402
from coral_bleaching.visualize import (  # noqa: E402
    plot_annual_sst_trend,
    plot_correlation_matrix,
    plot_dhw_vs_bleaching,
    plot_monthly_thermal_stress,
    plot_seasonal_sst_boxplot,
    plot_sst_time_series,
    plot_sst_vs_bleaching,
    plot_station_hotspot_summary,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Florida Keys coral bleaching EDA pipeline.")
    parser.add_argument("--config", default="configs/config.yaml", help="Path to YAML config file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = (ROOT / args.config).resolve()
    cfg = load_config(config_path)

    data_cfg = cfg["data"]
    out_cfg = cfg["outputs"]
    columns = cfg["columns"]
    analysis_cfg = cfg["analysis"]

    raw_path = ROOT / data_cfg["raw_path"]
    processed_path = ROOT / data_cfg["processed_path"]
    figures_dir = ROOT / out_cfg["figures_dir"]
    tables_dir = ROOT / out_cfg["tables_dir"]
    reports_dir = ROOT / out_cfg["reports_dir"]

    for directory in [processed_path.parent, figures_dir, tables_dir, reports_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    raw_df = load_raw_data(raw_path)
    df = clean_data(raw_df, columns=columns, date_format=analysis_cfg["date_format"])
    save_processed_data(df, processed_path)

    annual_df = annual_sst_summary(df, columns)
    monthly_df = monthly_summary(df, columns)
    corr_df = correlation_matrix(df, columns)
    trend = fit_annual_sst_trend(annual_df)
    top_days = top_thermal_stress_days(
        df,
        columns=columns,
        n=analysis_cfg["top_n_thermal_stress_days"],
    )
    metrics = build_summary_metrics(df, annual_df, monthly_df, corr_df, trend, columns)

    annual_df.to_csv(tables_dir / "annual_sst_summary.csv", index=False)
    monthly_df.to_csv(tables_dir / "monthly_thermal_stress_summary.csv", index=False)
    corr_df.to_csv(tables_dir / "correlation_matrix.csv")
    top_days.to_csv(tables_dir / "top_thermal_stress_days.csv", index=False)

    with (reports_dir / "summary_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    plot_sst_time_series(df, columns, figures_dir / "01_daily_sst_time_series.png")
    plot_annual_sst_trend(annual_df, figures_dir / "02_annual_sst_trend.png")
    plot_seasonal_sst_boxplot(df, columns, figures_dir / "03_seasonal_sst_boxplot.png")
    plot_monthly_thermal_stress(monthly_df, figures_dir / "04_monthly_thermal_stress.png")
    plot_station_hotspot_summary(df, columns, figures_dir / "05_station_hotspot_summary.png")
    plot_correlation_matrix(corr_df, figures_dir / "06_correlation_matrix.png")
    plot_dhw_vs_bleaching(df, columns, figures_dir / "07_dhw_vs_bleaching_alert.png")
    plot_sst_vs_bleaching(df, columns, figures_dir / "08_sst_vs_bleaching_alert.png")

    print("Pipeline complete.")
    print(f"Processed data: {processed_path.relative_to(ROOT)}")
    print(f"Figures: {figures_dir.relative_to(ROOT)}")
    print(f"Tables: {tables_dir.relative_to(ROOT)}")
    print(f"Summary report: {(reports_dir / 'summary_metrics.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
