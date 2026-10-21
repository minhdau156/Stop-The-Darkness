# Tổng hợp chức năng game: Chặn Bóng Tối

Tài liệu này liệt kê toàn bộ loại ô và công trình trong game, cho mỗi cấp độ: chi phí xây dựng, sản lượng tài nguyên sinh ra mỗi phút, % tăng sản lượng cho ô kề bên, và các hiệu ứng đặc biệt (làm chậm/đẩy lùi bóng tối, điều kiện thắng). Dùng như bảng tra cứu nhanh khi lập kế hoạch xây dựng.

---

## 0. Bốn loại tài nguyên

| Tài nguyên | Màu | Nguồn chính |
| :--- | :--- | :--- |
| **Gỗ** | Nâu | Rừng, Làng, Thành phố |
| **Đá** | Xám | Đá, Trung tâm công nghệ đá, Thành phố |
| **Phép thuật** | Tím | Rừng nấm, Rừng rễ cây, Làng phép thuật |
| **Khoa học** | Vàng-xanh | Thành phố, Hải đăng, Thành phố nghiên cứu mỏ |

> **Lưu ý:** Tài nguyên khởi đầu: **10 Gỗ**, các loại khác đều là **0**. Mọi thứ trong game đều xuất phát từ việc khai thác Gỗ đầu tiên.

---

## 1. Cơ bản, thành phố và nước

*Cánh đồng (`field`) và Nước (`water`) là ô gốc trung tính, không tự có cấp độ — chúng rẽ nhánh thành các loại Làng bên dưới tùy ô kề bên (Field thành Làng/Làng cảng/Làng khai mỏ/Làng phép thuật...; Water thành Bến tàu hoặc Hải đăng).*

| Công trình | Cấp | Chi phí | Sản lượng/phút | Tăng ích ô kề | Ghi chú |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Làng** | 1 | 7 Gỗ | — | +25% Gỗ, +25% Đá | Từ Cánh đồng không kề Nước/Đá/Nấm |
| **Làng** | 2 | 12 Gỗ + 12 Đá | — | +50% Gỗ, +50% Đá | Cần $\ge 4$ ô kề đã xây hoặc $\ge 2$ làng/thành phố kề để lên Thành phố |
| **Thành phố** | 1 | 15 Gỗ + 60 Đá + 10 Khoa | 2.5 Khoa | +50% Gỗ, +50% Đá | Nâng cấp từ Làng cấp 2 |
| **Thành phố** | 2 | 40 Gỗ + 150 Đá + 30 Khoa | 6.2 Khoa | +50% Gỗ, +50% Đá, +25% Khoa | Cấp tối đa |
| **Làng cảng** | 1 | 5 Gỗ | 2 Gỗ | +25% Gỗ, +25% Đá | Từ Cánh đồng kề Nước |
| **Làng cảng** | 2 | 45 Gỗ + 18 Đá | 6 Gỗ | +50% Gỗ, +50% Đá | |
| **Thành phố cảng** | 1 | 120 Gỗ + 60 Đá + 10 Khoa | 12 Gỗ + 6 Đá + 2.5 Khoa | +50% Gỗ, +50% Đá | |
| **Thành phố cảng** | 2 | 300 Gỗ + 150 Đá + 40 Khoa | 25 Gỗ + 12 Đá + 6 Khoa | +50% Gỗ, +50% Đá, +25% Khoa | Cấp tối đa |
| **Bến tàu** | 1 | 20 Gỗ + 10 Đá | 6 Gỗ | +25% Gỗ, +25% Đá | Từ Nước kề Làng cảng; chỉ 1 cấp |
| **Hải đăng** | 1 | 15 Gỗ + 15 Đá | 1 Khoa | +25% Gỗ, +25% Đá | Từ Nước không kề Làng cảng; chỉ 1 cấp |

---

## 2. Rừng và gỗ

| Công trình | Cấp | Chi phí | Sản lượng/phút | Tăng ích ô kề | Ghi chú |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Rừng** | 1 | Miễn phí (ô gốc) | 3 Gỗ | +25% Gỗ | |
| **Rừng** | 2 | 3 Gỗ | 4.5 Gỗ | +25% Gỗ | |
| **Rừng** | 3 | 7 Gỗ | 8.7 Gỗ | +25% Gỗ | |
| **Rừng** | 4 | 15 Gỗ | 22.5 Gỗ | +25% Gỗ | Nếu có 4 ô Rừng kề 1 ô Rừng cấp 1 thì ô đó thành Làng trên cây thay vì lên cấp |
| **Làng trên cây** | 1 | 15 Gỗ | 10 Gỗ + 1 Khoa | +50% Gỗ | |
| **Làng trên cây** | 2 | 30 Gỗ + 5 Khoa | 22.5 Gỗ + 2 Khoa | +100% Gỗ | |
| **Làng trên cây** | 3 | 100 Gỗ + 20 Đá + 20 Phép | 40 Gỗ + 5 Khoa | +100% Gỗ | Cấp tối đa |

