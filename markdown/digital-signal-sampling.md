---
title: "Tín hiệu số và Lấy mẫu: Cầu nối từ thế giới Analog đến công nghệ Digital"
date: "2025-01-25"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["Digital Signal", "Analog Signal", "Sampling", "Nyquist Theorem", "Quantization", "Computer Vision"]
excerpt: "Tìm hiểu về tín hiệu số và quá trình lấy mẫu - nền tảng cốt lõi của công nghệ số. Từ analog đến digital, hiểu rõ định lý Nyquist và ứng dụng trong Computer Vision."
featured: false
---

# Tín hiệu số và Lấy mẫu: Hiểu bản chất từ A đến Z

Trong loạt bài viết trước, chúng ta đã cùng tìm hiểu về các khái niệm cốt lõi của AI và Machine Learning. Để có thể đi sâu hơn vào lĩnh vực Computer Vision (Thị giác máy tính), việc hiểu rõ cách máy tính "nhìn" và xử lý thông tin là vô cùng quan trọng. Trước khi bắt đầu, chúng ta hãy cùng nhau tìm hiểu những kiến thức nền tảng về tín hiệu số và tín hiệu analog, hai khái niệm cốt lõi định hình cách máy tính tương tác với thế giới.

## 1. Tín hiệu Analog và Digital: Sự khác biệt cốt lõi

Thế giới xung quanh chúng ta là một thế giới của tín hiệu **Analog** (tương tự). Tín hiệu analog là tín hiệu liên tục trong cả thời gian và biên độ. Ví dụ, sóng âm từ giọng nói của bạn, nhiệt độ không khí, hay ánh sáng phản chiếu từ một vật thể đều là các tín hiệu analog. Chúng thay đổi một cách mượt mà và vô hạn.

Tuy nhiên, thế giới của máy tính lại là thế giới của các giá trị rời rạc. Máy tính không thể xử lý những giá trị vô hạn đó. Đó là lý do tín hiệu **Digital** (số) ra đời. Tín hiệu số có hai đặc điểm cốt lõi:

- **Rời rạc theo thời gian (Discrete in time)**: Tín hiệu chỉ được xác định tại các thời điểm cụ thể, chứ không phải mọi thời điểm.
- **Rời rạc theo biên độ (Discrete in amplitude)**: Biên độ của tín hiệu chỉ có thể nhận một trong một tập hợp hữu hạn các giá trị.

Nói một cách đơn giản, một tín hiệu số chỉ là một chuỗi các con số 0 và 1. Khả năng biểu diễn mọi thứ bằng các giá trị rời rạc này mang lại những lợi thế vượt trội: chống nhiễu tốt, dễ dàng lưu trữ và xử lý. Tín hiệu số bao gồm cả âm thanh số và hình ảnh số, chúng đều được biểu diễn bằng các giá trị rời rạc này.

## 2. Lấy mẫu (Sampling) - Cầu nối từ Analog sang Digital

Vậy làm thế nào để chuyển một tín hiệu Analog thành một tín hiệu Digital? Quá trình này được gọi là **Chuyển đổi Analog-to-Digital (ADC)** và bao gồm hai bước chính: **Lấy mẫu** và **Lượng tử hóa**.

**Lấy mẫu (Sampling)** là bước đầu tiên và quan trọng nhất. Đây là quá trình chúng ta "chụp ảnh" giá trị của tín hiệu Analog tại các khoảng thời gian đều đặn. Cứ sau mỗi khoảng thời gian **Ts**, chúng ta lại ghi lại một giá trị của tín hiệu.

Tham số quan trọng nhất của quá trình này là **tần số lấy mẫu (fs)**, được định nghĩa là số lượng mẫu lấy được trong một giây.

$$f_s = \frac{1}{T_s}$$

### 2.1. Định lý Nyquist-Shannon: Nền tảng của việc lấy mẫu

Để có thể tái tạo lại tín hiệu Analog ban đầu một cách hoàn hảo từ các mẫu rời rạc, chúng ta phải tuân theo một quy tắc vàng: **Định lý Nyquist-Shannon**.

Định lý này khẳng định rằng: **Tần số lấy mẫu (fs) phải lớn hơn hoặc bằng gấp đôi tần số cao nhất (fmax) của tín hiệu gốc**.

$$f_s \geq 2f_{max}$$

### 2.2. Ví dụ thực tế: Tần số âm thanh CD (44.1 kHz)

