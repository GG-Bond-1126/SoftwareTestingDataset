# -*- coding: utf-8 -*-
"""由 data/external.json 生成 links.html（精选外链页）。

只做导读与跳转，不复制原文，版权归原作者。
"""
import os, json, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "external.json")
OUT = os.path.join(ROOT, "links.html")
BASE = "https://37lh5701lxo5frtwh6h.traesite.cn"

TITLE = "精选外链 · 软件测试资料集"
DESC = "站外精选：公众号测试长文与开源项目导读，按主题整理并链接原文。"

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='14' fill='%230d141d'/%3E%3Ctext x='50%25' y='54%25' "
           "text-anchor='middle' dominant-baseline='middle' font-family='monospace' font-size='30' "
           "fill='%233ddc84'%3EQA%3C/text%3E%3C/svg%3E")


def e(s):
    return H.escape(str(s or ""), quote=True)


def stars(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return "0"
    return "%.1fk" % (n / 1000.0) if n >= 1000 else str(n)


def render_wechat(item):
    topics = "".join('<span class="link-tag">#%s</span>' % e(t) for t in item.get("topics") or [])
    points = "".join("<li>%s</li>" % e(p) for p in item.get("points") or [])
    meta = []
    if item.get("account"):
        meta.append('<span class="link-account">%s</span>' % e(item["account"]))
    if item.get("date"):
        meta.append("<span>%s</span>" % e(item["date"]))
    related = ""
    if item.get("related_post"):
        related = ('<a class="link-related" href="posts/%s.html">站内延伸 →</a>'
                   % e(item["related_post"]))
    return (
        '      <article class="link-card">\n'
        '        <div class="link-meta">%s</div>\n'
        '        <h3><a href="%s" target="_blank" rel="noopener noreferrer">%s</a></h3>\n'
        '        <p class="link-summary">%s</p>\n'
        '        <ul class="link-points">%s</ul>\n'
        '        <div class="link-foot"><span class="link-topics">%s</span>%s</div>\n'
        '      </article>'
    ) % ("".join(meta), e(item.get("url")), e(item.get("title")),
         e(item.get("summary")), points, topics, related)


def render_github(item):
    topics = "".join('<span class="link-tag">#%s</span>' % e(t) for t in item.get("topics") or [])
    return (
        '        <li class="repo-item">\n'
        '          <div class="repo-head"><a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
        '<span class="repo-stars">★ %s</span></div>\n'
        '          <p>%s</p>\n'
        '          <div class="link-topics">%s</div>\n'
        '        </li>'
    ) % (e(item.get("url")), e(item.get("title")), stars(item.get("stars")),
         e(item.get("summary")), topics)


data = {"wechat": [], "github": []}
if os.path.exists(DATA):
    data = json.load(open(DATA, encoding="utf-8"))
wechat = [x for x in data.get("wechat", []) if x.get("url") and x.get("title")]
repos = [x for x in data.get("github", []) if x.get("url") and x.get("title")]

blocks = []
if wechat:
    blocks.append(
        '    <section class="link-block">\n'
        '      <h2>公众号精选 <span class="link-count">%d 篇</span></h2>\n'
        '      <div class="link-grid">\n%s\n      </div>\n'
        '    </section>' % (len(wechat), "\n".join(render_wechat(x) for x in wechat)))
if repos:
    blocks.append(
        '    <section class="link-block">\n'
        '      <h2>GitHub 资源 <span class="link-count">%d 个</span></h2>\n'
        '      <ul class="repo-list">\n%s\n      </ul>\n'
        '    </section>' % (len(repos), "\n".join(render_github(x) for x in repos)))

body = "\n\n".join(blocks) if blocks else '    <p class="link-note">暂时还没有收录内容。</p>'

doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<link rel="icon" href="%s">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html">
      <span class="brand-mark">QA</span>
      <span class="brand-text">
        <span class="brand-name">软件测试资料集</span>
        <span class="brand-sub">by GG Bond</span>
      </span>
    </a>
    <nav class="nav-links">
      <a href="index.html">首页</a>
      <a href="index.html#posts">文章</a>
      <a href="tags.html">标签</a>
      <a href="paths.html">路径</a>
      <a href="links.html" class="active">外链</a>
      <a href="favorites.html">收藏</a>
      <a href="about.html">关于</a>
    </nav>
    <a class="nav-gh" href="index.html#posts">./notes →</a>
  </div>
</header>

<main>
  <div class="page-head">
    <h1>精选外链</h1>
    <p>站外值得一读的测试实践：公众号长文与开源项目。这里只写导读，不转载正文，版权归原作者，点击标题前往原文。</p>
  </div>
  <div class="page-body">
%s

    <p class="link-note">外链可能失效或被作者删除。如果遇到打不开的，欢迎在 GitHub 仓库提 Issue 告知。</p>
  </div>
</main>

<footer class="site-footer">
  <div class="wrap footer-inner">
    <span>© 2026 软件测试资料集 · GG Bond</span>
    <span>Built with plain HTML / CSS / JS · <a href="index.html">回到首页</a></span>
  </div>
</footer>

<script src="assets/main.js"></script>
</body>
</html>
""" % (TITLE, DESC, FAVICON, body)

open(OUT, "w", encoding="utf-8", newline="\n").write(doc)
print("links.html: wechat=%d github=%d" % (len(wechat), len(repos)))
