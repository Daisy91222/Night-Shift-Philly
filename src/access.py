"""第 4 步：可达性。写成“输入站点 × 线路表 → 输出每个节点的选择”，供第 6 步重复调用。

效率 = 步行时间 + 时刻表损失（0.5 × 单线发车间隔）。
"""
import pandas as pd

import config


def walk_minutes(distance_m):
    return distance_m / config.WALK_SPEED_MPS / 60


def schedule_delay(headway_min):
    """时刻表损失：为配合时刻表平均损失的时间，不是站台等车时间。"""
    return config.SCHEDULE_DELAY_FACTOR * headway_min


def nearest_stops(net, demand_nodes: pd.Index, stops: pd.DataFrame,
                  n: int = config.N_CANDIDATE_STOPS,
                  max_dist_m: float = config.SEARCH_RADIUS_M) -> pd.DataFrame:
    """pandana nearest_pois：每个需求节点最近的 n 个站（不是站点 × 线路组合）。

    返回长表：node_id, rank, stop_id, walk_m。
    """
    raise NotImplementedError


def choose_stop_route(candidates: pd.DataFrame, stop_routes: pd.DataFrame) -> pd.DataFrame:
    """把候选站展开到各站经过的全部线路，选 walk + schedule_delay 最小的组合。

    返回：node_id, stop_id, route_id, walk_m, walk_min, delay_min, access_min
    最近 3 个站内都没有 Owl 线路的节点 access_min 为 NaN（覆盖缺口）。
    """
    raise NotImplementedError


def run_access(net, demand: pd.DataFrame, stop_routes: pd.DataFrame,
               stop_nodes: pd.Series) -> pd.DataFrame:
    """第 4 步完整流程（第 6 步每个情景调用一次）：nearest_stops → choose_stop_route。

    demand：节点需求表（index 为 node_id）；stop_nodes：stop_id → 网络节点。
    """
    raise NotImplementedError


def coverage(net, demand: pd.DataFrame, stop_nodes: pd.Series,
             radius_m: float = config.COVERAGE_RADIUS_M) -> float:
    """radius_m 步行范围内有站点的需求占比（白天站点和 Owl 站点各算一次）。"""
    raise NotImplementedError


def detour_ratio(network_m: pd.Series, euclid_m: pd.Series) -> pd.Series:
    """绕行系数 = 网络距离 ÷ 直线距离。"""
    return network_m / euclid_m
