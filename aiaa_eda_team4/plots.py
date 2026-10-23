"""График зурах функцууд. `path` өгвөл PNG файлаар хадгална."""

import os

import matplotlib.pyplot as plt
import seaborn as sns


def _save(fig, path):
    """`path` өгсөн бол хавтсыг үүсгээд PNG хадгална (сангийн дотоод туслах функц)."""
    if path:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)              # figures/ байхгүй бол үүсгэнэ
        fig.savefig(path, dpi=150, bbox_inches="tight")


def plot_hist(df, col, path=None, bins=50, vline=None, title=None):
    """Тоон баганын тархалтын (histogram) график зурна.

    Параметр:
        df: DataFrame.
        col: тоон багана, жишээ нь "pm25".
        path: хадгалах зам, жишээ нь "figures/01_pm25_hist.png" (заавал биш).
        bins: баганын тоо.
        vline: лавлах босоо шугам, жишээ нь 15 (заавал биш).
        title: гарчиг (заавал биш).

    Буцаах утга:
        matplotlib Axes.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df[col].dropna(), bins=bins, ax=ax, color="steelblue")
    if vline is not None:
        ax.axvline(vline, color="red", linestyle="--", label=f"Хязгаар ({vline})")
        ax.legend()
    ax.set_title(title or f"{col} тархалт")
    ax.set_xlabel(col)
    ax.set_ylabel("Давтамж")
    _save(fig, path)
    return ax


def plot_bar(series, path=None, title=None, hline=None, xlabel=None, ylabel=None,
             color="steelblue", horizontal=False):
    """pandas Series-ийн баганан график зурна (индекс = ангилал, утга = урт).

    Параметр:
        series: жишээ нь сар бүрийн дундаж.
        path: хадгалах зам (заавал биш).
        title, xlabel, ylabel: гарчиг ба тэнхлэгийн нэр (заавал биш).
        hline: лавлах шугам, жишээ нь 15 (заавал биш).
        color: нэг өнгө, эсвэл багана бүрийн өнгөний жагсаалт.
        horizontal: True бол хэвтээ багана. Нэр урт үед (станцууд) тохиромжтой.

    Буцаах утга:
        matplotlib Axes.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    if horizontal:
        series.plot(kind="barh", ax=ax, color=color)
        draw_line = ax.axvline                            # хэвтээ графикт босоо шугам
    else:
        series.plot(kind="bar", ax=ax, color=color)
        ax.tick_params(axis="x", rotation=0)              # X тэнхлэгийн бичвэр тэгшин
        draw_line = ax.axhline                            # босоо графикт хэвтээ шугам
    if hline is not None:
        line = draw_line(hline, color="red", linestyle="--", label=f"Хязгаар ({hline})")
        ax.legend(handles=[line])                         # тайлбарт зөвхөн хязгаарын шугам
    ax.set_title(title or "")
    ax.set_xlabel(xlabel or "")
    ax.set_ylabel(ylabel or "")
    _save(fig, path)
    return ax
