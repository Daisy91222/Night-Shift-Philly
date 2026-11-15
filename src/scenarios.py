"""第 6 步：班次减少情景。情景只修改“站点 × 线路”表，然后重跑第 4 步和第 5b 步。"""
import pandas as pd

import config


def apply_scenario(stop_routes: pd.DataFrame, headway_multiplier: float = 1,
                   drop_routes: list[str] = ()) -> pd.DataFrame:
    """返回修改后的站点 × 线路表。

    - headway_multiplier：所有发车间隔乘以该系数（间隔加倍 = 2）
    - drop_routes：删除这些线路（按 route_short_name）的全部行
    """
    out = stop_routes.copy()
    if drop_routes:
        missing = set(drop_routes) - set(out["route_short_name"])
        if missing:
            raise ValueError(f"GTFS 中找不到这些线路：{missing}，核对 config.SCENARIOS 的写法")
        out = out[~out["route_short_name"].isin(drop_routes)]
    out["headway_min"] = out["headway_min"] * headway_multiplier
    return out


def run_scenario(name: str, net, stop_routes: pd.DataFrame, demand: dict,
                 stop_nodes: pd.Series, edges, edge_light, stop_light) -> pd.DataFrame:
    """跑一个情景：apply_scenario → access.run_access → corridors.run_corridors。

    demand：{"home": 居住端节点表, "work_all": …, "work_nonhealth": …}，逐一计算。
    返回长表：scenario, end, node_id, access_min, poorly_lit_walk_m, stop_poorly_lit
    """
    raise NotImplementedError


def compare_to_baseline(results: pd.DataFrame) -> pd.DataFrame:
    """各情景相对现状的变化（按通勤者加权），汇总到站点和社区；工作端含 / 不含医疗两版。"""
    raise NotImplementedError
