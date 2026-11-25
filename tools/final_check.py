# -*- coding: utf-8 -*-
"""由仓库根目录解析路径，确保脚本在任意机器上可运行。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Final check: remaining ASCII quotes in prose (outside pre/code), broken meta, missing h1/tags."""
import os, re, glob

POSTS = os.path.join(ROOT, "posts")
bad = []
meta_bad = []
low = []
for f in sorted(glob.glob(os.path.join(POSTS, "*.html"))):
    name = os.path.basename(f)
    h = open(f, encoding="utf-8").read()
    i = h.find('<div class="article-body">')
    j = h.find('<footer class="article-foot">')
    q = 0
    if i != -1 and j != -1:
        region = h[i:j]
        tokens = re.split(r'(<[^>]*>)', region)
        pre = code = 0
        for tok in tokens:
            if tok.startswith('<'):
                low_t = tok.lower()
                if low_t.startswith('<pre'): pre += 1
                elif low_t.startswith('</pre'): pre = max(0, pre-1); code = 0
                elif low_t.startswith('<code'): code += 1
                elif low_t.startswith('</code'): code = max(0, code-1)
            elif not (pre or code):
                q += tok.count('"')
    if q:
        bad.append((name, q))
    m = re.search(r'<meta name="description" content="([^"]*)"', h)
    if not m or len(m.group(1)) > 60 or '"' in m.group(1):
        meta_bad.append(name)
    cjk = len(re.findall(r'[\u4e00-\u9fff]', re.sub(r'<[^>]+>', '', h)))
    if cjk < 700:
        low.append((name, cjk))

print("PROSE-QUOTES-LEFT:", len(bad))
for n, q in bad[:20]: print("  ", q, n)
print("META-ISSUE:", len(meta_bad))
for n in meta_bad[:20]: print("  ", n)
print("SHORT(<700 cjk):", len(low))
for n, c in low[:20]: print("  ", c, n)
