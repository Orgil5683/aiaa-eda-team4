"""aiaa_eda_team4: Улаанбаатарын PM2.5 өгөгдөлд зориулсан EDA туслах сан.

Хэрэглээ:
    import aiaa_eda_team4 as et
    clean = et.filter_coverage(df)
"""

from .constants import MIN_COVERAGE, MNS_PM25_24H, WHO_PM25_24H, WINTER_MONTHS
from .cleaning import (
    add_time_columns,
    drop_period,
    filter_coverage,
    iqr_outliers,
    missing_report,
)
from .stats import basic_stats, group_rate, winter_summary
from .plots import plot_bar, plot_hist

__version__ = "0.1.0"

# `from aiaa_eda_team4 import *` хийхэд гарах нэрс
__all__ = [
    "WHO_PM25_24H",
    "MNS_PM25_24H",
    "MIN_COVERAGE",
    "WINTER_MONTHS",
    "missing_report",
    "iqr_outliers",
    "filter_coverage",
    "drop_period",
    "add_time_columns",
    "basic_stats",
    "group_rate",
    "winter_summary",
    "plot_hist",
    "plot_bar",
]
