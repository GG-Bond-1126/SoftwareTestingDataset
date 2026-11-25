# 软件测试资料集

> 自动化测试与 AI 测试的实践笔记：把公开资料整理成能直接照着做的长文。

**在线阅读：<https://37lh5701lxo5frtwh6h.traesite.cn>**
**源码仓库：<https://github.com/GG-Bond-1126/SoftwareTestingDataset>**

纯静态的测试知识库，124 篇文章，覆盖 Web / APP / PC 自动化、接口测试、Python、Git、数据库，以及 AI 测试与 AI 提效落地。每篇文章按「机制拆解 → 从最小可用到生产可用 → 常见坑 → 上线检查清单」组织，代码示例可直接运行。

---

## 目录

- [内容概览](#内容概览)
- [功能特性](#功能特性)
- [目录结构](#目录结构)
- [本地运行](#本地运行)
- [构建与校验](#构建与校验)
- [部署](#部署)
- [可下载的 AI Skill](#可下载的-ai-skill)
- [写作规范](#写作规范)
- [更新记录](#更新记录)
- [贡献与许可](#贡献与许可)

## 内容概览

| 维度 | 数量 | 说明 |
|---|---|---|
| 文章 | 124 篇 | 每篇 2500 字以上，8–13 个章节，6–12 个代码块 |
| 学习路径 | 4 条 | 四周入门 / Web 自动化进阶 / AI 测试落地 / 大模型应用测试 |
| 架构图 | 15 张 | 内联 SVG，深浅色自适应，随文章一起走 |
| 可下载 Skill | 10 个 | AI 生成类任务的 `SKILL.md`，见下表 |
| 标签 | 50 个 | 按主题聚合浏览 |

### 十大方向

1. **AI 测试**：Prompt 测试、幻觉测试、模型评测、RAG 测试、内容生成测试、安全测试、Agent 测试进阶
2. **AI 提效落地**：需求点分析、测试点生成、业务用例生成、接口用例生成、测试数据生成、回归圈选、缺陷根因、日志分析、用例维护、提效度量
3. **Web 自动化**：Playwright / Selenium、等待策略、元素定位、Page Object、视觉回归、CI 集成
4. **APP 自动化**：小程序、推送、弱网、Hybrid / WebView、崩溃与性能、测试数据管理
5. **PC 自动化**：桌面端驱动、造数与清理、报告与取证
6. **接口测试**：requests、鉴权、断言设计、契约与 Mock
7. **Python**：语法、函数、装饰器、并发、性能分析
8. **Git**：分支模型、冲突解决、cherry-pick、子模块、Tag 发布
9. **数据库测试**：索引验证、事务隔离、缓存一致性、数据校验
10. **工程与度量**：报告体系、质量门禁、提效指标口径

## 功能特性

- **全文搜索**：标题、分类、标签、章节标题与正文摘要一起检索，`Ctrl/⌘ + K` 唤起，命中词高亮，正文命中单独标注
- **文章目录**：从章节标题自动生成，滚动高亮当前章节，宽屏固定在左侧
- **串读**：上一篇 / 下一篇、按标签与分类算出的 3 篇相关阅读、正文术语内链
- **收藏**：文章页一键收藏，独立收藏页支持导出 / 导入 JSON，多标签页实时同步
- **最近阅读**：首页显示继续阅读入口，接着上次的位置看
- **深浅色主题**：一键切换并记住选择，变量驱动，无闪烁
- **PWA**：可安装到桌面，断网可读已访问过的文章；路径全部相对，支持部署在子路径
- **检查清单**：每篇文章可一键下载 Markdown 版检查清单
- **SEO**：sitemap、RSS、canonical、Open Graph、JSON-LD 结构化数据齐备

## 目录结构

```
.
├── index.html              首页（搜索、只看收藏、最近阅读）
├── about.html              关于
├── tags.html               标签总览
├── paths.html              学习路径（4 条阅读顺序 + 专题合集）
├── links.html              精选外链（公众号长文与 GitHub 项目导读，构建生成）
├── favorites.html          我的收藏（导入 / 导出）
├── 404.html
├── manifest.webmanifest    PWA 清单（相对路径）
├── sw.js                   Service Worker（相对路径，network-first + 缓存回退）
├── sitemap.xml / robots.txt / rss.xml
├── posts/                  124 篇文章
├── data/
│   └── external.json       精选外链数据（源站、标题、导读、要点）
├── assets/
│   ├── style.css           全站样式（深浅色变量 + 组件样式）
│   ├── main.js             搜索、目录、收藏、主题、最近阅读、SW 注册
│   ├── posts-index.json    文章索引（搜索与相关阅读数据源）
│   ├── downloads/          10 个可下载的 SKILL.md
│   ├── icon-192.png / icon-512.png
│   └── og-cover.png        分享封面 1200×630
└── tools/                  构建与校验脚本
```

## 本地运行

不要直接双击 `index.html`，浏览器会拦截 `fetch` 索引文件的请求。用任意静态服务器：

```bash
python -m http.server 8899
# 打开 http://127.0.0.1:8899/
```

## 构建与校验

```bash
python tools/build.py
```

可选依赖：`pip install pypinyin`。装了它，索引会额外生成标题拼音首字母，支持用 `jkcscs` 这类缩写搜到「接口测试」相关文章；没装则自动跳过，构建照常成功。

依次执行八步，任一步失败即中断并给出原因：

1. `build_data.py` — 扫描 `posts/` 生成 `assets/posts-index.json`
2. `rebuild_index2.py` — 按框架与分类重建首页文章卡片
3. `seo.py` — 生成 sitemap、RSS 与 OG 元信息
4. `pwa_seo.py` — 生成 manifest 与 Service Worker，注入 PWA 元信息
5. `validate.py` — HTML 结构与标签闭合校验
6. `health_check.py` — 全站链接、锚点、下载文件体检
7. `final_check.py` — 中文引号与 meta description 长度检查
8. `asset_guard.py` — 体积守卫：图片单张 ≤300 KB、索引 ≤600 KB、单页 ≤300 KB、整站 ≤6 MB

第 5–8 步都会以非零退出码报错，CI 中表现为失败。

单独运行某一项：

```bash
python tools/build_data.py     # 只重建文章索引
python tools/health_check.py   # 只跑链接与锚点体检
python tools/asset_guard.py    # 只跑体积守卫
python tools/gen_assets.py     # 重新生成封面与图标（需 Pillow + 微软雅黑字体）
```

每次 push 到 `main` 或提 PR，GitHub Actions 会自动跑一遍完整构建（见 `.github/workflows/build.yml`）。

## 部署

站点是纯静态文件，整个目录即站点根，无需构建产物。

### 方式一：Trae 部署插件

在 Trae 中打开本目录，用部署插件发布。站点已设为所有人可见，重新部署会沿用该设置。

### 方式二：GitHub Pages

1. 仓库 Settings → Pages
2. Source 选 `Deploy from a branch`，分支 `main`，目录 `/ (root)`
3. 访问 `https://<用户名>.github.io/SoftwareTestingDataset/`

Service Worker 注册与 manifest 路径均为相对路径，因此子路径部署时 PWA 与离线缓存同样可用。

### 方式三：其它静态托管

Netlify / Vercel 拖拽目录即可，或上传对象存储 + CDN。不要开启对 `sw.js` 的强缓存，否则更新不生效。

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

所有生成类 Skill 内置同一条铁律：**只能依据用户提供的文档、代码、日志原文和当前上下文输出，不允许凭想象补充业务规则、字段名、阈值或版本号；信息不足时进「待确认清单」，标不出来源的结论不得进入正式产出。** 这条约束写在每个 `SKILL.md` 的最前面；Skill 本身不附带脚本，执行方式由使用者的 AI 工具决定。

## 写作规范

- 每篇 2500 字以上，至少 8 个二级标题，每个标题下 2–4 段散文，不做要点罗列
- 代码块 6–12 个，示例可直接运行，不写占位断言
- 讲清楚「什么时候不该用」，给出取舍而不只讲优点
- 结尾固定：上线检查清单 + 参考来源（官方文档）
- 中文正文不使用英文双引号，强调统一用「」
- meta description 不超过 60 字，且不含英文双引号

## 更新记录

| 版本 | 内容 |
|---|---|
| V16 | Service Worker 与 manifest 改为相对路径，支持子路径部署 |
| V15 | 关于页个人简介从业时长修正为第 7 年 |
| V14 | 修复首页「只看收藏」激活态文字与背景同色不可见 |
| V13 | 内容串联（内链 / 最近阅读 / 搜索高亮 / ⌘K / 标签直达）、15 张内联 SVG 架构图、构建流水线与链接体检 |
| V11 | 文章目录、上下篇与相关阅读、标签页、学习路径、收藏页、SEO 基础设施 |

## 贡献与许可

发现问题或想补充主题，欢迎提 Issue 或直接提交 PR。提交前请先跑一遍 `python tools/build.py`，确保索引与校验全绿。

内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh) 协议，代码示例采用 MIT 协议。转载或引用请注明来源。
