
"""Статистикийн функцууд: үндсэн үзүүлэлт, босго давсан хувь, өвлийн дундаж."""

import pandas as pd

from .cleaning import add_time_columns
from .constants import WINTER_MONTHS


def basic_stats(df, col, by=None):
    """Тоон баганын үндсэн статистикийг тооцно."""
    if col not in df.columns:
        raise ValueError(f"'{col}' багана өгөгдөлд алга.")

    data = df.copy()
    data[col] = pd.to_numeric(data[col], errors="coerce")

    if by is None:
        return data[col].describe()[
            ["count", "mean", "50%", "min", "max", "std"]
        ].rename(
            {"50%": "median"}
        ).to_frame().T.rename(index={col: col}).round(1).rename(
            columns={"50%": "median"}
        )

    if by not in data.columns:
        raise ValueError(f"'{by}' бүлэглэх багана өгөгдөлд алга.")

    return (
        data.groupby(by)[col]
        .agg(["count", "mean", "median", "min", "max", "std"])
        .round(1)
    )


def group_rate(df, group_col, col, threshold):
    """Бүлэг тус бүрт босго давсан утгын хувийг тооцно."""
    if group_col not in df.columns:
        raise ValueError(f"'{group_col}' багана өгөгдөлд алга.")

    if col not in df.columns:
        raise ValueError(f"'{col}' багана өгөгдөлд алга.")

    data = df[[group_col, col]].copy()
    data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=[group_col, col])

    if data.empty:
        return pd.Series(dtype=float, name=col)

    return (
        data.assign(exceeded=data[col] > threshold)
        .groupby(group_col)["exceeded"]
        .mean()
        .mul(100)
        .round(1)
        .rename(col)
    )


def winter_summary(
    df,
    col="pm25",
    min_days=15,
    winter_col="winter",
    month_col="month",
):
    """
    Бүтэн өвөл бүрийн PM2.5 дундаж болон хэмжилтийн тоог тооцно.

    winter, month багана байхгүй бол cleaning.py доторх
    add_time_columns() функцийг автоматаар ашиглана.

    Өвлийн саруудад WINTER_MONTHS тогтмолыг ашиглана.
    Өвөл бүрд хамгийн багадаа min_days хэмжилттэй байна.
    """
    if col not in df.columns:
        raise ValueError(f"'{col}' багана өгөгдөлд алга.")

    data = df.copy()

    if winter_col not in data.columns or month_col not in data.columns:
        data = add_time_columns(data)

    if winter_col not in data.columns or month_col not in data.columns:
        raise ValueError(
            f"'{winter_col}', '{month_col}' баганууд үүссэнгүй. "
            "Огнооны багана байгаа эсэхийг шалгана уу."
        )

    data[col] = pd.to_numeric(data[col], errors="coerce")
    data[month_col] = pd.to_numeric(data[month_col], errors="coerce")

    data = data.dropna(subset=[winter_col, month_col, col]).copy()

    # Өвлийн саруудын хэмжилтийг сонгоно.
    data = data[data[month_col].isin(WINTER_MONTHS)]

    if data.empty:
        return pd.DataFrame(columns=["mean", "count"])

    # Өвөл бүрийн сар тус бүрийн хэмжилтийн тоо.
    counts = (
        data.groupby([winter_col, month_col])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=WINTER_MONTHS, fill_value=0)
    )

    # Бүх өвлийн саруудад хангалттай хэмжилттэй өвлүүд.
    complete_winters = counts[
        (counts >= min_days).all(axis=1)
    ].index

    if len(complete_winters) == 0:
        return pd.DataFrame(columns=["mean", "count"])

    # Бүтэн өвлүүдийн дундаж болон хэмжилтийн тоо.
    result = (
        data[data[winter_col].isin(complete_winters)]
        .groupby(winter_col)[col]
        .agg(["mean", "count"])
        .round(1)
    )

    return result
