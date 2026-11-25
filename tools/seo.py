# -*- coding: utf-8 -*-
"""由仓库根目录解析路径，确保脚本在任意机器上可运行。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Generate sitemap/robots/rss and inject canonical + Open Graph + JSON-LD into every page."""
import os, re, glob, json, html as H, datetime

ROOT = ROOT
BASE = "https://37lh5701lxo5frtwh6h.traesite.cn"
POSTS = os.path.join(ROOT, "posts")

items = json.load(open(os.path.join(ROOT, "assets", "posts-index.json"), encoding="utf-8"))
by_slug = {it["slug"]: it for it in items}


def mtime_iso(path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")


def mtime_rfc(path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%a, %d %b %Y %H:%M:%S +0800")


# ---------------- inject head tags ----------------
def inject(path, url, title, desc, is_article, extra=None):
    s = open(path, encoding="utf-8").read()
    if 'property="og:title"' in s:
        return False
    block = ['<link rel="canonical" href="%s">' % url,
             '<meta property="og:type" content="%s">' % ("article" if is_article else "website"),
             '<meta property="og:site_name" content="软件测试资料集">',
             '<meta property="og:title" content="%s">' % H.escape(title, quote=True),
             '<meta property="og:description" content="%s">' % H.escape(desc, quote=True),
             '<meta property="og:url" content="%s">' % url,
             '<meta property="og:locale" content="zh_CN">',
             '<meta name="twitter:card" content="summary">',
             '<meta name="twitter:title" content="%s">' % H.escape(title, quote=True),
             '<meta name="twitter:description" content="%s">' % H.escape(desc, quote=True)]
    if extra:
        block.extend(extra)
    s = s.replace("</head>", "\n".join(block) + "\n</head>", 1)
    open(path, "w", encoding="utf-8").write(s)
    return True


n = 0
for f in sorted(glob.glob(os.path.join(POSTS, "*.html"))):
    slug = os.path.basename(f)[:-5]
    it = by_slug.get(slug)
    if not it:
        continue
    url = "%s/posts/%s.html" % (BASE, slug)
    ld = {"@context": "https://schema.org", "@type": "BlogPosting",
          "headline": it["title"], "description": it["desc"], "inLanguage": "zh-CN",
          "url": url, "articleSection": it["cat"], "keywords": ", ".join(it["tags"]),
          "author": {"@type": "Person", "name": "GG Bond"},
          "publisher": {"@type": "Organization", "name": "软件测试资料集"},
          "datePublished": mtime_iso(f), "dateModified": mtime_iso(f)}
    extra = ['<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False, separators=(",", ":"))]
    if inject(f, url, it["title"], it["desc"], True, extra):
        n += 1

for name, title, desc in [
    ("index.html", "软件测试资料集 · GG Bond", "软件测试资料集：自动化测试与 AI 测试的实践笔记，覆盖 AI 用例生成、Agent 测试、脚本自愈与接口自动化。"),
    ("about.html", "关于 · 软件测试资料集", "关于这个资料集：收录范围、内容标准与写作原则。"),
    ("tags.html", "标签总览 · 软件测试资料集", "按标签浏览全部测试笔记：自动化框架、AI 测试、性能、数据与工具链。"),
    ("paths.html", "学习路径 · 软件测试资料集", "按目标编排的阅读顺序：自动化入门、Web 进阶、AI 测试落地与大模型应用测试。"),
    ("favorites.html", "我的收藏 · 软件测试资料集", "查看已收藏的测试笔记，支持导出与导入收藏列表。"),
    ("links.html", "精选外链 · 软件测试资料集", "站外精选：公众号测试长文与开源项目导读，按主题整理并链接原文。"),
]:
    p = os.path.join(ROOT, name)
    if os.path.exists(p) and inject(p, BASE + "/" + name, title, desc, False):
        n += 1
print("og injected:", n)

# ---------------- sitemap ----------------
rows = []
for name in ["index.html", "about.html", "tags.html", "paths.html", "links.html"]:
    p = os.path.join(ROOT, name)
    rows.append((BASE + "/" + name, mtime_iso(p), "1.0" if name == "index.html" else "0.6"))
for f in sorted(glob.glob(os.path.join(POSTS, "*.html"))):
    slug = os.path.basename(f)[:-5]
    rows.append((BASE + "/posts/" + slug + ".html", mtime_iso(f), "0.8"))
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, mod, pri in rows:
    xml.append("<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (loc, mod, pri))
xml.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml))
print("sitemap urls:", len(rows))

# ---------------- robots ----------------
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
    "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)

# ---------------- rss ----------------
rss = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<rss version="2.0"><channel>',
       "<title>软件测试资料集 · GG Blog</title>",
       "<link>%s</link>" % BASE,
       "<description>自动化测试与 AI 测试的实践笔记</description>",
       "<language>zh-cn</language>"]
for it in items[:30]:
    f = os.path.join(POSTS, it["slug"] + ".html")
    if not os.path.exists(f):
        continue
    rss.append("<item><title>%s</title><link>%s/posts/%s.html</link><description>%s</description>"
               "<pubDate>%s</pubDate><guid>%s/posts/%s.html</guid></item>"
               % (H.escape(it["title"]), BASE, it["slug"], H.escape(it["desc"]),
                  mtime_rfc(f), BASE, it["slug"]))
rss.append("</channel></rss>")
open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8").write("\n".join(rss))
print("rss items:", len(rss) - 6)
