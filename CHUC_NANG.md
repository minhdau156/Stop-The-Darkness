# Các chức năng trong game: Chặn Bóng Tối

## Màn hình Menu
- **Chọn chế độ:** Tiêu chuẩn (`std`) hoặc Mở rộng (`ext`).
- **Chơi!** — bắt đầu ván chơi.
- **Tạo lại bản đồ** — sinh ngẫu nhiên bản đồ mới (không cần vào chơi).
- **Nhật ký khu vực** — xem trước danh sách công trình đã khám phá.

## Khi đang chơi

**Bảng tài nguyên** (góc trên bên phải): hiển thị số lượng và tốc độ sinh mỗi phút của 4 tài nguyên (Gỗ, Đá, Phép thuật, Khoa học).

**Thông tin ô** (di chuột vào một ô trên bản đồ):
- Tên, cấp, mô tả của ô đang trỏ.
- Sản lượng hiện tại + % tăng cho ô kề (nếu đã xây).
- Nâng cấp tiếp theo là gì, chi phí, và gợi ý nếu đang bị khóa.
- Bấm vào ô để thực hiện nâng cấp (nếu đủ điều kiện + tài nguyên).

**Thanh nút điều khiển (dưới bảng bên phải):**

| Nút | Chức năng |
|---|---|
| ▶ / \|\| | Tạm dừng / Tiếp tục |
| `1x/2x/4x >>` | Đổi tốc độ game (bấm xoay vòng 1x → 2x → 4x) |
| Nhật ký | Mở sổ nhật ký khu vực |
| X | Thoát về menu (bản đồ bị xóa, phải chơi lại từ đầu) |
| Nhạc: Bật/Tắt | Bật/tắt nhạc nền ngẫu nhiên |
| Âm: Bật/Tắt | Bật/tắt hiệu ứng âm thanh (nâng cấp, thắng, thua...) |
| Sáng: Bật/Tắt | Viền xanh các ô đang đủ điều kiện + đủ tài nguyên để nâng cấp ngay |

**Sổ Nhật ký khu vực:** sưu tập mọi loại ô + cấp đã từng xây được (ô chưa tìm ra hiện "???"), chia thành nhiều trang theo chủ đề (Cơ bản, Rừng, Khai mỏ, Phép thuật...). Điều hướng bằng nút `<` `>`, đóng bằng nút `X`.

**Hộp thông báo:** hiện ở dưới bản đồ khi có sự kiện (hướng dẫn mở đầu, thông báo thắng/thua kèm nút "Về menu"/"Chơi lại"/"Tiếp tục").

## Phím tắt

| Phím | Chức năng |
|---|---|
| `Space` | Tạm dừng / tiếp tục |
| `J` | Mở/đóng Nhật ký |
| `Esc` | Đóng Nhật ký (nếu đang mở), hoặc thoát về menu |

## Âm thanh

Toàn bộ nhạc và hiệu ứng âm thanh được **sinh bằng công thức toán** (sóng sin) ngay trong code, không dùng file âm thanh.

## Điều kiện thắng

| Công trình | Cấp cuối | Thắng ở chế độ nào |
|---|---|---|
| Vòng Đá | Cấp 4 ("Chặn đứng bóng tối!") | Cả Tiêu chuẩn lẫn Mở rộng |
| Thành phố nghiên cứu ánh sáng | Cấp 2 ("Chặn đứng bóng tối!") | Cả Tiêu chuẩn lẫn Mở rộng |
| Tháp ánh sáng | Cấp 2 ("Làm chậm và chặn đứng bóng tối!") | Chỉ **Tiêu chuẩn** |

## Điều kiện thua

Khi tất cả Vòng Đá trên bản đồ đã bị Bóng Tối nuốt.
