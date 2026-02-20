import pandas as pd
import numpy as np
from data_cleaning import clean_coordinates, validate_demographics, clean_law_category

mock_df = pd.DataFrame(
    {
        "latitude": [
            40.71,
            0.0,
            np.nan,
        ],
        "longitude": [-74.00, 0.0, -73.90],
        "perp_sex": [
            "M",
            "U",
            np.nan,
        ],
        "law_cat_cd": [
            "F",
            "Z",
            np.nan,
        ],
    }
)


def test_clean_coordinates():
    cleaned = clean_coordinates(mock_df)

    assert len(cleaned) == 1


def test_validate_demographics():
    cleaned = validate_demographics(mock_df)

    assert len(cleaned) == 1


def test_clean_law_category():
    cleaned = clean_law_category(mock_df)

    assert len(cleaned) == 1
