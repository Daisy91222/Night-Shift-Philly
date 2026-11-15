# Who Keeps Philadelphia Running After Dark?

费城夜班通勤者的公交可达性与脆弱性，以及 Owl 班次减少对效率和安全的影响。MUSA 5500 期末项目。

设计细节和决策见项目里的《夜班通勤项目 · 工程记录》。本 README 只说明代码怎么组织、按什么顺序运行。

## 运行顺序

| Notebook | 步骤 | 读入 | 写出（`data/processed/`） |
| --- | --- | --- | --- |
| `00_network` | 步行网络、边界、普查区 → PUMA | OSM | `00_*` |
| `01_profile` | PUMS 群体画像与全市参数 | PUMS | `01_*`（含 `01_pums_params.json`） |
| `02_place_on_network` | 居住端与工作端落到节点 | ACS、街区人口、LODES、`00_*`、`01_pums_params.json` | `02_*` |
| `03_night_service` | 夜间站点 × 线路表 | GTFS | `03_*` |
| `04_access` | 选站选线、覆盖率、绕行 | `00_*`、`02_*`、`03_*` | `04_*` |
| `05a_lighting` | 有效路灯密度 | 路灯、311、`00_*`、`03_*` | `05a_*` |
| `05b_corridors` | 通勤走廊与安全指标 | `00_*`、`02_*`、`04_*`、`05a_*` | `05b_*` |
| `06_scenarios` | 四个情景对比 | 以上全部 | `06_*`、`data/web/` |

`00`、`01`、`03` 互不依赖，可以并行；`05a` 只需要网络和站点，可以早于 `04` 做。

## 目录

```
config.py        全部参数和输出文件路径（调参只改这里）
src/             可重复调用的计算函数
  fetch.py       下载原始数据
  pums.py        PUMS 加权统计
  network.py     步行网络；普查区 → 街区 → 节点
  gtfs.py        夜间站点 × 线路表
  access.py      第 4 步：选站选线（第 6 步复用）
  lighting.py    第 5a 步：有效路灯密度
  corridors.py   第 5b 步：最短路径与走廊（第 6 步复用）
  scenarios.py   第 6 步：修改站点 × 线路表并重跑
notebooks/       每步一个 notebook：讲清楚做了什么、出图
data/raw/        原始下载，只读不改，不进 git
data/processed/  每步的输出，步骤之间唯一的交接点
data/web/        导出给网站和仪表盘的轻量文件
dashboard/       Panel 仪表盘
site/            网站（Quarto 或 Vite，待定）
```

## 三条约定

1. **每个 notebook 只读 `data/processed/` 里的文件**，不依赖其他 notebook 内存中的变量。任何一步都可以单独重跑。
2. **第 4 步和第 5b 步的计算写在 `src/` 里**，签名是“输入站点 × 线路表 → 输出结果”，第 6 步的每个情景都调用同一个函数。
3. **单位**：`EPSG:2272` 的单位是英尺。几何缓冲和空间连接先用 `config.m_to_ft()` 换算；网络距离一律用米。

## 环境

```bash
conda env create -f environment.yml
conda activate night-shift
cp .env.example .env   # 填入 Census API key
jupyter lab
```

pandana 用 conda-forge 安装最稳，pip 安装常在编译时失败。
