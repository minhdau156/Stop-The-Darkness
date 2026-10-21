# Giải thích code: StopTheDarknessPretty.py

Game pygame, một file. Logic giống `StopTheDarknessFake.py`. File này chỉ thay phần hiển thị (pixel-art, bo góc, bảng bên phải).

Chạy: `pip install pygame`, rồi `python StopTheDarknessPretty.py`.
Phím: `Space` tạm dừng, `J` nhật ký, `Esc` đóng nhật ký / về menu.

---

## 1. Cấu trúc file

| Phần | Nội dung |
|---|---|
| Hằng số | Kích thước lưới, màu, tên tài nguyên |
| Âm thanh | `play`, `sfx`: tự sinh sóng sin, không cần file |
| Dữ liệu | `K`, `NEXT`, `HARVEST`, `VFAM`, `PAGES` |
| `spiral()` | Thứ tự Bóng Tối lan |
| `draw_tile()` | Vẽ pixel-art từng loại ô |
| `Tile`, `Game` | Trạng thái và luật chơi |
| Tiện ích vẽ | `rr`, `txt`, `button`, `chips`, `gem`... |
| `draw_*` | Vẽ bản đồ, bảng phải, thông báo, nhật ký |
| `main()` | Vòng lặp game |

## 2. Hằng số

- `W, H = 15, 12`: lưới 15 cột × 12 hàng.
- `T = 54`: cạnh một ô (pixel). `U = 6`: kích thước một "pixel-art" khi vẽ ô (ô vẽ trên lưới 9×9).
- `MW = W*T`: bề rộng bản đồ. `PW = 330`: bề rộng bảng phải. `SW, SH`: kích thước cửa sổ.
- `RC`, `RN`: màu và tên 4 tài nguyên. Chỉ số 0 = Gỗ, 1 = Đá, 2 = Phép thuật, 3 = Khoa học.

## 3. Âm thanh

- `play(f, dur, vol, decay)`: tạo nốt sin tần số `f`, tắt dần theo `decay`. Lưu cache trong `_snd`. Nếu mixer lỗi thì bỏ qua (`AUDIO = False`).
- `sfx(name)`: hiệu ứng `up`, `no`, `win`, `lose`. Không phát nếu `g.sound` tắt.
- Nhạc nền: `main()` phát một nốt ngẫu nhiên mỗi 0.5–1.4 giây.

## 4. Dữ liệu công trình

### `L(name, cost, prod, boost, **kw)`
Tạo một cấp công trình. Mỗi tuple tự đệm thành 4 phần tử (Gỗ, Đá, Phép thuật, Khoa học).

| Khóa | Ý nghĩa |
|---|---|
| `n` | Tên |
| `c` | Chi phí xây/nâng |
| `p` | Sản lượng mỗi phút |
| `b` | % tăng cho ô kề (0.25 = 25%) |
| `t` | Chú thích hiển thị |
| `push` | Đẩy lùi Bóng Tối (số ô = `12 * push`) |
| `light` | Điểm làm chậm Bóng Tối (Tháp ánh sáng) |
| `win` | `2` = thắng mọi chế độ. `1` = thắng chế độ Tiêu chuẩn |

### Các bảng khác
- `K[loại]` = danh sách cấp. `K['forest'][2]` là Rừng cấp 3.
- `NEXT`: Làng → Thành phố (`village → city`...).
- `HARVEST`: ô có thể nhấn để thu hoạch: `{loại: (chỉ số tài nguyên, số lượng)}`.
- `VFAM`: nhóm làng/thành phố. Dùng để kiểm tra điều kiện tiến hóa.
- `PAGES`: các trang của Nhật ký.

## 5. `spiral()` — đường Bóng Tối

Trả về `(d, order)`:
- `order`: danh sách `(x, y)` theo thứ tự bị nuốt.
- `d[y][x]`: số thứ tự của ô đó.

Cách đi: hàng dưới từ trái sang phải → cột phải đi lên → hàng trên đi sang trái → cột trái đi xuống. Rồi thu vào một lớp và lặp lại.

Ô `(x, y)` tối khi `d[y][x] < g.dn` (xem `Game.dark`).

## 6. `draw_tile()` — pixel-art

Vẽ một ô trên lưới 9×9, mỗi "pixel" = `u` pixel màn hình.

- `r(col, x, y, w, h)`: vẽ một khối pixel.
- `part`: `'base'` (nền), `'obj'` (vật thể), `'all'`.
- Nền: nước = xanh dương, đất công trình = màu be, còn lại = cỏ xanh. Thêm vài chấm để có chất liệu.
- Hàm con: `tree`, `house`, `mush`.
- Mỗi `k` có một nhánh `if/elif` vẽ riêng. Cấp `l` quyết định số nhà, số cây, màu mái...

