---
title: "Feature Engineering trong Python (Phần 1): Pandas, Numpy, và Scikit-learn"
date: "2025-01-27"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["python", "feature engineering", "pandas", "numpy", "scikit-learn", "machine learning"]
excerpt: "Hướng dẫn chuyên sâu về kỹ thuật đặc trưng (feature engineering) trong Python sử dụng các thư viện mạnh mẽ như Pandas, Numpy, và Scikit-learn, từ xử lý dữ liệu đến chuẩn hóa và tạo đặc trưng."
featured: false
---

## Giới thiệu: Feature Engineering là gì?

Trong một pipeline Machine Learning, Feature Engineering (FE) là bước tiền xử lý dữ liệu nhằm tạo ra các đặc trưng (features) mới hoặc biến đổi các đặc trưng hiện có để cải thiện hiệu suất của mô hình. Dữ liệu tốt và các đặc trưng phù hợp thường quan trọng hơn cả việc lựa chọn thuật toán phức tạp. Một mô hình đơn giản với các đặc trưng tốt có thể vượt qua một mô hình phức tạp với các đặc trưng kém chất lượng.

Trong bài viết này, chúng ta sẽ khám phá cách thực hiện Feature Engineering trong Python bằng ba công cụ không thể thiếu: **Pandas** cho thao tác dữ liệu, **Numpy** cho tính toán số học hiệu suất cao, và **Scikit-learn** cho các bộ tiền xử lý tiêu chuẩn.

---

## 1. Pandas: Người bạn đồng hành cho thao tác dữ liệu

Pandas là công cụ mạnh mẽ nhất để làm sạch, biến đổi và phân tích dữ liệu có cấu trúc. Dưới đây là các kỹ thuật FE phổ biến với Pandas.

```python
import pandas as pd
import numpy as np

# Dữ liệu giả lập
data = {
    'order_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'product_category': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'A'],
    'price': [100, 150, 110, 200, 160, 90, 210, 95],
    'order_date': pd.to_datetime([
        '2025-01-15 08:30', '2025-01-15 12:45', '2025-01-16 09:00', 
        '2025-01-16 14:00', '2025-01-17 11:30', '2025-01-17 08:00',
        '2025-01-18 18:00', '2025-01-18 10:00'
    ]),
    'rating': [4.5, 5.0, 4.0, 3.5, np.nan, 5.0, 4.0, 4.5]
}
df = pd.DataFrame(data)
```

### a. Tạo đặc trưng mới từ các cột hiện có

Đây là kỹ thuật cơ bản nhất, ví dụ như tính toán giá trị tương tác giữa các cột.

```python
# Tạo đặc trưng giá có phải là số chẵn không
df['price_is_even'] = df['price'].apply(lambda x: 1 if x % 2 == 0 else 0)
```

### b. Xử lý đặc trưng thời gian (Datetime)

Thời gian là một mỏ vàng cho feature engineering. Ta có thể trích xuất nhiều thông tin từ một cột datetime.

```python
df['order_hour'] = df['order_date'].dt.hour
df['order_day_of_week'] = df['order_date'].dt.dayofweek # Monday=0, Sunday=6
df['is_weekend'] = df['order_day_of_week'].isin([5, 6]).astype(int)
```

### c. Đặc trưng dựa trên nhóm (Group-based Features)

Sử dụng `groupby()` kết hợp với `transform()` hoặc `agg()` để tạo các đặc trưng thống kê cho mỗi nhóm.

```python
# Tính giá trung bình cho mỗi danh mục sản phẩm
# transform() trả về một Series có cùng index với DataFrame gốc
avg_price_per_category = df.groupby('product_category')['price'].transform('mean')
df['avg_price_category'] = avg_price_per_category

# Tạo đặc trưng so sánh giá của sản phẩm với giá trung bình của danh mục đó
df['price_vs_category_avg'] = df['price'] - df['avg_price_category']
```

### d. Xử lý giá trị thiếu (Missing Data)

Thay thế giá trị thiếu là một phần quan trọng. Ta có thể điền giá trị trung bình, trung vị, hoặc một giá trị không đổi.

```python
# Điền giá trị thiếu ở cột rating bằng giá trị trung bình của cột
mean_rating = df['rating'].mean()
df['rating_filled'] = df['rating'].fillna(mean_rating)
```

---

## 2. Numpy: Nền tảng cho tính toán số học

Numpy cung cấp các cấu trúc dữ liệu mảng đa chiều và các hàm toán học hiệu suất cao. Nó thường được sử dụng sau khi đã xử lý dữ liệu bằng Pandas.

### a. Biến đổi toán học

