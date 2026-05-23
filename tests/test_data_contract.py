from pathlib import Path

import pandas as pd


def test_raw_data_has_expected_columns():
    path = Path("data/raw/Florida_Keys.csv")
    df = pd.read_csv(path, nrows=5)
    expected = {
        "Date",
        "Latitude",
        "Longitude",
        "Sea_Surface_Temperature",
        "HotSpots",
        "Degree_Heating_Weeks",
        "Bleaching_Alert_Area",
    }
    assert expected.issubset(df.columns)
