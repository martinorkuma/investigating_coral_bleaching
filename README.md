# Investigating Coral Bleaching in the Florida Keys

## Project Overview

Coral bleaching is a major environmental threat to reef ecosystems. In the Florida Keys, prolonged thermal stress from elevated sea surface temperature (SST) can increase coral bleaching risk. This project uses NOAA Coral Reef Watch data to quantify SST trends, seasonal thermal stress, and statistical relationships among SST, HotSpots, Degree Heating Weeks (DHW), and Bleaching Alert Area.

## Primary Objectives

- Quantify long-term trends in sea surface temperature in the Florida Keys from 1985 to 2025.
- Examine seasonal patterns in SST and identify periods of elevated thermal stress.
- Visualize station-level geospatial thermal stress associated with high SST values.
- Evaluate statistical relationships between SST, DHW, HotSpots, and Bleaching Alert Area.
- Assess how increasing temperatures and prolonged heat exposure contribute to coral bleaching risk.

## Data Source

Dataset: NOAA Coral Reef Watch 5 km Regional Virtual Station data for the Florida Keys.

Download link: https://www.nnvl.noaa.gov/Portal/Output/NOAA_CRW_5km_Regional_Virtual_Stations/Florida_Keys.csv

Methodology reference: https://coralreefwatch.noaa.gov/product/5km/methodology.php#ssttrend

## Key Variables

| Variable | Description |
|---|---|
| `Date` | Daily observation date |
| `Latitude`, `Longitude` | Florida Keys virtual station coordinates |
| `Sea_Surface_Temperature` | Daily SST in degrees Celsius |
| `HotSpots` | Positive SST anomaly above coral bleaching threshold |
| `Degree_Heating_Weeks` | Accumulated thermal stress over time |
| `Bleaching_Alert_Area` | NOAA bleaching alert category/area metric |

## Project Structure

```text
investigating_coral_bleaching_full/
├── configs/
│   └── config.yaml
├── data/
│   ├── raw/
│   │   └── Florida_Keys.csv
│   └── processed/
│       └── florida_keys_clean.csv
├── docs/
│   └── analysis_plan.md
├── outputs/
│   ├── figures/
│   │   ├── 01_daily_sst_time_series.png
│   │   ├── 02_annual_sst_trend.png
│   │   ├── 03_seasonal_sst_boxplot.png
│   │   ├── 04_monthly_thermal_stress.png
│   │   ├── 05_station_hotspot_summary.png
│   │   ├── 06_correlation_matrix.png
│   │   ├── 07_dhw_vs_bleaching_alert.png
│   │   └── 08_sst_vs_bleaching_alert.png
│   ├── reports/
│   │   └── summary_metrics.json
│   └── tables/
│       ├── annual_sst_summary.csv
│       ├── correlation_matrix.csv
│       ├── monthly_thermal_stress_summary.csv
│       └── top_thermal_stress_days.csv
├── scripts/
│   └── run_analysis.py
├── src/
│   └── coral_bleaching/
│       ├── __init__.py
│       ├── analysis.py
│       ├── config.py
│       ├── data.py
│       └── visualize.py
├── tests/
│   └── test_data_contract.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Reproducibility

Run from the project root in Bash/WSL:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_analysis.py
```

The pipeline writes:

- cleaned data to `data/processed/`
- figures to `outputs/figures/`
- summary tables to `outputs/tables/`
- headline metrics to `outputs/reports/summary_metrics.json`

## Analysis Workflow

1. Load the raw NOAA Florida Keys CSV.
2. Clean the `Date` field and validate numeric columns.
3. Derive temporal features: `Year`, `Month`, `Month_Name`, and `Season`.
4. Summarize annual SST trends and monthly thermal stress patterns.
5. Calculate correlations among SST, HotSpots, DHW, and Bleaching Alert Area.
6. Identify the highest thermal-stress days.
7. Generate reproducible visualizations and reporting tables.

## Headline Results

- Records analyzed: **14,654 daily observations**.
- Date range: **1985-01-01 to 2025-02-13**.
- Mean SST: **27.218 °C**.
- SST range: **21.520 °C to 32.840 °C**.
- Annual SST trend: **+0.02246 °C/year**, or about **+0.898 °C** across the study period.
- Linear annual SST trend p-value: **0.0076**.
- Hottest year by annual mean SST: **2023** at **28.490 °C**.
- Peak month by mean SST: **August** at **30.328 °C**.
- Peak month by mean DHW: **September** at **3.768 DHW**.
- Correlation between SST and Bleaching Alert Area: **0.667**.
- Correlation between DHW and Bleaching Alert Area: **0.604**.

## Interpretation

The analysis shows a statistically detectable long-term increase in SST for the Florida Keys virtual station. Seasonal warming is strongest in late summer, with August showing the highest mean SST and September showing the highest mean DHW. This lag is consistent with DHW representing accumulated heat stress rather than same-day temperature alone.

SST, HotSpots, DHW, and Bleaching Alert Area are positively correlated, supporting the interpretation that both elevated temperature and prolonged heat exposure contribute to coral bleaching risk.

## Geospatial Note

The dataset contains one NOAA virtual-station coordinate: **24.75° N, -81.625° W**. Because there is only one unique latitude/longitude pair, the geospatial visualization should be interpreted as a station-level thermal-stress summary, not a multi-location spatial hotspot map across the entire Florida Keys reef tract.

## Key Outputs

| Output | Purpose |
|---|---|
| `outputs/figures/01_daily_sst_time_series.png` | Daily SST trend over time |
| `outputs/figures/02_annual_sst_trend.png` | Annual mean SST with linear trend |
| `outputs/figures/03_seasonal_sst_boxplot.png` | Monthly SST distribution |
| `outputs/figures/04_monthly_thermal_stress.png` | Monthly DHW and HotSpot patterns |
| `outputs/figures/05_station_hotspot_summary.png` | Station-level thermal-stress location summary |
| `outputs/figures/06_correlation_matrix.png` | Correlations among key variables |
| `outputs/figures/07_dhw_vs_bleaching_alert.png` | DHW relationship with bleaching alert area |
| `outputs/figures/08_sst_vs_bleaching_alert.png` | SST relationship with bleaching alert area |

## Conclusion

The Florida Keys data show increasing SST over the 1985–2025 period, strong seasonal thermal stress patterns, and positive associations between SST, DHW, HotSpots, and Bleaching Alert Area. These results support the conclusion that both higher temperatures and prolonged heat exposure are important contributors to coral bleaching risk.
