"""第 1 步：PUMS 加权统计。

所有统计都要加权（个人用 PWGTP）。分母是“有出发时间（JWDP 非空）的通勤者”。
"""
import numpy as np
import pandas as pd


def weighted_share(df: pd.DataFrame, numer: pd.Series, denom: pd.Series | None = None,
                   weight: str = "PWGTP") -> float:
    """加权比例：sum(w[numer & denom]) / sum(w[denom])。denom 为空时用全部行。"""
    if denom is None:
        denom = pd.Series(True, index=df.index)
    w = df[weight]
    return w[numer & denom].sum() / w[denom].sum()


def replicate_se(df: pd.DataFrame, stat_fn, n_rep: int = 80) -> float:
    """用 80 组重复权重算标准误：SE = sqrt(4/80 × Σ(θ_r − θ)²)。

    stat_fn(df, weight_col) -> float，例如
    lambda d, w: weighted_share(d, night & carless, night, weight=w)
    """
    theta = stat_fn(df, "PWGTP")
    reps = np.array([stat_fn(df, f"PWGTP{r}") for r in range(1, n_rep + 1)])
    return float(np.sqrt(4 / n_rep * ((reps - theta) ** 2).sum()))


def night_departure_codes(jwdp_dictionary: pd.DataFrame) -> list:
    """从 PUMS 数据字典挑出起点落在 00:00–04:59 的 JWDP 编码。

    JWDP 是分段编码，不是钟点；输入为数据字典中 JWDP 的编码与起止时间表。
    """
    raise NotImplementedError


def evening_departure_codes(jwdp_dictionary: pd.DataFrame) -> list:
    """挑出起点落在 config.EVENING_DEPART（16:00–21:00）的 JWDP 编码。"""
    raise NotImplementedError