---

## 3. Khai mỏ

| Công trình | Cấp | Chi phí | Sản lượng/phút | Tăng ích ô kề | Ghi chú |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Đá** | 1 | Miễn phí (ô gốc) | 3 Đá | — | |
| **Đá** | 2 | 8 Gỗ | 3 Đá | — | |
| **Đá** | 3 | 10 Gỗ + 3 Đá | 7 Đá | — | |
| **Đá** | 4 | 15 Gỗ + 12 Đá + 2 Khoa | 30 Đá | +25% Khoa | |
| **Đá** | 5 | 10 Gỗ + 60 Đá + 8 Khoa | 60 Đá + 4 Khoa | +33% Khoa | Cần có Trung tâm công nghệ đá trên bản đồ |
| **Trung tâm công nghệ đá** | 1 | 200 Gỗ + 100 Đá + 50 Khoa | 100 Đá + 8.7 Khoa | +50% Đá, +25% Khoa | Từ Đá cấp 4 kề 1 thành phố; duy nhất trên bản đồ; tăng sản lượng đá của mọi ô Đá theo sản lượng khoa học |
| **Trung tâm công nghệ đá** | 2 | 400 Gỗ + 200 Đá + 200 Khoa | 75 Đá + 15 Khoa | +50% Đá, +50% Khoa | Cấp tối đa |
| **Làng khai mỏ** | 1 | 10 Gỗ + 5 Đá | 5 Khoa | +50% Khoa | Từ Cánh đồng kề $\ge 2$ ô Đá |
| **Làng khai mỏ** | 2 | 30 Gỗ + 30 Đá | 12 Khoa | +50% Khoa | |
| **Thành phố nghiên cứu mỏ** | 1 | 60 Gỗ + 100 Đá + 10 Khoa | 3 Khoa | +50% Đá, +25% Khoa | |
| **Thành phố nghiên cứu mỏ** | 2 | 200 Gỗ + 300 Đá + 30 Khoa | 6 Khoa | +50% Đá, +25% Khoa | Mở khoá Thành phố nghiên cứu ánh sáng |
| **Thành phố nghiên cứu ánh sáng** | 1 | 400 Gỗ + 500 Đá + 100 Khoa | 8 Khoa | +50% Đá, +25% Khoa | Đẩy lùi bóng tối; duy nhất trên bản đồ |
| **Thành phố nghiên cứu ánh sáng** | 2 | 1200 Gỗ + 1200 Đá + 600 Khoa | 12 Khoa | +50% Đá, +50% Khoa | **THẮNG GAME** (không cần Phép thuật) |

---

## 4. Phép thuật

| Công trình | Cấp | Chi phí | Sản lượng/phút | Tăng ích ô kề | Ghi chú |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Rừng nấm** | 1 | Miễn phí (ô gốc) | 1.2 Gỗ + 2 Phép | +25% Phép | |
| **Rừng nấm** | 2 | 6 Gỗ | 1.2 Gỗ + 2 Phép | +25% Phép | |
| **Rừng nấm** | 3 | 20 Gỗ + 2 Phép | 3.5 Gỗ + 7 Phép | +25% Phép | |
| **Thành phố nấm** | 1 | 50 Gỗ + 30 Phép + 5 Khoa | 10 Gỗ + 20 Phép + 2 Khoa | +50% Phép, +25% Khoa | Cấp duy nhất |
| **Rừng rễ cây** *(Mở rộng)* | 1-4 | Miễn phí $\rightarrow$ 10G $\rightarrow$ 25G+5P $\rightarrow$ 60G+15P | 2G+3P $\rightarrow$ 2G+3P $\rightarrow$ 8G+12P $\rightarrow$ 20G+24P | +25% Gỗ, +25% Phép | Chỉ Chế độ Mở rộng |
| **Thành phố rễ cây** *(Mở rộng)* | 1 | 100G + 60P + 10K | 20G + 40P + 3K | +25% Gỗ, +50% Phép | Chỉ Chế độ Mở rộng; Cấp duy nhất |
| **Vòng đá** | 1 | Miễn phí (ô gốc duy nhất trên bản đồ) | — | — | Mở khoá cấp 2 khi có Làng phép thuật cấp 2 bất kỳ đâu |
| **Vòng đá** | 2 | 100 Đá + 100 Phép | — | — | Đẩy lùi bóng tối |
| **Vòng đá** | 3 | 100G + 300Đ + 300P + 20K | — | — | Đẩy lùi bóng tối thêm |
| **Vòng đá** | 4 | 1000G + 1500Đ + 1000P | — | — | **THẮNG GAME** (mọi chế độ) |
| **Làng phép thuật** | 1 | 5G + 1P | 2 Phép | +25% Gỗ, +25% Phép | Từ Cánh đồng kề Nấm; kề 1 Làng để mở Tháp ánh sáng |
| **Làng phép thuật** | 2 | 20G + 10Đ + 5P | 5 Phép | +50% Gỗ, +50% Phép | Mở khoá nâng cấp Vòng đá |
| **Thành phố phép thuật** | 1 | 60G + 30Đ + 20P + 10K | 10 Phép + 2 Khoa | +50% Phép, +25% Khoa | Cấp duy nhất |
| **Làng cảng phép thuật** | 1 | 7G + 1P | 2G + 2P | +25% Gỗ, +25% Phép | Từ Cánh đồng kề cả Nấm lẫn Nước |
| **Làng cảng phép thuật** | 2 | 45G + 18Đ + 6P | 4G + 5P | +50% Gỗ, +50% Phép | |
| **Thành phố cảng phép thuật** | 1 | 120G + 60Đ + 20P + 10K | 8G + 4Đ + 10P + 2K | +50% Phép, +50% Phép | Cấp duy nhất |
| **Tháp ánh sáng** | 1 | 30G + 20Đ + 15P | 1.2 Phép | +25% Phép | Từ Cánh đồng kề Làng phép thuật (đã cấp 2, kề Làng); làm chậm bóng tối |
| **Tháp ánh sáng** | 2 | 200G + 100Đ + 100P + 20K | 6 Phép | +50% Phép | Làm chậm mạnh hơn; **THẮNG** (chỉ chế độ Tiêu chuẩn) |

