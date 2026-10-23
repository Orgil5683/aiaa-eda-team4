# aiaa-eda-team4

Улаанбаатарын PM2.5 агаарын чанарын өгөгдөлд зориулсан EDA туслах сан. AI Academy, 4-р баг.

## Суулгах

```bash
pip install aiaa-eda-team4
```

Colab дээр:

```python
!pip install -q aiaa-eda-team4
import aiaa_eda_team4 as et
```

## Жишээ

```python
import pandas as pd
import aiaa_eda_team4 as et

df = pd.read_csv("ub_pm25_daily.csv", parse_dates=["date"])
et.missing_report(df)

# Цэвэрлэх
clean = et.filter_coverage(df).dropna(subset=["pm25"])
clean = et.drop_period(clean, "2021-03-01", "2021-10-31", station="US Embassy")
clean = et.add_time_columns(clean)

# Шинжилгээ (нэг станцаар)
us = clean[clean["station"] == "US Embassy"]
et.basic_stats(us, "pm25")
et.winter_summary(us)
et.group_rate(us, by="year", col="pm25", threshold=et.WHO_PM25_24H)

# График
et.plot_hist(us, "pm25", path="figures/01_pm25_hist.png", vline=et.WHO_PM25_24H)
et.plot_bar(us.groupby("month")["pm25"].mean(), path="figures/02_monthly.png",
            hline=et.WHO_PM25_24H, xlabel="Сар", ylabel="PM2.5 (µg/m³)")
```

## Функцууд

### constants.py
| Нэр | Утга | Тайлбар |
|---|---|---|
| `WHO_PM25_24H` | 15 | ДЭМБ-ын 2021 оны өдрийн зөвлөмж, µg/m³ |
| `MNS_PM25_24H` | 50 | Монголын стандарт MNS 4585:2016, µg/m³ |
| `MIN_COVERAGE` | 75 | Бүрэн өдөр гэж тооцох цагийн хэмжилтийн доод % |
| `WINTER_MONTHS` | [12, 1, 2] | Өвөлд тооцох сарууд |

### cleaning.py
| Функц | Параметр | Буцаах утга |
|---|---|---|
| `missing_report(df)` | DataFrame | Багана бүрийн дутуу утгын тоо ба % |
| `iqr_outliers(df, col, k=1.5, by=None)` | баганын нэр; `by` = бүлэглэх багана (жишээ нь `"month"`) | Q1 - k·IQR ба Q3 + k·IQR хязгаараас гадуурх мөрүүд |
| `filter_coverage(df, col="coverage", min_pct=75)` | хамрах хүрээний багана, доод % | Хамрах хүрээ ≥ min_pct мөрүүд |
| `drop_period(df, start, end, station=None)` | `"YYYY-MM-DD"` огноо, станц (заавал биш) | Тухайн хугацаанаас гадуурх мөрүүд |
| `add_time_columns(df, date_col="date")` | огнооны багана | `year`, `month`, `winter` багана нэмсэн df |

### stats.py
| Функц | Параметр | Буцаах утга |
|---|---|---|
| `basic_stats(df, col, by=None)` | багана, бүлэглэх багана (заавал биш) | тоо, дундаж, медиан, min, max, стандарт хазайлт |
| `group_rate(df, by, col, threshold)` | бүлэглэх багана, утгын багана, хязгаар | Бүлэг бүрт хязгаараас дээш мөрийн % |
| `winter_summary(df, col="pm25", min_days=15)` | нэг станцаар шүүсэн өгөгдөл; `winter`, `month` байхгүй бол автоматаар нэмнэ | Бүрэн өвөл бүрийн дундаж ба өдрийн тоо |

### plots.py
| Функц | Параметр | Буцаах утга |
|---|---|---|
| `plot_hist(df, col, path=None, bins=50, vline=None, title=None)` | `vline` = лавлах шугам (жишээ нь 15) | Axes; `path` өгвөл PNG хадгална |
| `plot_bar(series, path=None, title=None, hline=None, xlabel=None, ylabel=None, color="steelblue", horizontal=False)` | `color` = нэг өнгө эсвэл жагсаалт; `horizontal=True` бол хэвтээ | Axes; `path` өгвөл PNG хадгална |

## Хувилбар
- **0.1.0**: Анхны хувилбар. Цэвэрлэгээ, статистик, графикийн 10 функц.