## 7. Lớp `Tile`

```python
Tile(k, x, y, v)   # k: loại, l: cấp, v: số ngẫu nhiên (biến thể hình), built: đã xây, hv: đã thu hoạch
```
- `l = 0`, `built = False` lúc đầu.
- `hv`: ô Rừng/Đá/Nấm chỉ thu hoạch được một lần (xem `click`).

## 8. Lớp `Game`

### Trạng thái
`mode` (`std`/`ext`), `state` (`menu`/`play`), `speed` (1/2/4), `paused`, `res` (4 tài nguyên), `rate` (sản lượng mỗi phút), `dn` (số ô đã tối), `dacc` (thời gian tích lũy), `light` (điểm Tháp ánh sáng), `jset` (nhật ký đã mở), `over`.

### `gen()`
1. Mỗi ô random loại: field 36%, forest 24%, rocks 11%, water 13%, mushroom 8%, roots 8%. `roots` đổi thành `field` nếu không phải chế độ Mở rộng.
2. 38% (trái) / 30% (trên) lấy loại của ô lân cận → tạo mảng đất liền.
3. Đặt 1 `circle` (Vòng đá) ở khu vực giữa.
4. Reset tài nguyên (10 Gỗ), Bóng Tối, nhật ký.

### `dark(x, y)`, `nb(t)`, `exists(k)`
- `dark`: ô đã bị nuốt chưa.
- `nb`: 4 ô kề (trên, phải, dưới, trái), bỏ ô tối.
- `exists`: có ô loại `k` trên bản đồ không.

### `up(t)` — nâng cấp tiếp theo
Trả về `(loại, cấp, lời_khóa | None)` hoặc `None` (đã tối đa). Thứ tự kiểm tra:

1. **Vòng đá** cấp 0: khóa tới khi có Làng phép thuật cấp 2.
2. **Cánh đồng**: loại công trình tùy 4 ô kề. Ưu tiên: Tháp ánh sáng → Tháp nước → Làng cảng phép thuật (nấm + nước) → Làng phép thuật (nấm) → Làng khai mỏ (≥2 đá) → Làng cảng (nước) → Làng.
3. **Rừng** cấp 4 + Rừng rễ cây cấp 4 kề → Nhà máy thuốc.
4. **Rừng** cấp 0 + 4 ô kề đều Rừng → Làng trên cây.
5. **Đá** cấp 4 → Trung tâm công nghệ đá (cần Thành phố kề).
6. **Nước** → Bến tàu (kề cảng) hoặc Hải đăng.
7. `miningres` cấp 0 → Thành phố nghiên cứu ánh sáng.
8. Còn cấp trong `K[k]` → cấp kế tiếp.
9. Hết cấp → `NEXT`. Điều kiện: ≥4 ô kề đã xây, **hoặc** đủ 1–2 ô thuộc `VFAM`.

### `mult(t, r)`
Hệ số nhân sản lượng của ô `t` cho tài nguyên `r`: `1 + tổng boost của các ô kề đã xây`.

### `recalc()`
Tính lại `rate` và `light`:
- Bỏ ô tối và ô chưa xây.
- `rate[r] += p[r] * mult`.
- Trung tâm công nghệ đá tăng sản lượng Đá của mọi ô Đá theo sản lượng Khoa học (`techpct`).

### `cost(d, k, l)`
Giá cơ sở × 1.5 (chế độ Mở rộng) × `(1 + 0.2 × số ô cùng loại đã xây)`. Công trình độc nhất (`circle`, `tower`, `towerwater`, `potion`, `stonetech`, `lightres`) không tăng giá.

### `click(t)`
1. Thoát nếu không đang chơi, đã kết thúc, tạm dừng, hoặc ô tối.
2. Nếu ô là Rừng/Đá/Nấm và chưa `hv`: đánh dấu `hv = True`, cộng `HARVEST` (+2).
3. Lấy `up(t)`. Thoát nếu không có hoặc bị khóa.
4. Thiếu tài nguyên → `sfx('no')`, thoát.
5. Trừ tài nguyên. Đổi `t.k, t.l, t.built`. Ghi nhật ký.
6. `push` → lùi `dn` đi `12 * push` ô. Gọi `recalc()`.
7. `win` đủ điều kiện → `win()`.

### `tick(dt)` — mỗi khung hình
1. Cập nhật thông báo hết hạn.
2. Cộng tài nguyên: `res += rate * dt * speed / 60`.
3. Chu kỳ Bóng Tối: `iv = (8 hoặc 5.5 giây) * (1 + 0.35 * light)`. Khi `dacc >= iv`: `dn += 1`, `recalc()`.
4. Không còn `circle` sáng → `lose()`.
5. `dprog = dacc / iv`: dùng để làm mờ dần ô sắp tối.