Đã bao giờ bạn để ý đến tần số âm thanh của đĩa CD thường là **44.1 kHz**?

Đây là một ví dụ thực tế hoàn hảo để minh họa cho Định lý Nyquist-Shannon.

1. **Giới hạn thính giác con người**: Tai người có thể nghe được âm thanh trong dải tần từ khoảng 20 Hz đến 20 kHz. Do đó, tần số cao nhất (fmax) mà chúng ta cần quan tâm khi số hóa âm thanh là 20 kHz.

2. **Áp dụng định lý Nyquist-Shannon**: Theo định lý, tần số lấy mẫu tối thiểu phải lớn hơn hoặc bằng gấp đôi tần số cao nhất:

$$f_s \geq 2 \times 20 \text{ kHz} = 40 \text{ kHz}$$

3. **Lý do chọn 44.1 kHz**: Các kỹ sư âm thanh không chọn chính xác 40 kHz, mà là 44.1 kHz. Lý do là để có một "khoảng đệm" an toàn. Khi chuyển đổi tín hiệu, người ta phải sử dụng một bộ lọc gọi là **bộ lọc chống Aliasing** để loại bỏ các tần số cao hơn 20 kHz trước khi lấy mẫu. Việc có thêm 4.1 kHz giúp bộ lọc này hoạt động hiệu quả hơn, đảm bảo rằng không có hiện tượng aliasing nào xảy ra, từ đó bảo toàn chất lượng âm thanh một cách hoàn hảo.

## 3. Aliasing - Vấn đề lớn nhất cần tránh

Điều gì sẽ xảy ra nếu chúng ta vi phạm định lý Nyquist-Shannon, tức là lấy mẫu với tần số:

$$f_s < 2f_{max}$$

Khi đó, một hiện tượng nghiêm trọng gọi là **Aliasing** (chồng lấn phổ) sẽ xảy ra.

Hãy tưởng tượng một chiếc bánh xe đang quay rất nhanh. Nếu bạn quay một bộ phim ở tốc độ khung hình thấp, bạn sẽ thấy chiếc bánh xe dường như quay chậm lại, thậm chí quay ngược chiều. Tương tự, aliasing khiến cho các tần số cao trong tín hiệu Analog bị "biến dạng" và được tái tạo thành các tần số thấp hơn trong tín hiệu số.

Hậu quả là tín hiệu sau khi được chuyển đổi và khôi phục sẽ bị sai lệch hoàn toàn so với bản gốc.

## 4. Lượng tử hóa (Quantization) - Bước hoàn thiện quá trình chuyển đổi

Sau khi lấy mẫu xong, chúng ta có một chuỗi các giá trị rời rạc theo thời gian, nhưng biên độ của chúng vẫn còn là giá trị liên tục. **Lượng tử hóa** là bước tiếp theo để gán cho mỗi giá trị đó một mức biên độ rời rạc, từ một tập hợp hữu hạn các mức.

Tham số quan trọng của lượng tử hóa là **độ phân giải (số bit)**. Mỗi bit cho phép chúng ta có 2¹ = 2 mức.

- **Với 8 bit**, ta có 2⁸ = 256 mức biên độ khác nhau.
- **Với 16 bit** (chuẩn CD), ta có 2¹⁶ = 65,536 mức.

Số bit càng lớn, số mức biên độ càng nhiều, quá trình lượng tử hóa càng chính xác và **lỗi lượng tử hóa (Quantization Error)** càng nhỏ. Lỗi này chính là sự sai khác giữa giá trị thực tế của tín hiệu và mức giá trị rời rạc mà nó được gán.

## 5. Tóm lại

Việc chuyển đổi tín hiệu từ Analog sang Digital là một quá trình hai bước: **Lấy mẫu** để rời rạc hóa theo thời gian và **Lượng tử hóa** để rời rạc hóa theo biên độ.

Để quá trình này diễn ra thành công và có thể tái tạo lại tín hiệu gốc một cách chính xác, việc tuân thủ **Định lý Nyquist-Shannon** là điều kiện tiên quyết. Đây là nền tảng cốt lõi của toàn bộ công nghệ số, từ âm nhạc, hình ảnh, đến các mô hình Computer Vision mà chúng ta sẽ khám phá ở những bài viết tiếp theo.

---

*Bài viết này cung cấp nền tảng kiến thức về tín hiệu số và quá trình lấy mẫu, là bước chuẩn bị quan trọng để hiểu sâu hơn về Computer Vision và xử lý hình ảnh số.* 