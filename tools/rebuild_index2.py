# -*- coding: utf-8 -*-
"""由仓库根目录解析路径，确保脚本在任意机器上可运行。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Rebuild index.html post cards from real article metadata."""
import os, re, glob, html as H

POSTS = os.path.join(ROOT, "posts")
INDEX = os.path.join(ROOT, "index.html")

FW_RANK = {"AI 框架": 0, "传统+AI 接口": 1, "传统框架": 2}
CAT_RANK = {
    "落地实践": 0, "AI 测试": 1, "接口测试": 2, "CI/CD": 3,
    "Web 自动化": 4, "APP 自动化": 5, "PC 自动化": 6, "桌面自动化": 7,
    "Python 编程入门": 8, "Python 进阶": 9, "单元测试": 10,
    "数据库测试": 11, "Git 版本控制": 12, "自动化": 13,
}

def clean_desc(s):
    s = H.unescape(s)
    s = s.replace('"', '「', 1)
    s = s.replace('"', '」')
    s = re.sub(r'\s+', '', s)
    if len(s) > 56:
        cut = s[:56]
        for sep in ('。', '；', '，', '、'):
            p = cut.rfind(sep)
            if p >= 30:
                cut = cut[:p]
                break
        s = cut + '…'
    return s

def parse(f):
    src = open(f, encoding="utf-8").read()
    name = os.path.basename(f)
    t = re.search(r'<h1>(.*?)</h1>', src, re.S)
    title = H.unescape(re.sub(r'<[^>]+>', '', t.group(1))).strip() if t else name
    c = re.search(r'<span class="post-cat">([^<]*)</span>', src)
    cat = c.group(1).strip() if c else "测试"
    w = re.search(r'<span class="post-fw">([^<]*)</span>', src)
    fw = w.group(1).strip() if w else "传统框架"
    d = re.search(r'<meta name="description" content="([^"]*)"', src)
    desc = clean_desc(d.group(1)) if d else ""
    tag_m = re.search(r'<div class="tag-row">(.*?)</div>', src, re.S)
    tags = []
    if tag_m:
        tags = [H.unescape(x).strip() for x in re.findall(r'<span[^>]*>(.*?)</span>', tag_m.group(1))]
    tags = [x for x in tags if x and x != "#tags"][:3]
    dt = re.search(r'<span>(\d{4}-\d{2}-\d{2})</span>', src)
    date = dt.group(1) if dt else "2026-11-23"
    return {
        "name": name, "title": title, "cat": cat, "fw": fw,
        "desc": desc, "tags": tags, "date": date,
    }

items = [parse(f) for f in sorted(glob.glob(os.path.join(POSTS, "*.html")))]

def key(it):
    return (
        FW_RANK.get(it["fw"], 9),
        CAT_RANK.get(it["cat"], 20),
        it["name"],
    )

items.sort(key=key)

cards = []
for it in items:
    dcat = "ai" if it["fw"] == "AI 框架" or it["cat"] in ("AI 测试", "落地实践") else "auto"
    tag_str = " ".join(it["tags"]) if it["tags"] else ""
    cards.append(f'''      <a class="post-card" href="posts/{it["name"]}" data-cats="{dcat}" data-slug="{it["name"][:-5]}">
        <div class="post-meta">
          <span class="post-cat">{it["cat"]}</span>
          <span class="post-fw">{it["fw"]}</span>
          <span>{it["date"]}</span>
        </div>
        <h3>{it["title"]}</h3>
        <p>{it["desc"]}</p>
        <div class="post-foot">
          <span>{tag_str}</span>
          <span class="read">阅读全文 →</span>
        </div>
      </a>''')

grid = '<div class="post-grid">\n\n' + "\n\n".join(cards) + '\n\n    </div>'
EMPTY = ('    <div class="search-empty" id="search-empty">没有匹配的文章。换个关键词，或到 '
         '<a href="tags.html">标签总览</a> 里按主题找。</div>')

idx = open(INDEX, encoding="utf-8").read()
start = idx.find('<div class="post-grid">')
if start == -1:
    raise SystemExit("post-grid not found")
sec_end = idx.find('</section>', start)
if sec_end == -1:
    raise SystemExit("post-grid end not found")
empty_at = idx.find('<div class="search-empty"', start)
if 0 <= empty_at < sec_end:
    idx = idx[:start] + grid + "\n\n" + idx[empty_at:]
else:
    idx = idx[:start] + grid + "\n\n" + EMPTY + "\n  " + idx[sec_end:]

n = len(items)
idx = re.sub(r'<div class="stat-num">\d+</div>(\s*)<div class="stat-label">实践笔记</div>',
             '<div class="stat-num">%d</div>\\1<div class="stat-label">实践笔记</div>' % n, idx)
idx = re.sub(r'\d+ 篇笔记 · ', '%d 篇笔记 · ' % n, idx)

open(INDEX, "w", encoding="utf-8").write(idx)
print("cards:", n)
print("empty desc:", sum(1 for it in items if not it["desc"]))
print("first 6:", [ (it["fw"], it["cat"], it["name"]) for it in items[:6] ])