### Khác
`say`, `start`, `to_menu`, `lit`, `win`, `lose`: thông báo và đổi trạng thái. Điểm thắng = `lit*3 + 600 - gt/10`. Chế độ Mở rộng hiện thời gian.

## 9. Tiện ích vẽ

| Hàm | Việc |
|---|---|
| `mkfont` | Dùng font Noto Sans trong `assets/fonts`, nếu thiếu dùng font hệ thống |
| `wrap` | Ngắt dòng theo chiều rộng |
| `rr` | Hình chữ nhật bo góc, hỗ trợ alpha |
| `vgrad` | Nền gradient dọc (có cache) |
| `txt`, `ctxt`, `para` | Vẽ chữ: trái, giữa, đoạn văn |
| `gem` | Viên ngọc tròn đại diện tài nguyên |
| `draw_icon` | Biểu tượng pause, play, ff, close |
| `button` | Vẽ nút và đăng ký `(rect, callback)` vào `buttons` |
| `chips` | Hàng "ngọc + số". Đỏ nếu thiếu tài nguyên |

### Ô và cache
- `tile_surf(k, l, v, u, inset, rad)`: dựng Surface một ô, có cache `_ic`. Gồm nền, bóng đổ, viền tối quanh vật thể, bo góc.
- `icon(k, l, v, s)`: bản nhỏ cho bảng phải và nhật ký.
- `_dark`, `_wisp`, `_streak`, `_vig`: ảnh dựng sẵn cho ô tối, sương tím, sóng nước, viền tối mép màn hình.

## 10. Các hàm `draw_*`

- `draw_map()`: vẽ ô sáng → viền xanh nhấp nháy (nút "Sáng") → viền ô đang trỏ → ô tối (nền, viền sáng chỉ ở cạnh giáp vùng sáng, sương trôi) → ô sắp tối mờ dần → vignette → lớp "TẠM DỪNG".
- `draw_side()`: menu (chọn chế độ, Chơi, Tạo lại, Nhật ký), hoặc khi đang chơi: 4 ô tài nguyên + sản lượng, thanh Bóng Tối, thẻ thông tin ô đang trỏ (hiện tại / nâng cấp tiếp theo / gợi ý mở khóa), nút điều khiển.
- `card` + `it_*`: mỗi mục là `(chiều cao, hàm vẽ)`. `card` cộng chiều cao rồi vẽ khung.
- `hl_tiles()`: danh sách ô đủ điều kiện và đủ tài nguyên để nâng. Tính lại mỗi 300 ms.
- `draw_msg()`: hộp thông báo ở đáy bản đồ, có thể kèm nút.
- `draw_journal()`: nhật ký phân trang. Mục chưa mở hiện `???`.

## 11. `main()` — vòng lặp

Mỗi khung hình (60 FPS):
1. `dt = clock.tick(60) / 1000`.
2. Phát nhạc nền ngẫu nhiên.
3. Xử lý sự kiện:
   - Thoát cửa sổ.
   - Phím `Space`, `J`, `Esc`.
   - Chuột trái: kiểm tra nút trong `buttons` (duyệt từ nút vẽ sau cùng). Nếu trúng nút thì gọi callback. Nếu không và nhật ký đóng thì `tile_at(pos)` → `g.click(tile)`.
4. `g.hov = tile_at(mouse.get_pos())`: đọc chuột trực tiếp, tránh trễ.
5. `g.tick(dt)`.
6. `buttons.clear()`, rồi vẽ bản đồ, bảng phải, thông báo. `draw_journal()` nếu nhật ký mở.
7. `pygame.display.flip()`.

Lưu ý: `buttons` được dựng lại mỗi khung hình khi vẽ. Sự kiện chuột dùng danh sách của khung hình trước.

## 12. Muốn sửa gì thì sửa ở đâu

| Muốn | Sửa |
|---|---|
| Đổi giá, sản lượng, boost | `K` |
| Đổi tốc độ Bóng Tối | `Game.tick`: `iv` |
| Đổi luật nâng cấp | `Game.up` |
| Đổi lượng thu hoạch khi nhấn | `HARVEST` |
| Đổi hình công trình | `draw_tile` |
| Đổi giao diện bảng phải | `draw_side` |
| Đổi kích thước bản đồ | `W`, `H`, `T` |

## 13. Tra cứu nhanh từng hàm

### Âm thanh
| Hàm | Chức năng |
|---|---|
| `play` | Tạo và phát một nốt sin ngắn. Có cache |
| `sfx` | Phát hiệu ứng `up`, `no`, `win`, `lose` |

