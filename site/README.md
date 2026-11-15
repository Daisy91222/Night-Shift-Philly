# 网站

待定：Quarto 还是 Vite。

- 课程评分标准的“写作”一项写的是 *Multi-page Quarto site*。如果改用 Vite，先和老师确认是否接受。
- 两者都从同一处取材：图和数字来自 `notebooks/` 的输出，交互地图的数据来自 `data/web/`。
- Quarto：可以直接把 `notebooks/*.ipynb` 渲染成页面（数据收集、分析、可视化、结果各一页）。
- Vite：notebook 负责导出 `data/web/` 下的 GeoJSON / JSON，前端只读这些文件。
