# Hướng dẫn chiến thắng: Chặn Bóng Tối

**Mục tiêu duy nhất của game:** Xây xong một trong các công trình "chặn đứng bóng tối" trước khi bóng tối nuốt hết ô Vòng đá. Bạn thua ngay khi không còn ô Vòng đá nào còn sáng. 

> **Chiến thuật cốt lõi:** Chiến thắng = Phát triển kinh tế đủ nhanh để hoàn thành một trong các mục tiêu thắng trước khi bóng tối lan đến tâm bản đồ — hoặc làm chậm/đẩy lùi bóng tối để có thêm thời gian.

---

## 1. Hiểu cơ chế bóng tối

* **Quy luật di chuyển:** Bóng tối luôn bắt đầu từ góc dưới-trái, đi theo hình xoắn ốc ngược chiều kim đồng hồ, cuốn dần vào tâm. Thứ tự này cố định mỗi ván (phụ thuộc bản đồ $15 \times 12$), nên bạn có thể ước lượng trước ô nào sẽ bị nuốt sớm hay muộn.
* **Tốc độ lan:** Cứ sau một khoảng thời gian lại nuốt thêm 1 ô. Khoảng thời gian này tăng lên (lan chậm hơn) khi bạn có nhiều ánh sáng từ Tháp ánh sáng đã xây. Ở chế độ **Mở rộng**, bóng tối lan nhanh hơn đáng kể so với **Tiêu chuẩn**.
* **Hiệu ứng Đẩy lùi (Push):** Một số công trình có khả năng đẩy lùi bóng tối ngay khi xây xong (cờ `push`): Các cấp nâng cấp đầu của Vòng đá, và cấp đầu của Thành phố nghiên cứu ánh sáng. Đây là công cụ cứu nguy quan trọng khi bóng tối sắp đến gần Vòng đá.
* **Chiến lược:** Xây càng nhiều Tháp ánh sáng càng tốt để kéo dài thời gian, đồng thời chạy đua phát triển kinh tế để hoàn thành một mục tiêu thắng.

---

## 2. Ba con đường để thắng

| Con đường | Áp dụng | Tài nguyên cần | Độ khó |
| :--- | :--- | :--- | :--- |
| **Tháp ánh sáng cấp 2** | Chỉ chế độ Tiêu chuẩn | Gỗ, đá, phép thuật, một ít khoa học (200/100/100/20) | Dễ nhất, nhanh nhất |
| **Vòng đá cấp 4** | Cả 2 chế độ | Rất nhiều gỗ, đá, phép thuật (1000/1500/1000) | Trung bình-khó, cần kinh tế phép thuật mạnh |
| **Thành phố nghiên cứu ánh sáng cấp 2** | Cả 2 chế độ | Rất nhiều gỗ, đá, khoa học, không cần phép thuật (1200/1200/0/600) | Khó, cần kinh tế đá + khoa học rất mạnh |

> **Khuyến nghị:**
> * **Chế độ Tiêu chuẩn:** Hãy nhắm thắng bằng **Tháp ánh sáng** — rẻ nhất và lại có thêm tác dụng làm chậm bóng tối trong lúc chờ xây. 
> * **Chế độ Mở rộng:** Không dùng được lối tắt Tháp ánh sáng. Hãy so sánh xem bản đồ của bạn thuận lợi cho kinh tế phép thuật (nhiều Nấm) hay kinh tế đá/khoa học (nhiều Đá) hơn rồi chọn **Vòng đá** hay **Thành phố nghiên cứu ánh sáng** cho phù hợp.

---

## 3. Chiến thuật mở đầu (1-2 phút đầu)

1. **Xây Rừng trước tiên:** Bạn chỉ có 10 Gỗ ban đầu và không có tài nguyên nào khác, nên mọi thứ đều phải xuất phát từ gỗ. Hãy nhấn vào các ô Rừng gần Vòng đá để nâng cấp, tạo dòng tiền gỗ ổn định.
2. **Quan sát ô kề Vòng đá:** Cánh đồng kề Nấm sẽ thành Làng phép thuật — đây là mắt xích quan trọng nhất vì mở khoá cả Vòng đá lẫn Tháp ánh sáng. Nếu bản đồ có Nấm, ưu tiên hướng phát triển về phía đó.
3. **Dùng tính năng "Làm nổi bật" (viền xanh):** Nhanh chóng nhận ra ô nào đang có thể nâng cấp và đủ tiền, tránh mất thời gian rà soát thủ công.
4. **Không dàn trải quá rộng:** Đừng cố nâng cấp những ô xa Vòng đá hoặc xa khu vực bạn đang phát triển — thời gian và tài nguyên có hạn, hãy tập trung xây một cụm đặc kín quanh Vòng đá để các ô tăng ích (boost) cho nhau.

