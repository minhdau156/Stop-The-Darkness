#!/usr/bin/env python3
"""Chặn Bóng Tối - bản giao diện đẹp (logic giống StopTheDarknessFake.py, chỉ làm lại phần hiển thị).
Chạy:  pip install pygame   rồi   python StopTheDarknessPretty.py
Phím: Space = tạm dừng, J = nhật ký, Esc = đóng/thoát về menu."""
import math, os, random, sys
import pygame

W, H, T, U = 15, 12, 54, 6
MW, PW = W * T, 330
SW, SH = MW + PW, H * T
C = pygame.Color
BG, PN, CARD, LINE = C('#14131c'), C('#1d1b27'), C('#2a2839'), C('#3d3a55')
INK, MUTE, GOLD, GREEN, RED = C('#f0ecf8'), C('#9b97b0'), C('#f2c14e'), C('#7ddc95'), C('#ff7070')
RC = [C('#b9803f'), C('#a8a8b4'), C('#b56be8'), C('#d8ea3c')]
RN = ['Gỗ', 'Đá', 'Phép thuật', 'Khoa học']


import array
try:
    pygame.mixer.init(); AUDIO = pygame.mixer.get_init() is not None
except Exception:
    AUDIO = False
_snd = {}
def play(f, dur=.12, vol=.25, decay=4.0):
    """Phát một nốt sin ngắn (tự sinh, không cần file âm thanh)."""
    if not AUDIO: return
    try:
        key = (f, dur, vol, decay)
        if key not in _snd:
            fr, _fmt, ch = pygame.mixer.get_init(); n = int(fr * dur)
            a = array.array('h')
            for i in range(n):
                v = int(32767 * vol * math.exp(-decay * i / n) * math.sin(2 * math.pi * f * i / fr)); a.extend([v] * ch)
            _snd[key] = pygame.mixer.Sound(buffer=a.tobytes())
        _snd[key].play()
    except Exception:
        pass
def sfx(name):
    if not g.sound: return
    if name == 'up': play(660, .1); play(990, .14, .15)
    elif name == 'no': play(140, .18, .3, 6)
    elif name == 'win': [play(f, .9, .2, 2) for f in (523, 659, 784, 1047)]
    elif name == 'lose': play(110, 1.2, .35, 2)


def L(name, cost=(), prod=(), boost=(), **kw):
    p4 = lambda a: tuple(a) + (0,) * (4 - len(a))
    return dict(n=name, c=p4(cost), p=p4(prod), b=p4(boost), **kw)


K = {
 'field': [L('Cánh đồng')], 'water': [L('Nước')],
 'forest': [L('Rừng', (), (3,), (.25,)), L('Rừng', (3,), (4.5,), (.25,)), L('Rừng', (7,), (8.7,), (.25,)), L('Rừng', (15,), (22.5,), (.25,))],
 'treetop': [L('Làng trên cây', (15,), (10, 0, 1), (.5,)), L('Làng trên cây', (30, 0, 5), (22.5, 0, 2), (1,)), L('Làng trên cây', (100, 20, 20), (40, 0, 5), (1,))],
 'rocks': [L('Đá', (), (0, 3)), L('Đá', (8,), (0, 3)), L('Đá', (10, 3), (0, 7)), L('Đá', (15, 12, 0, 2), (0, 30), (0, .25)), L('Đá', (10, 60, 0, 8), (0, 60, 0, 4), (0, .33), t='Cần có Trung tâm công nghệ đá.')],
 'stonetech': [L('Trung tâm công nghệ đá', (200, 100, 0, 50), (0, 100, 0, 8.7), (0, .5, 0, .25), t='Tăng sản lượng đá của mọi ô Đá theo sản lượng khoa học.'), L('Trung tâm công nghệ đá', (400, 200, 0, 200), (0, 75, 0, 15), (0, .5, 0, .5), t='Tăng sản lượng đá của mọi ô Đá theo sản lượng khoa học.')],
 'mushroom': [L('Rừng nấm', (), (1.2, 0, 2), (0, 0, .25)), L('Rừng nấm', (6,), (1.2, 0, 2), (0, 0, .25)), L('Rừng nấm', (20, 0, 2), (3.5, 0, 7), (0, 0, .25))],
 'mushcity': [L('Thành phố nấm', (50, 0, 30, 5), (10, 0, 20, 2), (0, 0, .5, .25))],
 'roots': [L('Rừng rễ cây', (), (2, 0, 3), (.25, 0, .25)), L('Rừng rễ cây', (10,), (2, 0, 3), (.25, 0, .25)), L('Rừng rễ cây', (25, 0, 5), (8, 0, 12), (.25, 0, .25)), L('Rừng rễ cây', (60, 0, 15), (20, 0, 24), (.25, 0, .25))],
 'rootscity': [L('Thành phố rễ cây', (100, 0, 60, 10), (20, 0, 40, 3), (.25, 0, .5))],
 'circle': [L('Vòng đá'), L('Vòng đá', (0, 100, 100), push=1, t='Đẩy lùi bóng tối.'), L('Vòng đá', (100, 300, 300, 20), push=1, t='Đẩy lùi bóng tối một chút.'), L('Vòng đá', (1000, 1500, 1000), win=2, t='Chặn đứng bóng tối!')],
 'village': [L('Làng', (7,), (), (.25, .25)), L('Làng', (12, 12), (), (.5, .5))],
 'city': [L('Thành phố', (15, 60, 0, 10), (0, 0, 0, 2.5), (.5, .5)), L('Thành phố', (40, 150, 0, 30), (0, 0, 0, 6.2), (.5, .5, 0, .25))],
 'port': [L('Làng cảng', (5,), (2,), (.25, .25)), L('Làng cảng', (45, 18), (6,), (.5, .5))],
 'portcity': [L('Thành phố cảng', (120, 60, 0, 10), (12, 6, 0, 2.5), (.5, .5)), L('Thành phố cảng', (300, 150, 0, 40), (25, 12, 0, 6), (.5, .5, 0, .25))],
 'docks': [L('Bến tàu', (20, 10), (6,), (.25, .25))],
 'lighthouse': [L('Hải đăng', (15, 15), (0, 0, 0, 1), (.25, .25), t='Dẫn đường cho tàu thuyền.')],
 'magic': [L('Làng phép thuật', (5, 0, 1), (0, 0, 2), (.25, 0, .25), t='Xây cạnh một Làng để mở Tháp ánh sáng ở ô kề.'), L('Làng phép thuật', (20, 10, 5), (0, 0, 5), (.5, 0, .5), t='Mở khóa nâng cấp Vòng đá.')],
 'magiccity': [L('Thành phố phép thuật', (60, 30, 20, 10), (0, 0, 10, 2), (.5, 0, .5, .25))],
 'magicport': [L('Làng cảng phép thuật', (7, 0, 1), (2, 0, 2), (.25, 0, .25)), L('Làng cảng phép thuật', (45, 18, 6), (4, 0, 5), (.5, 0, .5))],
 'magicportcity': [L('Thành phố cảng phép thuật', (120, 60, 20, 10), (8, 4, 10, 2), (.5, 0, .5))],
 'mining': [L('Làng khai mỏ', (10, 5), (0, 5), (0, .5)), L('Làng khai mỏ', (30, 30), (0, 12), (0, .5))],
 'miningres': [L('Thành phố nghiên cứu mỏ', (60, 100, 0, 10), (0, 0, 0, 3), (0, .5, 0, .25)), L('Thành phố nghiên cứu mỏ', (200, 300, 0, 30), (0, 0, 0, 6), (0, .5, 0, .25))],
 'lightres': [L('Thành phố nghiên cứu ánh sáng', (400, 500, 0, 100), (0, 0, 0, 8), (0, .5, 0, .25), push=1, t='Đẩy lùi bóng tối.'), L('Thành phố nghiên cứu ánh sáng', (1200, 1200, 0, 600), (0, 0, 0, 12), (0, .5, 0, .5), win=2, t='Chặn đứng bóng tối!')],
 'tower': [L('Tháp ánh sáng', (30, 20, 15), (0, 0, 1.2), (0, 0, .25), light=1, t='Làm chậm bóng tối.'), L('Tháp ánh sáng', (200, 100, 100, 20), (0, 0, 6), (0, 0, .5), light=3, win=1, t='Làm chậm và chặn đứng bóng tối!')],
 'towerwater': [L('Tháp nước', (100, 50, 50, 10), (0, 0, 5, 3), (0, 0, .5, .25))],
 'potion': [L('Nhà máy thuốc', (80, 40, 40, 10), (0, 0, 5, 10), (0, 0, 0, .5))],
}
NEXT = {'village': 'city', 'port': 'portcity', 'magic': 'magiccity', 'magicport': 'magicportcity',
        'mushroom': 'mushcity', 'roots': 'rootscity', 'mining': 'miningres', 'miningres': 'lightres'}
