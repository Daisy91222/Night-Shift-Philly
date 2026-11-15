"""第 5a 步：有效路灯密度。只依赖网络、路灯和 311，与流量无关，可以先做。

有效路灯密度 =（灯杆数 × 365 − 故障灯·天）÷ 365 ÷ 路段长度
即一年中平均每米正常工作的灯数；展示时 × 100 换成“每 100 m”。
"""
import geopandas as gpd
import pandas as pd

import config


def in_service_density(n_poles, outage_pole_days, length_m, days: int = 365):
    """每米平均正常工作的灯数。参数可以是标量或等长 Series。"""
    return (n_poles * days - outage_pole_days) / days / length_m


def outage_durations(outages: pd.DataFrame, window=config.OUTAGE_WINDOW) -> pd.DataFrame:
    """故障时长（天）= 关闭 − 报修；未关闭的截到窗口末；报修早于窗口的从窗口起算。"""
    raise NotImplementedError


def dedup_outages(outages: gpd.GeoDataFrame, dist_m: float = config.OUTAGE_DEDUP_M) -> gpd.GeoDataFrame:
    """15 m 内且时间重叠的报告合并为一次故障：从最早报修算到最晚关闭。"""
    raise NotImplementedError


def snap_to_edges(points: gpd.GeoDataFrame, edges: gpd.GeoDataFrame,
                  max_dist_m: float = config.POLE_SNAP_MAX_M) -> pd.Series:
    """点 → 最近的边（sjoin_nearest，距离换成英尺）。返回每个点对应的边索引。"""
    raise NotImplementedError


def edge_lighting(edges: gpd.GeoDataFrame, poles: gpd.GeoDataFrame,
                  outages: gpd.GeoDataFrame) -> pd.DataFrame:
    """每条边：n_poles, outage_pole_days, density_per_100m, poorly_lit。

    poorly_lit = density 处于最低 config.POORLY_LIT_QUANTILE。
    """
    raise NotImplementedError


def stop_lighting(stops: gpd.GeoDataFrame, edges: gpd.GeoDataFrame, edge_light: pd.DataFrame,
                  radius_m: float = config.STOP_LIGHTING_RADIUS_M) -> pd.DataFrame:
    """站点周围 radius_m 内所有边的有效路灯密度（按边长加权平均），并标记照明不足。

    半径为初始值，待调研后调整。
    """
    raise NotImplementedError
