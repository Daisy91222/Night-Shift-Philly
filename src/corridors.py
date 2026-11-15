"""第 5b 步：通勤走廊。写成函数，供第 6 步每个情景重复调用。

安全 = 照明不足路段上的步行距离 + 所选站点是否照明不足（不含等车时间）。
"""
import pandas as pd


def shortest_paths(net, origins: pd.Series, destinations: pd.Series) -> list:
    """每个需求节点 → 其所选站点节点的最短路径（pandana shortest_paths，返回节点序列）。"""
    raise NotImplementedError


def accumulate_edge_flows(paths: list, weights: pd.Series, edges: pd.DataFrame) -> pd.Series:
    """把每条路径的人数累加到经过的每条边上，返回以边索引为 index 的流量。"""
    raise NotImplementedError


def commuter_safety(paths: list, edges: pd.DataFrame, edge_light: pd.DataFrame,
                    chosen: pd.DataFrame, stop_light: pd.DataFrame) -> pd.DataFrame:
    """每个需求节点：poorly_lit_walk_m（路径上照明不足边的长度之和）、stop_poorly_lit。"""
    raise NotImplementedError


def run_corridors(net, choice: pd.DataFrame, demand: pd.DataFrame, edges: pd.DataFrame,
                  edge_light: pd.DataFrame, stop_light: pd.DataFrame):
    """第 5b 步完整流程，返回 (edge_flows, commuter_safety)。"""
    raise NotImplementedError
