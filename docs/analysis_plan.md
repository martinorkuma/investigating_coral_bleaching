# Analysis Plan

## Objectives

1. Quantify long-term trends in sea surface temperature in the Florida Keys from 1985 to 2025.
2. Examine seasonal SST patterns and identify periods of elevated thermal stress.
3. Visualize station-level geospatial thermal stress and high-SST hotspot behavior.
4. Evaluate statistical relationships among SST, Degree Heating Weeks, HotSpots, and Bleaching Alert Area.
5. Assess how increasing temperature and prolonged heat exposure contribute to coral bleaching risk.

## Workflow

1. Ingest the raw NOAA Florida Keys CSV.
2. Clean dates and numeric fields.
3. Derive `Year`, `Month`, `Month_Name`, and `Season` features.
4. Save an analysis-ready processed CSV.
5. Generate annual, monthly, correlation, and top thermal-stress summary tables.
6. Generate reproducible figures into `outputs/figures/`.
7. Save headline metrics into `outputs/reports/summary_metrics.json`.

## Notes on geospatial interpretation

The current dataset contains one NOAA Coral Reef Watch virtual-station coordinate for the Florida Keys. Because the coordinate is fixed across records, the geospatial figure should be interpreted as a station-level location and thermal-stress summary, not a multi-station spatial interpolation across the entire reef tract.
