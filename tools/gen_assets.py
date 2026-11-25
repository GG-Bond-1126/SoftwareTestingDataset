# -*- coding: utf-8 -*-
"""由仓库根目录解析路径，确保脚本在任意机器上可运行。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Generate OG cover image and PWA icons with Pillow."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(ROOT, "assets")
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"

BG = (13, 20, 29)
PANEL = (20, 30, 42)
GREEN = (61, 220, 132)
CYAN = (70, 200, 240)
DIM = (140, 160, 180)


def grid(draw, w, h, step=40, color=(24, 36, 50)):
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=color, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=color, width=1)


# ---------- OG cover 1200x630 ----------
W, H = 1200, 630
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
grid(d, W, H)
d.rectangle([0, 0, W, 6], fill=GREEN)
d.rectangle([60, 96, 66, 232], fill=GREEN)

f_brand = ImageFont.truetype(FONT_BOLD, 30)
f_title = ImageFont.truetype(FONT_BOLD, 66)
f_sub = ImageFont.truetype(FONT_REG, 30)
f_tag = ImageFont.truetype(FONT_REG, 26)
f_mono = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 24)

d.text((92, 92), "软件测试资料集", font=f_brand, fill=GREEN)
d.text((92, 150), "自动化测试与 AI 测试", font=f_title, fill=(240, 246, 252))
d.text((92, 240), "把公开实践整理成可复用的笔记", font=f_title, fill=(240, 246, 252))
d.text((96, 350), "AI 用例生成 · Agent 测试 · 脚本自愈 · 接口自动化 · 性能与安全",
       font=f_sub, fill=DIM)

d.rounded_rectangle([92, 430, 512, 492], radius=10, fill=PANEL, outline=(34, 50, 68), width=2)
d.text((116, 448), "124 篇笔记 · 6 大方向", font=f_tag, fill=GREEN)
d.rounded_rectangle([532, 430, 872, 492], radius=10, fill=PANEL, outline=(34, 50, 68), width=2)
d.text((556, 448), "每篇附原文出处", font=f_tag, fill=CYAN)

d.text((96, 545), "> npm run test -- --grep \"agent\"", font=f_mono, fill=(150, 200, 230))
d.ellipse([1100, 552, 1112, 564], fill=GREEN)

img.save(os.path.join(ROOT, "og-cover.png"), optimize=True)
print("og-cover.png", os.path.getsize(os.path.join(ROOT, "og-cover.png")))

# ---------- icons ----------
for size in (192, 512):
    ic = Image.new("RGB", (size, size), BG)
    di = ImageDraw.Draw(ic)
    r = int(size * 0.22)
    di.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BG)
    f = ImageFont.truetype(FONT_BOLD, int(size * 0.36))
    txt = "QA"
    bb = di.textbbox((0, 0), txt, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    di.text(((size - tw) / 2 - bb[0], (size - th) / 2 - bb[1]), txt, font=f, fill=GREEN)
    di.rectangle([int(size * 0.3), size - int(size * 0.18), int(size * 0.7), size - int(size * 0.14)], fill=CYAN)
    ic.save(os.path.join(ROOT, "icon-%d.png" % size), optimize=True)
    print("icon-%d.png" % size, os.path.getsize(os.path.join(ROOT, "icon-%d.png" % size)))
