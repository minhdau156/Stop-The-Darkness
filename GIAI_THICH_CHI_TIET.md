# Giải thích CHI TIẾT code: Chặn Bóng Tối

Tài liệu này giải thích từng dòng/khối logic quan trọng của `StopTheDarknessFake.py`
(bản gốc) / `StopTheDarkness_GiaiThich.py` (bản đã chú thích). Đọc cùng với
`GIAI_THICH.md` (tổng quan) và `CHUC_NANG.md` (tính năng giao diện) để có bức
tranh đầy đủ.

---

## Mục lục

1. [Hằng số toàn cục](#1-hằng-số-toàn-cục)
2. [Âm thanh tự sinh](#2-âm-thanh-tự-sinh)
3. [Hàm `L()` và cấu trúc một "cấp nâng cấp"](#3-hàm-l-và-cấu-trúc-một-cấp-nâng-cấp)
4. [Toàn bộ cây công nghệ `K` (chi tiết từng công trình)](#4-toàn-bộ-cây-công-nghệ-k)
5. [`NEXT`, `VFAM`, `PAGES`](#5-next-vfam-pages)
6. [`spiral()` — thuật toán Bóng Tối lan](#6-spiral--thuật-toán-bóng-tối-lan)
7. [`pages()`](#7-pages)
8. [Vẽ pixel-art: `draw_tile()`, `icon()`](#8-vẽ-pixel-art-draw_tile-icon)
9. [`class Tile`](#9-class-tile)
10. [`class Game` — từng phương thức](#10-class-game--từng-phương-thức)
11. [Lớp giao diện (hàm vẽ, nút bấm)](#11-lớp-giao-diện-hàm-vẽ-nút-bấm)
12. [`main()` — vòng lặp sự kiện](#12-main--vòng-lặp-sự-kiện)
13. [Những điểm dễ nhầm / quirk trong code](#13-những-điểm-dễ-nhầm--quirk-trong-code)

---

## 1. Hằng số toàn cục

```python
W, H, T, U = 15, 12, 54, 6
MW, PW = W * T, 300
SW, SH = MW + PW, H * T
```

| Tên | Giá trị | Ý nghĩa |
|---|---|---|
| `W` | 15 | Số cột của lưới bản đồ |
| `H` | 12 | Số hàng của lưới bản đồ |
| `T` | 54 | Kích thước 1 ô bản đồ, tính bằng pixel thật trên màn hình |
| `U` | 6 | Hệ số phóng to khi vẽ chi tiết pixel-art bên trong 1 ô (lưới ảo 9×9 pixel × 6 = 54px, khớp với `T`) |
| `MW` | 15×54 = 810 | Chiều rộng vùng bản đồ (pixel) |
| `PW` | 300 | Chiều rộng bảng thông tin bên phải (panel) |
| `SW` | 810+300 = 1110 | Chiều rộng toàn cửa sổ |
| `SH` | 12×54 = 648 | Chiều cao toàn cửa sổ |

```python
C = pygame.Color
BG, PN, LN, INK = C('#e9e6dc'), C('#d6d3c6'), C('#9a968a'), C('#2b2a26')
RC = [C('#8a5a2b'), C('#8d8d94'), C('#9b59d6'), C('#c8d92b')]
RN = ['Gỗ', 'Đá', 'Phép thuật', 'Khoa học']
RED = C('#c62828')
```

- `BG/PN/LN/INK` — các màu nền/panel/viền/chữ dùng xuyên suốt giao diện.
- `RC` — **bảng màu đại diện cho 4 tài nguyên**, luôn theo đúng thứ tự cố định:
  chỉ số `0 = Gỗ`, `1 = Đá`, `2 = Phép thuật`, `3 = Khoa học`. Thứ tự này
  được dùng xuyên suốt toàn bộ code (mọi tuple `cost`/`prod`/`boost`/`res`/`rate`
  đều có 4 phần tử theo đúng thứ tự này).
- `RN` — tên hiển thị tương ứng (không được dùng trực tiếp nhiều trong code hiện tại,
  nhưng giữ để tham chiếu/mở rộng).

---

## 2. Âm thanh tự sinh

```python
import array
try:
    pygame.mixer.init(); AUDIO = pygame.mixer.get_init() is not None
except Exception:
    AUDIO = False
```

Khởi tạo hệ thống âm thanh của pygame. Nếu máy không có thiết bị âm thanh hoặc
lỗi driver, `AUDIO = False` và toàn bộ hàm phát âm thanh sẽ im lặng bỏ qua
(không crash game).

```python
_snd = {}
def play(f, dur=.12, vol=.25, decay=4.0):
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
```

Đây là một **synth sóng sin đơn giản**, không cần file `.wav`/`.mp3`:

1. `fr` = tần số lấy mẫu của thiết bị âm thanh (ví dụ 44100 Hz); `n` = tổng số
   mẫu cần tạo = `fr * dur` (số mẫu cho `dur` giây âm thanh).
2. Với mỗi mẫu `i` (từ 0 đến n-1):
   - `math.sin(2π f i / fr)` — giá trị sóng sin tần số `f` Hz tại thời điểm `i`.
   - `math.exp(-decay * i / n)` — **đường bao giảm dần** (envelope decay): bắt đầu
     ở 1.0 và giảm dần về gần 0 theo cấp số mũ, tạo cảm giác nốt nhạc "tắt dần"
     tự nhiên thay vì cắt cụt đột ngột. `decay` càng lớn thì tắt càng nhanh.
   - `32767` = giá trị tối đa của số nguyên 16-bit có dấu (giới hạn biên độ âm thanh).
   - `vol` = hệ số âm lượng tổng thể (0–1).
3. `array.array('h')` — mảng số nguyên 16-bit (định dạng mẫu âm thanh PCM chuẩn).
   `a.extend([v] * ch)` lặp lại giá trị cho đủ số kênh (`ch`, thường là 2 = stereo).
4. Kết quả được bọc thành `pygame.mixer.Sound` và phát ngay (`.play()`).
5. **Cache** (`_snd` dict theo khóa `(f, dur, vol, decay)`): âm thanh với cùng
   tham số chỉ cần tính toán sóng sin **một lần**, các lần phát sau chỉ cần
   gọi lại `.play()` trên Sound đã tạo — tránh tính toán lại tốn CPU.

```python
def sfx(name):
    if not g.sound: return
    if name == 'up': play(660, .1); play(990, .14, .15)
    elif name == 'no': play(140, .18, .3, 6)
    elif name == 'win': [play(f, .9, .2, 2) for f in (523, 659, 784, 1047)]
    elif name == 'lose': play(110, 1.2, .35, 2)
```

Ánh xạ "tên sự kiện" sang các nốt nhạc cụ thể:
- `'up'` (nâng cấp thành công): 2 nốt cao liên tiếp (660Hz rồi 990Hz) — cảm giác "ting!".
- `'no'` (không đủ tài nguyên): 1 nốt trầm, tắt nhanh (decay=6) — cảm giác "bụp" cảnh báo.
- `'win'`: hợp âm 4 nốt (Đô-Mi-Sol-Đô cao, gần giống hợp âm Đô trưởng ở quãng 523-1047Hz) phát cùng lúc.
- `'lose'`: 1 nốt rất trầm (110Hz), kéo dài 1.2 giây — cảm giác u ám.

`g.sound` là cờ bật/tắt hiệu ứng âm thanh do người chơi điều khiển qua nút "Âm".

---

## 3. Hàm `L()` và cấu trúc một "cấp nâng cấp"

```python
def L(name, cost=(), prod=(), boost=(), **kw):
    p4 = lambda a: tuple(a) + (0,) * (4 - len(a))
    return dict(n=name, c=p4(cost), p=p4(prod), b=p4(boost), **kw)
```

- `p4(a)` — hàm đệm thêm số 0 vào cuối tuple `a` cho đủ **đúng 4 phần tử**
  (vì luôn có 4 loại tài nguyên). Ví dụ `p4((3,))` → `(3, 0, 0, 0)`;
  `p4((0, 3))` → `(0, 3, 0, 0)`. Nhờ vậy khi khai báo dữ liệu, người viết
  chỉ cần ghi "tắt" các giá trị khác 0 đầu tiên, không cần ghi đủ 4 số 0.
- Kết quả trả về là 1 dict có các khóa:
  - `n` — tên hiển thị.
  - `c` — chi phí xây/nâng cấp (tuple 4 phần tử: Gỗ, Đá, Phép thuật, Khoa học).
  - `p` — sản lượng mỗi phút khi đã xây (cùng thứ tự 4 tài nguyên).
  - `b` — % tăng sản lượng (boost) mà ô này cộng thêm cho **ô kề cạnh đã xây**
    (cùng thứ tự 4 tài nguyên, ví dụ `0.25` nghĩa là +25%).
  - Các khóa khác truyền qua `**kw` (tùy chọn, không phải cấp nào cũng có):
    - `t` (text) — chuỗi mô tả/gợi ý hiển thị cho người chơi.
    - `push` — số nguyên/thực: khi xây xong, đẩy lùi Bóng Tối (giảm `s.dn`
      đi `12 * push` ô — xem `Game.click`).
    - `win` — `1` hoặc `2`: đạt cấp này có thể kích hoạt thắng ván chơi
      (xem phần [13](#13-những-điểm-dễ-nhầm--quirk-trong-code) để biết sự khác biệt 1 và 2).
    - `light` — số nguyên: cộng dồn vào `s.light` (tổng "ánh sáng" toàn bản đồ),
      làm **chậm** chu kỳ lan của Bóng Tối (xem `Game.tick`).

---

## 4. Toàn bộ cây công nghệ `K`

`K` là một `dict`: khóa = **loại ô** (kind, ví dụ `'forest'`), giá trị = **danh sách
các cấp theo thứ tự tăng dần** (mỗi phần tử là 1 dict do `L()` tạo ra). Cấp hiện
tại của một ô được lưu trong `Tile.l` (chỉ số 0-based: `l=0` là cấp đầu tiên đã xây).

Dưới đây là toàn bộ dữ liệu, diễn giải sang đơn vị tài nguyên cụ thể
(thứ tự luôn là **Gỗ / Đá / Phép thuật / Khoa học**, bỏ qua giá trị 0):

### `field` — Cánh đồng (ô trống, điểm khởi đầu)
| Cấp | Chi phí | Sản lượng | Boost ô kề | Ghi chú |
|---|---|---|---|---|
| 0 | — | — | — | Ô hoang sơ, là điểm bắt đầu để nâng thành Làng/Cảng/Khai mỏ/Phép thuật/Tháp (xem `Game.up`) |

### `water` — Nước
| Cấp | Chi phí | Sản lượng | Boost | Ghi chú |
|---|---|---|---|---|
| 0 | — | — | — | Ô nước hoang sơ, nâng thành Bến tàu hoặc Hải đăng |

### `forest` — Rừng
| Cấp | Chi phí | Sản lượng | Boost ô kề |
|---|---|---|---|
| 0 | — | Gỗ 3 | +25% Gỗ |
| 1 | Gỗ 3 | Gỗ 4.5 | +25% Gỗ |
| 2 | Gỗ 7 | Gỗ 8.7 | +25% Gỗ |
| 3 | Gỗ 15 | Gỗ 22.5 | +25% Gỗ |

Ở cấp 3: nếu kề Rừng rễ cây cấp 3 → mở khóa **Nhà máy thuốc** (chỉ ext).
Ở cấp 0, nếu cả 4 ô kề đều là Rừng → mở khóa **Làng trên cây**.

### `treetop` — Làng trên cây
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 15 | Gỗ 10, Phép thuật 1 | +50% Gỗ |
| 1 | Gỗ 30, Phép thuật 5 | Gỗ 22.5, Phép thuật 2 | +100% Gỗ |
| 2 | Gỗ 100, Đá 20, Phép thuật 20 | Gỗ 40, Phép thuật 5 | +100% Gỗ |

### `rocks` — Đá
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | — | Đá 3 | — |
| 1 | Gỗ 8 | Đá 3 | — |
| 2 | Gỗ 10, Đá 3 | Đá 7 | — |
| 3 | Gỗ 15, Đá 12, Khoa học 2 | Đá 30 | +25% Đá |
| 4 | Gỗ 10, Đá 60, Khoa học 8 | Đá 60, Khoa học 4 | +33% Đá | *"Cần có Trung tâm công nghệ đá."* |

Ở cấp 3: nếu kề một Thành phố (`city/portcity/magiccity/miningres`) và chưa có
Trung tâm công nghệ đá nào → mở khóa.

### `stonetech` — Trung tâm công nghệ đá (độc nhất về giá — không bị tăng giá theo số lượng)
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 200, Đá 100, Khoa học 50 | Đá 100, Khoa học 8.7 | +50% Đá, +25% Khoa học |
| 1 | Gỗ 400, Đá 200, Khoa học 200 | Đá 75, Khoa học 15 | +50% Đá, +50% Khoa học |

Hiệu ứng đặc biệt (xem `Game.recalc`): mỗi Trung tâm công nghệ đá đã xây sẽ
cộng thêm sản lượng Đá cho **toàn bộ** ô Đá trên bản đồ, tỉ lệ theo % sản
lượng Khoa học hiện tại (`techpct = 0.01 * tổng_khoa_học * số_trung_tâm`).

### `mushroom` — Rừng nấm
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | — | Gỗ 1.2, Phép thuật 2 | +25% Phép thuật |
| 1 | Gỗ 6 | Gỗ 1.2, Phép thuật 2 | +25% Phép thuật |
| 2 | Gỗ 20, Phép thuật 2 | Gỗ 3.5, Phép thuật 7 | +25% Phép thuật |

→ tiến hóa thành **Thành phố nấm** (`mushcity`).

### `mushcity` — Thành phố nấm
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 50, Phép thuật 30, Khoa học 5 | Gỗ 10, Phép thuật 20, Khoa học 2 | +50% Phép thuật, +25% Khoa học |

### `roots` — Rừng rễ cây (chỉ chế độ Mở rộng)
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | — | Gỗ 2, Phép thuật 3 | +25% Gỗ, +25% Phép thuật |
| 1 | Gỗ 10 | Gỗ 2, Phép thuật 3 | +25% Gỗ, +25% Phép thuật |
| 2 | Gỗ 25, Phép thuật 5 | Gỗ 8, Phép thuật 12 | +25% Gỗ, +25% Phép thuật |
| 3 | Gỗ 60, Phép thuật 15 | Gỗ 20, Phép thuật 24 | +25% Gỗ, +25% Phép thuật |

→ tiến hóa thành **Thành phố rễ cây** (`rootscity`).

### `rootscity` — Thành phố rễ cây
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 100, Phép thuật 60, Khoa học 10 | Gỗ 20, Phép thuật 40, Khoa học 3 | +25% Gỗ, +50% Khoa học |

### `circle` — Vòng Đá (công trình phòng thủ trung tâm, độc nhất về giá)
| Cấp | Chi phí | Cờ đặc biệt |
|---|---|---|
| 0 | (đặt sẵn khi sinh bản đồ) | — |
| 1 | Đá 100, Phép thuật 100 | `push=1` — đẩy lùi Bóng Tối |
| 2 | Gỗ 100, Đá 300, Phép thuật 300, Khoa học 20 | `push=1` |
| 3 | Gỗ 1000, Đá 1500, Phép thuật 1000 | `win=2` — **THẮNG** (mọi chế độ) |

Lưu ý: cấp 0 → 1 bị khóa cho tới khi có một Làng phép thuật đạt cấp ≥ 2 ở
bất kỳ đâu trên bản đồ (không cần kề).

### `village` — Làng
| Cấp | Chi phí | Boost |
|---|---|---|
| 0 | Gỗ 7 | +25% Gỗ, +25% Đá |
| 1 | Gỗ 12, Đá 12 | +50% Gỗ, +50% Đá |

→ tiến hóa thành **Thành phố** (`city`).

### `city` — Thành phố
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 15, Đá 60, Khoa học 10 | Khoa học 2.5 | +50% Gỗ, +50% Đá |
| 1 | Gỗ 40, Đá 150, Khoa học 30 | Khoa học 6.2 | +50% Gỗ, +50% Đá, +25% Khoa học |

### `port` — Làng cảng
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 5 | Gỗ 2 | +25% Gỗ, +25% Đá |
| 1 | Gỗ 45, Đá 18 | Gỗ 6 | +50% Gỗ, +50% Đá |

→ tiến hóa thành **Thành phố cảng** (`portcity`).

### `portcity` — Thành phố cảng
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 120, Đá 60, Khoa học 10 | Gỗ 12, Đá 6, Khoa học 2.5 | +50% Gỗ, +50% Đá |
| 1 | Gỗ 300, Đá 150, Khoa học 40 | Gỗ 25, Đá 12, Khoa học 6 | +50% Gỗ, +50% Đá, +25% Khoa học |

### `docks` — Bến tàu
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 20, Đá 10 | Gỗ 6 | +25% Gỗ, +25% Đá |

### `lighthouse` — Hải đăng
| Cấp | Chi phí | Sản lượng | Boost | Ghi chú |
|---|---|---|---|---|
| 0 | Gỗ 15, Đá 15 | Khoa học 1 | +25% Gỗ, +25% Đá | *"Dẫn đường cho tàu thuyền."* |

### `magic` — Làng phép thuật
| Cấp | Chi phí | Sản lượng | Boost | Ghi chú |
|---|---|---|---|---|
| 0 | Gỗ 5, Phép thuật 1 | Phép thuật 2 | +25% Gỗ, +25% Phép thuật | *"Xây cạnh một Làng để mở Tháp ánh sáng ở ô kề."* |
| 1 | Gỗ 20, Đá 10, Phép thuật 5 | Phép thuật 5 | +50% Gỗ, +50% Phép thuật | *"Mở khóa nâng cấp Vòng đá."* |

→ tiến hóa thành **Thành phố phép thuật** (`magiccity`).

### `magiccity` — Thành phố phép thuật
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 60, Đá 30, Phép thuật 20, Khoa học 10 | Phép thuật 10, Khoa học 2 | +50% Gỗ, +50% Phép thuật, +25% Khoa học |

### `magicport` — Làng cảng phép thuật
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 7, Phép thuật 1 | Gỗ 2, Phép thuật 2 | +25% Gỗ, +25% Phép thuật |
| 1 | Gỗ 45, Đá 18, Phép thuật 6 | Gỗ 4, Phép thuật 5 | +50% Gỗ, +50% Phép thuật |

→ tiến hóa thành **Thành phố cảng phép thuật** (`magicportcity`).

### `magicportcity` — Thành phố cảng phép thuật
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 120, Đá 60, Phép thuật 20, Khoa học 10 | Gỗ 8, Đá 4, Phép thuật 10, Khoa học 2 | +50% Gỗ, +50% Phép thuật |

### `mining` — Làng khai mỏ
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 10, Đá 5 | Đá 5 | +50% Đá |
| 1 | Gỗ 30, Đá 30 | Đá 12 | +50% Đá |

→ tiến hóa thành **Thành phố nghiên cứu mỏ** (`miningres`).

### `miningres` — Thành phố nghiên cứu mỏ
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 60, Đá 100, Khoa học 10 | Khoa học 3 | +50% Đá, +25% Khoa học |
| 1 | Gỗ 200, Đá 300, Khoa học 30 | Khoa học 6 | +50% Đá, +25% Khoa học |

> Cấp 1 ở đây **gần như không bao giờ được chọn** trong thực tế vì có luật
> đặc biệt khiến cấp 0 nhảy thẳng sang `lightres` — xem mục 13.

### `lightres` — Thành phố nghiên cứu ánh sáng (con đường thắng thứ 2, độc nhất)
| Cấp | Chi phí | Sản lượng | Boost | Cờ |
|---|---|---|---|---|
| 0 | Gỗ 400, Đá 500, Khoa học 100 | Khoa học 8 | +50% Đá, +25% Khoa học | `push=1` |
| 1 | Gỗ 1200, Đá 1200, Khoa học 600 | Khoa học 12 | +50% Đá, +50% Khoa học | `win=2` — **THẮNG** (mọi chế độ) |

### `tower` — Tháp ánh sáng (con đường thắng thứ 3, chỉ thắng ở chế độ Tiêu chuẩn)
| Cấp | Chi phí | Sản lượng | Boost | Cờ |
|---|---|---|---|---|
| 0 | Gỗ 30, Đá 20, Phép thuật 15 | Phép thuật 1.2 | +25% Phép thuật | `light=1` — làm chậm Bóng Tối |
| 1 | Gỗ 200, Đá 100, Phép thuật 100, Khoa học 20 | Phép thuật 6 | +50% Phép thuật | `light=3`, `win=1` — thắng **chỉ ở chế độ `std`** |

### `towerwater` — Tháp nước
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 100, Đá 50, Phép thuật 50, Khoa học 10 | Phép thuật 5, Khoa học 3 | +50% Phép thuật, +25% Khoa học |

### `potion` — Nhà máy thuốc (chỉ chế độ Mở rộng)
| Cấp | Chi phí | Sản lượng | Boost |
|---|---|---|---|
| 0 | Gỗ 80, Đá 40, Phép thuật 40, Khoa học 10 | Phép thuật 5, Khoa học 10 | +50% Khoa học |

---

## 5. `NEXT`, `VFAM`, `PAGES`

```python
NEXT = {'village': 'city', 'port': 'portcity', 'magic': 'magiccity', 'magicport': 'magicportcity',
        'mushroom': 'mushcity', 'roots': 'rootscity', 'mining': 'miningres', 'miningres': 'lightres'}
```
Bản đồ "tiến hóa": khi một ô đã đạt **cấp cao nhất** trong danh sách `K[loại_hiện_tại]`,
nếu loại đó có mặt trong `NEXT`, ô có thể tiếp tục nâng cấp bằng cách **đổi hẳn
sang loại mới** (đặt lại `l=0` của loại mới). Đây là cách các "Làng" trở thành
"Thành phố".

```python
VFAM = {'village', 'port', 'magic', 'magicport', 'mining', 'city', 'portcity',
        'magiccity', 'magicportcity', 'miningres', 'lightres', 'mushcity', 'rootscity'}
```
Tập hợp các loại được tính là **"làng/thành phố"** khi `Game.up()` kiểm tra điều
kiện tiến hóa (xem mục 10.5): cần đủ số ô kề thuộc nhóm này.

```python
PAGES = [('Cơ bản, thành phố và nước', [...]), ('Rừng và gỗ', [...]),
         ('Khai mỏ', [...]), ('Phép thuật', [...]), ('Phép thuật (tiếp)', [...])]
```
Chỉ dùng để **chia trang hiển thị** trong sổ Nhật ký khu vực — không ảnh hưởng
luật chơi.

---

## 6. `spiral()` — thuật toán Bóng Tối lan

```python
def spiral():
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
```

Đây là thuật toán kinh điển "duyệt ma trận theo vòng xoắn ốc", nhưng áp dụng
theo hướng ngược (bắt đầu từ **cạnh dưới**, không phải cạnh trên như hay gặp),
vì luật game yêu cầu Bóng Tối xuất phát từ **góc dưới-trái**.

Biến `(x0, x1, y0, y1)` là khung hình chữ nhật còn lại chưa duyệt (ban đầu là
toàn bộ bản đồ: cột 0..14, hàng 0..11). Mỗi vòng lặp `while`:

1. **Cạnh dưới** của khung (hàng `y1`): đi từ trái (`x0`) sang phải (`x1`).
2. **Cạnh phải** của khung (cột `x1`): đi từ dưới (`y1-1`, vì góc đã đi ở bước 1)
   lên trên (`y0`).
3. **Cạnh trên** (hàng `y0`), chỉ nếu `y0 < y1` (tức khung còn cao hơn 1 hàng,
   tránh duyệt trùng khi khung chỉ còn 1 hàng): đi từ phải (`x1-1`) sang trái (`x0`).
4. **Cạnh trái còn lại** (cột `x0`, chỉ phần giữa, không lặp 2 góc đã đi),
   chỉ nếu `x0 < x1`: đi từ dưới (`y0+1`) lên... thực ra từ `y0+1` đến `y1-1`
   theo chiều tăng — tức từ gần cạnh dưới lên gần cạnh trên.
5. Thu hẹp khung vào trong: `x0+=1, x1-=1, y0+=1, y1-=1` — chuẩn bị vòng xoắn
   kế tiếp, nhỏ hơn 1 lớp ở mỗi phía.

Lặp lại tới khi khung không còn hợp lệ (`x0 > x1` hoặc `y0 > y1`).

Kết quả `order` là danh sách toạ độ `(x, y)` theo **đúng thứ tự bị Bóng Tối nuốt**
(phần tử đầu = ô bị nuốt đầu tiên). `d[y][x]` là ma trận tra cứu ngược: cho biết
"thứ tự" của ô `(x, y)` là bao nhiêu (số càng nhỏ, bị nuốt càng sớm).

Trong `Game`, biến `s.dn` (darkness-number) = **số ô đã bị nuốt tính từ đầu**.
Hàm `Game.dark(x, y)` chỉ đơn giản so sánh: `d[y][x] < s.dn` → ô đó đã "tới lượt".

Minh họa trên lưới nhỏ 4×3 (W=4, H=3), thứ tự nuốt sẽ là:
```
Bước 1 (khung ngoài, y1=2 là hàng dưới cùng):
  cạnh dưới (hàng 2): (0,2)(1,2)(2,2)(3,2)
  cạnh phải (cột 3):  (3,1)(3,0)
  cạnh trên (hàng 0):  (2,0)(1,0)(0,0)
  cạnh trái còn lại (cột 0): (0,1)
Bước 2 (khung thu hẹp còn x0=1,x1=2,y0=1,y1=1 — chỉ còn 1 hàng ở giữa):
  cạnh dưới (hàng 1): (1,1)(2,1)
```
→ tổng thứ tự: `(0,2)(1,2)(2,2)(3,2)(3,1)(3,0)(2,0)(1,0)(0,0)(0,1)(1,1)(2,1)`.
Có thể thấy: xuất phát góc dưới-trái, đi hết vòng ngoài theo chiều ngược kim
đồng hồ, rồi thu vào trong.

---

## 7. `pages()`

```python
def pages():
    ex = () if g.mode == 'ext' else ('roots', 'rootscity', 'potion')
    return [(t, [k for k in ks if k not in ex]) for t, ks in PAGES]
```
Lọc các mục chỉ-dành-cho-chế-độ-Mở-rộng (Rễ cây, Thành phố rễ cây, Nhà máy
thuốc) ra khỏi danh sách trang nếu đang ở chế độ Tiêu chuẩn. Dùng cho cả
hiển thị Nhật ký lẫn đếm "tổng số mục có thể khám phá".

---

## 8. Vẽ pixel-art: `draw_tile()`, `icon()`

Mỗi ô được vẽ trên một **lưới ảo 9×9 "pixel"**, mỗi "pixel ảo" được vẽ thành
1 hình chữ nhật thật có cạnh `u` pixel (hàm nội bộ `r(màu, x, y, w, h)`).
Khi vẽ trên bản đồ chính, `u = U = 6` (và ô thật rộng `T = 54 = 9×6`); khi vẽ
icon nhỏ trong bảng thông tin, `u` khác (ví dụ 4) để icon nhỏ hơn.

```python
def draw_tile(s, k, l, v, ox, oy, u):
    def r(col, x, y, w, h):
        pygame.draw.rect(s, C(col), (ox + int(x*u), oy + int(y*u), max(1, int(w*u)), max(1, int(h*u))))
    ...
```
`(ox, oy)` = góc trên-trái thật của ô trên mặt vẽ `s`. Mọi tọa độ `x, y, w, h`
bên trong các hàm vẽ tiếp theo đều tính theo đơn vị "pixel ảo" (0-9), được
hàm `r()` tự động quy đổi ra pixel thật.

Nền ô được tô theo 3 nhóm màu:
- `wet` (xanh nước nhạt): các loại liên quan tới nước — `water, lighthouse, docks, towerwater`.
- `tan` (nâu be): các loại công trình "đất xây dựng" — làng, thành phố, tháp, vòng đá, nấm, rễ...
- còn lại (xanh cỏ): đất tự nhiên chưa xây (`field, forest, rocks, treetop`).

Sau đó, theo từng `k` cụ thể, code vẽ thêm chi tiết: cây (`tree()`), nhà
(`house()`, có biến thể `tall=True` cho nhà cao tầng của "thành phố"), nấm
(`mush()`), đá, vòng tròn 8 viên đá quanh Vòng Đá, hải đăng, tháp... Số lượng
chi tiết vẽ thường tăng theo cấp `l` (ví dụ Rừng cấp 0 vẽ 6 cây rải rác, cấp
≥1 vẽ 4 cây góc + nhà ở giữa).

```python
_ic = {}
def icon(k, l, v=7, s=4):
    key = (k, l, v, s)
    if key not in _ic:
        sf = pygame.Surface((9*s, 9*s)); draw_tile(sf, k, l, v, 0, 0, s); _ic[key] = sf
    return _ic[key]
```
Cache icon theo khóa `(loại, cấp, giá_trị_ngẫu_nhiên, tỉ_lệ)` — vẽ 1 lần, tái
sử dụng nhiều lần trong bảng thông tin và sổ Nhật ký (tránh vẽ lại pixel-art
mỗi khung hình, dù thực ra chi phí vẽ cũng không quá lớn ở quy mô game này).

---

## 9. `class Tile`

```python
class Tile:
    def __init__(s, k, x, y, v): s.k, s.l, s.x, s.y, s.v, s.built = k, 0, x, y, v, False
```
Trạng thái tối thiểu của 1 ô: loại (`k`), cấp (`l`, luôn khởi tạo 0), tọa độ
`(x, y)`, số ngẫu nhiên cố định `v` (0–59, dùng để chọn họa tiết nền không lặp
y hệt giữa các ô cùng loại), và cờ `built` (đã từng được người chơi bấm xây
hay vẫn là ô hoang sơ mặc định của bản đồ sinh ra).

**Lưu ý quan trọng:** `field` và `water` cũng có `k`/`l` như mọi ô khác, nhưng
`built=False` cho tới khi người chơi nâng cấp chúng lần đầu. Sản lượng/boost
chỉ được tính (`Game.recalc`) cho ô có `built=True`.

---

## 10. `class Game` — từng phương thức

### 10.1 `__init__`
Khởi tạo các cờ trạng thái giao diện/game: chế độ (`mode`), màn hình hiện tại
(`state`: `'menu'`/`'play'`), tốc độ (`speed`), tạm dừng (`paused`), ô đang
trỏ chuột (`hov`), thông báo hiện tại (`msg`/`msg_t`), trang/trạng thái Nhật ký
(`jpage`/`jopen`), các cờ bật/tắt (`music`/`sound`/`hl`), rồi gọi `s.gen()` để
sinh bản đồ đầu tiên.

### 10.2 `gen()` — sinh bản đồ

```python
def gen(s):
    rd = random.Random()
    s.G = [[None]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            r = rd.random()
            k = ('field' if r < .36 else 'forest' if r < .60 else 'rocks' if r < .71
                 else 'water' if r < .84 else 'mushroom' if r < .92 else 'roots')
            if k == 'roots' and s.mode != 'ext': k = 'field'
            a = s.G[y][x-1] if x else None; b = s.G[y-1][x] if y else None
            if a and a.k in ('forest','rocks','water','field') and rd.random() < .38: k = a.k
            elif b and b.k in ('forest','rocks','water','field') and rd.random() < .3: k = b.k
            s.G[y][x] = Tile(k, x, y, rd.randrange(60))
    s.G[rd.randrange(4, 8)][rd.randrange(5, 10)].k = 'circle'
    ...
```

**Bước 1 — chọn loại đất cơ bản theo xác suất tích lũy** (mỗi ô độc lập ban đầu):

| Khoảng `r` | Loại | Xác suất riêng |
|---|---|---|
| `[0, .36)` | Cánh đồng | 36% |
| `[.36, .60)` | Rừng | 24% |
| `[.60, .71)` | Đá | 11% |
| `[.71, .84)` | Nước | 13% |
| `[.84, .92)` | Rừng nấm | 8% |
| `[.92, 1)` | Rễ cây | 8% |

Nếu ra "Rễ cây" nhưng đang ở chế độ Tiêu chuẩn (`std`) → đổi lại thành Cánh
đồng (vì Rễ cây chỉ tồn tại ở chế độ Mở rộng).

**Bước 2 — "lan cụm"**: để bản đồ không bị lổn nhổn như nhiễu ngẫu nhiên, mỗi
ô có 38% cơ hội **sao chép loại đất của ô bên trái** (nếu ô đó là 1 trong 4
loại "đất nền": field/forest/rocks/water — không sao chép nấm/rễ cây), và nếu
không sao chép trái thì có 30% cơ hội sao chép loại đất của **ô bên trên**.
Kết quả: các mảng Rừng/Đá/Nước/Cánh đồng có xu hướng tạo thành cụm liền kề
tự nhiên hơn, thay vì xen kẽ hỗn loạn.

**Bước 3 — đặt Vòng Đá**: chọn ngẫu nhiên 1 ô trong vùng `x ∈ [5,9]`, `y ∈ [4,7]`
(khu vực gần giữa bản đồ — tránh đặt ở rìa, vì rìa dưới-trái sẽ bị Bóng Tối
nuốt sớm nhất) và ép loại ô đó thành `'circle'` (đè lên loại đất ngẫu nhiên
đã sinh trước đó).

**Bước 4 — khởi tạo trạng thái ván chơi**: tài nguyên ban đầu `res = [10, 0, 0, 0]`
(chỉ có sẵn 10 Gỗ), `dn = 0` (chưa ô nào bị nuốt), tính lại thứ tự xoắn ốc
(`spiral()`), reset bộ đếm thời gian, cờ thắng/thua, và `jset` (tập hợp các
mục đã khám phá cho Nhật ký — mặc định đã biết Cánh đồng và Nước cấp 0, cộng
tất cả loại đất tự nhiên vừa sinh ra trên bản đồ ở cấp 0 của chúng).

### 10.3 `dark(x, y)`, `nb(t)`, `exists(k)`

```python
def dark(s, x, y): return s.dord[y][x] < s.dn
```
So sánh thứ tự xoắn ốc của ô với số ô đã bị nuốt — xem mục 6.

```python
def nb(s, t):
    return [s.G[t.y+b][t.x+a] for a, b in ((0,-1),(1,0),(0,1),(-1,0))
            if 0 <= t.x+a < W and 0 <= t.y+b < H and not s.dark(t.x+a, t.y+b)]
```
Trả về danh sách tối đa 4 ô kề (trên, phải, dưới, trái — **không tính đường
chéo**), đã lọc bỏ:
- Ô nằm ngoài biên bản đồ.
- Ô đã bị Bóng Tối nuốt (ô tối không được tính là "ô kề" cho bất kỳ mục đích
  nào — cả tính sản lượng/boost lẫn điều kiện mở khóa nâng cấp).

Đây là hàm được gọi **rất nhiều lần mỗi khung hình** (trong `up`, `mult`,
`recalc`, `hl_tiles`...) — toàn bộ luật game "phụ thuộc hàng xóm" đều dựa vào
danh sách này.

```python
def exists(s, k): return any(t.k == k for row in s.G for t in row)
```
Kiểm tra "đã từng xây loại `k` này ở bất kỳ đâu trên bản đồ chưa" — dùng cho
các công trình **độc nhất** (chỉ xây được 1 cái, như `stonetech`, `towerwater`,
`tower`, `lightres`...), hoặc điều kiện toàn cục (như Vòng Đá cần có Làng phép
thuật cấp 2 "ở bất kỳ đâu", không nhất thiết kề cạnh).

### 10.4–10.5 `up(t)` — chi tiết từng nhánh luật

Đây là hàm trung tâm, trả về `(loại_mới, cấp_mới, văn_bản_khóa)` hoặc `None`
(đã đạt cấp tối đa, không còn gì để nâng). Thứ tự kiểm tra **có ý nghĩa** —
nhánh nào đứng trước được ưu tiên trước:

**(a) Vòng Đá cấp 0:**
```python
if k == 'circle' and l == 0 and not any(q.k=='magic' and q.l>=1 and q.built for row in s.G for q in row):
    return ('circle', 1, 'Dùng phép thuật. (...)')
```
Nếu CHƯA có Làng phép thuật nào đã xây tới cấp ≥ 1 (tức cấp hiển thị "Cấp 2")
ở bất kỳ đâu trên bản đồ → trả về nâng cấp nhưng **kèm khóa** (văn bản khác
`None`), nghĩa là hiển thị cho người chơi biết sắp có gì nhưng chưa cho xây.
Nếu điều kiện đã thỏa, code **rơi xuống các nhánh dưới** — cụ thể ô `circle`
không khớp bất kỳ nhánh đặc biệt nào khác nên sẽ rơi vào nhánh chung
`if l + 1 < len(K[k])` ở cuối hàm, trả về `('circle', 1, None)` (không khóa).

**(b) Cánh đồng (`field`, luôn ở cấp 0):** như đã liệt kê ở
`GIAI_THICH.md`, theo đúng **thứ tự ưu tiên trong code**:
1. Kề Làng phép thuật đã xây + CHƯA tồn tại Tháp ánh sáng nào →
   - Nếu trong số các Làng phép thuật kề đó, có ít nhất 1 cái mà **bản thân nó**
     cũng kề 1 Làng/Thành phố đã xây VÀ đã đạt cấp ≥ 1 → mở khóa **Tháp ánh sáng** (không khóa).
   - Nếu có Làng phép thuật kề 1 Làng/Thành phố nhưng **chưa** đạt cấp ≥ 1 →
     vẫn trả về `('tower', 0, ...)` nhưng kèm khóa "Nâng cấp làng phép thuật
     lên cấp 2 trước."
   - Nếu không có Làng phép thuật nào thỏa điều kiện trên → rơi xuống bước 2.
2. Nếu kề 1 ô Phép-thuật-họ (`magic/magiccity/magicport/magicportcity`) đã
   xây VÀ kề Nước VÀ chưa tồn tại Tháp nước → mở khóa **Tháp nước**.
3. Đếm số ô kề là Rừng nấm (`mu`) và số ô kề là Nước (`wat`):
   - `mu>0 and wat>0` → **Làng cảng phép thuật**.
   - `mu>0` (chỉ nấm) → **Làng phép thuật**.
   - Đếm số ô kề là Đá ≥ 2 → **Làng khai mỏ**.
   - `wat>0` (chỉ nước) → **Làng cảng**.
   - Không rơi vào trường hợp nào → **Làng** thường (mặc định).

**(c) Rừng đặc biệt:**
```python
if k=='forest' and l==3 and not s.exists('potion') and any(q.k=='roots' and q.l==3 for q in n):
    return ('potion', 0, None)
if k=='forest' and l==0 and cnt('forest')==4 and not cnt('treetop'):
    return ('treetop', 0, None)
```
Rừng cấp 3 kề 1 ô Rễ cây cấp 3 (và chưa có Nhà máy thuốc nào) → Nhà máy thuốc.
Rừng cấp 0 mà **cả 4** ô kề đều là Rừng (bất kể cấp) và chưa có Làng trên cây
nào → Làng trên cây.

**(d) Đá đặc biệt:**
```python
if k=='rocks' and l==3 and not s.exists('stonetech'):
    ok = cnt('city','portcity','magiccity','miningres')
    return ('stonetech', 0, None if ok else 'Cần một Thành phố kề bên...')
```
Đá cấp 3 (cấp 4 hiển thị), chưa có Trung tâm công nghệ đá → mở khóa nếu kề
1 trong 4 loại Thành phố liệt kê, ngược lại hiện khóa nhắc nhở.

**(e) Nước:**
```python
if k == 'water': return ('docks', 0, None) if cnt('port','portcity') else ('lighthouse', 0, None)
```
Không có điều kiện khóa — luôn cho nâng cấp ngay, chỉ chọn loại tùy láng giềng.

**(f) Thành phố nghiên cứu mỏ:**
```python
if k=='miningres' and l==0 and not s.exists('lightres'):
    return ('lightres', 0, None)
```
→ xem quirk ở mục 13.

**(g) Nhánh chung — tăng cấp trong cùng loại:**
```python
if l + 1 < len(K[k]): return (k, l+1, None)
```
Nếu loại hiện tại còn cấp cao hơn trong danh sách `K[k]` mà các nhánh đặc
biệt bên trên chưa "chặn" lại, luôn cho tăng thẳng 1 cấp, không khóa.

**(h) Nhánh chung — tiến hóa sang loại mới (`NEXT`):**
```python
if k in NEXT:
    nk = NEXT[k]
    if nk == 'lightres':
        return (nk, 0, 'Duy nhất: chỉ xây được một.' if s.exists('lightres') else None)
    need = 1 if nk in ('portcity', 'magicportcity') else 2
    if not (len(built) >= 4 or sum(q.k in VFAM for q in built) >= need):
        return (nk, 0, f'Thử xây thêm xung quanh: cần 4 ô kề đã xây, hoặc {need} làng/thành phố kề bên.')
    return (nk, 0, None)
```
Chỉ chạy tới đây khi ô đã ở **cấp cao nhất** của loại hiện tại (nhánh (g) ở
trên không còn áp dụng). Nếu loại đích là `lightres` (từ `miningres`) — dùng
lại thông điệp "độc nhất" tương tự. Ngược lại, kiểm tra điều kiện tiến hóa:
- `need = 1` cho `portcity`/`magicportcity` (dễ hơn — chỉ cần 1 ô kề thuộc
  nhóm làng/thành phố), `need = 2` cho tất cả các trường hợp `NEXT` còn lại.
- Điều kiện thỏa nếu: **(có ≥4 ô kề bất kỳ đã xây) HOẶC (có ≥ need ô kề
  thuộc `VFAM`)** — tức là có 2 cách đạt điều kiện, cách nào dễ hơn thì dùng.
- Nếu chưa đủ → trả về kèm khóa với gợi ý cụ thể số lượng cần thiết.

**(i) Không còn gì để nâng:** nếu không khớp bất kỳ nhánh nào ở trên (đã max
cấp và không có trong `NEXT`, ví dụ Thành phố nghiên cứu ánh sáng cấp 1,
Vòng Đá cấp 3...) → trả về `None`.

### 10.6 `mult(t, r)`
```python
def mult(s, t, r): return 1 + sum(K[q.k][q.l]['b'][r] for q in s.nb(t) if q.built)
```
Hệ số nhân sản lượng tài nguyên `r` (0-3) của ô `t`: bắt đầu từ hệ số 1 (100%),
cộng thêm **tổng % boost** của tài nguyên `r` từ tất cả ô kề **đã xây** (không
quan tâm ô `t` có xây hay không — hàm này chỉ tính hệ số, việc có áp dụng hay
không do `recalc()` quyết định dựa vào `t.built`).

### 10.7 `recalc()`
```python
def recalc(s):
    s.rate = [0.0]*4; s.light = 0; rs = 0.0; tech = 0
    for row in s.G:
        for t in row:
            if s.dark(t.x, t.y) or not t.built: continue
            d = K[t.k][t.l]; s.light += d.get('light', 0)
            if t.k == 'stonetech': tech += 1
            for r in range(4):
                if d['p'][r]:
                    v = d['p'][r] * s.mult(t, r); s.rate[r] += v
                    if t.k == 'rocks' and r == 1: rs += v
    s.techpct = .01 * s.rate[3] * tech if tech else 0
    s.rate[1] += rs * s.techpct
```
Duyệt **toàn bộ** bản đồ (bỏ qua ô tối hoặc chưa xây), với mỗi ô đã xây:
- Cộng `light` của ô đó vào tổng `s.light` (ảnh hưởng tốc độ lan Bóng Tối).
- Đếm số Trung tâm công nghệ đá (`tech`).
- Với từng loại tài nguyên `r`, nếu ô có sản xuất tài nguyên đó (`d['p'][r] != 0`):
  tính sản lượng thực = sản lượng gốc × hệ số boost (`mult`), cộng vào tổng `s.rate[r]`.
  Nếu ô là `rocks` và đang tính tài nguyên Đá (`r==1`) → cộng dồn riêng vào `rs`
  (tổng sản lượng Đá **chỉ từ các ô Đá**, dùng cho bước tiếp theo).
- Sau khi duyệt xong: `techpct` = % tăng thêm cho sản lượng Đá-từ-Đá, tính theo
  công thức `1% × tổng sản lượng Khoa học × số Trung tâm công nghệ đá đã xây`.
  Cộng thêm `rs * techpct` vào tổng Đá — đây là lý do Trung tâm công nghệ đá
  "tăng sản lượng đá của mọi ô Đá theo sản lượng khoa học" (như mô tả `t=...`
  trong dữ liệu `K['stonetech']`).

`recalc()` được gọi lại mỗi khi: sinh bản đồ mới, mỗi khi xây/nâng cấp thành
công (`click`), và mỗi khi Bóng Tối nuốt thêm 1 ô (`tick`) — vì bất kỳ thay
đổi nào ở trên đều có thể làm thay đổi `s.rate`/`s.light`.

### 10.8 `cost(d, k=None, l=0)`
```python
def cost(s, d, k=None, l=0):
    m = 1.5 if s.mode == 'ext' else 1
    if k and k not in ('circle','tower','towerwater','potion','stonetech','lightres'):
        m *= 1 + .2 * sum(1 for row in s.G for q in row if q.built and q.k == k and q.l >= l)
    return [math.ceil(c * m) if c else 0 for c in d['c']]
```
- Hệ số giá cơ bản `m`: 1.5× nếu đang ở chế độ Mở rộng, ngược lại 1×.
- **Trừ phi** loại `k` thuộc nhóm "độc nhất/đặc biệt" (Vòng Đá, Tháp ánh sáng,
  Tháp nước, Nhà máy thuốc, Trung tâm công nghệ đá, Thành phố nghiên cứu ánh
  sáng) — các loại này giá **cố định**, không tăng theo số lượng đã xây.
- Với các loại còn lại: đếm số ô **cùng loại `k`, cấp ≥ `l`** đã xây trên toàn
  bản đồ, mỗi ô như vậy cộng thêm **20%** vào hệ số `m`. Đây là cơ chế "lạm
  phát giá" — xây càng nhiều Làng, Làng tiếp theo càng đắt — khuyến khích
  người chơi đa dạng hóa thay vì chỉ nhân bản 1 loại công trình.
- Giá cuối cùng = làm tròn lên (`math.ceil`) của chi phí gốc nhân `m`, cho
  từng loại trong 4 tài nguyên (giữ nguyên 0 nếu chi phí gốc là 0).

### 10.9 `click(t)`
```python
def click(s, t):
    if s.state != 'play' or s.over or s.paused or s.dark(t.x, t.y): return
    u = s.up(t)
    if not u or u[2]: return
    d = K[u[0]][u[1]]; need = s.cost(d, u[0], u[1])
    if any(s.res[i] < need[i] for i in range(4)): sfx('no'); return
    for i in range(4): s.res[i] -= need[i]
    t.k, t.l, t.built = u[0], u[1], True; s.jset.add((u[0], u[1])); sfx('up')
    if d.get('push'): s.dn = max(0, s.dn - 12 * d['push'])
    s.recalc()
    if not s.first:
        s.first = True; s.say('Nâng cấp có sẵn phụ thuộc vào bốn ô kề bên...', t=14)
    if d.get('win') == 2 or (d.get('win') == 1 and s.mode == 'std'): s.win()
```
Thứ tự xử lý khi người chơi bấm vào ô `t`:
1. **Chặn sớm** nếu: không ở màn hình chơi, ván đã kết thúc, đang tạm dừng,
   hoặc ô đã bị Bóng Tối nuốt (không thể tương tác).
2. Lấy đề xuất nâng cấp `u = s.up(t)`. Nếu không có đề xuất (`None`) hoặc đề
   xuất đang bị khóa (`u[2]` khác `None`) → không làm gì.
3. Tính chi phí thực (`s.cost`, đã gồm lạm phát giá). Nếu thiếu **bất kỳ**
   loại tài nguyên nào → phát âm thanh từ chối (`sfx('no')`) và dừng.
4. Trừ tài nguyên, áp dụng nâng cấp vào `t` (đổi `k/l`, đánh dấu `built=True`),
   ghi vào sổ Nhật ký (`jset`), phát âm thanh thành công.
5. Nếu cấp vừa đạt có cờ `push` → đẩy lùi Bóng Tối: giảm `s.dn` (số ô đã bị
   nuốt) đi `12 * push` ô, nhưng không âm (kẹp ở 0).
6. Gọi lại `recalc()` để cập nhật sản lượng/ánh sáng theo trạng thái mới.
7. Nếu đây là lần nâng cấp **đầu tiên** của ván chơi → hiện thông báo hướng
   dẫn (tự ẩn sau 14 giây, `t=14`).
8. Kiểm tra điều kiện thắng (xem mục 13) và gọi `s.win()` nếu thỏa.

### 10.10 `say`, `start`, `to_menu`, `lit`, `win`, `lose`
- `say(text, btns, t)` — thiết lập hộp thoại thông báo: nội dung, danh sách
  nút `(nhãn, hàm_callback)`, và thời gian tự ẩn (`t=0` nghĩa là ở lại cho
  tới khi bị thay thế bởi thông báo khác, không tự ẩn).
- `start()` — chuyển sang màn hình chơi, bỏ tạm dừng, hiện thông báo mở đầu.
- `to_menu()` — quay về menu, **sinh lại bản đồ mới** (ván chơi cũ coi như mất).
- `lit()` — đếm tổng số ô còn sáng (chưa bị Bóng Tối nuốt) trên toàn bản đồ,
  dùng để tính điểm khi thắng.
- `win()` — đánh dấu `over=True`, phát âm thanh thắng, tính điểm:
  `sc = max(1, round(số_ô_sáng × 3 + 600 − thời_gian_chơi / 10))` (chơi càng
  nhanh, càng nhiều ô còn sáng → điểm càng cao). Ở chế độ Mở rộng, hiển thị
  thời gian hoàn thành thay vì điểm (vì đó là chế độ đua tốc độ). Hiện thông
  báo thắng kèm 2 nút: "Về menu" hoặc "Tiếp tục" (chơi tiếp sau khi thắng,
  không bắt buộc dừng lại).
- `lose()` — đánh dấu `over=True`, phát âm thanh thua, hiện thông báo thua
  kèm 2 nút: "Về menu" hoặc "Chơi lại" (sinh bản đồ mới và bắt đầu lại ngay).

### 10.11 `tick(dt)`
```python
def tick(s, dt):
    if s.msg_t > 0:
        s.msg_t -= dt
        if s.msg_t <= 0: s.msg = None
    if s.state != 'play' or s.paused or s.over: return
    g = dt * s.speed; s.gt += g
    for i in range(4): s.res[i] += s.rate[i] * g / 60
    s.dacc += g; iv = (5.5 if s.mode == 'ext' else 8) * (1 + .35 * s.light)
    while s.dacc >= iv and not s.over:
        s.dacc -= iv; s.dn = min(W*H, s.dn + 1)
        s.recalc()
        if not any(t.k=='circle' and not s.dark(t.x,t.y) for row in s.G for t in row): s.lose()
    s.dprog = min(1.0, s.dacc / iv)
```
Gọi mỗi khung hình, `dt` = số giây thực đã trôi qua kể từ khung trước (giới
hạn 60 FPS bởi `clock.tick(60)` trong `main()`).

1. **Đồng hồ thông báo**: nếu thông báo hiện tại có hẹn giờ tự ẩn (`msg_t>0`),
   giảm dần, tự xóa khi về 0 — hoạt động **độc lập** với trạng thái tạm dừng/
   màn hình (để thông báo vẫn đếm giờ ẩn ngay cả ở menu).
2. Nếu không đang chơi, hoặc đang tạm dừng, hoặc ván đã kết thúc (`over`) →
   dừng tại đây, không cập nhật gì thêm (tài nguyên và Bóng Tối đứng yên).
3. `g = dt × speed` — thời gian "trong game" đã trôi, nhân theo tốc độ người
   chơi chọn (1×/2×/4×). Cộng dồn vào tổng thời gian chơi `s.gt`.
4. Cộng tài nguyên: mỗi tài nguyên tăng theo `rate` (đơn vị: mỗi **phút**),
   nên phần trăm thời gian thực tế cộng vào là `rate × g / 60` (quy đổi giây
   sang phút).
5. **Bóng Tối lan**: cộng dồn thời gian trôi vào bộ đếm `s.dacc`. Chu kỳ `iv`
   (số giây giữa 2 lần nuốt ô) = giá trị gốc theo chế độ (Mở rộng nhanh hơn:
   5.5s so với 8s ở Tiêu chuẩn), nhân hệ số `(1 + 0.35 × s.light)` — **ánh
   sáng càng nhiều** (từ Tháp ánh sáng) → `iv` càng lớn → Bóng Tối lan **càng
   chậm**. Vòng lặp `while` cho phép nuốt **nhiều ô liền** nếu khung hình bị
   trễ hoặc tốc độ game rất cao (4×) khiến `dacc` vượt `iv` nhiều lần cùng lúc.
   Mỗi lần nuốt 1 ô: tăng `s.dn`, gọi lại `recalc()` (vì ô bị nuốt có thể vừa
   mất đi 1 nguồn sản xuất/boost), rồi kiểm tra thua ngay lập tức (không đợi
   hết vòng lặp) — nếu không còn Vòng Đá nào sáng, gọi `s.lose()` và vòng
   `while` tự dừng (điều kiện `not s.over`).
6. `s.dprog` = tiến độ (0.0–1.0) của **ô tiếp theo sắp bị nuốt** trong chu kỳ
   hiện tại — dùng để vẽ hiệu ứng tối dần mượt trên bản đồ (`draw_map`), thay
   vì ô đột ngột biến mất.

---

## 11. Lớp giao diện (hàm vẽ, nút bấm)

Phần này (từ `pygame.init()` tới hết `draw_journal()`) thuần túy là trình bày,
không chứa luật chơi — tất cả quyết định (nâng cấp được gì, giá bao nhiêu,
có thắng/thua không) đã được tính xong bởi `class Game` ở trên; giao diện chỉ
**đọc** dữ liệu đó ra và vẽ, cùng việc **ghi nhận vị trí các nút bấm** để
`main()` dò va chạm chuột.

- `txt/wrap/para` — tiện ích vẽ chữ và tự xuống dòng theo độ rộng cho trước.
- `button(label, rect, cb, sel)` — vẽ 1 nút, và **quan trọng**: thêm
  `(rect, cb)` vào danh sách toàn cục `buttons`. Danh sách này được dò trong
  `main()` mỗi khi có sự kiện click chuột — xem mục 12.
- `chips(...)` — vẽ hàng ô vuông màu + số cho 4 loại tài nguyên (dùng chung
  cho hiển thị sản lượng, boost %, và chi phí — tô màu đỏ nếu thiếu tài
  nguyên khi hiển thị chi phí nhờ tham số `afford`).
- `hl_tiles()` — tính (có cache 300ms) danh sách ô đang **vừa đủ điều kiện
  vừa đủ tài nguyên** để nâng cấp ngay, phục vụ tính năng gợi ý "Sáng".
- `draw_map/draw_side/draw_msg/draw_journal` — vẽ từng vùng màn hình tương
  ứng (bản đồ, panel phải, hộp thông báo, toàn màn hình Nhật ký).
- `tile_at(pos)` — quy đổi tọa độ pixel chuột sang ô bản đồ tương ứng (hoặc
  `None` nếu ở ngoài vùng bản đồ / trên panel phải).

---

## 12. `main()` — vòng lặp sự kiện

```python
def main():
    clock = pygame.time.Clock(); mt = 0
    while True:
        dt = clock.tick(60) / 1000
        ...
        for e in pygame.event.get():
            ...
        g.tick(dt); buttons.clear()
        draw_map(); draw_side(); draw_msg()
        if g.jopen: buttons.clear(); draw_journal()
        pygame.display.flip()
```

Vòng lặp vô hạn, giới hạn **60 khung hình/giây** (`clock.tick(60)` vừa giới
hạn tốc độ vừa trả về số mili-giây đã trôi, quy đổi ra giây làm `dt`).

Mỗi khung hình:
1. **Nhạc nền**: bộ đếm `mt` đếm ngược một khoảng ngẫu nhiên (0.5–1.4 giây);
   khi về 0, nếu đang chơi/không tạm dừng/chưa kết thúc và đã bật nhạc →
   phát 1 nốt ngẫu nhiên trong thang âm 7 nốt cho trước (tạo giai điệu ambient
   ngẫu nhiên liên tục, không cần file nhạc).
2. **Xử lý sự kiện** (`pygame.event.get()`):
   - `QUIT` (đóng cửa sổ) → thoát chương trình.
   - `KEYDOWN`: `Space` đảo trạng thái tạm dừng (chỉ khi đang chơi); `J` đảo
     trạng thái mở/đóng Nhật ký (bất kỳ lúc nào); `Esc` — nếu Nhật ký đang mở
     thì đóng nó, ngược lại nếu đang chơi thì về menu.
   - `MOUSEMOTION` → cập nhật `g.hov` (ô đang được trỏ, để hiển thị thông tin).
   - `MOUSEBUTTONDOWN` (chuột trái):
     - Trước tiên dò xem có **nút bấm nào** (trong danh sách `buttons`, xét
       từ **cuối lên đầu** — `reversed` — vì nút vẽ sau nằm "trên" về mặt thị
       giác, nên được ưu tiên bắt sự kiện trước) đang nằm dưới điểm click. Nếu
       có, gọi callback của nút đó và **bỏ qua** phần xử lý còn lại (`continue`).
     - Nếu không trúng nút nào, và Nhật ký đang **đóng**, mới coi là click vào
       bản đồ → tìm ô tương ứng (`tile_at`) và gọi `g.click(t)` để thử nâng cấp.
3. Gọi `g.tick(dt)` cập nhật toàn bộ logic game cho khung hình này.
4. **Xóa danh sách nút cũ** (`buttons.clear()`) trước khi vẽ lại — vì vị trí
   nút có thể thay đổi theo trạng thái (ví dụ số dòng text khác nhau).
5. Vẽ bản đồ, panel bên phải, hộp thông báo. Nếu Nhật ký đang mở, xóa lại
   danh sách nút (vì Nhật ký vẽ **đè lên toàn màn hình** với bộ nút khác hẳn,
   không muốn lẫn với nút của màn hình chơi bên dưới) rồi vẽ Nhật ký.
6. `pygame.display.flip()` — đẩy khung hình vừa vẽ ra màn hình thật.

---

## 13. Những điểm dễ nhầm / quirk trong code

1. **`win=1` so với `win=2`:** chỉ có 2 giá trị cờ `win`. Trong `Game.click`:
   `if d.get('win') == 2 or (d.get('win') == 1 and s.mode == 'std'): s.win()`.
   Nghĩa là `win=2` (Vòng Đá cấp cuối, Thành phố nghiên cứu ánh sáng cấp cuối)
   luôn thắng ở **mọi** chế độ; `win=1` (chỉ Tháp ánh sáng cấp cuối) **chỉ**
   thắng khi đang ở chế độ Tiêu chuẩn — ở chế độ Mở rộng, nâng Tháp ánh sáng
   lên cấp cuối vẫn có tác dụng (làm chậm Bóng Tối rất nhiều, `light=3`) nhưng
   **không** kết thúc ván chơi.

2. **`miningres` cấp 1 gần như vô dụng:** Trong `K['miningres']` có khai báo
   đủ 2 cấp. Nhưng `Game.up()` có nhánh đặc biệt kiểm tra **trước** nhánh tăng
   cấp thông thường:
   ```python
   if k == 'miningres' and l == 0 and not s.exists('lightres'):
       return ('lightres', 0, None)
   ```
   Vì nhánh này đứng trước `if l + 1 < len(K[k])`, ngay khi Thành phố nghiên
   cứu mỏ đạt cấp 0 (đã xây), lần click tiếp theo sẽ đề xuất nhảy thẳng sang
   `lightres` cấp 0, **bỏ qua hoàn toàn** cấp 1 của chính `miningres`. Cấp 1
   trong dữ liệu `K['miningres']` trên thực tế không bao giờ được chọn qua
   luồng nâng cấp bình thường (trừ khi đã có `lightres` trên bản đồ — khi đó
   dòng `not s.exists('lightres')` sai, code rơi xuống nhánh chung và mới cho
   nâng lên cấp 1 thật sự). Đây nhiều khả năng là chủ ý thiết kế: ép người
   chơi phải rẽ nhánh sang con đường thắng `lightres` ngay khi đủ điều kiện,
   thay vì tiếp tục đầu tư thêm vào `miningres`.

3. **Vòng Đá "cấp 0" không có trong `K` với chi phí** — `L('Vòng đá')` không
   truyền `cost`, nên mặc định `(0,0,0,0)`. Tuy nhiên cấp 0 **không bao giờ
   được "xây"** qua `click()` — nó được đặt sẵn trực tiếp vào bản đồ lúc
   `gen()` (`s.G[...].k = 'circle'`), nhưng **`built` vẫn là `False`** cho tới
   khi người chơi bấm nâng lên cấp 1 lần đầu. Điều này có nghĩa: Vòng Đá ban
   đầu **không sản xuất/boost gì cả** (vì `recalc()` chỉ tính ô có `built=True`),
   nó chỉ đóng vai trò "điểm neo" để kiểm tra điều kiện thua (`any(t.k=='circle'
   and not s.dark(...))` trong `tick()` — **không** yêu cầu `built=True`, chỉ
   cần `k=='circle'` và còn sáng).

4. **Chi phí tăng dần chỉ tính ô "cấp ≥ l"**: trong `cost()`,
   `sum(1 for ... if q.built and q.k==k and q.l>=l)` — nghĩa là khi tính giá
   để **nâng lên cấp `l`**, chỉ đếm các ô cùng loại đã đạt **từ cấp `l` trở
   lên**, không đếm ô cùng loại nhưng đang ở cấp thấp hơn. Ví dụ: nếu bạn có
   3 Làng cấp 0 và 1 Làng cấp 1, giá xây **Làng mới (cấp 0)** sẽ tính dựa trên
   toàn bộ 4 Làng (vì tất cả đều có cấp ≥ 0), nhưng giá **nâng 1 Làng lên cấp 1**
   chỉ tính dựa trên Làng đã ở cấp 1 (1 ô) — không bị ảnh hưởng bởi 3 Làng
   cấp 0 còn lại.

5. **`nb()` không tính ô tối là hàng xóm** — hệ quả: nếu Bóng Tối nuốt một ô
   nằm giữa 2 công trình, 2 công trình đó **ngay lập tức không còn được coi
   là "kề nhau"** nữa (mất boost lẫn nhau, mất điều kiện mở khóa dựa vào
   nhau) — dù khoảng cách vật lý không đổi. Đây là lý do `recalc()` phải được
   gọi lại mỗi khi `s.dn` tăng trong `tick()`.

6. **`push` làm giảm `s.dn` chứ không "xóa bóng tối đã có"**: về bản chất,
   lùi `s.dn` chỉ đơn giản là giảm bộ đếm, khiến các ô có thứ tự xoắn ốc gần
   với `s.dn` mới (tức là những ô **vừa mới bị nuốt gần đây nhất** theo đúng
   đường xoắn ốc cố định) quay lại trạng thái sáng. Nó không "chữa lành" một
   ô cụ thể theo ý người chơi chọn — thứ tự phục hồi luôn tuân theo đúng
   đường xoắn ốc ngược lại.

---

*Xem thêm:* `GIAI_THICH.md` (tổng quan ngắn gọn), `CHUC_NANG.md` (danh sách
tính năng giao diện và điều khiển), `StopTheDarkness_GiaiThich.py` (code đầy
đủ kèm chú thích tiếng Việt inline).