---

## 4. Lộ trình xây Tháp ánh sáng (nhanh nhất, chỉ áp dụng ở chế độ Tiêu chuẩn)

1. Nâng cấp Rừng để có gỗ đều.
2. Tìm một ô Cánh đồng (Field) kề ô Nấm (Mushroom) $\rightarrow$ Nâng cấp thành **Làng phép thuật**. Làng này cần tự sản xuất phép thuật từ các ô Nấm đã xây.
3. **Bắt buộc:** Làng phép thuật này phải nằm kề một Làng hoặc Thành phố thường (không phải phép thuật), nếu chưa có hãy nâng cấp thêm một Cánh đồng gần đó thành Làng thường.
4. Nâng cấp Làng phép thuật lên cấp 2 (cần tích lũy 20 gỗ + 10 đá + 5 phép thuật).
5. Khi đó, một ô Cánh đồng khác kề Làng phép thuật đó sẽ mở khoá thành **Tháp ánh sáng**. Xây cấp 1 trước (30/20/15 gỗ/đá/phép thuật) để bắt đầu làm chậm bóng tối ngay.
6. Tích lũy thêm tài nguyên (đặc biệt là 20 khoa học — cần xây thêm ít nhất một ô Đá để có khoa học) rồi nâng cấp Tháp lên cấp 2 (200/100/100/20) $\rightarrow$ **THẮNG NGAY** nhờ cờ `win=1`.

*Đây là con đường ngắn nhất vì chỉ cần 2 bước nâng cấp phép thuật + 2 bước nâng cấp tháp, không cần xây Thành phố.*

---

## 5. Lộ trình nâng cấp Vòng đá tối đa (dùng được ở cả 2 chế độ)

1. Làm theo bước 1-4 ở mục 4 để có **Làng phép thuật cấp 2** — điều kiện bắt buộc để mở khoá nâng cấp đầu tiên của Vòng đá.
2. Nâng cấp **Vòng đá lên cấp 2** (100 đá + 100 phép thuật) $\rightarrow$ Nhận được hiệu ứng đẩy lùi bóng tối ngay.
3. Nâng cấp **Vòng đá lên cấp 3** (100 gỗ + 300 đá + 300 phép thuật + 20 khoa học) $\rightarrow$ Đẩy lùi thêm lần nữa.
4. Xây dựng thêm nhiều Làng phép thuật và nâng cấp chúng lên Thành phố phép thuật để có nguồn phép thuật lớn, đồng thời xây thêm Rừng/Đá để có đủ gỗ và đá.
5. Khi đã tích lũy đủ 1000 gỗ + 1500 đá + 1000 phép thuật $\rightarrow$ Nâng cấp **Vòng đá lên cấp 4** $\rightarrow$ **THẮNG** (`win=2`, áp dụng mọi chế độ).

*Lưu ý: Chi phí này rất lớn so với Tháp ánh sáng, nên con đường này đòi hỏi xây dựng kinh tế rộng và cân nhắc dùng Tháp ánh sáng (nếu ở chế độ Tiêu chuẩn) để câu giờ trước.*

---

## 6. Lộ trình thay thế: Khai mỏ $\rightarrow$ Thành phố nghiên cứu ánh sáng

*Dùng khi bản đồ có ít Nấm nhưng nhiều Đá, hoặc bạn muốn tránh hoàn toàn phép thuật:*

1. Nâng cấp một Cánh đồng kề $\ge 2$ ô Đá $\rightarrow$ Thành **Làng khai mỏ**.
2. Nâng cấp Làng khai mỏ lên cấp 2, rồi chuyển thành **Thành phố nghiên cứu mỏ** (cần $\ge 4$ ô kề đã xây hoặc đủ làng/thành phố kề bên).
3. Nâng cấp Thành phố nghiên cứu mỏ lên cấp 2 để có sản lượng khoa học lớn.
4. Khi đủ điều kiện, Thành phố nghiên cứu mỏ sẽ mở khoá **Thành phố nghiên cứu ánh sáng** (duy nhất trên bản đồ). Xây cấp 1 (400/500/0/100) để đẩy lùi bóng tối.
5. Tiếp tục tích lũy đủ 1200 gỗ + 1200 đá + 600 khoa học, nâng cấp lên cấp 2 $\rightarrow$ **THẮNG** (`win=2`).

