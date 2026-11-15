"""第 0、2 步：步行网络，以及“街区 → 节点”分配。

网络距离用米（OSMnx 边长 `length`）；几何操作在 EPSG:2272（英尺）下进行。
"""
import geopandas as gpd
import pandas as pd

import config


def build_walk_network(place: str = config.PLACE_NAME):
    """用 OSMnx 下载步行网络，返回 (nodes, edges) 两个 GeoDataFrame，投影到 config.CRS。

    nodes 保留 osmid、x、y；edges 保留 u、v、length（米）、geometry。
    """
    raise NotImplementedError


def to_pandana(nodes: gpd.GeoDataFrame, edges: gpd.GeoDataFrame):
    """由节点和边构建 pandana.Network，边权重为 length（米）。每次运行从 parquet 重建。"""
    raise NotImplementedError


def block_node_lookup(blocks: gpd.GeoDataFrame, nodes: gpd.GeoDataFrame,
                      buffer_m: float = config.BLOCK_NODE_BUFFER_M) -> pd.DataFrame:
    """街区 → 节点对照表，每行一个 (block_geoid, node_id, share)。

    1. 街区多边形外扩 buffer_m（换成英尺），取落在范围内的节点；
    2. 每个街区内 share = 1 / 节点数；
    3. 外扩后仍无节点的街区：质心 → 最近节点，share = 1。
    居住端和工作端共用这一张表。
    """
    raise NotImplementedError


def tract_to_blocks(tract_counts: pd.DataFrame, block_pop: pd.DataFrame,
                    value_cols: list[str]) -> pd.DataFrame:
    """按 2020 年人口比例把普查区计数分到街区。

    block_value = tract_value × block_pop / tract_pop；零人口街区自然为 0。
    """
    raise NotImplementedError


def blocks_to_nodes(block_values: pd.DataFrame, lookup: pd.DataFrame,
                    value_cols: list[str]) -> pd.DataFrame:
    """用 block_node_lookup 把街区数值平均分给节点，并按节点加总（一个路口可由多个街区共用）。"""
    raise NotImplementedError