Áp dụng các phép biến đổi như log, căn bậc hai để thay đổi phân phối của dữ liệu, giúp mô hình hoạt động tốt hơn.

```python
# Giả sử cột price có phân phối lệch (skewed)
# Áp dụng log transform để chuẩn hóa phân phối
# Thêm 1 để tránh log(0)
df['price_log'] = np.log1p(df['price'])
```

### b. Vectorization

Numpy cho phép thực hiện các phép toán trên toàn bộ mảng (vectorization) thay vì dùng vòng lặp, giúp tăng tốc độ xử lý đáng kể.

```python
# Thay vì dùng .apply() của Pandas, ta có thể dùng np.where
# Ví dụ: tạo đặc trưng dựa trên ngưỡng giá
df['is_expensive'] = np.where(df['price'] > 150, 1, 0)
```

---

## 3. Scikit-learn: Chuẩn hóa và Mã hóa

Scikit-learn cung cấp một bộ công cụ tiền xử lý mạnh mẽ và nhất quán thông qua API `Transformer` (`fit`, `transform`, `fit_transform`).

### a. Chuẩn hóa (Scaling)

-   **StandardScaler**: Chuẩn hóa đặc trưng bằng cách loại bỏ giá trị trung bình và chia cho độ lệch chuẩn. Kết quả là phân phối có trung bình là 0 và phương sai là 1.
-   **MinMaxScaler**: Co giãn đặc trưng về một khoảng giá trị cho trước, thường là [0, 1].

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler_std = StandardScaler()
df['price_scaled'] = scaler_std.fit_transform(df[['price']])

scaler_minmax = MinMaxScaler()
df['price_minmax'] = scaler_minmax.fit_transform(df[['price']])
```

### b. Mã hóa biến phân loại (Categorical Encoding)

-   **OneHotEncoder**: Biến mỗi giá trị trong biến phân loại thành một cột nhị phân mới.
-   **OrdinalEncoder**: Ánh xạ mỗi giá trị trong biến phân loại thành một số nguyên. Hữu ích khi các giá trị có thứ tự.

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

# One-Hot Encoding cho product_category
ohe = OneHotEncoder(sparse_output=False)
category_encoded = ohe.fit_transform(df[['product_category']])
# Tạo DataFrame từ kết quả và nối vào df gốc
df_category = pd.DataFrame(category_encoded, columns=ohe.get_feature_names_out())
df = pd.concat([df.reset_index(drop=True), df_category], axis=1)
```

### c. Tạo đặc trưng đa thức (Polynomial Features)

`PolynomialFeatures` tạo ra các đặc trưng tương tác và đặc trưng bậc cao, giúp mô hình tuyến tính có thể học các mối quan hệ phi tuyến.

```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
price_poly = poly.fit_transform(df[['price']])
# price_poly sẽ chứa [price, price^2]
```

---

## So sánh và Kết hợp

| Thư viện | Vai trò chính trong Feature Engineering | Điểm mạnh |
|:---:|:---:|:---:|
| **Pandas** | Thao tác, làm sạch, tạo đặc trưng từ dữ liệu có cấu trúc | Linh hoạt, mạnh mẽ với dữ liệu dạng bảng, xử lý datetime và group-based features |
| **Numpy** | Biến đổi toán học và tính toán số học hiệu suất cao | Tốc độ (vectorization), hiệu quả về bộ nhớ, nền tảng cho các thư viện khác |
| **Scikit-learn** | Cung cấp các bộ tiền xử lý tiêu chuẩn, có thể tái sử dụng | API nhất quán (`fit/transform`), dễ dàng tích hợp vào pipeline, nhiều thuật toán sẵn có |

**Workflow thực tiễn:**

1.  **Dùng Pandas để tải và làm sạch dữ liệu**: Xử lý giá trị thiếu, sửa kiểu dữ liệu.
2.  **Dùng Pandas để tạo các đặc trưng phức tạp**: Trích xuất thông tin từ datetime, tạo các đặc trưng thống kê theo nhóm.
3.  **Dùng Numpy cho các phép biến đổi toán học**: Áp dụng log, sin, cos... trên các cột số đã được làm sạch.
4.  **Dùng Scikit-learn để chuẩn hóa và mã hóa**: Áp dụng `StandardScaler` cho các cột số và `OneHotEncoder` cho các cột phân loại để chuẩn bị dữ liệu cho mô hình.

Bằng cách kết hợp sức mạnh của cả ba thư viện, bạn có thể xây dựng một quy trình feature engineering mạnh mẽ, hiệu quả và dễ bảo trì cho hầu hết mọi bài toán Machine Learning.
