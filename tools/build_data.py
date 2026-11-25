# -*- coding: utf-8 -*-
"""由仓库根目录解析路径，确保脚本在任意机器上可运行。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Build assets/posts-index.json: metadata + headings + text excerpt + prev/next/related."""
import os, re, json, glob, html as H

POSTS = os.path.join(ROOT, "posts")
OUT = os.path.join(ROOT, "assets", "posts-index.json")

FW_RANK = {"AI 框架": 0, "传统+AI 接口": 1, "传统框架": 2}
CAT_RANK = {
    "落地实践": 0, "AI 测试": 1, "接口测试": 2, "CI/CD": 3,
    "Web 自动化": 4, "APP 自动化": 5, "PC 自动化": 6, "桌面自动化": 7,
    "Python 编程入门": 8, "Python 进阶": 9, "单元测试": 10,
    "数据库测试": 11, "Git 版本控制": 12, "自动化": 13,
}

def parse(f):
    src = open(f, encoding="utf-8").read()
    slug = os.path.basename(f)[:-5]
    t = re.search(r'<h1>(.*?)</h1>', src, re.S)
    title = H.unescape(re.sub(r'<[^>]+>', '', t.group(1))).strip() if t else slug
    cat = (re.search(r'class="post-cat">([^<]*)<', src) or [None, "测试"])[1]
    fw = (re.search(r'class="post-fw">([^<]*)<', src) or [None, "传统框架"])[1]
    d = re.search(r'<meta name="description" content="([^"]*)"', src)
    desc = H.unescape(d.group(1)).strip() if d else ""
    body = src.split('<div class="article-body">', 1)[1].split('<footer class="article-foot">', 1)[0]
    headings = [H.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)]
    headings = [h for h in headings if h]
    tag_m = re.search(r'<div class="tag-row">(.*?)</div>', src, re.S)
    tags = []
    if tag_m:
        tags = [H.unescape(x).strip().lstrip('#') for x in re.findall(r'<span[^>]*>(.*?)</span>', tag_m.group(1))]
    tags = [x for x in tags if x and x != 'tags'][:4]
    nocode = re.sub(r'<pre>.*?</pre>', '', body, flags=re.S)
    txt = H.unescape(re.sub(r'<[^>]+>', ' ', nocode))
    txt = re.sub(r'\s+', ' ', txt).strip()[:1200]
    return {"slug": slug, "title": title, "cat": cat.strip(), "fw": fw.strip(),
            "desc": desc, "tags": tags, "headings": headings, "text": txt}

items = [parse(f) for f in sorted(glob.glob(os.path.join(POSTS, "*.html")))]
items.sort(key=lambda it: (FW_RANK.get(it["fw"], 9), CAT_RANK.get(it["cat"], 20), it["slug"]))

for i, it in enumerate(items):
    it["prev"] = items[i - 1]["slug"] if i > 0 else ""
    it["next"] = items[i + 1]["slug"] if i < len(items) - 1 else ""

by_slug = {it["slug"]: it for it in items}
for it in items:
    scores = []
    for other in items:
        if other["slug"] == it["slug"]:
            continue
        s = 0
        s += 3 * len(set(it["tags"]) & set(other["tags"]))
        s += 2 if other["cat"] == it["cat"] else 0
        s += 1 if other["fw"] == it["fw"] else 0
        if s > 0:
            scores.append((s, other["slug"]))
    scores.sort(key=lambda x: (-x[0], x[1]))
    it["related"] = [s for _, s in scores[:3]]

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(items, fh, ensure_ascii=False, separators=(",", ":"))

print("posts:", len(items))
print("json bytes:", os.path.getsize(OUT))
print("no desc:", sum(1 for it in items if not it["desc"]))
print("no headings:", sum(1 for it in items if not it["headings"]))
print("no related:", [it["slug"] for it in items if not it["related"]])
print("no tags:", sum(1 for it in items if not it["tags"]))
