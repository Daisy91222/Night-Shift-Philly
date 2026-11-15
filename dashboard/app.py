"""Panel 仪表盘：选择情景和 Owl 站点，显示服务范围、走廊和变化。

只读 data/processed/ 和 data/web/，不做计算。
本地运行：panel serve dashboard/app.py --show
部署方式待定：panel convert（Pyodide，放 GitHub Pages）或 Hugging Face Spaces，尽早测试。
"""
import sys
from pathlib import Path

import panel as pn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402

pn.extension()

scenario = pn.widgets.Select(name="情景", options=list(config.SCENARIOS))
stop = pn.widgets.Select(name="Owl 站点", options=[])  # TODO：从 03_owl_stops 读入

# TODO：
# 1. 地图：所选站点的服务范围（选择该站的节点）与通勤走廊
# 2. 指标卡：现状 vs 情景的可达时间、照明不足步行距离
# 3. 脆弱性：无车通勤比例与情景变化并列

pn.template.FastListTemplate(
    title="Who Keeps Philadelphia Running After Dark?",
    sidebar=[scenario, stop],
    main=[pn.pane.Markdown("TODO")],
).servable()
