# -*- coding: utf-8 -*-
"""体积守卫：防止图片 / 数据文件 / 整站体积悄悄回涨。

超出预算时以非零码退出，构建流水线随之中断。
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".github", ".trae-html-share-packages", ".screenshots", "__pycache__", "node_modules"}
SKIP_EXT = {".pyc", ".bak", ".tmp", ".ds_store"}

KB = 1024
LIMITS = {
    "image": (300 * KB, {".png", ".jpg", ".jpeg", ".webp", ".gif"}),
    "json": (600 * KB, {".json"}),
    "html": (300 * KB, {".html"}),
    "code": (150 * KB, {".css", ".js", ".svg"}),
}
TOTAL_BUDGET = 6 * 1024 * KB

problems = []
total = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        ext = os.path.splitext(fn)[1].lower()
        if ext in SKIP_EXT:
            continue
        path = os.path.join(dirpath, fn)
        size = os.path.getsize(path)
        total += size
        for label, (limit, exts) in LIMITS.items():
            if ext in exts and size > limit:
                problems.append("%s %.0f KB > %d KB (%s)" % (
                    os.path.relpath(path, ROOT), size / KB, limit // KB, label))

if total > TOTAL_BUDGET:
    problems.append("站点总体积 %.2f MB > %d MB" % (total / 1024 / KB, TOTAL_BUDGET // 1024 // KB))

print("ASSETS-TOTAL: %.2f MB" % (total / 1024 / KB))
if problems:
    print("ASSET-BUDGET-EXCEEDED:", len(problems))
    for p in problems[:20]:
        print("  ", p)
    sys.exit(1)
print("体积预算通过。")
