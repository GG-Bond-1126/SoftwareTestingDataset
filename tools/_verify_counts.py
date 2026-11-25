# -*- coding: utf-8 -*-
import re, os
os.chdir(r"D:\user\文档\Trae-CN\temp_20261123_01")
i = open("index.html", encoding="utf-8").read()
print("cards:", i.count('class="post-card"'))
l = open("links.html", encoding="utf-8").read()
new = re.findall(r'posts/(android-ai-agent-harness|browser-agent-testing|traffic-replay-api-testing|wireless-android-control|testing-skill-build|ai-mobile-operation|open-source-testing-projects|mobile-mcp-cases|google-mobile-ai-testing)\.html', l)
print("links page -> new articles:", len(new), sorted(set(new)))
sm = open("sitemap.xml", encoding="utf-8").read()
print("sitemap urls:", sm.count("<loc>"))
rss = open("rss.xml", encoding="utf-8").read()
print("rss items:", rss.count("<item>"))
print("new in sitemap:", sum(sm.count(s) for s in set(new)))