### Dữ liệu và logic phụ
| Hàm | Chức năng |
|---|---|
| `L` | Tạo định nghĩa một cấp công trình |
| `spiral` | Tạo thứ tự Bóng Tối lan (xoắn ốc vào trong) |
| `pages` | Trả về các trang nhật ký. Chế độ thường ẩn `roots`, `rootscity`, `potion` |

### Vẽ pixel-art
| Hàm | Chức năng |
|---|---|
| `draw_tile` | Vẽ một ô theo loại `k` và cấp `l`. Hàm con: `r`, `tree`, `house`, `mush` |

### Lớp `Game`
| Hàm | Chức năng |
|---|---|
| `__init__` | Đặt trạng thái ban đầu, gọi `gen` |
| `gen` | Sinh bản đồ ngẫu nhiên, đặt lại tài nguyên và Bóng Tối |
| `dark` | Ô đã bị Bóng Tối nuốt chưa |
| `nb` | Các ô kề (4 hướng) còn sáng |
| `exists` | Bản đồ đã có công trình loại `k` chưa |
| `up` | Quyết định nâng cấp tiếp theo của ô. Chứa luật xây dựng |
| `mult` | Hệ số nhân sản lượng từ boost của ô kề |
| `recalc` | Tính lại sản lượng, độ sáng Tháp, thưởng Trung tâm công nghệ đá |
| `cost` | Tính giá thực. Tăng 20% cho mỗi công trình cùng loại |
| `click` | Xử lý nhấn ô: thu hoạch, trừ tiền, nâng cấp, đẩy lùi, thắng |
| `say` | Hiện thông báo, có thể kèm nút và hạn tự tắt |
| `start` | Bắt đầu ván, hiện hướng dẫn |
| `to_menu` | Về menu, tạo bản đồ mới |
| `lit` | Đếm ô còn sáng |
| `win` | Kết thúc thắng, tính điểm hoặc thời gian |
| `lose` | Kết thúc thua |
| `tick` | Cập nhật mỗi khung hình: tài nguyên, Bóng Tối, điều kiện thua |

### Tiện ích giao diện
| Hàm | Chức năng |
|---|---|
| `mkfont` | Nạp font Noto Sans, dự phòng font hệ thống |
| `now` | Thời gian hiện tại (giây) |
| `fmt` | Định dạng số (`1.2k`, `3.5`) |
| `wrap` | Ngắt dòng theo bề rộng |
| `rr` | Hình chữ nhật bo góc, hỗ trợ alpha |
| `vgrad` | Nền chuyển màu dọc. Có cache |
| `txt`, `ctxt`, `para` | Vẽ chữ: trái, giữa, đoạn nhiều dòng |
| `gem` | Vẽ viên ngọc tài nguyên |
| `draw_icon` | Vẽ biểu tượng `pause`, `play`, `ff`, `close` |
| `button` | Vẽ nút, đăng ký vùng bấm vào `buttons` |
| `chips` | Vẽ dãy "ngọc + số". Đỏ nếu thiếu tài nguyên |

### Vẽ ô và bản đồ
| Hàm | Chức năng |
|---|---|
| `round_surf` | Bo góc ô, thêm viền mờ |
| `tile_surf` | Dựng ảnh ô hoàn chỉnh (nền, bóng đổ, viền). Có cache |
| `icon` | Ảnh nhỏ của ô cho bảng phải và nhật ký |
| `hl_tiles` | Liệt kê ô đủ tài nguyên để nâng. Làm mới mỗi 0.3 giây |
| `blit_tile` | Vẽ một ô, thêm vệt sóng cho nước |
| `draw_map` | Vẽ cả bản đồ: ô, viền gợi ý, ô đang trỏ, Bóng Tối, vignette, lớp "TẠM DỪNG" |

### Bảng phải và màn hình phụ
| Hàm | Chức năng |
|---|---|
| `it_label`, `it_para`, `it_head`, `it_dark`, `it_row` | Tạo từng mục của thẻ. Trả về `(chiều cao, hàm vẽ)` |
| `card` | Vẽ thẻ chứa các mục. Trả về y kế tiếp |
| `draw_side` | Vẽ bảng phải: menu, hoặc tài nguyên, thanh Bóng Tối, thẻ ô, nút điều khiển |
| `toggle_hl` | Bật/tắt nổi bật ô nâng cấp được |
| `draw_msg` | Vẽ hộp thông báo ở đáy bản đồ |
| `draw_journal` | Vẽ nhật ký phân trang. Mục chưa mở hiện `???` |

### Điều khiển
| Hàm | Chức năng |
|---|---|
| `tile_at` | Đổi tọa độ chuột thành ô bản đồ |
| `main` | Vòng lặp: nhạc nền, sự kiện, `tick`, vẽ, `flip` |