# Nhấn vào ô đã xây thuộc nhóm này sẽ thu hoạch ngay (ô loại, (chỉ số tài nguyên, số lượng mỗi lần nhấn)).
HARVEST = {'forest': (0, 2), 'rocks': (1, 2), 'mushroom': (2, 2)}
VFAM = {'village', 'port', 'magic', 'magicport', 'mining', 'city', 'portcity', 'magiccity', 'magicportcity', 'miningres', 'lightres', 'mushcity', 'rootscity'}
PAGES = [('Cơ bản, thành phố và nước', ['field', 'water', 'village', 'city', 'port', 'portcity', 'docks', 'lighthouse']),
         ('Rừng và gỗ', ['forest', 'treetop']),
         ('Khai mỏ', ['rocks', 'stonetech', 'mining', 'miningres', 'lightres']),
         ('Phép thuật', ['mushroom', 'roots', 'circle', 'magic', 'magiccity', 'magicport', 'magicportcity', 'mushcity', 'rootscity', 'tower']),
         ('Phép thuật (tiếp)', ['towerwater', 'potion'])]

def spiral():
    """Thứ tự bóng tối: từ góc dưới-trái chạy sang phải, rồi vòng ngược chiều kim đồng hồ, thu dần vào trong."""
    order, x0, x1, y0, y1 = [], 0, W - 1, 0, H - 1
    while x0 <= x1 and y0 <= y1:
        order += [(x, y1) for x in range(x0, x1 + 1)]
        order += [(x1, y) for y in range(y1 - 1, y0 - 1, -1)]
        if y0 < y1: order += [(x, y0) for x in range(x1 - 1, x0 - 1, -1)]
        if x0 < x1: order += [(x0, y) for y in range(y0 + 1, y1)]
        x0 += 1; x1 -= 1; y0 += 1; y1 -= 1
    d = [[0] * W for _ in range(H)]
    for i, (x, y) in enumerate(order): d[y][x] = i
    return d, order


def pages():
    ex = () if g.mode == 'ext' else ('roots', 'rootscity', 'potion')
    return [(t, [k for k in ks if k not in ex]) for t, ks in PAGES]


