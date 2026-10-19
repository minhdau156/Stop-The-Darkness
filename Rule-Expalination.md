# Luật chơi: Stop the Darkness

## Mục tiêu
Ngăn bóng tối nuốt bản đồ. Thắng bằng nghiên cứu hoặc bằng cách đẩy lùi bóng tối hoàn toàn.

## Tài nguyên (resources)
4 loại: **Wood** (gỗ), **Stone** (đá), **Magic** (phép), **Research** (nghiên cứu).
Bắt đầu: 10 Wood, 0 các loại khác.

## Các loại ô (tile) trên bản đồ
- **Field** (đất trống): ô để xây công trình.
- **Forest** (rừng) → nâng cấp thành **Lumber Camp** (trại gỗ).
- **Stone** (mỏ đá) → nâng cấp thành **Quarry** (mỏ khai thác).
- **Water** (nước): không xây được, cũng không bị bóng tối lan vào.
- **Village** (làng) → **Town** (thị trấn) → **City** (thành phố).
- **Port** (cảng) → **Mainport** (cảng chính).
- **Magic Grove** (rừng phép).
- **Stone Circle** (vòng đá): 3 trạng thái — Dormant (ngủ) → Awake (tỉnh) → Empowered (toàn năng).
- **Darkness** (bóng tối): ô bị bóng tối chiếm.

Bản đồ khởi tạo ngẫu nhiên: 12% Water, 22% Forest, 16% Stone, còn lại là Field. Vòng đá (Stone Circle) đặt ở giữa bản đồ, trạng thái Dormant. 4 góc bản đồ bắt đầu là Darkness.

## Cách xây làng và các công trình khác

### Bước 1: Khai thác tài nguyên cơ bản (miễn phí)
- Click vào ô **Forest** → tự động thành **Lumber Camp** (không tốn tài nguyên).
- Click vào ô **Stone** → tự động thành **Quarry** (không tốn tài nguyên).

### Bước 2: Xây trên ô Field
Ở bảng bên phải (panel), chọn 1 trong 3 lựa chọn xây dựng. Sau đó click vào ô Field để xây.

| Công trình | Chi phí | Điều kiện |
|---|---|---|
| Village (làng) | 10 Wood | Phải có Lumber Camp liền kề |
| Port (cảng) | 8 Wood | Phải có Water liền kề |
| Magic Grove | 10 Wood + 5 Research | Phải có ≥2 Lumber Camp liền kề |

"Liền kề" nghĩa là 1 trong 4 ô trên/dưới/trái/phải (không tính chéo).

### Bước 3: Nâng cấp tiếp
Click vào công trình đã xây để nâng cấp lên bậc kế tiếp.

| Từ | Lên | Chi phí | Điều kiện |
|---|---|---|---|
| Village | Town | 15 Wood + 10 Stone | Liền kề 1 Quarry |
| Town | City | 20 Wood + 20 Stone + 10 Research | Liền kề 1 Town hoặc City |
| Port | Mainport | 15 Stone + 15 Magic | Có ≥3 Port/Mainport bất kỳ đâu trên bản đồ |

### Vòng đá (Stone Circle)
| Từ | Lên | Chi phí |
|---|---|---|
| Dormant | Awake | 30 Stone + 20 Magic |
| Awake | Empowered | 40 Stone + 40 Magic + 20 Research |

Trạng thái vòng đá quyết định bóng tối lan hay lùi (xem phần dưới).

## Sản xuất tài nguyên (mỗi giây 1 lần)
- Village: +1 Research. Town: +2 Research. City: +4 Research.
- Port: +1 Magic. Mainport: +3 Magic, +2 Research.
- Stone Circle Empowered: +2 Research.
- Lumber Camp: +1 Wood cơ bản. Quarry: +1 Stone cơ bản. Magic Grove: +2 Magic cơ bản.
- Lumber Camp, Quarry, Magic Grove được **boost** (tăng thêm) nếu có Town/City liền kề: +1 cho mỗi Town liền kề, +2 cho mỗi City liền kề.

## Bóng tối (Darkness) tăng như thế nào
Cứ mỗi 5 giây, hệ thống kiểm tra trạng thái Vòng đá:

- **Dormant (ngủ)**: mỗi ô Darkness có **35% xác suất** lan sang 1 ô liền kề ngẫu nhiên (không lan vào Water, không lan vào ô Vòng đá, không lan vào ô Darkness khác).
- **Awake (tỉnh)**: bóng tối **ngừng lan** hoàn toàn. Không lùi, không tiến.
- **Empowered (toàn năng)**: bóng tối **lùi lại** — tối đa 2 ô Darkness ngẫu nhiên biến trở lại thành Field mỗi 5 giây.

### Darkness Wisp (bóng ma)
- Cứ khoảng 15 giây, nếu bản đồ có ô Darkness và có công trình giá trị, 1 con Wisp xuất hiện.
- Wisp đi từ 1 ô Darkness, nhắm đến công trình giá trị **gần nhất** (Lumber Camp, Quarry, Village, Town, City, Port, Mainport, Magic Grove).
- Nếu Wisp đến nơi, công trình đó **biến thành Darkness ngay lập tức**.
- Người chơi click trúng Wisp để giết nó, nhận thưởng +5 Wood.

## Điều kiện Thắng (2 cách, đạt 1 trong 2 là thắng)
1. **Research ≥ 150**.
2. Vòng đá ở trạng thái **Empowered** VÀ số ô Darkness trên bản đồ = **0**.

## Điều kiện Thua
Số ô Darkness chiếm **≥ 60%** tổng số ô bản đồ (bản đồ 16×12 = 192 ô, tức khoảng 115 ô trở lên là Darkness).

## Chiến lược gợi ý
1. Khai thác Forest/Stone sớm để có Wood/Stone miễn phí.
2. Xây Village gần Lumber Camp, rồi nâng Quarry liền kề để lên Town.
3. Đưa Vòng đá lên Awake sớm để chặn lan bóng tối, rồi tích lũy để lên Empowered và đẩy lùi.
4. Luôn để ý Wisp xuất hiện — không giết kịp sẽ mất công trình.
