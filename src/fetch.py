"""数据下载。每个函数把原始数据原样写进 data/raw/<来源>/，已存在则跳过；清理放在各步 notebook 里。

只有 ACS 需要 Census API key：复制 .env.example 为 .env，填入 CENSUS_API_KEY。
运行全部：在仓库根目录执行 `python -m src.fetch`。
"""
import json
import os
import zipfile
from pathlib import Path

import requests
from dotenv import load_dotenv

import config

load_dotenv(config.ROOT / ".env")

CENSUS_API = "https://api.census.gov/data"
TIGER = "https://www2.census.gov/geo/tiger/TIGER2024"
TRACT_PUMA = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/2020_Census_Tract_to_2020_PUMA.txt"
TIGERWEB_BLOCKS = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Tracts_Blocks/MapServer/12"
PUMS_FTP = "https://www2.census.gov/programs-surveys/acs/data/pums"
PUMS_DICT = "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict"
LODES = "https://lehd.ces.census.gov/data/lodes/LODES8/pa"
GTFS_URL = "https://github.com/septadev/GTFS/releases/latest/download/gtfs_public.zip"
POLES_URL = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Street_Poles/FeatureServer/0"
CARTO_URL = "https://phl.carto.com/api/v2/sql"


def census_key() -> str:
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        raise RuntimeError("缺少 CENSUS_API_KEY：在 .env 中填写，或 export 到环境变量")
    return key


def _download(url: str, path: Path, **params) -> Path:
    """下载 url 到 path；文件已存在则跳过。"""
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, params=params or None, timeout=600)
    r.raise_for_status()
    path.write_bytes(r.content)
    return path


def fetch_tiger(out_dir: Path = config.RAW / "boundaries"):
    """宾州普查区、PUMA、place（城市边界）TIGER/Line 2024，以及 2020 普查区 → PUMA 关系文件。"""
    st = config.STATE_FIPS
    urls = [f"{TIGER}/TRACT/tl_2024_{st}_tract.zip", f"{TIGER}/PUMA20/tl_2024_{st}_puma20.zip",
            f"{TIGER}/PLACE/tl_2024_{st}_place.zip", TRACT_PUMA]
    return [_download(u, out_dir / u.rsplit("/", 1)[1]) for u in urls]


def fetch_block_population(out_dir: Path = config.RAW / "census_blocks"):
    """费城 2020 年街区边界与人口（TIGERweb，POP100 = 2020 年普查人口）。"""
    return _download(f"{TIGERWEB_BLOCKS}/query", out_dir / "blocks2020_phl.geojson",
                     where=f"STATE='{config.STATE_FIPS}' AND COUNTY='{config.COUNTY_FIPS}'",
                     outFields="*", outSR=4326, f="geojson")


def fetch_acs_tracts(out_dir: Path = config.RAW / "acs"):
    """费城普查区 ACS 5 年版：config.ACS_VARS 的估计值和 MOE（需要 API key）。"""
    est = list(config.ACS_VARS)
    cols = ["NAME"] + est + [v[:-1] + "M" for v in est]
    return _download(f"{CENSUS_API}/{config.ACS_YEAR}/acs/acs5", out_dir / f"acs5_{config.ACS_YEAR}_tracts.json",
                     get=",".join(cols), key=census_key(),
                     **{"for": "tract:*", "in": f"state:{config.STATE_FIPS} county:{config.COUNTY_FIPS}"})


def fetch_pums(out_dir: Path = config.RAW / "pums"):
    """PUMS 5 年版个人（p）和住户（h）CSV，每州两个 zip，州见 config.PUMS_STATES；另存数据字典。"""
    names = [f"csv_{t}{s}.zip" for s in config.PUMS_STATES for t in "ph"]
    dict_name = f"PUMS_Data_Dictionary_{config.PUMS_YEAR - 4}-{config.PUMS_YEAR}.csv"
    return ([_download(f"{PUMS_FTP}/{config.PUMS_YEAR}/5-Year/{n}", out_dir / n) for n in names]
            + [_download(f"{PUMS_DICT}/{dict_name}", out_dir / dict_name)])


def fetch_lodes_wac(year: int = config.LODES_YEAR, out_dir: Path = config.RAW / "lodes"):
    """LODES WAC（宾州，S000，JT00）。"""
    name = f"pa_wac_S000_JT00_{year}.csv.gz"
    return _download(f"{LODES}/wac/{name}", out_dir / name)


def fetch_lodes_od(year: int = config.LODES_YEAR, out_dir: Path = config.RAW / "lodes"):
    """LODES OD main（居住地和工作地都在宾州），工作类型 config.OD_JOB_TYPE。"""
    name = f"pa_od_main_{config.OD_JOB_TYPE}_{year}.csv.gz"
    return _download(f"{LODES}/od/{name}", out_dir / name)


def fetch_osm(out_dir: Path = config.RAW / "osm"):
    """OSM 步行网络快照（OSMnx，network_type="walk"，保留全部分量），存成 GraphML；最大连通分量和投影在第 00 步做。"""
    import osmnx as ox
    path = out_dir / "philly_walk.graphml"
    if not path.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        ox.save_graphml(ox.graph_from_place(config.PLACE_NAME, network_type="walk", retain_all=True), path)
    return path


def fetch_gtfs(out_dir: Path = config.RAW / "gtfs"):
    """SEPTA GTFS：原样保存 gtfs_public.zip，并把其中的公交 feed 解压到 out_dir/google_bus/。"""
    path = _download(GTFS_URL, out_dir / "gtfs_public.zip")
    with zipfile.ZipFile(path) as z:
        z.extract("google_bus.zip", out_dir)
    zipfile.ZipFile(out_dir / "google_bus.zip").extractall(out_dir / "google_bus")
    return out_dir / "google_bus"


def fetch_streetlights(out_dir: Path = config.RAW / "streetlights"):
    """OpenDataPhilly Street_Poles 全部灯杆（含 type、nlumin），分页取完存成一个 GeoJSON。"""
    path = out_dir / "street_poles.geojson"
    if path.exists():
        return path
    feats, offset = [], 0
    while True:
        r = requests.get(f"{POLES_URL}/query", timeout=120, params={
            "where": "1=1", "outFields": "*", "outSR": 4326, "f": "geojson",
            "orderByFields": "objectid", "resultOffset": offset, "resultRecordCount": 2000})
        r.raise_for_status()
        page = r.json()["features"]
        feats += page
        if len(page) < 2000:
            break
        offset += 2000
    out_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"type": "FeatureCollection", "features": feats}))
    return path


def fetch_311_outages(out_dir: Path = config.RAW / "outages_311"):
    """311 工单：service_name 含 light 的全部类别，报修时间在 config.OUTAGE_WINDOW 内；类别在 notebook 里再筛。"""
    start, end = config.OUTAGE_WINDOW
    q = (f"SELECT * FROM public_cases_fc WHERE service_name ILIKE '%light%' "
         f"AND requested_datetime >= '{start}' AND requested_datetime < date '{end}' + 1")
    return _download(CARTO_URL, out_dir / f"311_light_{start}_{end}.csv", q=q, format="csv")


if __name__ == "__main__":
    for fn in [fetch_tiger, fetch_block_population, fetch_lodes_wac, fetch_lodes_od, fetch_osm, fetch_gtfs,
               fetch_streetlights, fetch_311_outages, fetch_pums, fetch_acs_tracts]:
        print(fn.__name__, "->", fn())