---

## 5. Phép thuật (tiếp)

| Công trình | Cấp | Chi phí | Sản lượng/phút | Tăng ích ô kề | Ghi chú |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Tháp nước** | 1 | 100G + 50Đ + 50P + 10K | 5 Phép + 3 Khoa | +50% Phép, +25% Khoa | Từ Cánh đồng kề Làng phép thuật và Nước; duy nhất; cấp duy nhất |
| **Nhà máy thuốc** *(Mở rộng)* | 1 | 80G + 40Đ + 40P + 10K | 5 Phép + 10 Khoa | +50% Khoa | Chỉ Chế độ Mở rộng; Từ Rừng cấp 4 kề Rừng rễ cây cấp 4; duy nhất; cấp duy nhất |

---

## 6. Công trình đặc biệt & Quy tắc hiệu ứng

- **Duy nhất trên bản đồ (chỉ xây được 1 cái):** Vòng đá (ô gốc cố định), Trung tâm công nghệ đá, Tháp ánh sáng, Tháp nước, Thành phố nghiên cứu ánh sáng, Nhà máy thuốc.
- **Có hiệu ứng đẩy lùi bóng tối (push):** Lùi ngay 12 ô trong thứ tự xoắn ốc khi xây xong:
  - Vòng đá cấp 2
  - Vòng đá cấp 3
  - Thành phố nghiên cứu ánh sáng cấp 1
- **Làm chậm bóng tối (light):** Tăng khoảng cách/thời gian giữa các lần lan:
  - Tháp ánh sáng cấp 1 (nhẹ)
  - Tháp ánh sáng cấp 2 (mạnh hơn)
- **Điều kiện thắng trực tiếp (win):**
  - **Thắng ở mọi chế độ:** Vòng đá cấp 4, Thành phố nghiên cứu ánh sáng cấp 2.
  - **Thắng chỉ ở chế độ Tiêu chuẩn:** Tháp ánh sáng cấp 2 *(ở chế độ Mở rộng, xây Tháp cấp 2 vẫn có ích để làm chậm bóng tối nhưng không tự thắng)*.

---

## 7. Khác biệt giữa hai chế độ

| Đặc tính | Tiêu chuẩn | Mở rộng |
| :--- | :--- | :--- |
| **Tốc độ lan bóng tối** | Chậm hơn (khoảng thời gian gốc 8 giây) | Nhanh hơn (khoảng thời gian gốc 5.5 giây) |
| **Giá cả** | Giá tiêu chuẩn | Mọi giá nhân thêm 1.5 lần |
| **Công trình riêng** | Không có Rừng rễ cây / Thành phố rễ cây / Nhà máy thuốc | Có thêm Rừng rễ cây, Thành phố rễ cây, Nhà máy thuốc |
| **Thắng bằng Tháp ánh sáng Cấp 2** | Có, thắng ngay | Không tự thắng, chỉ làm chậm bóng tối |
| **Cách thắng duy nhất còn lại** | Vòng đá cấp 4 hoặc Thành phố nghiên cứu ánh sáng cấp 2 | Vòng đá cấp 4 hoặc Thành phố nghiên cứu ánh sáng cấp 2 |

> **Tóm tắt chiến thuật:** Chế độ Tiêu chuẩn phù hợp để chơi nhanh và học luật, còn chế độ Mở rộng thử thách hơn với tài nguyên và ép buộc phải đi theo con đường Vòng đá hoặc Thành phố nghiên cứu ánh sáng.