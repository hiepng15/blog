---
title: "NLP, LLM và Computer Vision: Hiểu đúng các khái niệm nền tảng"
date: "2025-01-25"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["NLP", "LLM", "Computer Vision", "Machine Learning", "AI", "Deep Learning"]
excerpt: "Tìm hiểu về NLP, LLM và Computer Vision từ góc nhìn khác về khái niệm machine learning. Hiểu rõ mối quan hệ giữa các lĩnh vực ứng dụng và cách thức học."
featured: false
---

# NLP, LLM và Computer Vision: Hiểu đúng các khái niệm nền tảng

Trong bài viết lần trước, chúng ta đã cùng tìm hiểu về khái niệm của Machine Learning và ba cách thức học cơ bản của nó. Tuy nhiên, đó chỉ là một trong những cách tiếp cận. Hôm nay, chúng ta sẽ nhìn Machine Learning ở một góc độ khác, cụ thể hơn là dựa trên các lĩnh vực ứng dụng nổi bật, bao gồm NLP, LLM và Computer Vision.

Đây là ba khái niệm cốt lõi, thường xuyên được nhắc đến khi bàn luận về các ứng dụng thực tế của AI. Vậy chúng là gì và khác nhau ra sao? Hãy cùng tìm hiểu qua bài viết này nhé.

## 1. Phân loại Machine Learning: Hai góc nhìn khác nhau

Trong Machine Learning, có hai cách chính để phân loại các mô hình, tùy thuộc vào góc nhìn của chúng ta.

### 1.1. Phân loại theo cách thức học (góc độ thuật toán)

Đây là cách phân loại cơ bản và mang tính học thuật, dựa trên cách mà mô hình học từ dữ liệu. Dựa vào bản chất của dữ liệu đầu vào và mục tiêu học, chúng ta có 3 loại chính:

- **Học có giám sát (Supervised Learning)**: Giống như một học sinh có giáo viên. Mô hình được cung cấp dữ liệu đã có "đáp án" (nhãn) và nhiệm vụ của nó là học cách đưa ra đáp án chính xác.

- **Học không giám sát (Unsupervised Learning)**: Giống như học sinh tự học. Mô hình được cung cấp dữ liệu không có "đáp án" và phải tự tìm ra các cấu trúc, quy luật, hoặc mối liên hệ ẩn bên trong.

- **Học tăng cường (Reinforcement Learning)**: Giống như một đứa trẻ học qua thử và sai. Mô hình tương tác với môi trường và học cách hành động để nhận được "phần thưởng" cao nhất.

### 1.2. Phân loại theo lĩnh vực ứng dụng (góc độ bài toán)

Đây là cách phân loại dựa trên loại dữ liệu đầu vào và mục tiêu của bài toán mà AI cần giải quyết. Đây chính là lúc các thuật ngữ như NLP, LLM và Computer Vision xuất hiện.

Mối quan hệ giữa hai cách phân loại này rất đơn giản: một lĩnh vực ứng dụng sẽ sử dụng một hoặc nhiều cách thức học để giải quyết các bài toán của nó.

## 2. Hiểu về NLP, LLM và Computer Vision

### 2.1. Xử lý Ngôn ngữ Tự nhiên (Natural Language Processing - NLP)

Nếu bạn đang cố gắng trò chuyện với một chiếc máy tính, NLP chính là lĩnh vực của AI giúp máy tính hiểu được bạn.

NLP là một lĩnh vực rộng lớn, nghiên cứu cách máy tính tương tác với ngôn ngữ tự nhiên của con người. Mục tiêu của NLP là giúp máy tính có thể đọc, giải mã, hiểu và tạo ra ngôn ngữ có ý nghĩa. Các mô hình NLP thường sử dụng thuật toán Học có giám sát hoặc Học không giám sát.

**Một số ứng dụng của NLP:**

1. **Phân tích cảm xúc**: Xác định xem một bài đánh giá sản phẩm là tích cực hay tiêu cực.
2. **Dịch thuật tự động**: Dịch văn bản từ ngôn ngữ này sang ngôn ngữ khác (ví dụ: Google Translate).
3. **Tóm tắt văn bản**: Tự động rút gọn một văn bản dài thành các ý chính.
4. **Chatbot**: Xây dựng các bot trả lời tự động dựa trên câu hỏi của người dùng.

### 2.2. Mô hình Ngôn ngữ Lớn (Large Language Model - LLM)

Nếu NLP là cả một lĩnh vực rộng lớn, thì LLM là một bước tiến vượt bậc trong lĩnh vực đó. LLM là một loại mô hình học máy tiên tiến, thường sử dụng Deep Learning, được huấn luyện trên một lượng dữ liệu khổng lồ từ Internet. Nhờ vậy, chúng có khả năng hiểu và tạo ra văn bản một cách cực kỳ tự nhiên và phức tạp.

Bạn có thể coi LLM như một "bộ não" siêu việt được xây dựng để xử lý ngôn ngữ. Ví dụ nổi bật nhất của LLM chính là ChatGPT.

**Mối quan hệ giữa NLP và LLM**: LLM là một loại mô hình của NLP, nhưng ở một cấp độ cao hơn hẳn. Trong khi NLP có thể bao gồm những tác vụ đơn giản, LLM tập trung vào việc tạo ra và hiểu ngôn ngữ ở mức độ sâu hơn nhiều, thường là nhờ sự kết hợp của các thuật toán Học không giám sát và Học có giám sát.

### 2.3. Thị giác Máy tính (Computer Vision)

Nếu NLP và LLM tập trung vào ngôn ngữ, thì Computer Vision là lĩnh vực giúp máy tính "nhìn thấy" và hiểu thế giới qua hình ảnh và video.

Computer Vision là một lĩnh vực của AI, cho phép máy tính trích xuất, phân tích và hiểu thông tin từ các hình ảnh số. Hầu hết các ứng dụng của Computer Vision đều sử dụng các thuật toán Học có giám sát và Học không giám sát để giải quyết bài toán.

**Một số ứng dụng của Computer Vision:**

1. **Nhận dạng khuôn mặt**: Mở khóa điện thoại bằng khuôn mặt hoặc camera an ninh.
2. **Xe tự lái**: Nhận biết người đi bộ, đèn giao thông và các phương tiện khác.
3. **Phân tích hình ảnh y tế**: Giúp bác sĩ phát hiện các dấu hiệu bệnh tật từ ảnh chụp X-quang hoặc MRI.

## 3. Kết luận

Hy vọng bài viết này đã giúp bạn có một cái nhìn rõ ràng hơn về các khái niệm quan trọng này trong thế giới AI. Việc hiểu được mối quan hệ giữa các cách phân loại Machine Learning và các lĩnh vực ứng dụng cụ thể sẽ giúp bạn có cái nhìn toàn diện hơn về thế giới AI đang phát triển nhanh chóng.

---

*Bài viết này tiếp nối bài viết trước về AI, Machine Learning và AI Agent, cung cấp góc nhìn khác về cách phân loại và ứng dụng của Machine Learning.* 