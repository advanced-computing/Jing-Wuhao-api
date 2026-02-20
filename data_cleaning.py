import pandas as pd
import numpy as np


def clean_coordinates(df: pd.DataFrame) -> pd.DataFrame:

    cleaned_df = df.dropna(subset=["latitude", "longitude"]).copy()

    cleaned_df = cleaned_df[
        (cleaned_df["latitude"] != 0.0) & (cleaned_df["longitude"] != 0.0)
    ]

    return cleaned_df


def validate_demographics(df: pd.DataFrame) -> pd.DataFrame:

    valid_sexes = ["M", "F"]

    cleaned_df = df.dropna(subset=["perp_sex"]).copy()

    cleaned_df = cleaned_df[cleaned_df["perp_sex"].isin(valid_sexes)]

    return cleaned_df


def clean_law_category(df: pd.DataFrame) -> pd.DataFrame:

    cleaned_df = df.dropna(subset=["law_cat_cd"]).copy()

    # Keep only standard categories: Misdemeanor (M), Felony (F), Violation (V), Infraction (I)
    valid_cats = ["M", "F", "V", "I"]
    cleaned_df = cleaned_df[cleaned_df["law_cat_cd"].isin(valid_cats)]

    return cleaned_df
