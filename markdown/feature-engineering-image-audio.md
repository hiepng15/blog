---
title: "Feature Engineering trong Xử lý Ảnh và Âm thanh: Từ Cổ điển đến Hiện đại"
date: "2025-01-26"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["feature engineering", "computer vision", "audio processing", "machine learning", "deep learning"]
excerpt: "Khám phá các kỹ thuật feature engineering kinh điển và hiện đại cho xử lý ảnh và âm thanh, từ HOG, SIFT đến MFCC, Spectrogram, và vai trò của chúng trong kỷ nguyên Deep Learning."
featured: false
---

## Giới thiệu

Trong thế giới của Machine Learning, "dữ liệu là vua". Nhưng dữ liệu thô (raw data) - dù là một bức ảnh hàng triệu pixel hay một file âm thanh hàng nghìn mẫu - hiếm khi có thể được sử dụng trực tiếp một cách hiệu quả. Đây là lúc **Feature Engineering** (Kỹ thuật Đặc trưng) tỏa sáng. Đó là nghệ thuật và khoa học của việc trích xuất, biến đổi và lựa chọn những đặc trưng (features) hữu ích từ dữ liệu thô để mô hình học máy có thể "hiểu" và đưa ra dự đoán chính xác hơn.

Ngay cả trong kỷ nguyên của Deep Learning, nơi các mô hình có khả năng tự học đặc trưng, feature engineering vẫn giữ một vai trò không thể thiếu. Bài viết này sẽ đi sâu vào các kỹ thuật feature engineering kinh điển và hiện đại cho hai lĩnh vực quan trọng: xử lý ảnh và âm thanh.

## Tại sao Feature Engineering vẫn quan trọng?

Nhiều người cho rằng các mạng nơ-ron sâu (Deep Neural Networks) đã khiến feature engineering trở nên lỗi thời. Điều này chỉ đúng một phần. Dưới đây là những lý do tại sao kỹ thuật này vẫn cực kỳ quan trọng:

1.  **Tăng hiệu suất với dữ liệu nhỏ**: Các mô hình Deep Learning cần một lượng dữ liệu khổng lồ để tự học đặc trưng hiệu quả. Với các bộ dữ liệu nhỏ hoặc vừa, việc cung cấp các đặc trưng được thiết kế tốt (hand-crafted features) có thể giúp mô hình hội tụ nhanh hơn và đạt độ chính xác cao hơn.
2.  **Tăng khả năng diễn giải (Interpretability)**: Đặc trưng do con người thiết kế (ví dụ: "mức độ đỏ" trong ảnh, "tần số cơ bản" trong giọng nói) thường dễ hiểu hơn rất nhiều so với các đặc trưng được học bởi một mạng nơ-ron sâu. Điều này rất quan trọng trong các lĩnh vực y tế, tài chính, nơi việc giải thích quyết định của mô hình là bắt buộc.
3.  **Giảm chi phí tính toán**: Việc trích xuất đặc trưng trước có thể làm giảm đáng kể kích thước của dữ liệu đầu vào, từ đó giảm thời gian huấn luyện và chi phí tính toán so với việc đưa toàn bộ dữ liệu thô vào một mô hình lớn.
4.  **Bổ sung cho Deep Learning**: Feature engineering có thể được sử dụng kết hợp với Deep Learning. Ví dụ, thay vì đưa ảnh thô, ta có thể đưa cả ảnh thô và các đặc trưng HOG của nó vào mô hình để cung cấp thêm "gợi ý" cho mạng.

---

## Feature Engineering cho Xử lý Hình ảnh (Computer Vision)

Hình ảnh là một ma trận các giá trị pixel. Mục tiêu của feature engineering là biến đổi ma trận này thành một tập hợp các đặc trưng mang nhiều thông tin hơn về nội dung của ảnh.

### 1. Histogram of Oriented Gradients (HOG)

