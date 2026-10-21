# Giải thích code: Chặn Bóng Tối (Stop the Darkness clone)

File tham chiếu: `StopTheDarkness_GiaiThich.py` (bản có chú thích đầy đủ của `StopTheDarknessFake.py`).

## 1. Giới thiệu chung

Game chiến lược nâng cấp ô đất, lấy cảm hứng từ *Stop the Darkness*. Viết bằng `pygame`, không dùng file ảnh/âm thanh — mọi hình ảnh và âm thanh được vẽ/sinh bằng code.

Vòng lặp chính: người chơi nâng cấp các ô trên lưới bản đồ để sinh tài nguyên, trong khi Bóng Tối lan dần và nuốt các ô. Mục tiêu: xây đủ mạnh để đẩy lùi hoặc chặn đứng Bóng Tối trước khi nó nuốt hết các Vòng Đá.

## 2. Luật chơi cốt lõi

| Luật | Mô tả |
|---|---|
| Bản đồ | Lưới 15 × 12 ô (`W, H`). Mỗi ô có **loại đất** (`k`) và **cấp** (`l`). |
| Tài nguyên | 4 loại: Gỗ, Đá, Phép thuật, Khoa học (chỉ số 0-3 trong mọi mảng). |
| Sản xuất | Ô đã xây sinh tài nguyên mỗi phút, và có thể tăng % sản lượng cho ô **kề cạnh** (trên/dưới/trái/phải, không chéo). |
| Nâng cấp | Bấm vào ô → `Game.up()` tính xem ô có thể lên thành gì, dựa vào loại + cấp hiện tại và 4 ô kề. |
| Bóng Tối | Lan theo đường xoắn ốc cố định (`spiral()`), từ góc dưới-trái vào tâm. Ô bị nuốt thì ngừng sản xuất và không tính là ô kề hợp lệ. |
| Vòng Đá | Công trình phòng thủ trung tâm. Một số cấp của nó (hoặc của vài công trình khác) có thể **đẩy lùi** Bóng Tối (`push`) hoặc **thắng ngay** (`win`). |
| Thua | Khi **tất cả** Vòng Đá trên bản đồ đã bị Bóng Tối nuốt. |
| Thắng | Khi nâng cấp một công trình có cờ `win` tới điều kiện tương ứng. |
| Chế độ | `std` (Tiêu chuẩn: thắng nhanh hơn) và `ext` (Mở rộng: thêm Rừng rễ cây/Nhà máy thuốc, giá cao hơn, Bóng Tối lan nhanh hơn). |

## 3. Cấu trúc file

```
Hằng số bản đồ & màu sắc
Âm thanh tự sinh (play, sfx)
Dữ liệu cây công nghệ (L, K, NEXT, VFAM, PAGES)
spiral()              -> thứ tự Bóng Tối nuốt ô
pages()               -> trang nhật ký theo chế độ
draw_tile() / icon()  -> vẽ pixel-art từng loại ô
class Tile            -> trạng thái 1 ô
class Game            -> toàn bộ trạng thái & luật chơi
Giao diện (vẽ màn hình, nút bấm, nhật ký)
main()                -> vòng lặp sự kiện 60 FPS
```

## 4. Dữ liệu cây công nghệ (`K`)

`K` là dict: khóa = loại ô (`'field'`, `'forest'`, `'circle'`, ...), giá trị = danh sách các **cấp** theo thứ tự, mỗi cấp tạo bằng hàm `L(...)`:

```python
L(name, cost=(), prod=(), boost=(), **kw)
```

- `cost` — chi phí (Gỗ, Đá, Phép thuật, Khoa học) để xây/nâng lên cấp này.
- `prod` — sản lượng mỗi phút, cùng thứ tự 4 tài nguyên.
- `boost` — % tăng sản lượng cộng cho **ô kề** đã xây, theo từng loại tài nguyên.
- Cờ đặc biệt trong `kw`:
  - `t` — văn bản gợi ý hiển thị cho người chơi.
  - `push` — đẩy lùi Bóng Tối (số ô lùi = `12 * push`).
  - `win` — đạt cấp này là thắng (`2` = thắng mọi chế độ, `1` = chỉ thắng ở `std`).
  - `light` — làm chậm tốc độ lan Bóng Tối.

`NEXT` định nghĩa các công trình "họ làng" tiến hóa sang loại mới khi đạt cấp tối đa (vd: `village` → `city`). `VFAM` là tập các loại được tính là "làng/thành phố" khi kiểm tra điều kiện tiến hóa.

## 5. Bộ não luật chơi: `Game.up(t)`

Đây là hàm quan trọng nhất — quyết định ô `t` sẽ nâng cấp thành gì tiếp theo, dựa vào 4 ô kề còn sáng (`Game.nb`). Trả về `(loại_mới, cấp_mới, văn_bản_khóa)` hoặc `None`.

Thứ tự ưu tiên khi nâng cấp từ **Cánh đồng** (ô trống, `field` cấp 0):

