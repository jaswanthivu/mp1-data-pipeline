import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    rows_before = len(df)

    df = df.drop_duplicates()

    rows_after = len(df)
    logger.debug(
        f"remove_duplicates: {rows_before} -> {rows_after} rows"
    )

    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        before = len(df)
        df = df.dropna()
        after = len(df)

        logger.debug(
            f"handle_missing: {before} -> {after} rows"
        )

    elif axis == "columns":
        before = len(df.columns)
        df = df.dropna(axis=1)
        after = len(df.columns)

        logger.debug(
            f"handle_missing: {before} -> {after} columns"
        )

    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")

    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""

    if method not in ["iqr", "zscore"]:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    for column in columns:
        if column not in df.columns:
            logger.warning(f"Column not found: {column}")
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            logger.warning(f"Column is not numeric: {column}")
            continue

        rows_before = len(df)

        if method == "iqr":
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr

            df = df[
                (df[column] >= lower) &
                (df[column] <= upper)
            ]

            rows_removed = rows_before - len(df)

            logger.debug(
                f"{column}: lower={lower}, upper={upper}, "
                f"removed={rows_removed}"
            )

        elif method == "zscore":
            mean = df[column].mean()
            std = df[column].std()

            zscore = (df[column] - mean) / std

            df = df[zscore.abs() <= threshold]

            rows_removed = rows_before - len(df)

            logger.debug(
                f"{column}: method={method}, threshold={threshold}, "
                f"removed={rows_removed}"
            )

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    processing = config["processing"]

    if processing["remove_duplicates"]:
        df = remove_duplicates(df)

    missing = processing["missing"]
    if missing["enabled"]:
        df = handle_missing(df, missing["axis"])

    outliers = processing["outliers"]
    if outliers["enabled"]:
        df = remove_outliers(
            df,
            outliers["columns"],
            outliers["method"],
            outliers["threshold"]
        )

    return df

def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    report = {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns)
    }

    return report