-   **Ý tưởng**: HOG mô tả vật thể dựa trên sự phân bố hướng của gradient (độ dốc về cường độ sáng). Nó hoạt động dựa trên nguyên tắc rằng hình dạng và cấu trúc của một vật thể có thể được nhận dạng tốt bởi sự thay đổi cường độ sáng cục bộ, ngay cả khi bỏ qua màu sắc.
-   **Cách hoạt động**:
    1.  Ảnh được chia thành các ô (cell) nhỏ.
    2.  Trong mỗi ô, thuật toán tính toán gradient theo hướng x ($G_x$) và y ($G_y$).
    3.  Từ đó, tính toán độ lớn và hướng của gradient:
        -   Độ lớn: $G = \sqrt{G_x^2 + G_y^2}$
        -   Hướng: $\theta = \arctan\left(\frac{G_y}{G_x}\right)$
    4.  Một histogram của các hướng gradient được tạo ra cho mỗi ô. Các "phiếu bầu" vào histogram được trọng số hóa bởi độ lớn của gradient.
    5.  Các histogram của các ô lân cận được gộp lại thành các khối (block) và chuẩn hóa để chống lại sự thay đổi về ánh sáng.
    6.  Vector cuối cùng là sự kết hợp của tất cả các histogram đã được chuẩn hóa từ các khối.
-   **Ví dụ**: Rất thành công trong bài toán phát hiện người đi bộ.
-   **Ưu điểm**: Bất biến với thay đổi ánh sáng và biến dạng hình học nhỏ.
-   **Nhược điểm**: Không hiệu quả với các vật thể có cấu trúc phức tạp, dễ bị ảnh hưởng bởi xoay và thay đổi tỷ lệ lớn.

### 2. Scale-Invariant Feature Transform (SIFT)

-   **Ý tưởng**: SIFT là một thuật toán mạnh mẽ để phát hiện và mô tả các "điểm đặc trưng" (keypoints) cục bộ trong ảnh. Các đặc trưng này bất biến với thay đổi tỷ lệ (scale), xoay (rotation) và phần nào đó là thay đổi ánh sáng và góc nhìn.
-   **Cách hoạt động**:
    1.  **Phát hiện điểm đặc trưng**: Sử dụng hàm Differenc-of-Gaussian (DoG) trên nhiều tỷ lệ của ảnh để tìm các điểm cực trị (local extrema), đây chính là các keypoint.
    2.  **Định hướng cho Keypoint**: Gán một hoặc nhiều hướng cho mỗi keypoint dựa trên hướng gradient cục bộ để đạt được tính bất biến với phép xoay.
    3.  **Tạo mô tả Keypoint**: Một vùng 16x16 pixel xung quanh keypoint được lấy. Vùng này được chia thành 16 ô 4x4. Trong mỗi ô, một histogram 8 hướng được tính. Kết quả là một vector 128 chiều (16 ô * 8 hướng) mô tả keypoint đó.
-   **Ví dụ**: Ghép ảnh (image stitching), nhận dạng đối tượng, theo dõi vật thể.
-   **Ưu điểm**: Rất mạnh mẽ, bất biến với xoay, tỷ lệ, và thay đổi ánh sáng.
-   **Nhược điểm**: Chi phí tính toán cao, đã được cấp bằng sáng chế (dù đã hết hạn ở một số nơi). Các biến thể như SURF, ORB nhanh hơn.

### 3. Color Histograms (Lược đồ màu)

-   **Ý tưởng**: Là đặc trưng đơn giản nhất, mô tả sự phân bố của các màu sắc trong ảnh.
-   **Cách hoạt động**: Đếm số lượng pixel cho mỗi khoảng giá trị màu (bin) trong một không gian màu nhất định (ví dụ: RGB, HSV).
-   **Ví dụ**: Phân loại ảnh dựa trên bối cảnh (ví dụ: ảnh bãi biển thường có nhiều màu xanh dương và vàng cát).
-   **Ưu điểm**: Rất nhanh, đơn giản, bất biến với xoay và thay đổi vị trí của đối tượng.
-   **Nhược điểm**: Mất hoàn toàn thông tin về không gian và cấu trúc. Hai ảnh rất khác nhau có thể có cùng lược đồ màu.

### 4. Các đặc trưng khác

-   **Edge Detection (Dò cạnh)**: Sử dụng các bộ lọc như Sobel, Canny để tìm các đường biên của vật thể. Kết quả có thể được dùng làm đặc trưng nhị phân.
-   **Texture Features (Đặc trưng vân/kết cấu)**: Các phương pháp như Local Binary Patterns (LBP) hoặc bộ lọc Gabor mô tả kết cấu bề mặt của vật thể (ví dụ: vỏ cây, vải).
-   **PCA (Principal Component Analysis)**: Mặc dù là một kỹ thuật giảm chiều, PCA có thể được dùng để tạo đặc trưng. Ví dụ, trong nhận dạng khuôn mặt (Eigenfaces), các "thành phần chính" của một tập hợp ảnh mặt người được dùng làm đặc trưng.