# ---------------------------------------------------------------- vẽ pixel
def draw_tile(s, k, l, v, ox, oy, u, part='all'):
    def r(col, x, y, w, h):
        pygame.draw.rect(s, C(col), (ox + int(x * u), oy + int(y * u), max(1, int(w * u)), max(1, int(h * u))))
    wet = k in ('water', 'lighthouse', 'docks', 'towerwater')
    tan = k in ('circle', 'mushroom', 'roots', 'village', 'port', 'magic', 'magicport', 'mushcity', 'rootscity', 'tower', 'city',
                'portcity', 'magiccity', 'magicportcity', 'mining', 'miningres', 'lightres', 'stonetech', 'potion')
    if part != 'obj': r('#bcd9f2' if wet else '#e8d6b8' if tan else '#b9eea5', 0, 0, 9, 9)
    if part == 'obj': pass
    elif wet:
        r('#d4e9f9', v % 6, 2, 2, 1); r('#d4e9f9', (v * 5) % 6, 6, 2, 1)
    elif k in ('field', 'forest', 'rocks', 'treetop'):
        r('#a4dd90', v % 9, (v * 3) % 9, 1, 1); r('#a4dd90', (v * 5) % 9, (v * 7) % 9, 1, 1)

    if part == 'base': return

    def tree(x, y):
        r('#4aa63a', x, y + 1, 3, 2); r('#4aa63a', x + 1, y, 1, 1); r('#2f7f2a', x, y + 2, 3, 1); r('#8a5a2b', x + 1, y + 3, 1, 1)

    def house(x, y, roof, wall, tall=False):
        if tall:
            r(roof, x, y, 3, 1); r(wall, x, y + 1, 3, 4); r('#d9e6f2', x + 1, y + 2, 1, 1); return
        r(roof, x, y, 3, 1); r(wall, x, y + 1, 3, 2); r('#6b4a2a', x + 1, y + 2, 1, 1)

    def mush(x, y, cap):
        r(cap, x, y + 1, 4, 1); r(cap, x + 1, y, 2, 1); r('#b89a78', x + 1, y + 2, 2, 2)

    if k == 'forest':
        if l == 0:
            for p in [(0, 0), (3, 1), (6, 0), (1, 5), (4, 4), (6, 5)]: tree(*p)
        else:
            for p in [(0, 0), (6, 0), (0, 5), (6, 5)]: tree(*p)
            for x, y in [(3, 3), (0, 3), (6, 3)][:min(3, l)]: house(x, y, '#b5651d' if l == 1 else '#c0392b', '#e0c196')
    elif k == 'treetop':
        for p in [(0, 0), (6, 0), (0, 5), (6, 5)][:2 + l]: tree(*p)
        house(3, 3, '#c0392b', '#e0c196')
    elif k == 'rocks':
        for x, y in ([(0, 1), (4, 0), (2, 4), (5, 5), (0, 6), (6, 2)] if l == 0 else [(0, 0), (6, 0), (0, 5), (6, 5)]):
            r('#8c8c92', x, y + 1, 3, 2); r('#a9a9b0', x, y, 2, 1); r('#6b6b72', x, y + 3, 3, 1)
        if l:
            for x, y in [(3, 3), (0, 3), (6, 3)][:min(3, l)]: house(x, y, '#3a7bd5' if l >= 4 else '#555a66', '#c9b08a')
    elif k == 'mushroom':
        for (x, y, cap) in [(0, 0, '#d93030'), (4, 1, '#8a6a4a'), (5, 5, '#6e4f9a'), (1, 5, '#d93030'), (6, 6, '#8a6a4a')][:min(5, 2 + l)]: mush(x, y, cap)
        r('#d93030', 6, 3, 1, 1)
    elif k == 'roots':
        for x, y in [(0, 1), (3, 0), (6, 2), (2, 5), (5, 6)]:
            r('#7a5230', x + 1, y, 1, 3); r('#7a5230', x, y + 1, 1, 1); r('#7a5230', x + 2, y, 1, 1)
        for i, (x, y) in enumerate([(1, 6), (4, 3), (6, 7), (0, 3)][:l]): r('#6a5acd', x, y, 2, 1); r('#8a7ae0', x, y - 1, 1, 1)
    elif k == 'circle':
        for i in range(8):
            a = i * math.pi / 4; r('#7d7d85', 4 + round(math.cos(a) * 3.2), 4 + round(math.sin(a) * 3.2), 1, 1)
        r('#c9a46a', 3, 3, 3, 3)
        if l >= 1: r('#9b59d6', 4, 4, 1, 1)
        if l >= 2: r('#9b59d6', 1, 4, 1, 1); r('#9b59d6', 7, 4, 1, 1)
    elif k == 'lighthouse':
        r('#ffffff', 3, 1, 3, 6); r('#dd3333', 3, 2, 3, 1); r('#dd3333', 3, 4, 3, 1); r('#555555', 2, 0, 5, 1); r('#ffe36b', 4, 0, 1, 1)
    elif k == 'docks':
        r('#b0916a', 1, 3, 7, 1); r('#b0916a', 1, 3, 1, 5); r('#8a6f4a', 3, 4, 4, 1)
    elif k == 'tower':
        r('#7a4fd0', 3, 0, 3, 7); r('#d4b6ff', 3, 0, 3, 1); r('#8c8c92', 2, 7, 5, 1); r('#ffe36b', 4, 2, 1, 1)
        if l: r('#ffe36b', 4, 4, 1, 1)
    elif k == 'towerwater':
        r('#3a7bd5', 3, 0, 3, 7); r('#9fd0ff', 3, 0, 3, 1); r('#8c8c92', 2, 7, 5, 1)
    elif k == 'potion':
        r('#6e4f9a', 3, 1, 3, 1); r('#8fd18f', 2, 3, 5, 4); r('#d4b6ff', 3, 3, 1, 1); r('#555555', 3, 0, 3, 1)
    elif k == 'stonetech':
        r('#8c8c92', 1, 1, 7, 6); r('#3a7bd5', 3, 2, 3, 2); r('#555555', 1, 0, 7, 1); r('#a9a9b0', 2, 5, 5, 1)
    elif k in ('village', 'port', 'magic', 'magicport', 'mining', 'city', 'portcity', 'magiccity', 'magicportcity',
               'miningres', 'lightres', 'mushcity', 'rootscity'):
        roof = {'village': '#b5651d', 'port': '#2aa7a0', 'magic': '#8a4fd0', 'magicport': '#8a4fd0', 'mining': '#777777',
                'city': '#555a66', 'portcity': '#2aa7a0', 'magiccity': '#8a4fd0', 'magicportcity': '#8a4fd0',
                'miningres': '#555a66', 'lightres': '#3a7bd5', 'mushcity': '#d93030', 'rootscity': '#5b3a1e'}[k]
        city = k in ('city', 'portcity', 'magiccity', 'magicportcity', 'miningres', 'lightres', 'mushcity', 'rootscity')
        wall = '#9fb4c7' if city else '#e0c196'
        n = min(4, l + 2) if not city else 4
        for x, y in [(0, 0), (5, 0), (0, 4), (5, 4)][:n]: house(x, y, roof, wall, tall=city and l >= 0 and y == 0)
        if k in ('magic', 'magicport', 'magiccity', 'magicportcity'): r('#d4b6ff', 4, 4, 1, 1)
        if k in ('port', 'magicport', 'portcity', 'magicportcity'): r('#bcd9f2', 3, 7, 3, 1)


# ---------------------------------------------------------------- trạng thái
class Tile:
    def __init__(s, k, x, y, v): s.k, s.l, s.x, s.y, s.v, s.built, s.hv = k, 0, x, y, v, False, False