1. Kề Làng phép thuật đã xây, chưa có Tháp ánh sáng nào → **Tháp ánh sáng** (cần Làng phép thuật đó cũng kề một Làng/Thành phố).
2. Kề Làng phép thuật + kề Nước, chưa có Tháp nước → **Tháp nước**.
3. Kề cả Rừng nấm và Nước → **Làng cảng phép thuật**.
4. Chỉ kề Rừng nấm → **Làng phép thuật**.
5. Kề ≥ 2 ô Đá → **Làng khai mỏ**.
6. Kề Nước → **Làng cảng**.
7. Mặc định → **Làng** thường.

Các luật đặc biệt khác:

- **Vòng Đá** cấp 0 → 1: cần có Làng phép thuật cấp ≥ 2 đã xây ở bất kỳ đâu trên bản đồ.
- **Rừng** cấp 3 kề Rừng rễ cây cấp 3, chưa có Nhà máy thuốc → **Nhà máy thuốc**.
- **Rừng** cấp 0 mà cả 4 ô kề đều là Rừng, chưa có Làng trên cây → **Làng trên cây**.
- **Đá** cấp 3, chưa có Trung tâm công nghệ đá → mở khóa, nhưng cần kề một Thành phố.
- **Nước**: kề Làng cảng/Thành phố cảng → **Bến tàu**, ngược lại → **Hải đăng**.
- **Thành phố nghiên cứu mỏ** cấp 0 → **Thành phố nghiên cứu ánh sáng** (công trình thắng, chỉ xây 1 lần duy nhất).
- Nếu còn cấp cao hơn trong `K[k]` → tăng thẳng 1 cấp.
- Nếu đã max cấp và thuộc `NEXT`: cần đủ 4 ô kề đã xây, HOẶC đủ N ô kề thuộc nhóm làng/thành phố (`VFAM`) mới được tiến hóa sang loại mới.

## 6. Tính toán sản lượng

- `Game.mult(t, r)` — hệ số nhân cho tài nguyên `r` của ô `t`: bắt đầu từ 1, cộng % boost từ mọi ô kề đã xây.
- `Game.recalc()` — duyệt toàn bản đồ, cộng dồn sản lượng (`s.rate`) và tổng "ánh sáng" (`s.light`, từ Tháp ánh sáng). Trung tâm công nghệ đá có luật riêng: tăng thêm sản lượng Đá của mọi ô Đá, tỉ lệ theo % sản lượng Khoa học hiện có.
- `Game.cost(d, k, l)` — giá tăng dần theo số công trình cùng loại đã xây (mỗi công trình đã xây làm giá +20%). Một số công trình độc nhất (Vòng Đá, Tháp, Trung tâm công nghệ đá, Nhà máy thuốc, Thành phố nghiên cứu ánh sáng) không áp dụng luật này. Chế độ `ext` có thêm hệ số giá ×1.5.

## 7. Bóng Tối lan — `spiral()` và `Game.tick()`

`spiral()` tính thứ tự các ô bị nuốt: bắt đầu từ góc dưới-trái, đi hết cạnh dưới sang phải, vòng lên cạnh phải, vòng sang cạnh trên, vòng xuống cạnh trái còn lại — tạo một vòng ngoài — rồi thu hẹp biên vào trong và lặp lại (giống "bóc vỏ" ma trận).

`Game.tick(dt)` mỗi khung hình:

- Cộng tài nguyên theo `s.rate`, nhân tốc độ game.
- Cộng dồn thời gian vào `s.dacc`. Chu kỳ nuốt ô (`iv`) = giá trị gốc theo chế độ (`std`=8s, `ext`=5.5s) nhân `(1 + 0.35 * s.light)` — **càng nhiều ánh sáng (Tháp ánh sáng) thì chu kỳ càng dài, Bóng Tối lan càng chậm**.
- Mỗi khi đủ một chu kỳ: nuốt thêm 1 ô, tính lại sản lượng, kiểm tra thua (không còn Vòng Đá nào sáng).

## 8. Vòng lặp chính (`main()`)

60 khung hình/giây. Mỗi khung hình:

1. Phát nhạc nền ngẫu nhiên (nếu đang chơi, chưa tắt nhạc).
2. Xử lý sự kiện: `Space` tạm dừng, `J` mở/đóng nhật ký, `Esc` thoát về menu/đóng nhật ký, click chuột để bấm nút hoặc nâng cấp ô (`Game.click`).
3. Gọi `Game.tick(dt)` cập nhật logic.
4. Vẽ lại: `draw_map()` (bản đồ + hiệu ứng tối dần + gợi ý), `draw_side()` (bảng tài nguyên/thông tin/nút), `draw_msg()` (thông báo), và `draw_journal()` nếu đang mở nhật ký.

## 9. Vẽ pixel-art (`draw_tile`, `icon`)

Mỗi ô được vẽ bằng các hình chữ nhật nhỏ (`r(màu, x, y, w, h)`) trên lưới ảo 9×9, phóng to theo hệ số `u`. Mỗi loại ô có hàm vẽ riêng (cây, nhà, nấm, tháp...). `icon()` cache lại hình đã vẽ để tái sử dụng trong bảng thông tin và nhật ký, tránh vẽ lại nhiều lần.
