"""Lost and Found: picture. Code-drawn, one static shot."""
import math, os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import timeline as TL

W, H = 1920, 1080
S = 2
VP = (960.0, 470.0)
DOOR = (330, 405, 450, 640)
PIVOT = (915.0, 1052.0)
COLD = np.array([1.00, 0.74, 0.44], np.float32)  # sodium from the platform


def C(c):
    return tuple(int(max(0, min(255, round(v * 255)))) for v in c)


def P(v):
    return int(round(v * S))


def font(size):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
              '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf',
              '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf']:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def lowfreq(h, w, cell, seed, amp):
    r = np.random.default_rng(seed)
    n = r.standard_normal((max(2, h // cell + 2), max(2, w // cell + 2))).astype(np.float32)
    im = Image.fromarray(n).resize((w, h), Image.BICUBIC)
    return 1.0 + amp * np.asarray(im, np.float32)


def build_plate():
    im = Image.new('RGB', (W * S, H * S), C((0.1, 0.1, 0.1)))
    d = ImageDraw.Draw(im)
    R = lambda x0, y0, x1, y1, c: d.rectangle([P(x0), P(y0), P(x1), P(y1)], fill=C(c))
    Poly = lambda pts, c: d.polygon([(P(x), P(y)) for x, y in pts], fill=C(c))
    L = lambda pts, c, w: d.line([(P(x), P(y)) for x, y in pts], fill=C(c), width=max(1, P(w)))
    E = lambda x0, y0, x1, y1, c: d.ellipse([P(x0), P(y0), P(x1), P(y1)], fill=C(c))

    R(0, 0, W, 150, (0.085, 0.09, 0.088))
    R(0, 150, W, 440, (0.40, 0.415, 0.385))
    R(0, 440, W, 625, (0.43, 0.49, 0.45))
    for y in range(440, 626, 24):
        L([(0, y), (W, y)], (0.33, 0.37, 0.34), 1.2)
    for x in range(0, W, 24):
        L([(x, 440), (x, 625)], (0.35, 0.39, 0.36), 1.0)
    R(0, 432, W, 442, (0.30, 0.33, 0.30))
    R(0, 622, W, 641, (0.12, 0.13, 0.12))

    R(0, 641, W, H, (0.215, 0.21, 0.195))
    for i in range(-30, 31):
        xb = VP[0] + i * 95
        k = (H - VP[1]) / (641 - VP[1])
        L([(xb, 641), (VP[0] + (xb - VP[0]) * k, H)], (0.17, 0.165, 0.155), 1.3)
    for z in [1.0, 1.35, 1.8, 2.5, 3.6, 5.5]:
        y = VP[1] + (641 - VP[1]) * z
        if y < H:
            L([(0, y), (W, y)], (0.17, 0.165, 0.155), 1.3)

    R(470, 128, 1270, 150, (0.16, 0.165, 0.16))
    R(490, 136, 1250, 146, (1.0, 1.0, 0.96))

    x0, y0, x1, y1 = DOOR
    R(x0 - 16, y0 - 16, x1 + 16, y1 + 2, (0.15, 0.16, 0.15))
    R(x0 - 10, y0 - 10, x1 + 10, y1, (0.20, 0.215, 0.20))
    R(x0 - 6, y1, x1 + 6, y1 + 6, (0.26, 0.26, 0.24))
    R(352, 358, 428, 384, (0.06, 0.20, 0.10))
    R(355, 361, 425, 381, (0.16, 0.62, 0.32))
    d.text((P(390), P(371)), 'WAY OUT', fill=C((0.92, 1.0, 0.94)), font=font(P(11)), anchor='mm')

    E(728, 262, 800, 334, (0.12, 0.12, 0.12))
    E(732, 266, 796, 330, (0.88, 0.87, 0.82))
    for k in range(12):
        a = k * math.pi / 6
        L([(764 + 26 * math.sin(a), 298 - 26 * math.cos(a)),
           (764 + 30 * math.sin(a), 298 - 30 * math.cos(a))], (0.15, 0.15, 0.15), 1.6)
    ah, am = (3 + 47 / 60) * math.pi / 6, 47 * math.pi / 30
    L([(764, 298), (764 + 15 * math.sin(ah), 298 - 15 * math.cos(ah))], (0.08, 0.08, 0.08), 3)
    L([(764, 298), (764 + 25 * math.sin(am), 298 - 25 * math.cos(am))], (0.08, 0.08, 0.08), 2)

    R(560, 250, 640, 360, (0.70, 0.68, 0.60))
    R(568, 262, 632, 272, (0.35, 0.33, 0.30))
    for yy in range(282, 350, 9):
        R(568, yy, 620 + (yy * 7) % 12, yy + 3, (0.50, 0.48, 0.43))
    R(860, 300, 950, 360, (0.62, 0.64, 0.62))

    for yy in (566, 580, 594):
        R(540, yy, 900, yy + 9, (0.26, 0.20, 0.14))
    R(540, 603, 900, 609, (0.15, 0.12, 0.09))
    for xx in (556, 880):
        R(xx, 603, xx + 8, 636, (0.10, 0.10, 0.10))
    Poly([(952, 560), (996, 560), (990, 638), (958, 638)], (0.17, 0.19, 0.18))
    R(950, 556, 998, 563, (0.12, 0.13, 0.12))

    wood, woodd, woodl = (0.25, 0.175, 0.11), (0.15, 0.10, 0.065), (0.34, 0.25, 0.165)
    R(1124, 105, W, 1044, (0.17, 0.15, 0.125))
    for yy in range(140, 1040, 46):
        L([(1124, yy), (W, yy)], (0.12, 0.105, 0.09), 1.2)
    R(1300, 34, 1652, 92, (0.07, 0.09, 0.16))
    R(1304, 38, 1648, 88, (0.90, 0.89, 0.84))
    d.text((P(1476), P(64)), 'LOST PROPERTY', fill=C((0.10, 0.15, 0.32)), font=font(P(30)), anchor='mm')
    L([(1330, 34), (1330, 0)], (0.1, 0.1, 0.1), 2)
    L([(1620, 34), (1620, 0)], (0.1, 0.1, 0.1), 2)

    def plank(y, top_face):
        if top_face:
            Poly([(1124, y - 16), (W, y - 16), (W, y), (1110, y)], woodl)
        R(1090, y, W, y + 24, wood)
        L([(1090, y + 24), (W, y + 24)], woodd, 2)
        if not top_face:
            R(1124, y + 24, W, y + 34, (0.05, 0.04, 0.035))

    def tag(x, y, num):
        L([(x + 6, y - 14), (x + 6, y)], (0.75, 0.72, 0.62), 1)
        Poly([(x, y), (x + 34, y), (x + 34, y + 18), (x, y + 18)], (0.78, 0.70, 0.52))
        E(x + 3, y + 7, x + 7, y + 11, (0.3, 0.25, 0.2))
        d.text((P(x + 20), P(y + 9)), num, fill=C((0.2, 0.15, 0.12)), font=font(P(8)), anchor='mm')

    E(1170, 300, 1370, 342, (0.10, 0.10, 0.10))
    Poly([(1210, 318), (1222, 246), (1268, 230), (1318, 246), (1330, 318)], (0.31, 0.30, 0.28))
    R(1212, 296, 1328, 312, (0.13, 0.12, 0.12))
    Poly([(1170, 322), (1370, 322), (1356, 338), (1184, 338)], (0.27, 0.26, 0.245))
    for i, (c, h) in enumerate([((0.34, 0.22, 0.19), 26), ((0.36, 0.30, 0.22), 22), ((0.26, 0.17, 0.15), 24)]):
        yb = 340 - sum([26, 22, 24][:i])
        R(1440, yb - h, 1610, yb, c)
        L([(1440, yb - h + 3), (1610, yb - h + 3)], tuple(v * 1.3 for v in c), 1.5)
    for xx in range(1446, 1606, 7):
        L([(xx, 340), (xx + 2, 352)], (0.32, 0.21, 0.18), 1.2)
    for i, (c, h, w) in enumerate([((0.55, 0.50, 0.40), 150, 26), ((0.22, 0.25, 0.32), 160, 30),
                                    ((0.38, 0.25, 0.20), 140, 22), ((0.30, 0.32, 0.26), 155, 28)]):
        x = 1690 + sum([26, 30, 22, 28][:i])
        R(x, 340 - h, x + w - 2, 340, c)
    tag(1380, 300, '214')

    plank(340, False)

    R(1180, 420, 1250, 575, (0.42, 0.44, 0.45))
    R(1186, 420, 1198, 575, (0.62, 0.64, 0.65))
    R(1176, 402, 1254, 432, (0.20, 0.30, 0.27))
    R(1180, 520, 1250, 530, (0.30, 0.31, 0.32))
    Poly([(1300, 575), (1310, 548), (1360, 540), (1380, 528), (1392, 534), (1384, 548),
          (1440, 548), (1452, 556), (1446, 566), (1458, 575)], (0.40, 0.26, 0.15))
    for xx in (1405, 1420, 1435):
        L([(xx, 549), (xx + 14, 553)], (0.20, 0.11, 0.06), 1.5)
    d.ellipse([P(1520), P(552), P(1556), P(572)], outline=C((0.12, 0.12, 0.12)), width=P(2.5))
    d.ellipse([P(1562), P(552), P(1598), P(572)], outline=C((0.12, 0.12, 0.12)), width=P(2.5))
    E(1527, 555, 1533, 559, (0.85, 0.92, 0.9))
    L([(1556, 560), (1562, 560)], (0.12, 0.12, 0.12), 2)
    L([(1598, 560), (1640, 568)], (0.12, 0.12, 0.12), 2)
    R(1700, 470, 1880, 575, (0.36, 0.33, 0.27))
    R(1700, 470, 1880, 486, (0.42, 0.39, 0.32))
    tag(1460, 512, '219')

    plank(575, True)

    rab = (0.62, 0.52, 0.48)
    rabd = (0.48, 0.39, 0.36)
    E(1250, 706, 1370, 815, rab)
    E(1262, 640, 1358, 726, rab)
    Poly([(1276, 652), (1266, 560), (1284, 548), (1300, 650)], rab)
    Poly([(1322, 650), (1336, 556), (1356, 562), (1344, 656)], rabd)
    Poly([(1280, 640), (1273, 574), (1283, 568), (1292, 640)], (0.70, 0.58, 0.56))
    E(1286, 672, 1298, 684, (0.03, 0.03, 0.03))
    E(1322, 672, 1334, 684, (0.03, 0.03, 0.03))
    E(1289, 674, 1292, 677, (0.5, 0.5, 0.5))
    E(1325, 674, 1328, 677, (0.5, 0.5, 0.5))
    L([(1304, 701), (1316, 701)], (0.16, 0.11, 0.1), 1.6)
    E(1232, 772, 1272, 812, rab)
    E(1348, 772, 1388, 812, rab)
    for xx, yy in [(1262, 760), (1300, 740), (1340, 765), (1318, 790)]:
        L([(xx, yy), (xx + 8, yy + 3)], rabd, 1.2)
    tag(1390, 770, '231')
    R(1520, 735, 1690, 815, (0.24, 0.32, 0.36))
    R(1520, 735, 1690, 748, (0.30, 0.40, 0.44))
    R(1596, 722, 1614, 735, (0.18, 0.22, 0.24))
    R(1760, 690, 1900, 815, (0.18, 0.16, 0.14))

    plank(815, True)

    R(1300, 900, 1660, 1020, (0.23, 0.15, 0.10))
    R(1300, 900, 1660, 912, (0.30, 0.21, 0.14))
    R(1440, 880, 1520, 900, (0.12, 0.08, 0.05))
    for xx in (1330, 1630):
        R(xx - 6, 900, xx + 6, 1020, (0.17, 0.11, 0.07))
    Poly([(1720, 1020), (1720, 900), (1780, 900), (1784, 980), (1850, 990), (1856, 1020)], (0.07, 0.065, 0.06))

    R(1090, 1020, W, 1050, wood)
    R(1090, 1044, W, 1052, woodd)
    R(1090, 98, W, 122, wood)
    R(1090, 96, W, 100, woodl)
    R(1088, 96, 1126, 1052, wood)
    R(1088, 96, 1096, 1052, woodl)
    R(1118, 96, 1126, 1052, woodd)

    E(PIVOT[0] - 34, PIVOT[1] - 8, PIVOT[0] + 34, PIVOT[1] + 8, (0.10, 0.10, 0.095))

    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255.0
    a *= lowfreq(H, W, 90, 3, 0.05)[..., None]
    a *= lowfreq(H, W, 14, 4, 0.025)[..., None]
    r = np.random.default_rng(7)
    speck = r.standard_normal((H - 641, W)).astype(np.float32)
    a[641:] *= (1 + 0.045 * speck)[..., None]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    pool = np.exp(-((xx - 870) / 760) ** 2 - ((yy - 200) / 520) ** 2)
    illum = 0.45 + 0.75 * pool + 0.5 * np.exp(-((xx - 1380) / 540) ** 2 - ((yy - 90) / 620) ** 2)
    illum *= 1.0 - 0.06 * np.clip((xx - 1050) / 600, 0, 1)
    def ao(cx, cy, rx, ry, k):
        return 1.0 - k * np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2))
    for b in [(560, 638, 38, 6, 0.6), (884, 638, 38, 6, 0.6), (720, 642, 240, 12, 0.35), (974, 641, 42, 7, 0.65),
              (1500, 1056, 560, 16, 0.6), (PIVOT[0], PIVOT[1] + 2, 30, 6, 0.7), (1106, 1056, 40, 14, 0.5)]:
        illum = illum * ao(*b)
    illum = illum * (1 + 0.22 * np.exp(-(((xx - PIVOT[0]) / 260) ** 2 + ((yy - 980) / 120) ** 2)))
    illum[641:672] *= np.linspace(0.62, 1.0, 31, dtype=np.float32)[:, None]
    vig = 1.0 - 0.38 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.4
    a *= (illum * vig)[..., None]
    tube = np.zeros((H, W), np.float32)
    tube[136:147, 490:1251] = 1.0
    tube = np.asarray(Image.fromarray((tube*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28)), np.float32) / 255.0
    a += (tube * 0.9)[..., None] * np.array([0.95, 1.0, 0.92], np.float32)
    a[136:147, 490:1251] = np.array([1.0, 1.0, 0.97])
    a *= np.array([0.88, 1.0, 0.97], np.float32)
    return np.clip(a, 0, 1.2).astype(np.float32)


UW, UH = 400, 800
UPX, UPY = 200, 790


def build_umbrella():
    s = 3
    im = Image.new('RGBA', (UW * s, UH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    Q = lambda v: int(round(v * s))
    cx = UPX
    left, right = [], []
    for i in range(61):
        t = i / 60.0
        y = 768 - t * (768 - 232)
        if t < 0.84:
            w = 3 + 21 * (t / 0.84) ** 1.25
        else:
            w = 24 - 15 * ((t - 0.84) / 0.16) ** 1.6
        bul = 5.5 * math.exp(-((t - 0.58) / 0.11) ** 2)
        bul2 = 3.0 * math.exp(-((t - 0.30) / 0.08) ** 2)
        left.append((cx - w - bul2, y))
        right.append((cx + w + bul, y))
    canopy = [(Q(x), Q(y)) for x, y in left + right[::-1]]
    fab = (0.065, 0.068, 0.08)
    d.polygon(canopy, fill=C(fab) + (255,))
    hl = [(cx - 0.55 * (cx - x), y) for x, y in left]
    hr = [(cx - 0.25 * (cx - x), y) for x, y in left]
    d.polygon([(Q(x), Q(y)) for x, y in hl + hr[::-1]], fill=C((0.15, 0.155, 0.175)) + (255,))
    for f in (0.15, 0.48, 0.80):
        pts = [(Q(cx + f * (xr - cx) + 1.5 * math.sin(y / 31)), Q(y)) for (xr, y) in right[4:57]]
        d.line(pts, fill=C((0.025, 0.025, 0.03)) + (255,), width=Q(1.4))
    pts = [(Q(cx - 0.75 * (cx - xl)), Q(y)) for (xl, y) in left[6:55]]
    d.line(pts, fill=C((0.03, 0.03, 0.035)) + (255,), width=Q(1.2))
    ys = 768 - 0.52 * (768 - 232)
    d.polygon([(Q(cx - 22), Q(ys - 6)), (Q(cx + 26), Q(ys - 2)), (Q(cx + 26), Q(ys + 8)), (Q(cx - 22), Q(ys + 4))],
              fill=C((0.10, 0.10, 0.115)) + (255,))
    d.ellipse([Q(cx + 10), Q(ys - 3), Q(cx + 18), Q(ys + 5)], fill=C((0.45, 0.44, 0.40)) + (255,))
    d.polygon([(Q(cx - 2.6), Q(768)), (Q(cx + 2.6), Q(768)), (Q(cx + 1.6), Q(790)), (Q(cx - 1.6), Q(790))],
              fill=C((0.20, 0.20, 0.19)) + (255,))
    d.rectangle([Q(cx - 6), Q(224), Q(cx + 6), Q(236)], fill=C((0.30, 0.30, 0.29)) + (255,))
    d.rectangle([Q(cx - 3.5), Q(120), Q(cx + 3.5), Q(226)], fill=C((0.12, 0.10, 0.08)) + (255,))
    wood = C((0.33, 0.21, 0.12)) + (255,)
    r0 = 30
    ccx, ccy = cx + 30, 122
    pts_o, pts_i = [], []
    for k in range(0, 41):
        a = math.pi + k / 40 * math.pi * 1.08
        pts_o.append((ccx + (r0 + 7) * math.cos(a), ccy + (r0 + 7) * math.sin(a)))
        pts_i.append((ccx + (r0 - 7) * math.cos(a), ccy + (r0 - 7) * math.sin(a)))
    d.polygon([(Q(x), Q(y)) for x, y in pts_o + pts_i[::-1]], fill=wood)
    d.rectangle([Q(cx - 7), Q(120), Q(cx + 7), Q(160)], fill=wood)
    d.rectangle([Q(cx - 8), Q(156), Q(cx + 8), Q(164)], fill=C((0.38, 0.36, 0.30)) + (255,))
    hl2 = [(ccx + (r0 + 3) * math.cos(math.pi + k / 30 * math.pi * 0.7),
            ccy + (r0 + 3) * math.sin(math.pi + k / 30 * math.pi * 0.7)) for k in range(31)]
    d.line([(Q(x), Q(y)) for x, y in hl2], fill=C((0.50, 0.36, 0.22)) + (255,), width=Q(2.2))
    tx, ty = ccx + r0 * math.cos(math.pi * 2.08), ccy + r0 * math.sin(math.pi * 2.08)
    d.ellipse([Q(tx - 7), Q(ty - 7), Q(tx + 7), Q(ty + 7)], fill=wood)
    im = im.filter(ImageFilter.GaussianBlur(0.5 * s))
    return im


UMB3 = None


def umbrella_layer(angle, light):
    s = 3
    rot = UMB3.rotate(-angle, resample=Image.BICUBIC, center=(UPX * s, UPY * s))
    rot = rot.resize((UW, UH), Image.LANCZOS)
    a = np.asarray(rot, np.float32) / 255.0
    rgb, al = a[..., :3], a[..., 3]
    yy = np.arange(UH, dtype=np.float32)[:, None]
    rgb = rgb * (0.70 + 0.45 * (1 - yy / UH))[..., None]
    sh = np.zeros_like(al)
    sh[:, 3:] = al[:, :-3]
    edge = np.clip(al - sh, 0, 1)
    rgb = rgb + edge[..., None] * np.array([0.60, 0.72, 0.70], np.float32) * 0.75 * ((1 - yy / UH) ** 2)[..., None]
    if light > 0.001:
        rim = edge * light * 1.7 * (0.25 + 0.75 * (yy / UH))
        rgb = rgb + rim[..., None] * COLD * 0.55
        rgb = rgb + al[..., None] * COLD * 0.05 * light
    x0 = int(PIVOT[0] - UPX)
    y0 = int(PIVOT[1] - UPY)
    return rgb * al[..., None], al, x0, y0


def door_layer(t, door, figs):
    x0, y0, x1, y1 = DOOR
    w, h = x1 - x0, y1 - y0
    s = 4
    im = Image.new('RGB', (w * s, h * s))
    d = ImageDraw.Draw(im)
    Q = lambda v: int(round(v * s))
    for i in range(h):
        f = i / h
        if f < 0.22:
            c = (0.05, 0.065, 0.09)
        elif f < 0.62:
            c = (0.66 + 0.1 * f, 0.47 + 0.08 * f, 0.24 + 0.05 * f)
        else:
            c = (0.74 - 0.15 * (f - 0.62), 0.55 - 0.12 * (f - 0.62), 0.30 - 0.08 * (f - 0.62))
        d.rectangle([0, Q(i), Q(w), Q(i + 1)], fill=C(c))
    d.rectangle([0, Q(h * 0.20), Q(w), Q(h * 0.235)], fill=C((0.18, 0.19, 0.2)))
    d.rectangle([Q(w * 0.15), Q(h * 0.235), Q(w * 0.85), Q(h * 0.25)], fill=C((1.0, 0.86, 0.6)))
    d.rectangle([0, Q(h * 0.70), Q(w), Q(h * 0.72)], fill=C((0.78, 0.70, 0.30)))
    for k in range(5):
        d.rectangle([Q(10 + k * 24), Q(h * 0.36), Q(22 + k * 24), Q(h * 0.52)], fill=C((0.36, 0.40, 0.44)))
    for (i, fx, fy, fh, bob) in figs:
        f0 = TL.EVENTS[i]['fig']
        dz = fy - 9.8
        sc = 1.0 / (1.0 + 0.09 * dz)
        px = w / 2 + (fx - f0['x_in']) * 82
        feet = h - 3 - 26 * dz
        hh = fh * 112 * sc
        top = feet - hh - bob * 112
        u = hh / 10.0
        col = C((0.035, 0.038, 0.045))
        d.ellipse([Q(px - 0.62 * u), Q(top), Q(px + 0.62 * u), Q(top + 1.45 * u)], fill=col)
        d.rectangle([Q(px - 0.3 * u), Q(top + 1.2 * u), Q(px + 0.3 * u), Q(top + 1.9 * u)], fill=col)
        d.polygon([(Q(px - 1.25 * u), Q(top + 2.0 * u)), (Q(px + 1.25 * u), Q(top + 2.0 * u)),
                   (Q(px + 1.5 * u), Q(top + 7.0 * u)), (Q(px - 1.5 * u), Q(top + 7.0 * u))], fill=col)
        d.ellipse([Q(px - 1.3 * u), Q(top + 1.7 * u), Q(px + 1.3 * u), Q(top + 2.6 * u)], fill=col)
        d.rectangle([Q(px - 0.8 * u), Q(top + 6.9 * u), Q(px - 0.15 * u), Q(feet)], fill=col)
        d.rectangle([Q(px + 0.15 * u), Q(top + 6.9 * u), Q(px + 0.8 * u), Q(feet)], fill=col)
        if i == 1:
            d.ellipse([Q(px - 1.1 * u), Q(top + 0.25 * u), Q(px + 1.1 * u), Q(top + 0.6 * u)], fill=col)
            d.rectangle([Q(px - 0.62 * u), Q(top - 0.35 * u), Q(px + 0.62 * u), Q(top + 0.45 * u)], fill=col)
    a = math.radians(door)
    wc = w * math.cos(a)
    sh = math.sin(a)
    ty = (VP[1] - y0) * 0.22 * sh
    by = (y1 - VP[1]) * 0.22 * sh
    dx = 8 * sh
    shade = 0.26 - 0.13 * sh
    leaf = [(0, 0), (wc + dx, ty), (wc + dx, h - by), (0, h)]
    d.polygon([(Q(x), Q(y)) for x, y in leaf], fill=C((shade * 0.85, shade, shade * 0.93)))

    def lp(u, v):
        xt = u * (wc + dx)
        top = ty * u
        bot = h - by * u
        return (xt, top + v * (bot - top))
    g = [lp(0.18, 0.12), lp(0.82, 0.12), lp(0.82, 0.48), lp(0.18, 0.48)]
    gl = 0.40 - 0.12 * sh
    d.polygon([(Q(x), Q(y)) for x, y in g], fill=C((gl * 0.9, gl, gl * 1.05)))
    pb = [lp(0.80, 0.56), lp(0.92, 0.56), lp(0.92, 0.59), lp(0.80, 0.59)]
    d.polygon([(Q(x), Q(y)) for x, y in pb], fill=C((0.45, 0.43, 0.38)))
    im = im.resize((w, h), Image.LANCZOS)
    return np.asarray(im, np.float32) / 255.0


PLATE = None
YY = XX = None


def spill_mask(door):
    if door < 0.05:
        return None
    q = 4
    sh = math.sin(math.radians(door))
    m = Image.new('L', (W // q, H // q), 0)
    d = ImageDraw.Draw(m)
    x0, y0, x1, y1 = DOOR
    near_l = 120
    near_r = 150 + 1050 * sh
    far_r = x0 + (x1 - x0) * min(1.0, sh * 1.15)
    d.polygon([(x0 / q, y1 / q), (far_r / q, y1 / q), (near_r / q, H / q), (near_l / q, H / q)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(7))
    a = np.asarray(m.resize((W, H), Image.BILINEAR), np.float32) / 255.0
    fall = np.clip(1.15 - (YY - y1) / 620.0, 0.0, 1.0) ** 1.3
    a = a * np.where(YY >= y1 - 2, fall, 0.0)
    glow = np.exp(-(((XX - 390) / 260) ** 2 + ((YY - 520) / 210) ** 2)) * 0.6
    return a, glow, sh


def render(frame, seed_base=1000):
    st = TL.state(frame)
    a = PLATE.copy()
    x0, y0, x1, y1 = DOOR
    a[y0:y1, x0:x1] = door_layer(st['t'], st['door'], st['figs'])
    light = 0.0
    sp = spill_mask(st['door'])
    if sp is not None:
        m, glow, sh = sp
        for (fi, fx, fy, fh, bob) in st["figs"]:
            px = x0 + (x1 - x0) / 2 + (fx - TL.EVENTS[fi]["fig"]["x_in"]) * 82
            if x0 - 30 < px < x1 + 30:
                far_r = x0 + (x1 - x0) * min(1.0, sh * 1.15)
                bx = 120 + (px - x0) / max(1.0, far_r - x0) * (150 + 1050 * sh - 120)
                smk = Image.new("L", (W // 4, H // 4), 0)
                ImageDraw.Draw(smk).polygon([((px - 12) / 4, y1 / 4), ((px + 12) / 4, y1 / 4), ((bx + 90) / 4, H / 4), ((bx - 90) / 4, H / 4)], fill=255)
                smk = np.asarray(smk.filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR), np.float32) / 255.0
                m = m * (1 - 0.85 * smk)
        light = sh
        k = (0.55 * m * sh)[..., None]
        a = a + k * COLD * (a + 0.10)
        a = a + (glow * 0.06 * sh)[..., None] * COLD
        crop = np.clip(a[y0 - 60:y1 + 60, x0 - 80:x1 + 80] - 0.55, 0, None)
        ci = Image.fromarray((np.clip(crop, 0, 1) * 255).astype(np.uint8))
        bl = np.asarray(ci.filter(ImageFilter.GaussianBlur(18)), np.float32) / 255.0
        a[y0 - 60:y1 + 60, x0 - 80:x1 + 80] += bl * 0.5 * sh
    reach = 0.0
    if sp is not None:
        reach = float(sp[0][1030:1060, int(PIVOT[0]) - 30:int(PIVOT[0]) + 30].mean()) * 1.6 + 0.25 * light
        smk = Image.new("L", (W // 4, H // 4), 0)
        ImageDraw.Draw(smk).polygon([((PIVOT[0] - 6) / 4, (PIVOT[1] - 4) / 4), ((PIVOT[0] + 6) / 4, (PIVOT[1] + 4) / 4), ((PIVOT[0] + 330 * sh + 40) / 4, (H + 40) / 4), ((PIVOT[0] + 330 * sh - 10) / 4, (H + 40) / 4)], fill=255)
        smk = np.asarray(smk.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR), np.float32) / 255.0
        a = a * (1 - (0.45 * smk * min(1.0, reach)))[..., None]
    rgb, al, ux, uy = umbrella_layer(st['umb'], min(1.0, reach))
    reg = a[uy:uy + UH, ux:ux + UW]
    a[uy:uy + UH, ux:ux + UW] = reg * (1 - al[..., None]) + rgb
    a = np.clip(a, 0, None)
    a = a / (1 + 0.18 * a)
    a = 0.015 + 0.985 * a
    lum = a.mean(axis=2, keepdims=True)
    a = lum + (a - lum) * 0.82
    a = np.clip(a, 0, 1) ** 1.06
    r = np.random.default_rng(seed_base + frame)
    g = r.standard_normal((H // 2, W // 2)).astype(np.float32)
    g = np.asarray(Image.fromarray(g).resize((W, H), Image.BILINEAR), np.float32)
    g2 = r.standard_normal((H, W)).astype(np.float32)
    grain = 0.028 * g + 0.014 * g2
    a = a + (grain * (0.2 + 1.0 * np.sqrt(np.clip(lum[..., 0], 0, 1))))[..., None]
    return (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)


def init():
    global PLATE, UMB3, YY, XX
    YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
    PLATE = build_plate()
    UMB3 = build_umbrella()


def _job(f):
    return render(f).tobytes()


if __name__ == '__main__':
    init()
    os.makedirs('out', exist_ok=True)
    if sys.argv[1] == 'stills':
        for n in sys.argv[2:]:
            Image.fromarray(render(int(n))).save('out/still_%04d.png' % int(n))
            print('still', n)
    elif sys.argv[1] == 'film':
        out = sys.argv[2]
        nw = int(sys.argv[3]) if len(sys.argv) > 3 else os.cpu_count()
        lo = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        hi = int(sys.argv[5]) if len(sys.argv) > 5 else TL.NFRAMES
        import multiprocessing as mp
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                               '-s', '%dx%d' % (W, H), '-r', str(TL.FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                               '-tune', 'grain', out], stdin=subprocess.PIPE)
        with mp.get_context('fork').Pool(nw) as pool:
            for i, b in enumerate(pool.imap(_job, range(lo, hi), chunksize=4)):
                ff.stdin.write(b)
                if i % 96 == 0:
                    print('frame', lo + i, flush=True)
        ff.stdin.close()
        ff.wait()
        print('done', out)