---

## Feature Engineering cho Xử lý Âm thanh

Tín hiệu âm thanh là một chuỗi các mẫu theo thời gian. Feature engineering chuyển đổi chuỗi này thành các đặc trưng mô tả nội dung âm thanh như cao độ, âm sắc, nhịp điệu.

### 1. Spectrogram (Phổ kế)

-   **Ý tưởng**: Spectrogram là một biểu diễn hình ảnh của âm thanh, cho thấy sự thay đổi của phổ tần số theo thời gian. Nó là một trong những đặc trưng quan trọng nhất.
-   **Cách hoạt động**:
    1.  Tín hiệu âm thanh được chia thành các khung (frame) ngắn, chồng chéo nhau.
    2.  Áp dụng phép biến đổi Fourier (cụ thể là Short-Time Fourier Transform - STFT) cho từng khung để chuyển từ miền thời gian sang miền tần số.
    3.  Kết quả là một ma trận 2D, trong đó trục x là thời gian, trục y là tần số, và cường độ (màu sắc) là biên độ của tần số đó.
-   **Ví dụ**: Hầu hết các mô hình Deep Learning cho âm thanh (nhận dạng giọng nói, phân loại nhạc) đều sử dụng Spectrogram (hoặc biến thể của nó) làm đầu vào.
-   **Ưu điểm**: Cung cấp một biểu diễn giàu thông tin, trực quan.
-   **Nhược điểm**: Kích thước lớn, có thể chứa thông tin dư thừa.

### 2. Mel-Frequency Cepstral Coefficients (MFCC)

-   **Ý tưởng**: MFCC là đặc trưng mô tả hình dạng tổng thể của phổ âm thanh, được thiết kế để mô phỏng cách tai người cảm nhận âm thanh. Tai người nhạy cảm hơn với sự thay đổi ở tần số thấp so với tần số cao.
-   **Cách hoạt động**:
    1.  Tính toán Spectrogram từ tín hiệu.
    2.  Chuyển đổi trục tần số sang thang đo Mel (Mel scale) bằng cách sử dụng một bộ lọc tam giác (triangular filter bank).
    3.  Lấy log của năng lượng ở mỗi băng tần Mel.
    4.  Áp dụng phép biến đổi Cosine rời rạc (Discrete Cosine Transform - DCT) để thu được các hệ số MFCC. Phép DCT giúp giảm sự tương quan giữa các hệ số.
    $$c_n = \sum_{k=1}^{K} (\log S_k) \cos\left[n\left(k - \frac{1}{2}\right)\frac{\pi}{K}\right]$$
    Trong đó $c_n$ là hệ số MFCC thứ n, $S_k$ là năng lượng log của băng tần Mel thứ k, và K là tổng số băng tần.
-   **Ví dụ**: Là tiêu chuẩn vàng trong các hệ thống nhận dạng giọng nói cổ điển.
-   **Ưu điểm**: Biểu diễn nhỏ gọn, hiệu quả, mô phỏng tốt cảm nhận của con người.
-   **Nhược điểm**: Có thể loại bỏ một số thông tin về cao độ (pitch).

### 3. Chroma Features (Đặc trưng Sắc độ)

