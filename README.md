# 3C Scout

一个面向个人兴趣的新品与好价聚合站，自动收集中英文公开 RSS / Atom 信息，重点覆盖：

- 3C 数码、存储、充电与桌面设备
- 音频、游戏掌机与外设、Maker 小硬件
- 厨房用品、生活小物、收纳、清洁与智能家居

网站把内容分为“新商品”和“好 Deal”两条流，提供搜索、分类、中英文筛选、排序、折叠详情和浏览器本地收藏。所有商品保留原始来源链接，识别到商家链接时会额外提供“查看商品”。

## 自动更新

`.github/workflows/daily-refresh.yml` 会在每天 `15:15 UTC` 自动运行，对应西雅图冬令时约 `07:15`、夏令时约 `08:15`。也可在仓库 **Actions → Refresh products and deploy → Run workflow** 手动刷新。

每个来源独立抓取；单个源失败不会阻断其他数据。最近 14 天的可用条目会被保留，页面底部会显示本轮来源健康状态。

## 发布

首次使用时，在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。之后工作流会在刷新数据后直接部署静态站点。

默认地址：`https://ximinhu66.github.io/3C-scout/`

## 本地检查

```bash
python -m unittest discover -s tests -v
python -m http.server 8000
```

不需要 API key，也不需要单独服务器。价格和库存仅从公开标题/摘要提取，最终以商家结账页为准。
