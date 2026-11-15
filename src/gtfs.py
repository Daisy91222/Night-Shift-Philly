"""第 3 步：从 GTFS 得到夜间“站点 × 线路”表。"""
import pandas as pd

import config


def time_to_seconds(t: str) -> int:
    """GTFS 时间 → 当日秒数。跨午夜的时间写成 '25:30:00'，保留超过 24 小时的值。"""
    h, m, s = (int(x) for x in t.strip().split(":"))
    return h * 3600 + m * 60 + s


def in_night_window(seconds: int) -> bool:
    """是否落在 00:00–04:59。'25:30:00' 这类时间先对 24 小时取模。"""
    s = seconds % (24 * 3600)
    return config.NIGHT_START_S <= s < config.NIGHT_END_S


def active_service_ids(calendar: pd.DataFrame, calendar_dates: pd.DataFrame,
                       service_date: str = config.GTFS_SERVICE_DATE) -> set:
    """代表性工作日当天运营的 service_id（calendar 加 calendar_dates 的增删）。

    注意：00:00–05:00 的班次在 GTFS 里常属于“前一个服务日”（写成 24:00 以后），
    筛选时要同时看前一天的 service_id 中 >= 24:00 的班次。
    """
    raise NotImplementedError


def stop_route_headways(stop_times: pd.DataFrame, trips: pd.DataFrame,
                        routes: pd.DataFrame, service_ids: set) -> pd.DataFrame:
    """夜间站点 × 线路表。

    每行：stop_id, route_id, route_short_name, direction_id, n_trips, headway_min
    headway_min = config.NIGHT_WINDOW_MIN / n_trips；同站其他线路不合并。
    只保留 n_trips >= config.OWL_MIN_TRIPS 的行。
    """
    raise NotImplementedError
