
"""Статистикийн функцууд: товч үзүүлэлт, босгоос дээших хувь, өвлийн дундаж."""

import pandas as pd

from .constants import WINTER_MONTHS


def basic_stats(df, col, by=None):
    """Тоон баганын үндсэн статистикийг тооцно.

    Параметр:
        df: DataFrame.
        col: тоон багана, жишээ нь "pm25".
        by: бүлэглэх багана (заавал биш), жишээ нь "station".

    Буцаах утга:
        DataFrame: count, mean, median, min, max, std.
        by өгвөл бүлэг бүрт нэг мөр.
    """
    funcs = ["count", "mean", "median", "min", "max", "std"]

    if by is None:
        return df[col].agg(funcs).round(1).to_frame(col).T

    return df.groupby(by)[col].agg(funcs).round(1)


def group_rate(df, by, col, threshold):
    """Бүлэг бүрт босгоос давсан утгын хувийг тооцно.

    Хоосон утгыг тооцохгүй.
    Буцаах утга: бүлэг бүрийн хувь (0-100).
    """
    data = df.dropna(subset=[col])
    above = data[col] > threshold

    return (above.groupby(data[by]).mean() * 100).round(1)


def winter_summary(
    df, col="pm25", min_days=15, winter_col="winter", month_col="month"
):
    """Бүрэн өвөл бүрийн дундаж утгыг тооцно.

    Өвлийн сар бүр дор хаяж min_days өдөртэй байвал
    тухайн өвлийг бүрэн гэж тооцно.
    """
    w = df.dropna(subset=[winter_col, col])

    counts = w.groupby([winter_col, month_col]).size().unstack(fill_value=0)
    counts = counts.reindex(columns=WINTER_MONTHS, fill_value=0)

    complete = counts[(counts >= min_days).all(axis=1)].index

    return (
        w[w[winter_col].isin(complete)]
        .groupby(winter_col)[col]
        .agg(["mean", "count"])
        .round(1)
    )
