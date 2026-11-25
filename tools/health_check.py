# -*- coding: utf-8 -*-
"""由仓库根目录解析路径，确保脚本在任意机器上可运行。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Link / anchor / download health check for the static site."""
import os, re, glob, sys

ROOT = ROOT
files = [f for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
         if ".trae-html-share-packages" not in f]

ids_cache = {}
def ids_of(path):
    if path not in ids_cache:
        s = open(path, encoding="utf-8", errors="ignore").read()
        ids_cache[path] = set(re.findall(r'\bid="([^"]+)"', s))
    return ids_cache[path]

href_re = re.compile(r'(?:href|src)="([^"]+)"')
broken, anchors, ok = [], [], 0

for f in files:
    s = open(f, encoding="utf-8", errors="ignore").read()
    s = re.sub(r"<pre>.*?</pre>", "", s, flags=re.S)
    rel_dir = os.path.dirname(f)
    for target in set(href_re.findall(s)):
        t = target.strip()
        if not t or t.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "//")):
            continue
        path_part, _, frag = t.partition("#")
        if path_part:
            p = os.path.normpath(os.path.join(rel_dir, path_part))
            if os.path.isdir(p):
                p = os.path.join(p, "index.html")
            if not os.path.exists(p):
                broken.append((os.path.relpath(f, ROOT), t))
                continue
        else:
            p = f
        if frag and p.endswith(".html"):
            if frag not in ids_of(p):
                anchors.append((os.path.relpath(f, ROOT), t))
        ok += 1

print("links checked:", ok)
print("broken targets:", len(broken))
for a, b in broken[:25]:
    print("  ", a, "->", b)
print("missing anchors:", len(anchors))
for a, b in anchors[:25]:
    print("  ", a, "->", b)
sys.exit(1 if (broken or anchors) else 0)