class Game:
    def __init__(s):
        s.mode, s.state, s.speed, s.paused = 'std', 'menu', 2, False
        s.hov, s.msg, s.msg_t, s.jpage, s.jopen = None, None, 0, 0, False
        s.music, s.sound, s.hl, s.hl_next, s.hl_list, s.dprog = True, True, False, 0, [], 0.0
        s.gen()

    def gen(s):
        rd = random.Random()
        s.G = [[None] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                r = rd.random()
                k = ('field' if r < .36 else 'forest' if r < .60 else 'rocks' if r < .71 else 'water' if r < .84
                     else 'mushroom' if r < .92 else 'roots')
                if k == 'roots' and s.mode != 'ext': k = 'field'
                a = s.G[y][x - 1] if x else None; b = s.G[y - 1][x] if y else None
                if a and a.k in ('forest', 'rocks', 'water', 'field') and rd.random() < .38: k = a.k
                elif b and b.k in ('forest', 'rocks', 'water', 'field') and rd.random() < .3: k = b.k
                s.G[y][x] = Tile(k, x, y, rd.randrange(60))
        s.G[rd.randrange(4, 8)][rd.randrange(5, 10)].k = 'circle'
        s.res = [10.0, 0, 0, 0]; s.dn = 0; s.dord, s.dpos = spiral(); s.dacc = 0; s.gt = 0; s.dprog = 0.0
        s.over = False; s.first = False
        s.jset = {('field', 0), ('water', 0)} | {(t.k, 0) for row in s.G for t in row}
        s.recalc()

    def dark(s, x, y): return s.dord[y][x] < s.dn
    def nb(s, t):
        return [s.G[t.y + b][t.x + a] for a, b in ((0, -1), (1, 0), (0, 1), (-1, 0))
                if 0 <= t.x + a < W and 0 <= t.y + b < H and not s.dark(t.x + a, t.y + b)]
    def exists(s, k): return any(t.k == k for row in s.G for t in row)

    def up(s, t):
        """Trả về (kind, level, lock_text|None) hoặc None."""
        n = s.nb(t); cnt = lambda *ks: sum(q.k in ks for q in n)
        built = [q for q in n if q.built]
        k, l = t.k, t.l
        if k == 'circle' and l == 0 and not any(q.k == 'magic' and q.l >= 1 and q.built for row in s.G for q in row):
            return ('circle', 1, 'Dùng phép thuật. (Nâng cấp Làng phép thuật lên cấp 2 để mở khóa.)')
        if k == 'field':
            mv = [q for q in n if q.k == 'magic' and q.built]
            if mv and not s.exists('tower'):
                good = [q for q in mv if any(z.k in ('village', 'city') and z.built for z in s.nb(q))]
                if any(q.l >= 1 for q in good): return ('tower', 0, None)
                if good: return ('tower', 0, 'Nâng cấp làng phép thuật lên cấp 2 trước.')
            if any(q.built and q.k in ('magic', 'magiccity', 'magicport', 'magicportcity') for q in n) and cnt('water') and not s.exists('towerwater'):
                return ('towerwater', 0, None)
            mu, wat = cnt('mushroom'), cnt('water')
            if mu and wat: return ('magicport', 0, None)
            if mu: return ('magic', 0, None)
            if cnt('rocks') >= 2: return ('mining', 0, None)
            if wat: return ('port', 0, None)
            return ('village', 0, None)
        if k == 'forest' and l == 3 and not s.exists('potion') and any(q.k == 'roots' and q.l == 3 for q in n): return ('potion', 0, None)
        if k == 'forest' and l == 0 and cnt('forest') == 4 and not cnt('treetop'): return ('treetop', 0, None)
        if k == 'rocks' and l == 3 and not s.exists('stonetech'):
            ok = cnt('city', 'portcity', 'magiccity', 'miningres')
            return ('stonetech', 0, None if ok else 'Cần một Thành phố kề bên để xây Trung tâm công nghệ đá.')
        if k == 'water': return ('docks', 0, None) if cnt('port', 'portcity') else ('lighthouse', 0, None)
        if k == 'miningres' and l == 0 and not s.exists('lightres'): return ('lightres', 0, None)
        if l + 1 < len(K[k]): return (k, l + 1, None)
        if k in NEXT:
            nk = NEXT[k]
            if nk == 'lightres': return (nk, 0, 'Duy nhất: chỉ xây được một.' if s.exists('lightres') else None)
            need = 1 if nk in ('portcity', 'magicportcity') else 2
            if not (len(built) >= 4 or sum(q.k in VFAM for q in built) >= need):
                return (nk, 0, f'Thử xây thêm xung quanh: cần 4 ô kề đã xây, hoặc {need} làng/thành phố kề bên.')
            return (nk, 0, None)
        return None

    def mult(s, t, r): return 1 + sum(K[q.k][q.l]['b'][r] for q in s.nb(t) if q.built)

    def recalc(s):
        s.rate = [0.0] * 4; s.light = 0; rs = 0.0; tech = 0
        for row in s.G:
            for t in row:
                if s.dark(t.x, t.y) or not t.built: continue
                d = K[t.k][t.l]; s.light += d.get('light', 0)
                if t.k == 'stonetech': tech += 1
                for r in range(4):
                    if d['p'][r]:
                        v = d['p'][r] * s.mult(t, r); s.rate[r] += v
                        if t.k == 'rocks' and r == 1: rs += v
        s.techpct = .01 * s.rate[3] * tech if tech else 0   # Trung tâm công nghệ đá tăng sản lượng đá
        s.rate[1] += rs * s.techpct

    def cost(s, d, k=None, l=0):
        """Giá tăng dần theo số công trình cùng loại đã xây (như game gốc)."""
        m = 1.5 if s.mode == 'ext' else 1
        if k and k not in ('circle', 'tower', 'towerwater', 'potion', 'stonetech', 'lightres'):
            m *= 1 + .2 * sum(1 for row in s.G for q in row if q.built and q.k == k and q.l >= l)
        return [math.ceil(c * m) if c else 0 for c in d['c']]

    def click(s, t):
        if s.state != 'play' or s.over or s.paused or s.dark(t.x, t.y): return
        if t.k in HARVEST and not t.hv:   # mỗi ô chỉ thu hoạch được một lần
            t.hv = True
            ri, amt = HARVEST[t.k]; s.res[ri] += amt; sfx('up')
        u = s.up(t)
        if not u or u[2]: return
        d = K[u[0]][u[1]]; need = s.cost(d, u[0], u[1])
        if any(s.res[i] < need[i] for i in range(4)): sfx('no'); return
        for i in range(4): s.res[i] -= need[i]
        t.k, t.l, t.built = u[0], u[1], True; s.jset.add((u[0], u[1])); sfx('up')
        if d.get('push'): s.dn = max(0, s.dn - 12 * d['push'])
        s.recalc()
        if not s.first:
            s.first = True; s.say('Nâng cấp có sẵn phụ thuộc vào bốn ô kề bên, hãy nhìn quanh và thử nghiệm. Chúc may mắn!', t=14)
        if d.get('win') == 2 or (d.get('win') == 1 and s.mode == 'std'): s.win()

    def say(s, text, btns=(), t=0): s.msg, s.msg_btns, s.msg_t = text, list(btns), t
    def start(s):
        s.state, s.paused = 'play', False
        s.say('Bóng tối sẽ lan từng ô từ góc dưới bên trái rồi xoáy dần vào trong. Bạn vẫn có thể ngăn nó! Hãy bắt đầu bằng việc sản xuất gỗ. Nhấn vào Rừng để nâng cấp. Mỗi ô Rừng/Đá/Nấm chỉ thu hoạch ngay được một lần ở lần nhấn đầu tiên.')
    def to_menu(s): s.state = 'menu'; s.msg = None; s.jopen = False; s.gen()
    def lit(s): return sum(not s.dark(x, y) for y in range(H) for x in range(W))
    def win(s):
        s.over = True; sfx('win'); sc = max(1, round(s.lit() * 3 + 600 - s.gt / 10))
        res = f'Thời gian: {int(s.gt // 60)}:{int(s.gt % 60):02d}' if s.mode == 'ext' else f'Điểm: {sc}'
        s.say('Bạn đã cứu vùng đất khỏi bóng tối! Làm tốt lắm! Bạn đã thắng, nhưng vẫn có thể tiếp tục cải tạo vùng đất nếu muốn. Hoặc chơi lại để tìm cách thắng khác. ' + res, [('Về menu', s.to_menu), ('Tiếp tục', lambda: (setattr(s, 'over', False), s.say(None)))])
    def lose(s):
        s.over = True; sfx('lose')
        s.say('Bóng tối đã nuốt chửng mọi vòng đá... vùng đất đã mất.', [('Về menu', s.to_menu), ('Chơi lại', lambda: (s.gen(), s.start()))])

    def tick(s, dt):
        if s.msg_t > 0:
            s.msg_t -= dt
            if s.msg_t <= 0: s.msg = None
        if s.state != 'play' or s.paused or s.over: return
        g = dt * s.speed; s.gt += g
        for i in range(4): s.res[i] += s.rate[i] * g / 60
        s.dacc += g; iv = (5.5 if s.mode == 'ext' else 8) * (1 + .35 * s.light)
        while s.dacc >= iv and not s.over:
            s.dacc -= iv; s.dn = min(W * H, s.dn + 1)
            s.recalc()
            if not any(t.k == 'circle' and not s.dark(t.x, t.y) for row in s.G for t in row): s.lose()
        s.dprog = min(1.0, s.dacc / iv)


# ================================================================ GIAO DIỆN MỚI
pygame.init()
scr = pygame.display.set_mode((SW, SH)); pygame.display.set_caption('Chặn Bóng Tối')
# Font Noto Sans tự mang theo trong project — hiển thị đúng dấu tiếng Việt trên mọi máy.
_FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fonts', 'NotoSans-Regular.ttf')
def mkfont(sz, bold=False):
    if os.path.isfile(_FONT_PATH):
        f = pygame.font.Font(_FONT_PATH, sz); f.set_bold(bold); return f
    return pygame.font.SysFont('segoeui,arial,dejavusans,freesans', sz, bold=bold)
F, FB, FS, FT, FH = mkfont(15), mkfont(18, True), mkfont(13), mkfont(32, True), mkfont(16, True)
g = Game(); buttons = []
X0, CWD = MW + 14, PW - 28          # lề trái và bề rộng nội dung của bảng bên phải
CW = CWD - 24                       # bề rộng chữ bên trong thẻ


def now(): return pygame.time.get_ticks() / 1000
def fmt(n): return f'{n/1000:.1f}k' if n >= 1000 else f'{n:.1f}' if n % 1 and n < 10 else str(int(n))
def wrap(s, f, w):
    out, line = [], ''
    for word in s.split():
        if f.size(line + ' ' + word)[0] > w and line: out.append(line); line = word
        else: line = (line + ' ' + word).strip()
    return out + [line]


def rr(rect, col, r=10, w=0):
    """Hình chữ nhật bo góc, hỗ trợ màu có alpha."""
    rc, col = pygame.Rect(rect), C(col)
    if col.a < 255:
        s = pygame.Surface(rc.size, pygame.SRCALPHA); pygame.draw.rect(s, col, s.get_rect(), w, border_radius=r); scr.blit(s, rc.topleft)
    else:
        pygame.draw.rect(scr, col, rc, w, border_radius=r)


_gr = {}
def vgrad(w, h, c1, c2):
    key = (w, h, c1, c2)
    if key not in _gr:
        s = pygame.Surface((w, h))
        for y in range(h):
            t = y / max(1, h - 1); pygame.draw.line(s, [int(a + (b - a) * t) for a, b in zip(c1, c2)], (0, y), (w, y))
        _gr[key] = s
    return _gr[key]


def txt(s, x, y, f=F, col=INK, shadow=False):
    if shadow: scr.blit(f.render(s, True, (8, 6, 14)), (x + 1, y + 2))
    sf = f.render(s, True, col); scr.blit(sf, (x, y)); return y + sf.get_height() + 2
def ctxt(s, cx, cy, f=F, col=INK, shadow=False):
    sf = f.render(s, True, col)
    if shadow: scr.blit(f.render(s, True, (8, 6, 14)), sf.get_rect(center=(cx + 1, cy + 2)))
    scr.blit(sf, sf.get_rect(center=(cx, cy)))
def para(s, x, y, w, f=F, col=INK):
    for ln in wrap(s, f, w): y = txt(ln, x, y, f, col)
    return y


def gem(cx, cy, i, r=8):
    pygame.draw.circle(scr, (10, 8, 16), (cx, cy + 1), r + 1)
    pygame.draw.circle(scr, RC[i], (cx, cy), r)
    pygame.draw.circle(scr, RC[i].lerp((255, 255, 255), .55), (cx - r // 3, cy - r // 3), max(2, r // 3))


def draw_icon(name, cx, cy, col):
    if name == 'pause': rr((cx - 6, cy - 7, 4, 14), col, 1); rr((cx + 2, cy - 7, 4, 14), col, 1)
    elif name == 'play': pygame.draw.polygon(scr, col, [(cx - 5, cy - 8), (cx - 5, cy + 8), (cx + 7, cy)])
    elif name == 'ff':
        pygame.draw.polygon(scr, col, [(cx - 9, cy - 6), (cx - 9, cy + 6), (cx - 1, cy)])
        pygame.draw.polygon(scr, col, [(cx, cy - 6), (cx, cy + 6), (cx + 8, cy)])
    elif name == 'close':
        pygame.draw.line(scr, col, (cx - 6, cy - 6), (cx + 6, cy + 6), 3); pygame.draw.line(scr, col, (cx - 6, cy + 6), (cx + 6, cy - 6), 3)


def button(label, rect, cb, sel=False, kind='n', dot=None, icon=None):
    rc = pygame.Rect(rect); hv = rc.collidepoint(pygame.mouse.get_pos()); pr = hv and pygame.mouse.get_pressed()[0]
    if kind == 'p':
        fill = GOLD.lerp((255, 255, 255), .25) if hv else GOLD; brd = GOLD.lerp((0, 0, 0), .35); fg = C('#2a2008')
    else:
        fill = C('#3b3855') if hv else C('#35314b') if sel else CARD
        brd = GOLD if sel else C('#6a668a') if hv else LINE; fg = INK
    rr((rc.x, rc.y + 3, rc.w, rc.h), (0, 0, 0, 90), 10)
    r2 = rc.move(0, 1 if pr else 0)
    rr(r2, fill, 10); rr(r2, brd, 10, 2 if sel else 1)
    if dot is not None: pygame.draw.circle(scr, GREEN if dot else (90, 86, 110), (r2.x + 14, r2.centery), 4)
    if icon and label: ctxt(label, r2.centerx - 11, r2.centery, F, fg); draw_icon(icon, r2.right - 17, r2.centery, fg)
    elif icon: draw_icon(icon, r2.centerx, r2.centery, fg)
    elif label: ctxt(label, r2.centerx + (7 if dot is not None else 0), r2.centery, F, fg)
    buttons.append((rc, cb))


def chips(x, y, vals, pct=False, good=False, afford=False):
    for i, v in enumerate(vals):
        if not v: continue
        gem(x + 6, y + 10, i, 6)
        col = GREEN if good else RED if afford and g.res[i] < v else INK
        sf = FS.render(f'{round(v*100)}%' if pct else fmt(v), True, col); scr.blit(sf, (x + 17, y + 1)); x += 17 + sf.get_width() + 10


# ---- ô đất: vẽ pixel-art rồi bo góc + đổ bóng nhẹ
_ic = {}
def round_surf(s, inset, rad):
    n = s.get_width(); s = s.convert_alpha()
    m = pygame.Surface((n, n), pygame.SRCALPHA); m.fill((255, 255, 255, 0))
    pygame.draw.rect(m, (255, 255, 255, 255), (inset, inset, n - 2 * inset, n - 2 * inset), border_radius=rad)
    s.blit(m, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    b = pygame.Surface((n, n), pygame.SRCALPHA)
    pygame.draw.rect(b, (0, 0, 0, 80), (inset, inset, n - 2 * inset, n - 2 * inset), 1, border_radius=rad)
    s.blit(b, (0, 0)); return s


def tile_surf(k, l, v=7, u=U, inset=2, rad=9):
    key = (k, l, v, u, inset, rad)
    if key not in _ic:
        n = 9 * u; s = pygame.Surface((n, n)); draw_tile(s, k, l, v, 0, 0, u, 'base')
        s.fill((v % 5 * 2,) * 3, special_flags=pygame.BLEND_RGB_ADD)        # mỗi ô sáng hơi khác nhau, nhìn như mảng đất liền
        o = pygame.Surface((n, n), pygame.SRCALPHA); draw_tile(o, k, l, v, 0, 0, u, 'obj')
        m = pygame.mask.from_surface(o); d = max(1, u // 6)
        s.blit(m.to_surface(setcolor=(0, 0, 0, 70), unsetcolor=(0, 0, 0, 0)), (u // 2, u // 2))      # bóng đổ
        ol = m.to_surface(setcolor=(44, 30, 26, 255), unsetcolor=(0, 0, 0, 0))                       # viền tối quanh công trình
        for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)): s.blit(ol, (dx, dy))
        s.blit(o, (0, 0))
        _ic[key] = round_surf(s, inset, rad) if rad else s
    return _ic[key]
def icon(k, l, v=7, s=4): return tile_surf(k, l, v, s, 0, 7)


_dark = vgrad(T, T, (30, 22, 48), (14, 10, 24)).copy()
_wisp = pygame.Surface((44, 44), pygame.SRCALPHA)
for _r in range(22, 0, -2): pygame.draw.circle(_wisp, (120, 70, 180, int(5 + (22 - _r) * 1.3)), (22, 22), _r)
_streak = pygame.Surface((10, 2), pygame.SRCALPHA); _streak.fill((255, 255, 255, 90))
_vig = pygame.Surface((MW, SH), pygame.SRCALPHA)
for _i in range(40): pygame.draw.rect(_vig, (0, 0, 0, int(110 * (1 - _i / 40) ** 2)), (_i, _i, MW - 2 * _i, SH - 2 * _i), 1)


def hl_tiles():
    t = pygame.time.get_ticks()
    if t >= g.hl_next:
        g.hl_next = t + 300; out = []
        for row in g.G:
            for q in row:
                if g.dark(q.x, q.y): continue
                u = g.up(q)
                if u and not u[2] and all(g.res[i] >= c for i, c in enumerate(g.cost(K[u[0]][u[1]], u[0], u[1]))): out.append(q)
        g.hl_list = out
    return g.hl_list


def blit_tile(t, dy=0, tm=0):
    x, y = t.x * T, t.y * T
    scr.blit(tile_surf(t.k, t.l, t.v, U, 0, 0), (x, y))
    if t.k == 'water': scr.blit(_streak, (x + 8 + int((tm * 10 + t.v * 7) % 30), y + 14 + t.v % 20))


def draw_map():
    scr.fill(BG, (0, 0, MW, SH))
    tm = now(); playing = g.state == 'play'
    hov = g.hov if playing and g.hov and not g.dark(g.hov.x, g.hov.y) else None
    for row in g.G:
        for t in row:
            if playing and g.dark(t.x, t.y): continue
            blit_tile(t, 0, tm)
    if g.hl and playing:
        pa = .5 + .5 * math.sin(tm * 4); col = (int(46 + 60 * pa), int(170 + 60 * pa), int(90 + 40 * pa))
        for t in hl_tiles(): pygame.draw.rect(scr, col, (t.x * T + 2, t.y * T + 2, T - 4, T - 4), 2, border_radius=6)
    if hov:
        hl = pygame.Surface((T, T), pygame.SRCALPHA); hl.fill((255, 255, 255, 34)); scr.blit(hl, (hov.x * T, hov.y * T))
        pygame.draw.rect(scr, (255, 255, 255), (hov.x * T + 1, hov.y * T + 1, T - 2, T - 2), 2, border_radius=6)
    if playing:
        pulse = .5 + .5 * math.sin(tm * 2.2); rim = (int(80 + 60 * pulse), 40, int(140 + 50 * pulse))
        for x, y in g.dpos[:g.dn]:
            px, py = x * T, y * T; scr.blit(_dark, (px, py))
            for a, b in ((0, -1), (1, 0), (0, 1), (-1, 0)):         # viền sáng chỉ ở cạnh giáp vùng còn sáng
                if 0 <= x + a < W and 0 <= y + b < H and not g.dark(x + a, y + b):
                    scr.fill(rim, (px + (T - 3 if a == 1 else 0), py + (T - 3 if b == 1 else 0), T if b else 3, T if a else 3))
            scr.blit(_wisp, (px + 5 + int(9 * math.sin(tm * .8 + x * 1.7 + y * .9)), py + 5 + int(9 * math.cos(tm * .7 + x * .9 + y * 1.3))))
        if g.dn < W * H:                          # ô tiếp theo bị bóng tối nuốt dần (mờ dần)
            x, y = g.dpos[g.dn]; _dark.set_alpha(int(255 * g.dprog)); scr.blit(_dark, (x * T, y * T)); _dark.set_alpha(255)
    scr.blit(_vig, (0, 0))
    if playing and g.paused and not g.over:
        ov = pygame.Surface((MW, SH), pygame.SRCALPHA); ov.fill((10, 8, 18, 160)); scr.blit(ov, (0, 0))
        ctxt('TẠM DỪNG', MW // 2, SH // 2 - 12, FT, GOLD, True); ctxt('Nhấn Space để tiếp tục', MW // 2, SH // 2 + 26, F, MUTE)


# ---- thẻ thông tin bên phải: mỗi mục là (chiều cao, hàm vẽ)
def it_label(s): return (19, lambda x, y: txt(s, x, y, FS, MUTE))
def it_para(s, f=F, col=MUTE):
    lines = wrap(s, f, CW); lh = f.get_height() + 2
    return (lh * len(lines) + 4, lambda x, y: [txt(ln, x, y + i * lh, f, col) for i, ln in enumerate(lines)])
def it_head(sub, k, l, v, col=MUTE):
    def fn(x, y):
        txt(sub, x, y, FS, col); scr.blit(icon(k, l, v), (x, y + 20))
        txt(K[k][l]['n'], x + 46, y + 19, FB); txt(f'Cấp {l+1}', x + 46, y + 40, FS, MUTE)
    return (60, fn)
def it_dark():
    def fn(x, y):
        txt('Khu vực này:', x, y, FS, MUTE); rr((x, y + 20, 36, 36), (14, 10, 24), 7); rr((x, y + 20, 36, 36), (110, 60, 170), 7, 2)
        txt('Bóng tối', x + 46, y + 19, FB); txt('Cấp 1', x + 46, y + 40, FS, MUTE)
    return (60, fn)
def it_row(label, vals, **kw):
    def fn(x, y):
        txt(label, x, y + 1, FS, MUTE)
        if any(vals): chips(x + 62, y + 2, vals, **kw)
        else: txt('Miễn phí', x + 62, y + 1, FS, GREEN)
    return (25, fn)
def card(x, y, w, items, accent=None):
    h = 20 + sum(i[0] for i in items)
    rr((x, y, w, h), CARD, 12); rr((x, y, w, h), accent or LINE, 12, 2 if accent else 1)
    cy = y + 10
    for ih, fn in items: fn(x + 12, cy); cy += ih
    return y + h + 8


def draw_side():
    scr.blit(vgrad(PW, SH, (34, 31, 47), (22, 20, 31)), (MW, 0)); pygame.draw.line(scr, (86, 72, 44), (MW, 0), (MW, SH), 2)
    if g.state == 'menu':
        y = txt('Chặn Bóng Tối', X0, 18, FT, GOLD, True)
        y = para('Game chiến lược nâng cấp ô đất, lấy cảm hứng từ Stop the Darkness.', X0, y + 2, CWD, FS, MUTE)
        y = txt('Chọn chế độ', X0, y + 12, FH, INK)
        for key, name, desc in (('std', 'Tiêu chuẩn', 'Ngắn gọn, không quá khó.'), ('ext', 'Mở rộng', 'Nhanh hơn, có Rừng rễ cây.')):
            rc = pygame.Rect(X0, y + 4, CWD, 66)
            button('', rc, lambda k=key: (setattr(g, 'mode', k), g.gen()), g.mode == key)
            txt(name, rc.x + 16, rc.y + 8, FB, GOLD if g.mode == key else INK); txt(desc, rc.x + 16, rc.y + 36, FS, MUTE); y += 76
        para('Space: tạm dừng  ·  J: nhật ký  ·  Esc: về menu', X0, SH - 208, CWD, FS, MUTE)
        button('Chơi!', (X0, SH - 170, CWD, 48), g.start, kind='p')
        button('Tạo lại bản đồ', (X0, SH - 114, CWD, 40), g.gen)
        button('Nhật ký khu vực', (X0, SH - 62, CWD, 40), lambda: setattr(g, 'jopen', True))
        return
    # tài nguyên
    hw = CWD // 2 - 4
    for i in range(4):
        x, y = X0 + (i % 2) * (hw + 8), 12 + (i // 2) * 46
        rr((x, y, hw, 40), CARD, 10); rr((x, y, hw, 40), LINE, 10, 1); gem(x + 17, y + 20, i, 9)
        txt(fmt(g.res[i]), x + 33, y + 8, FB)
        sf = FS.render('+' + fmt(g.rate[i]), True, GREEN if g.rate[i] else MUTE); scr.blit(sf, (x + hw - 9 - sf.get_width(), y + 12))
    # thanh bóng tối
    tot = W * H; fr = min(1.0, (g.dn + g.dprog) / tot)
    txt('Bóng tối', X0, 104, FS, MUTE); sf = FS.render(f'{g.dn}/{tot} ô', True, MUTE); scr.blit(sf, (X0 + CWD - sf.get_width(), 104))
    rr((X0, 125, CWD, 8), (12, 10, 20), 4)
    if fr > 0: rr((X0, 125, max(8, int(CWD * fr)), 8), (150, 84, 224), 4)
    # thông tin ô đang trỏ
    y = 146; t = g.hov
    if t and g.dark(t.x, t.y):
        card(X0, y, CWD, [it_dark()])
    elif t:
        d = K[t.k][t.l]; items = [it_head('Khu vực này:', t.k, t.l, t.v)]
        if d.get('t'): items.append(it_para(d['t'], FS))
        pr = [d['p'][i] * g.mult(t, i) if t.built else 0 for i in range(4)]
        if any(pr): items.append(it_row('Mỗi phút', pr, good=True))
        if t.built and any(d['b']): items.append(it_row('Ô kề', d['b'], pct=True))
        y = card(X0, y, CWD, items)
        u = g.up(t)
        if u and u[2]: card(X0, y, CWD, [it_label('Gợi ý mở khóa:'), it_para(u[2], F, INK)], GOLD)
        elif u:
            k2, l2, _ = u; n = K[k2][l2]; cc = g.cost(n, k2, l2); ok = all(g.res[i] >= cc[i] for i in range(4))
            items = [it_head('Nhấn để nâng cấp thành:' if ok else 'Nâng cấp tiếp theo:', k2, l2, t.v, GREEN if ok else MUTE)]
            if n.get('t'): items.append(it_para(n['t'], FS))
            items.append(it_row('Chi phí', cc, afford=True))
            if any(n['p']): items.append(it_row('Mỗi phút', n['p'], good=True))
            if any(n['b']): items.append(it_row('Ô kề', n['b'], pct=True))
            card(X0, y, CWD, items, GREEN if ok else None)
        else: card(X0, y, CWD, [it_para('Đã đạt cấp tối đa.', FS)])
    else: card(X0, y, CWD, [it_para('Di chuột vào một ô để xem thông tin. Nhấn để nâng cấp.', F)])
    # nút điều khiển
    by = SH - 90
    button('', (X0, by, 44, 36), lambda: setattr(g, 'paused', not g.paused), icon='play' if g.paused else 'pause')
    button(f'{g.speed}x', (X0 + 50, by, 76, 36), lambda: setattr(g, 'speed', {1: 2, 2: 4, 4: 1}[g.speed]), icon='ff')
    button('Nhật ký', (X0 + 132, by, 126, 36), lambda: setattr(g, 'jopen', True))
    button('', (X0 + 264, by, 38, 36), g.to_menu, icon='close')
    by = SH - 46; bw = (CWD - 12) // 3
    button('Nhạc', (X0, by, bw, 34), lambda: setattr(g, 'music', not g.music), dot=g.music)
    button('Âm', (X0 + bw + 6, by, bw, 34), lambda: setattr(g, 'sound', not g.sound), dot=g.sound)
    button('Sáng', (X0 + 2 * (bw + 6), by, bw, 34), toggle_hl, dot=g.hl)


def toggle_hl():
    g.hl = not g.hl; g.hl_next = 0
    g.say('Làm nổi bật ô có thể nâng cấp: ' + ('Bật' if g.hl else 'Tắt'), t=3)


def draw_msg():
    if not g.msg: return
    lines = wrap(g.msg, F, MW - 56); lh = F.get_height() + 2
    h = 28 + lh * len(lines) + (48 if g.msg_btns else 0)
    rc = pygame.Rect(12, SH - h - 12, MW - 24, h)
    rr(rc.move(0, 4), (0, 0, 0, 110), 14); rr(rc, (24, 22, 34, 238), 14); rr(rc, GOLD, 14, 2)
    y = rc.y + 14
    for ln in lines: y = txt(ln, rc.x + 16, y, F, INK)
    for i, (lab, cb) in enumerate(g.msg_btns): button(lab, (rc.x + 16 + i * 128, y + 8, 118, 34), cb, kind='p' if i == len(g.msg_btns) - 1 else 'n')


def draw_journal():
    scr.blit(vgrad(SW, SH, (28, 26, 40), (16, 15, 23)), (0, 0))
    txt(f'Nhật ký khu vực ({len(g.jset)}/{sum(len(K[k]) for _, ks in pages() for k in ks)})', 20, 12, FT, GOLD, True)
    txt('Nhật ký ghi lại các khu vực và nâng cấp bạn đã tìm thấy.', 20, 54, FS, MUTE)
    title, ks = pages()[g.jpage]; txt(title, 20, 78, FH, INK)
    items = [(k, l) for k in ks for l in range(len(K[k]))]
    for i, (k, l) in enumerate(items):
        col, row = i // 8, i % 8; x, y = 20 + col * 270, 108 + row * 56
        rr((x, y, 256, 50), CARD, 10); rr((x, y, 256, 50), LINE, 10, 1)
        if (k, l) in g.jset:
            scr.blit(icon(k, l, 7, 4), (x + 7, y + 7)); txt(K[k][l]['n'], x + 52, y + 5, F); txt(f'Cấp {l+1}', x + 52, y + 26, FS, MUTE)
        else:
            rr((x + 7, y + 7, 36, 36), (18, 16, 27), 7); ctxt('?', x + 25, y + 25, FH, MUTE); txt('???', x + 52, y + 14, F, MUTE)
    pygame.draw.rect(scr, (24, 22, 33), (0, SH - 52, SW, 52)); pygame.draw.line(scr, LINE, (0, SH - 52), (SW, SH - 52))
    button('<', (12, SH - 44, 40, 36), lambda: setattr(g, 'jpage', max(0, g.jpage - 1)))
    button('>', (58, SH - 44, 40, 36), lambda: setattr(g, 'jpage', min(len(PAGES) - 1, g.jpage + 1)))
    txt(f'Trang {g.jpage+1}/{len(PAGES)} - {title}', 114, SH - 36, F, MUTE)
    button('', (SW - 56, SH - 44, 44, 36), lambda: setattr(g, 'jopen', False), icon='close')


def tile_at(pos):
    x, y = pos[0] // T, pos[1] // T
    return g.G[y][x] if 0 <= x < W and 0 <= y < H and pos[0] < MW else None


def main():
    clock = pygame.time.Clock(); mt = 0
    while True:
        dt = clock.tick(60) / 1000
        mt -= dt
        if mt <= 0:
            mt = random.uniform(.5, 1.4)
            if g.music and g.state == 'play' and not g.paused and not g.over: play(random.choice((262, 294, 330, 392, 440, 523, 588)), 1.6, .10, 2.0)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and g.state == 'play': g.paused = not g.paused
                elif e.key == pygame.K_j: g.jopen = not g.jopen
                elif e.key == pygame.K_ESCAPE:
                    if g.jopen: g.jopen = False
                    elif g.state == 'play': g.to_menu()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                hit = next((cb for rc, cb in reversed(buttons) if rc.collidepoint(e.pos)), None)
                if hit: hit(); continue
                if not g.jopen:
                    t = tile_at(e.pos)
                    if t: g.click(t)
        g.hov = tile_at(pygame.mouse.get_pos())  # đọc vị trí chuột trực tiếp mỗi khung hình, tránh độ trễ của hàng đợi sự kiện
        g.tick(dt); buttons.clear()
        draw_map(); draw_side(); draw_msg()
        if g.jopen: buttons.clear(); draw_journal()
        pygame.display.flip()


if __name__ == '__main__':
    main()
