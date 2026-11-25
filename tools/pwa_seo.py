# -*- coding: utf-8 -*-
"""由仓库根目录解析路径，确保脚本在任意机器上可运行。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Add PWA manifest + service worker, and inject og:image / manifest / theme-color into all pages."""
import os, re, glob, json

ROOT = ROOT
BASE = "https://37lh5701lxo5frtwh6h.traesite.cn"

MANIFEST = {
    "name": "软件测试资料集 · GG Bond",
    "short_name": "测试资料集",
    "description": "自动化测试与 AI 测试的实践笔记，覆盖 AI 用例生成、Agent 测试与脚本自愈。",
    "start_url": "index.html",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait-primary",
    "background_color": "#0d141d",
    "theme_color": "#0d141d",
    "lang": "zh-CN",
    "icons": [
        {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}
open(os.path.join(ROOT, "manifest.webmanifest"), "w", encoding="utf-8").write(
    json.dumps(MANIFEST, ensure_ascii=False, indent=2))

SW = """/* 软件测试资料集 · Service Worker */
const VERSION = "ggbond-v2";
const BASE = new URL("./", self.location.href).href;
const SHELL = [
  "index.html",
  "assets/style.css",
  "assets/main.js",
  "assets/icon-192.png"
].map((p) => BASE + p);

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (req.mode === "navigate" || url.pathname.endsWith(".html")) {
    e.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(VERSION).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() =>
          caches.match(req).then((hit) => hit || caches.match(BASE + "index.html"))
        )
    );
    return;
  }

  e.respondWith(
    caches.match(req).then((hit) => {
      const network = fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(VERSION).then((c) => c.put(req, copy));
          }
          return res;
        })
        .catch(() => hit);
      return hit || network;
    })
  );
});
"""
open(os.path.join(ROOT, "sw.js"), "w", encoding="utf-8").write(SW)
print("wrote manifest.webmanifest + sw.js")

OG_IMG = BASE + "/assets/og-cover.png"

pages = [os.path.join(ROOT, p) for p in ("index.html", "about.html", "tags.html", "paths.html", "favorites.html")]
pages += sorted(glob.glob(os.path.join(ROOT, "posts", "*.html")))

added = 0
for f in pages:
    if not os.path.exists(f):
        continue
    prefix = "../" if os.sep + "posts" + os.sep in f else ""
    s = open(f, encoding="utf-8").read()
    orig = s

    ins = []
    if 'property="og:image"' not in s:
        ins.append('<meta property="og:image" content="%s">' % OG_IMG)
        ins.append('<meta property="og:image:width" content="1200">')
        ins.append('<meta property="og:image:height" content="630">')
        ins.append('<meta name="twitter:image" content="%s">' % OG_IMG)
    if 'name="twitter:card" content="summary"' in s:
        s = s.replace('<meta name="twitter:card" content="summary">',
                      '<meta name="twitter:card" content="summary_large_image">')
    if 'rel="manifest"' not in s:
        ins.append('<link rel="manifest" href="%smanifest.webmanifest">' % prefix)
    if 'name="theme-color"' not in s:
        ins.append('<meta name="theme-color" content="#0d141d">')
    if ins:
        s = s.replace("</head>", "\n".join(ins) + "\n</head>", 1)
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)
        added += 1

print("pages updated:", added)
