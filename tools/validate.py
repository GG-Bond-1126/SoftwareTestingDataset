# -*- coding: utf-8 -*-
"""由仓库根目录解析路径，确保脚本在任意机器上可运行。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Validate tag balance and required markers for every post."""
import os, re, glob
from html.parser import HTMLParser

POSTS = os.path.join(ROOT, "posts")
VOID = {"meta", "link", "img", "br", "hr", "input", "source", "area", "base", "col", "embed", "param", "track", "wbr"}

class V(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()[0]))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("extra </%s> line %d" % (tag, self.getpos()[0]))
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # search back
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                unclosed = [t for t, _ in self.stack[i + 1:]]
                self.errors.append("</%s> line %d closes over unclosed %s" % (tag, self.getpos()[0], unclosed))
                del self.stack[i:]
                return
        self.errors.append("stray </%s> line %d" % (tag, self.getpos()[0]))

bad = []
for f in sorted(glob.glob(os.path.join(POSTS, "*.html"))):
    name = os.path.basename(f)
    src = open(f, encoding="utf-8").read()
    p = V()
    p.feed(src)
    errs = p.errors + ["unclosed %s line %d" % (t, l) for t, l in p.stack]
    req = [
        ('class="article-body"', "no-body"),
        ('class="article-foot"', "no-foot"),
        ('class="site-header"', "no-header"),
        ('assets/main.js', "no-js"),
        ("<h1>", "no-h1"),
        ('class="tag-row"', "no-tags"),
    ]
    missing = [m for k, m in req if k not in src]
    if errs or missing:
        bad.append((name, errs[:3], missing))
print("BAD:", len(bad))
for n, e, m in bad:
    print(" ", n, m, e)