*Công nghệ đá (Trung tâm công nghệ đá) có thể hỗ trợ thêm con đường này vì nó làm tăng sản lượng đá dựa trên khoa học — nên đặt gần ô Đá và kề Thành phố.*

---

## 7. Mẹo tối ưu sản lượng

* **Cộng dồn % tăng ích:** Mỗi ô đã xây có thể tăng % sản lượng cho ô kề bên. Hệ số nhân từ nhiều ô kề cộng dồn (không phải nhân chồng nhau), nên hãy bao quanh một ô sản xuất chính bằng tối đa 4 ô tăng ích để đạt hiệu quả cao nhất.
* **Xây dựng theo cụm:** Các Làng/Thành phố thường tăng % cho nhau, nên đặt chúng sát nhau thay vì cách xa.
* **Chuẩn bị ô kề cho Thành phố:** Nâng cấp lên Thành phố (bước cuối của chuỗi Làng) cần $\ge 4$ ô kề đã xây hoặc đủ số làng/thành phố kề bên — hãy xây kín các ô xung quanh trước khi cần nâng cấp lớn.
* **Kiểm soát quy mô công trình:** Giá nâng cấp tăng 20% mỗi lần bạn đã xây thêm một công trình cùng loại — đừng xây quá nhiều Làng cùng một lúc mà hãy ưu tiên nâng cấp những ô đã có lên cấp cao hơn nếu có thể.
* **Tối ưu Trung tâm công nghệ đá:** Nếu xây Trung tâm công nghệ đá, hãy giữ sản lượng khoa học cao song song — càng nhiều khoa học, sản lượng Đá càng được cộng thêm.

---

## 8. Những sai lầm thường gặp khiến thua

* **Bỏ quên Vòng đá ban đầu:** Vì nó không sản xuất tài nguyên nên dễ bị lãng quên — nhưng nếu bóng tối đến gần nó mà chưa nâng cấp được, bạn thua ngay lập tức.
* **Không xây Tháp ánh sáng sớm:** Nếu chỉ tập trung làm kinh tế mà không xây ánh sáng, bóng tối lan với tốc độ đầy đủ và bạn sẽ hết giờ trước khi kịp hoàn thành mục tiêu thắng.
* **Phát triển quá xa trung tâm:** Nâng cấp những ô gần rìa bản đồ (nơi bị tối sớm) là lãng phí tài nguyên — ô đó sớm hay muộn cũng bị nuốt và ngừng sản xuất.
* **Quên điều kiện mở khoá:** Một số công trình cần ô kề bên cụ thể (ví dụ Làng phép thuật phải kề Làng thường mới nâng lên cấp 2 để mở Tháp). Nếu thấy thông báo khoá, hãy đọc kỹ gợi ý thay vì bỏ qua.
* **Chơi tốc độ cao mà không theo dõi:** Ở tốc độ 4x, thời gian trôi rất nhanh — nếu không chủ động nâng cấp liên tục, bạn sẽ mất nhiều thời gian cho bóng tối mà không kịp phản ứng.

---

## 9. Tận dụng các công cụ hỗ trợ trong game

* **Tốc độ (1x/2x/4x):** Tăng tốc khi bạn đang chờ tích lũy tài nguyên, giảm về 1x khi cần quan sát và ra quyết định xây cấp nhanh.
* **Phím `Space` để tạm dừng:** Dùng khi cần suy nghĩ kỹ nên nâng cấp ô nào tiếp theo mà không sợ bị bóng tối ăn lấn trong lúc do dự.
* **Nút "Làm nổi bật" (viền xanh quanh ô):** Luôn bật để nhanh chóng thấy ô nào đủ điều kiện và đủ tiền nâng cấp ngay, thay vì rê chuột từng ô để kiểm tra.
* **Nhật ký khu vực (Phím `J`):** Tra cứu lại các công trình đã khám phá và chi phí của chúng — hữu ích khi lập kế hoạch trước cho lộ trình thắng.
* **Bảng thông tin bên phải:** Rê chuột vào một ô luôn hiển thị rõ nâng cấp tiếp theo, chi phí và điều kiện mở khoá (nếu có) — dùng nó để lập kế hoạch trước nhiều bước thay vì bấm thử.