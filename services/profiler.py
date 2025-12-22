import pandas as pd
import numpy as np
import warnings


# ───────────────── Column Type Summary ─────────────────

def get_column_summary(df: pd.DataFrame) -> dict:
    numeric, categorical, datetime, text = [], [], [], []

    for col in df.columns:
        series = df[col].dropna()
        if series.empty:
            continue

        # Numeric
        if pd.api.types.is_numeric_dtype(series):
            numeric.append(col)
            continue

        # Datetime heuristic
        if pd.api.types.is_object_dtype(series):
            sample = series.sample(min(len(series), 50), random_state=42)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                parsed = pd.to_datetime(sample, errors="coerce")

            if parsed.notna().mean() > 0.7:
                datetime.append(col)
                continue

        # Categorical vs Text
        unique_ratio = series.nunique() / len(series)
        if unique_ratio < 0.3:
            categorical.append(col)
        else:
            text.append(col)

    return {
        "numeric": numeric,
        "categorical": categorical,
        "datetime": datetime,
        "text": text,
    }


# ───────────────── Main Profiler ─────────────────

def profile_dataframe(df: pd.DataFrame) -> dict:
    profile = {}

    # ───── Basic info ─────
    profile["rows"] = int(df.shape[0])
    profile["columns"] = int(df.shape[1])
    profile["duplicates"] = int(df.duplicated().sum())

    # ───── Missing values ─────
    missing = df.isnull().sum()
    profile["missing_values"] = {
        col: int(v) for col, v in missing.items() if v > 0
    }

    # ───── Column summary ─────
    summary = get_column_summary(df)
    profile["column_summary"] = summary

    # ───── Numeric statistics ─────
    numeric_stats = {}

    for col in summary["numeric"]:
        s = df[col].dropna()
        if s.empty:
            continue

        numeric_stats[col] = {
            "mean": float(round(s.mean(), 2)),
            "median": float(round(s.median(), 2)),
            "std": float(round(s.std(), 2)),
            "min": float(round(s.min(), 2)),
            "max": float(round(s.max(), 2)),
        }

    profile["numeric_stats"] = numeric_stats

    # ───── Outlier detection (IQR) ─────
    outliers = {}

    for col in summary["numeric"]:
        s = df[col].dropna()
        if len(s) < 10:
            continue

        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = int(((s < lower) | (s > upper)).sum())
        if count > 0:
            outliers[col] = count

    profile["outliers"] = outliers

    # ───── Categorical distributions (TOP 10 only) ─────
    categorical_values = {}

    for col in summary["categorical"]:
        vc = (
            df[col]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
        )
        categorical_values[col] = vc.to_dict()

    profile["categorical_values"] = categorical_values

    return profile
