"""Цэвэрлэгээний функцууд: дутуу, хэт их утга, IQR, хугацаа."""

from .constants import MIN_COVERAGE, WINTER_MONTHS
import pandas as pd


def missing_report(df):
    """Багана бүрийн дутуу (NaN) утгын тоо ба хувийг гаргана.

    Буцаах утга:
        DataFrame: `missing_count`, `missing_pct` баганатай,
        хамгийн их дутуутай багана эхэндээ.
    """
    count = df.isna().sum()                   
    pct = (count / len(df) * 100).round(1)    
    report = pd.DataFrame({"missing_count": count, "missing_pct": pct})
    return report.sort_values("missing_count", ascending=False)


def iqr_outliers(df, col, k=1.5, by=None):
    """IQR аргаар хэт утгатай (outlier) мөрүүдийг олно.

    Q1 - k*IQR-аас бага, эсвэл Q3 + k*IQR-аас их утгыг хэт утга гэж үзнэ.
    PM2.5 өвөл маш өндөр байдаг тул `by="month"` өгвөл хязгаарыг сар бүрт
    тусад нь тооцно. Ингэснээр өвлийн жирийн өдрүүд outliers болохгүй.

    Параметр:
        df: DataFrame.
        col: шалгах тоон багана, жишээ нь "pm25".
        k: хязгаарын өргөн. 1.5 стандарт.
        by: бүлэглэх багана (заавал биш), жишээ нь "month".

    Буцаах утга:
        DataFrame: хэт утгатай мөрүүд, `lower` ба `upper` хязгаарын хамт.
    """
    if by is None:
        # Бүх өгөгдөлд нэг хязгаар: мөр бүрт ижил Q1, Q3
        q1 = pd.Series(df[col].quantile(0.25), index=df.index)
        q3 = pd.Series(df[col].quantile(0.75), index=df.index)
    else:
        # Бүлэг бүрт тусдаа хязгаар: мөр бүр өөрийн бүлгийн Q1, Q3-ийг авна
        q1 = df.groupby(by)[col].transform(lambda s: s.quantile(0.25))
        q3 = df.groupby(by)[col].transform(lambda s: s.quantile(0.75))

    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr

    is_outlier = (df[col] < lower) | (df[col] > upper)  
    return df.loc[is_outlier].assign(lower=lower[is_outlier], upper=upper[is_outlier])

def filter_coverage(df, col="coverage", min_pct=MIN_COVERAGE):
    """Хэмжилтийн хамрах хүрээ хангалттай өдрүүдийг л үлдээнэ.

    Цагийн хэмжилтийн `min_pct`-ээс доош хувьтай өдрийн дундаж найдваргүй
    (жишээ нь оройн утаатай цагууд алга байж болно) тул хасна.

    Параметр:
        df: DataFrame.
        col: хамрах хүрээний багана (%), анхдагч "coverage".
        min_pct: доод хувь, анхдагч MIN_COVERAGE (75).

    Буцаах утга:
        DataFrame: col >= min_pct мөрүүд.
    """
    return df[df[col] >= min_pct].copy()


def drop_period(df, start, end, station=None, date_col="date", station_col="station"):
    """Тодорхой хугацааны (сэжигтэй) мөрүүдийг хасна.

    Параметр:
        df: DataFrame.
        start, end: "YYYY-MM-DD" огноо. Хоёулаа хугацаанд орно.
        station: зөвхөн энэ станцаас хасна (заавал биш). None бол бүх станц.
        date_col: огнооны багана.
        station_col: станцын багана.

    Буцаах утга:
        DataFrame: тухайн хугацаанаас гадуурх мөрүүд.
    """
    dates = pd.to_datetime(df[date_col])
    in_period = dates.between(start, end)                     # хасах мөрүүд: True
    if station is not None:
        in_period = in_period & (df[station_col] == station)  # зөвхөн тухайн станц
    return df.loc[~in_period].copy()                          # ~ = эсрэгээр нь: үлдэх мөрүүд


def add_time_columns(df, date_col="date"):
    """Огнооноос `year`, `month`, `winter` багана нэмнэ.

    `winter` нь өвлийг 1-р сарын оноор нь нэрлэнэ:
    2018 оны 12-р сар → 2019 оны өвөл. Өвлийн бус саруудад <NA>.

    Параметр:
        df: DataFrame.
        date_col: огнооны багана.

    Буцаах утга:
        DataFrame: шинэ багануудтай хуулбар.
    """
    out = df.copy()
    dates = pd.to_datetime(out[date_col])
    out["year"] = dates.dt.year
    out["month"] = dates.dt.month

    # 12-р сар бол дараа оны өвөлд хамаарна: +1, бусад сар: +0
    winter_year = dates.dt.year + (dates.dt.month == 12).astype(int)
    # Өвлийн бус саруудыг хоосон (<NA>) болгоно
    out["winter"] = winter_year.where(dates.dt.month.isin(WINTER_MONTHS)).astype("Int64")
    return out
