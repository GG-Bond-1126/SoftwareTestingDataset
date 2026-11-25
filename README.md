# 软件测试资料集

> 自动化测试与 AI 测试的实践笔记：把公开资料整理成能直接照着做的长文。

**在线阅读：https://37lh5701lxo5frtwh6h.traesite.cn**

一个纯静态的测试知识库，124 篇文章，覆盖 Web / APP / PC 自动化、接口测试、Python、Git、数据库，以及 AI 测试与 AI 提效落地。每篇文章都按「机制拆解 → 从最小可用到生产可用 → 常见坑 → 上线检查清单」组织，代码可直接运行。

---

## 内容概览

| 维度 | 数量 | 说明 |
|---|---|---|
| 文章 | 124 篇 | 每篇 2500 字以上，8–13 个章节，6–12 个代码块 |
| 学习路径 | 4 条 | 四周入门 / Web 自动化进阶 / AI 测试落地 / 大模型应用测试 |
| 架构图 | 15 张 | 内联 SVG，深浅色自适应，随文章一起走 |
| 可下载 Skill | 10 个 | AI 生成类任务的 `SKILL.md`，见下表 |
| 标签 | 50 个 | 按标签聚合页面浏览 |

### 十大方向

1. **AI 测试**：Prompt 测试、幻觉测试、模型评测、RAG 测试、内容生成测试、安全测试、Agent 测试进阶
2. **AI 提效落地**：需求点分析、测试点生成、业务用例生成、接口用例生成、测试数据生成、回归圈选、缺陷根因、日志分析、用例维护、提效度量
3. **Web 自动化**：Playwright / Selenium、等待策略、元素定位、Page Object、视觉回归、CI 集成
4. **APP 自动化**：小程序、推送、弱网、Hybrid/WebView、崩溃与性能、测试数据管理
5. **PC 自动化**：桌面端驱动、造数与清理、报告与取证
6. **接口测试**：requests、鉴权、断言设计、契约与 Mock
7. **Python**：语法、函数、装饰器、并发、性能分析
8. **Git**：分支模型、冲突解决、cherry-pick、子模块、Tag 发布
9. **数据库测试**：索引验证、事务隔离、缓存一致性、数据校验
10. **工程与度量**：报告体系、质量门禁、提效指标口径

## 功能特性

- **全文搜索**：标题、分类、标签、所有章节标题与正文摘要一起检索，`Ctrl/⌘ + K` 唤起，命中词高亮，正文命中会单独标注
- **文章目录**：从章节标题自动生成，滚动高亮当前章节，宽屏固定在左侧
- **串读**：上一篇 / 下一篇、按标签与分类算出的 3 篇相关阅读、正文术语内链
- **收藏**：文章页一键收藏，独立收藏页支持导出 / 导入 JSON，多标签页实时同步
- **最近阅读**：首页显示「继续阅读」，接着上次的位置看
- **深浅色主题**：一键切换并记住选择
- **PWA**：可安装到桌面，断网可读已访问过的文章
- **检查清单**：每篇文章可一键下载 Markdown 版检查清单（章节列表 + 5 条上线自查）
- **SEO**：sitemap、RSS、canonical、Open Graph、JSON-LD 结构化数据齐备

## 目录结构

```
.
├── index.html              首页（搜索、收藏筛选、最近阅读入口）
├── about.html              关于
├── tags.html               标签总览（按标签聚合）
├── paths.html              学习路径（4 条阅读顺序）
├── favorites.html          我的收藏（导入 / 导出）
├── 404.html
├── manifest.webmanifest    PWA 清单
├── sw.js                   Service Worker（离线缓存）
├── sitemap.xml / robots.txt / rss.xml
├── posts/                  124 篇文章
├── assets/
│   ├── style.css           全站样式（含深浅色变量）
│   ├── main.js             搜索、目录、收藏、主题、最近阅读
│   ├── posts-index.json    文章索引（搜索与相关阅读用）
│   ├── downloads/          10 个可下载的 SKILL.md
│   ├── icon-192.png / icon-512.png
│   └── og-cover.png        分享封面 1200×630
└── tools/                  构建与校验脚本
```