-   **Ý tưởng**: Mô tả sự phân bố năng lượng của tín hiệu qua 12 lớp cao độ (pitch classes) trong âm nhạc (C, C#, D, D#, E, F, F#, G, G#, A, A#, B).
-   **Ví dụ**: Rất hữu ích cho các tác vụ liên quan đến hòa âm như nhận dạng hợp âm, tìm kiếm bài hát theo giai điệu.
-   **Ưu điểm**: Bất biến với âm sắc (timbre), chỉ tập trung vào nội dung hòa âm.
-   **Nhược điểm**: Không hữu ích cho các tín hiệu không phải là nhạc.

### 4. Các đặc trưng khác

-   **Zero-Crossing Rate (ZCR)**: Đếm số lần tín hiệu đi qua giá trị 0 trong một khung. Đặc trưng này liên quan đến "độ nhiễu" của tín hiệu. ZCR cao thường thấy ở các âm vô thanh (như /s/) và thấp ở các âm hữu thanh (nguyên âm).
-   **Spectral Centroid (Tâm Phổ)**: Tính toán "tâm khối lượng" của phổ, cho biết tần số nào chiếm ưu thế. Nó liên quan đến sự "sáng" (brightness) của âm thanh.
-   **Spectral Rolloff, Flux, Flatness**: Các đặc trưng khác mô tả hình dạng của phổ.

---

## Khi nào nên dùng Feature Engineering thay vì Deep Learning?

Đây là câu hỏi quan trọng. Dưới đây là bảng so sánh giúp bạn quyết định:

| Tiêu chí | Feature Engineering Cổ điển | Deep Learning (End-to-End) |
|:---:|:---:|:---:|
| **Lượng dữ liệu** | Hiệu quả với dữ liệu nhỏ và vừa | Yêu cầu dữ liệu lớn |
| **Khả năng diễn giải** | Cao (đặc trưng có ý nghĩa) | Thấp (hộp đen) |
| **Chi phí tính toán** | Thấp hơn (cả huấn luyện và suy luận) | Cao, yêu cầu GPU/TPU |
| **Thời gian phát triển** | Cần nhiều kiến thức chuyên môn và thời gian để thiết kế | Nhanh hơn để thiết lập mô hình, nhưng cần nhiều thời gian tinh chỉnh |
| **Hiệu suất tối đa** | Có thể bị giới hạn bởi chất lượng đặc trưng | Thường đạt hiệu suất cao nhất với đủ dữ liệu |
| **Tính linh hoạt** | Kém linh hoạt, đặc trưng cho một tác vụ cụ thể | Rất linh hoạt, có thể học các tác vụ phức tạp |
| **Khả năng diễn giải** | Cao (đặc trưng có ý nghĩa) | Thấp (hộp đen) |
| **Chi phí tính toán** | Thấp hơn (cả huấn luyện và suy luận) | Cao, yêu cầu GPU/TPU |
| **Thời gian phát triển** | Cần nhiều kiến thức chuyên môn và thời gian để thiết kế | Nhanh hơn để thiết lập mô hình, nhưng cần nhiều thời gian tinh chỉnh |
| **Hiệu suất tối đa** | Có thể bị giới hạn bởi chất lượng đặc trưng | Thường đạt hiệu suất cao nhất với đủ dữ liệu |
| **Tính linh hoạt** | Kém linh hoạt, đặc trưng cho một tác vụ cụ thể | Rất linh hoạt, có thể học các tác vụ phức tạp |

**Khi nào nên ưu tiên Feature Engineering:**

-   Khi bạn có bộ dữ liệu nhỏ.
-   Khi bạn cần giải thích tại sao mô hình đưa ra quyết định đó.
-   Khi bạn bị giới hạn về tài nguyên tính toán.
-   Khi bạn có kiến thức chuyên môn sâu về lĩnh vực và có thể thiết kế các đặc trưng thực sự tốt.

**Khi nào nên ưu tiên Deep Learning:**

-   Khi bạn có một lượng dữ liệu khổng lồ.
-   Khi bài toán cực kỳ phức tạp và các đặc trưng thủ công không đủ để nắm bắt.
-   Khi hiệu suất là ưu tiên hàng đầu và bạn có đủ tài nguyên tính toán.

## Kết luận

Feature engineering không phải là một kỹ thuật lỗi thời mà là một công cụ mạnh mẽ và cần thiết trong kho vũ khí của bất kỳ nhà khoa học dữ liệu nào. Nó cung cấp khả năng kiểm soát, diễn giải và hiệu quả tính toán mà các mô hình end-to-end đôi khi còn thiếu. Hiểu rõ các đặc trưng kinh điển như HOG, SIFT cho hình ảnh và MFCC, Spectrogram cho âm thanh không chỉ giúp giải quyết các bài toán với phương pháp cổ điển mà còn cung cấp một nền tảng vững chắc để hiểu sâu hơn về cách các mô hình Deep Learning hoạt động và làm thế nào để kết hợp cả hai phương pháp một cách hiệu quả nhất.
