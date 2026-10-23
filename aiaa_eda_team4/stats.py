"""Статистикийн функцууд: үндсэн үзүүлэлт, босго давсан хувь, өвлийн дундаж."""

import pandas as pd

from .cleaning import add_time_columns
from .constants import WINTER_MONTHS


def basic_stats(df, col, by=None):
    """Үндсэн статистик үзүүлэлтүүдийг тооцно."""

    if col not in df.columns:
        raise ValueError(f"'{col}' багана өгөгдөлд алга.")

    data = df.copy()
    data[col] = pd.to_numeric(data[col], errors="coerce")

    if by is None:
        data = data.dropna(subset=[col])

        if data.empty:
            return pd.DataFrame(
                columns=["count", "mean", "median", "min", "max", "std"],
                index=pd.Index([], name=None),
            )

        return (
            data[col]
            .agg(["count", "mean", "median", "min", "max", "std"])
            .round(1)
            .to_frame(col)
            .T
        )

    if by not in data.columns:
        raise ValueError(f"'{by}' багана өгөгдөлд алга.")

    data = data.dropna(subset=[by, col])

    return (
        data.groupby(by)[col]
        .agg(["count", "mean", "median", "min", "max", "std"])
        .round(1)
    )


def group_rate(df, by, col, threshold):
    """Бүлэг тус бүрт босго давсан утгын хувийг тооцно."""

    if by not in df.columns:
        raise ValueError(f"'{by}' багана өгөгдөлд алга.")

    if col not in df.columns:
        raise ValueError(f"'{col}' багана өгөгдөлд алга.")

    data = df[[by, col]].copy()
    data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=[by, col])

    if data.empty:
        return pd.Series(dtype=float, name=col)

    return (
        data.assign(exceeded=data[col] > threshold)
        .groupby(by)["exceeded"]
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
    Бүрэн өвөл бүрийн дундаж утгыг тооцно.

    Өвлийн сар бүр дор хаяж min_days өдөртэй байвал
    тухайн өвлийг бүрэн гэж тооцно.

    Олон станц холилдохгүйн тулд нэг станцаар шүүсэн өгөгдөл өгнө.
    """

    if col not in df.columns:
        raise ValueError(f"'{col}' багана өгөгдөлд алга.")

    data = df.copy()

    # winter, month багана байхгүй бол cleaning.py-ээс үүсгэнэ.
    if winter_col not in data.columns or month_col not in data.columns:
        data = add_time_columns(data)

    required = [col, winter_col, month_col]
    missing = [c for c in required if c not in data.columns]

    if missing:
        raise ValueError(
            f"Дараах баганууд өгөгдөлд алга: {missing}. "
            "Огнооны багана болон cleaning.py-ийн add_time_columns() "
            "функцийг шалгана уу."
        )

    data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=required).copy()

    if data.empty:
        return pd.DataFrame(columns=["mean", "count"])

    # Өвлийн саруудын өдөр тутмын хэмжилтийн тоог тооцно.
    counts = (
        data[data[month_col].isin(WINTER_MONTHS)]
        .groupby([winter_col, month_col])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=WINTER_MONTHS, fill_value=0)
    )

    # Бүх өвлийн сар min_days-аас доошгүй хэмжилттэй байх ёстой.
    complete = counts.index[(counts >= min_days).all(axis=1)]

    if len(complete) == 0:
        return pd.DataFrame(columns=["mean", "count"])

    return (
        data[data[winter_col].isin(complete)]
        .groupby(winter_col)[col]
        .agg(["mean", "count"])
        .round(1)
    )