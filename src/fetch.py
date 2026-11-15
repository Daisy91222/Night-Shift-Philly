"""数据下载。每个函数把原始数据写进 data/raw/<来源>/，已存在则跳过。

Census API 需要 key：复制 .env.example 为 .env，填入 CENSUS_API_KEY。
标“待核实”的地址和表名，取数前先对照官方文档确认（见工程记录“待确认问题”）。
"""
import os
from pathlib import Path

import config

CENSUS_API = "https://api.census.gov/data"


def census_key() -> str:
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        raise RuntimeError("缺少 CENSUS_API_KEY：在 .env 中填写，或 export 到环境变量")
    return key


def fetch_pums(out_dir: Path = config.RAW / "pums"):
    """第 1 步：PUMS 个人记录（含所需住户变量），限定宾州费城的 PUMA。

    端点：{CENSUS_API}/{PUMS_YEAR}/acs/acs5/pums
    变量：SERIALNO, PUMA, POWPUMA, JWDP, JWAP, JWTRNS, NAICSP, PINCP, WAGP,
          SEX, AGEP, RAC1P, HISP, HINCP, VEH, PWGTP（及 PWGTP1–80 重复权重）
    待核实：PUMS 2020–2024 的 PUMA 编码版本（新旧两套是否并存）。
    """
    raise NotImplementedError


def fetch_acs_tracts(out_dir: Path = config.RAW / "acs"):
    """第 2 步：B08302、B08141 普查区数据（config.ACS_VARS），并下载普查区边界。"""
    raise NotImplementedError


def fetch_block_population(out_dir: Path = config.RAW / "census_blocks"):
    """第 2 步：2020 年街区人口（PL 94-171，P1_001N）与街区边界。"""
    raise NotImplementedError


def fetch_lodes_wac(year: int = config.LODES_YEAR, out_dir: Path = config.RAW / "lodes"):
    """第 2 步：LODES WAC（宾州，S000，JT00），保留费城街区和 CNS08/16/18。

    待确认：LODES_YEAR 取最新可用年份。
    """
    raise NotImplementedError


def fetch_gtfs(out_dir: Path = config.RAW / "gtfs"):
    """第 3 步：SEPTA 公交 GTFS（google_bus），解压到 out_dir。"""
    raise NotImplementedError


def fetch_streetlights(out_dir: Path = config.RAW / "streetlights"):
    """第 5a 步：路灯位置（ArcGIS REST）。待核实：数据集名称与图层地址。"""
    raise NotImplementedError


def fetch_311_outages(out_dir: Path = config.RAW / "outages_311"):
    """第 5a 步：311 路灯故障工单（Carto API），时间窗 config.OUTAGE_WINDOW。

    待核实：服务类别名；是否有 requested_datetime、closed_datetime；
    关闭原因能否区分“已修复”与转办、重复件。
    """
    raise NotImplementedError
