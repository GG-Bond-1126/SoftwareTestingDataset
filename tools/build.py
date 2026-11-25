# -*- coding: utf-8 -*-
"""一键构建：生成索引 -> 重建首页 -> SEO -> PWA -> 校验。

用法：
    python tools/build.py
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("生成文章索引", "build_data.py"),
    ("重建首页卡片", "rebuild_index2.py"),
    ("生成精选外链页", "build_links.py"),
    ("生成 sitemap / rss / OG", "seo.py"),
    ("生成 PWA 与分享图元信息", "pwa_seo.py"),
    ("HTML 结构校验", "validate.py"),
    ("全站链接体检", "health_check.py"),
    ("引号与 meta 检查", "final_check.py"),
    ("资源体积守卫", "asset_guard.py"),
]

for label, script in STEPS:
    path = os.path.join(HERE, script)
    if not os.path.exists(path):
        print("[skip] %s (%s 不存在)" % (label, script))
        continue
    print("\n>>> %s" % label)
    code = subprocess.run([sys.executable, path], cwd=HERE).returncode
    if code != 0:
        print("[fail] %s，已中断" % label)
        sys.exit(code)
print("\n全部完成。")