## 本地运行

任选一种静态服务器（不要直接双击 `index.html`，`fetch` 索引会被浏览器拦截）：

```bash
python -m http.server 8899
# 浏览器打开 http://127.0.0.1:8899/
```

## 构建与校验

```bash
python tools/build.py
```

依次执行：生成文章索引 → 重建首页卡片 → 生成 sitemap/RSS/OG → 生成 PWA 元信息 → HTML 结构校验 → 全站链接与锚点体检 → 引号与 meta 检查。任一步失败会中断并给出原因。

单独跑某一项：

```bash
python tools/build_data.py     # 重建 assets/posts-index.json
python tools/health_check.py   # 全站链接 / 锚点 / 下载文件体检
python tools/gen_assets.py     # 重新生成分享封面与图标（需 Pillow + 微软雅黑字体）
```

## 可下载的 AI Skill

每个 Skill 都是可直接放进 AI 编程助手使用的 `SKILL.md`，下载地址在对应文章末尾。

| Skill | 用途 | 下载 |
|---|---|---|
| 需求点分析 | 把 PRD 拆成可测的需求点与待确认清单 | [skill-requirement-analysis.md](assets/downloads/skill-requirement-analysis.md) |
| 测试点生成 | 从需求点推导可评审的测试点 | [skill-testpoint-generation.md](assets/downloads/skill-testpoint-generation.md) |
| 业务用例生成 | 按用户场景组织端到端用例 | [skill-business-case-generation.md](assets/downloads/skill-business-case-generation.md) |
| 接口用例生成 | 按字段、状态码、边界组织接口用例 | [skill-api-testcase-generation.md](assets/downloads/skill-api-testcase-generation.md) |
| 测试数据生成 | 按字段约束设计可用数据集 | [skill-testdata-generation.md](assets/downloads/skill-testdata-generation.md) |
| 回归范围圈选 | 用改动影响面替代全量回归 | [skill-regression-scope.md](assets/downloads/skill-regression-scope.md) |
| 缺陷根因分析 | 用上下文缩小排查面 | [skill-defect-rootcause.md](assets/downloads/skill-defect-rootcause.md) |
| 日志分析 | 从日志里提炼异常模式与线索 | [skill-log-analysis.md](assets/downloads/skill-log-analysis.md) |
| 用例维护 | 清理冗余、合并重复、补齐缺口 | [skill-case-maintenance.md](assets/downloads/skill-case-maintenance.md) |
| 提效度量 | 按明确口径统计提效指标 | [skill-qa-metrics.md](assets/downloads/skill-qa-metrics.md) |

### Skill 的硬性约束

所有生成类 Skill 都内置同一条铁律：**只能依据用户提供的文档、代码、日志原文和当前上下文输出，不允许凭想象补充业务规则、字段名、阈值或版本号；信息不足时进「待确认清单」，标不出来源的结论不得进入正式产出。** 这条约束写在每个 `SKILL.md` 的最前面。

## 内容标准

- 每篇 2500 字以上，至少 8 个二级标题，每个标题下 2–4 段散文，不是要点罗列
- 代码块 6–12 个，示例可直接运行；不写 `assert 1+1==2` 这类占位
- 讲清楚「什么时候不该用」，给出取舍而不是只讲优点
- 结尾固定：上线检查清单 + 参考来源（官方文档）
- 中文正文不使用英文双引号，强调统一用「」

## 部署

本站为纯静态站点，可部署到任意静态托管（GitHub Pages、Netlify、Vercel、对象存储 + CDN）。部署时整个目录即为站点根，无需构建步骤。

## 反馈

发现问题或想补充某个主题，欢迎提 Issue 或直接提交 PR。

## 许可

内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh) 协议，代码示例采用 MIT 协议。转载或引用请注明来源。
