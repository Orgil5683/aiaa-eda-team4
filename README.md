# aiaa-eda-team4

Улаанбаатарын PM2.5 агаарын чанарын өгөгдөлд зориулсан EDA туслах сан. AI Academy, 4-р баг.

## Суулгах

```bash
pip install aiaa-eda-team4
```

```python
import aiaa_eda_team4 as et
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
| `winter_summary(df, col="pm25", min_days=15)` | эхлээд `add_time_columns` ажиллуулна | Бүрэн өвөл бүрийн дундаж |

### plots.py
| Функц | Параметр | Буцаах утга |
|---|---|---|
| `plot_hist(df, col, path=None, bins=50, vline=None)` | `vline` = лавлах шугам (жишээ нь 15) | `path` өгвөл PNG хадгална |
| `plot_bar(series, path=None, title=None, hline=None)` | pandas Series | `path` өгвөл PNG хадгална |

## Хариуцагч
| Файл | Хариуцагч |
|---|---|
| `cleaning.py`, `stats.py` | Гишүүн 1 |
| `plots.py`, `__init__.py`, `constants.py`, `pyproject.toml` | Гишүүн 2 |