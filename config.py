"""项目参数与文件路径。

所有 notebook 和 src 模块都从这里读取参数，调参只改这一处。
数值来自工程记录“时间口径与参数”一节，均为初始值。

单位约定（重要）：
- EPSG:2272 的单位是美国测量英尺，不是米。几何操作（缓冲、空间连接）在
  2272 下进行时，必须先用 m_to_ft() 把米换成英尺。
- 网络距离一律用米：OSMnx 的边长 `length` 是米，pandana 也按米计算。
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RAW = DATA / "raw"              # 原始下载，只读不改
PROCESSED = DATA / "processed"  # 每一步的输出，也是步骤之间唯一的交接点
WEB = DATA / "web"              # 导出给网站和仪表盘的轻量文件（GeoJSON / JSON / CSV）

# ---------------------------------------------------------------------------
# 地理与单位
# ---------------------------------------------------------------------------
CRS = "EPSG:2272"   # NAD83 / Pennsylvania South (ftUS)
CRS_WGS84 = "EPSG:4326"
STATE_FIPS = "42"
COUNTY_FIPS = "101"  # 费城县 = 费城市
PLACE_NAME = "Philadelphia, Pennsylvania, USA"
PHL_POWPUMA = "03200"  # PUMS 在费城工作 = POWSP 042 且 POWPUMA 03200（全市 11 个 PUMA 合一，来源 IPUMS 对照表）

FT_PER_M = 3.280833333  # 美国测量英尺


def m_to_ft(meters: float) -> float:
    """米 → EPSG:2272 的单位（美国测量英尺）。"""
    return meters * FT_PER_M


# ---------------------------------------------------------------------------
# 时间口径
# ---------------------------------------------------------------------------
NIGHT_START_S = 0             # 00:00
NIGHT_END_S = 5 * 3600        # 05:00（不含）
NIGHT_WINDOW_MIN = 300        # 发车间隔的分子
EVENING_DEPART = ("16:00", "21:00")  # 小夜班出发时段，回程大致落在午夜到 5 点

# ---------------------------------------------------------------------------
# 数据版本（待确认的先填 None，取数前补上）
# ---------------------------------------------------------------------------
ACS_YEAR = 2024        # ACS 5 年版 2020–2024
PUMS_YEAR = 2024       # PUMS 5 年版 2020–2024
BLOCK_POP_YEAR = 2020  # 2020 年人口普查 PL 94-171
LODES_YEAR = 2024      # LODES8 宾州最新年份（2026-10 发布），WAC 与 OD 同年
OD_JOB_TYPE = "JT00"   # OD 与 WAC 一致，用全部工作
PUMS_STATES = ["pa"]   # 只用宾州居民；按 LODES，宾州居民占费城岗位的 86.6%，其余主要是 NJ/DE 通勤者
GTFS_SERVICE_DATE = "20261118"  # 代表性工作日（周三）：feed 有效期 20261101–20270220，避开感恩节和年底节假日

# ACS 汇总表变量（取数前对照 Census API 变量列表核对）
ACS_VARS = {
    "B08302_001E": "workers_total",       # 出发时间：总数
    "B08302_002E": "depart_0000_0459",    # 12:00–4:59 a.m.（大夜班）
    "B08302_015E": "depart_1600_2359",    # 4:00–11:59 p.m.（小夜班的上级档）
    "B08141_001E": "commuters_total",     # 按可用车辆数：总数
    "B08141_002E": "commuters_no_vehicle",  # 无车
    # 第 6b 步补充模型
    "B17001_001E": "pov_universe",        # 贫困状况：总数
    "B17001_002E": "pov_below",           # 低于贫困线
    "B03002_001E": "pop_total",           # 种族与西语裔：总数
    "B03002_004E": "pop_nh_black",        # 非西语裔黑人
    "B03002_012E": "pop_hispanic",        # 西语裔
}

# ---------------------------------------------------------------------------
# 第 2 步：落到路网
# ---------------------------------------------------------------------------
BLOCK_NODE_BUFFER_M = 15

# LODES WAC 20 个行业全部进入工作端：街区值 = Σₖ CNSk 岗位数 × p̃ₖ（p̃ₖ 来自第 1 步 01_pums_params.json）
WORK_SECTORS = [f"CNS{i:02d}" for i in range(1, 21)]
WORK_VERSIONS = {  # 第 6c 步敏感性检验用的工作端算法
    "pums": "PUMS 全行业加权（主结果）",
    "atus": "ATUS 全国比例加权（data/raw/atus/atus_night_share.csv）",
    "three_sector": "原来的 3 个行业 CNS08/16/18，不加权",
    "pums_no_cns16": "PUMS 加权，去掉医疗 CNS16",
}

# ---------------------------------------------------------------------------
# 第 3 步：夜间服务
# ---------------------------------------------------------------------------
OWL_MIN_TRIPS = 3  # 站点 × 线路在工作日 00:00–05:00 至少 3 班才算 Owl（平均间隔不超过 100 分钟）
# 发车间隔按“站点 × 线路”独立计算：NIGHT_WINDOW_MIN ÷ 该线在时间窗内的班次

# ---------------------------------------------------------------------------
# 第 4 步：可达性
# ---------------------------------------------------------------------------
WALK_SPEED_MPS = 1.3
COVERAGE_RADIUS_M = 800
SEARCH_RADIUS_M = 1600
N_CANDIDATE_STOPS = 3   # 先找最近 3 个站，再展开到各站经过的全部线路
SCHEDULE_DELAY_FACTOR = 0.5  # 时刻表损失 = 0.5 × 单线发车间隔

# ---------------------------------------------------------------------------
# 第 5 步：照明
# ---------------------------------------------------------------------------
OUTAGE_WINDOW = ("2025-11-01", "2026-10-31")  # LED 换装完成后 12 个月
OUTAGE_DEDUP_M = 15            # 15 m 内且时间重叠的报告合并为一次故障
LIGHT_COUNT_COL = "nlumin"     # 有效密度按灯头数计；nlumin 为空或 0 的杆计 0
OUTAGE_SERVICE_NAMES = ["Street Light Outage"]  # 311 只用街灯故障，不含 Alley Light Outage
POLE_SNAP_MAX_M = 20           # 路灯挂到最近边的最大距离（初始值，可调）
POORLY_LIT_QUANTILE = 0.25     # 有效路灯密度最低 25% 为照明不足
STOP_LIGHTING_RADIUS_M = 50    # 站点周围半径内的所有边；待调研后调整

# ---------------------------------------------------------------------------
# 第 6 步：情景
# ---------------------------------------------------------------------------
# route 的写法要和 GTFS routes.txt 中的 route_short_name 对上，取数后核对
SCENARIOS = {
    "baseline": {},
    "headway_x2": {"headway_multiplier": 2},
    "no_b1_owl": {"drop_routes": ["B1 OWL"]},
    "no_l1_owl": {"drop_routes": ["L1 OWL"]},
}

# ---------------------------------------------------------------------------
# 输出文件约定：每一步只读上一步写在这里的文件
# ---------------------------------------------------------------------------
OUT = {
    "00_network": {
        "nodes": PROCESSED / "00_walk_nodes.parquet",
        "edges": PROCESSED / "00_walk_edges.parquet",
        "boundary": PROCESSED / "00_city_boundary.parquet",
        "tract_puma": PROCESSED / "00_tract_puma_crosswalk.csv",
    },
    "01_profile": {
        "profile": PROCESSED / "01_profile_night_vs_day.csv",
        "params": PROCESSED / "01_pums_params.json",   # 第 2 步要读
        "puma_night": PROCESSED / "01_puma_night_commuters.csv",
    },
    "02_place": {
        "home_nodes": PROCESSED / "02_home_nodes.parquet",
        "work_nodes": PROCESSED / "02_work_nodes.parquet",
        "tract_bivariate": PROCESSED / "02_tract_bivariate.parquet",
        "consistency": PROCESSED / "02_consistency_check.csv",
        "block_nodes": PROCESSED / "02_block_node_lookup.parquet",
    },
    "03_service": {
        "stop_routes": PROCESSED / "03_owl_stop_routes.parquet",  # 站点 × 线路
        "owl_stops": PROCESSED / "03_owl_stops.parquet",
        "day_stops": PROCESSED / "03_day_stops.parquet",
    },
    "04_access": {
        "home": PROCESSED / "04_access_home.parquet",
        "work": PROCESSED / "04_access_work.parquet",
        "coverage": PROCESSED / "04_coverage_day_vs_night.csv",
    },
    "05a_lighting": {
        "outages": PROCESSED / "05a_outages_dedup.parquet",
        "edge_lighting": PROCESSED / "05a_edge_lighting.parquet",
        "stop_lighting": PROCESSED / "05a_stop_lighting.parquet",
    },
    "05b_corridors": {
        "edge_flows": PROCESSED / "05b_edge_flows_baseline.parquet",
        "commuter_safety": PROCESSED / "05b_commuter_safety_baseline.parquet",
    },
    "06_scenarios": {
        "results": PROCESSED / "06_scenario_results.parquet",
        "summary": PROCESSED / "06_scenario_summary.csv",
    },
}
