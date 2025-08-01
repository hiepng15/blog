---
title: "Xây dựng và Tối ưu hóa Mô hình Học máy"
date: "2025-01-27"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["machine learning", "model building", "hyperparameter tuning", "cross validation", "feature selection", "model evaluation", "python", "scikit-learn"]
excerpt: "Hướng dẫn chuyên sâu về quy trình xây dựng và tối ưu hóa mô hình học máy, từ chia dữ liệu, xây dựng pipeline, tối ưu siêu tham số đến đánh giá mô hình với các ví dụ code thực tế."
featured: false
---

# Xây dựng và Tối ưu hóa Mô hình Học máy

Chào mừng các bạn quay trở lại. Sau khi đã nắm vững các kỹ thuật **Feature Engineering** để tạo ra những đặc trưng chất lượng, chúng ta sẽ bước vào giai đoạn cốt lõi của quy trình học máy: xây dựng và tối ưu hóa mô hình. Giai đoạn này không chỉ đơn thuần là việc gọi một hàm `.fit()` mà còn là một quá trình có hệ thống, đòi hỏi sự lựa chọn, tinh chỉnh và đánh giá cẩn thận để đạt được hiệu suất tốt nhất. Bài viết này sẽ hướng dẫn các bạn từng bước, từ việc thiết lập một pipeline cơ bản cho đến các chiến lược tối ưu hóa nâng cao, đi kèm với các ví dụ code thực tế bằng Python.

## **1. Xây dựng Mô hình Học máy: Quy trình Vững chắc**

Việc xây dựng một mô hình không phải là một "cú hit may mắn" mà là một quy trình lặp đi lặp lại với các bước rõ ràng.

### **a. Chia tập dữ liệu (Data Splitting)**

Đây là bước đầu tiên và quan trọng nhất để tránh **data leakage** và đánh giá mô hình một cách khách quan. Chúng ta thường chia dữ liệu thành ba tập:

* **Tập huấn luyện (Training Set):** Dùng để huấn luyện mô hình.
* **Tập kiểm tra (Testing Set):** Dùng để đánh giá hiệu suất cuối cùng của mô hình, mô phỏng cách mô hình sẽ hoạt động trong môi trường thực tế.
* **Tập xác thực (Validation Set):** Dùng để tinh chỉnh các siêu tham số (hyperparameters) và chọn ra mô hình tốt nhất.

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Dữ liệu giả
data = {
    'feature_1': [10, 20, 30, 40, 50, 60, 70, 80],
    'feature_2': [1, 2, 3, 4, 5, 6, 7, 8],
    'target': [0, 0, 0, 1, 1, 1, 1, 1]
}
df = pd.DataFrame(data)
X = df.drop('target', axis=1)
y = df['target']

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Số lượng mẫu huấn luyện: {len(X_train)}")
print(f"Số lượng mẫu kiểm tra: {len(X_test)}")
```

### **b. Xây dựng Pipeline và Huấn luyện Mô hình**

Sử dụng Scikit-learn Pipeline là một thực tiễn tốt để đóng gói các bước tiền xử lý và mô hình vào một luồng làm việc duy nhất, giúp quy trình trở nên gọn gàng, có thể tái sử dụng và tránh lỗi.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Xây dựng một pipeline đơn giản: Scaling -> Mô hình
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(random_state=42))
])

# Huấn luyện mô hình trên tập huấn luyện
pipeline.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = pipeline.predict(X_test)
```

## **2. Tối ưu hóa Mô hình: Nâng cao Hiệu suất**

Sau khi có một mô hình cơ bản, chúng ta sẽ tập trung vào các kỹ thuật tối ưu hóa để cải thiện hiệu suất.

### **a. Tối ưu hóa Siêu tham số (Hyperparameter Tuning)**

Đây là quá trình tìm kiếm bộ siêu tham số tốt nhất cho mô hình.

* **Grid Search:** Thử tất cả các kết hợp siêu tham số trong một lưới đã định. Đơn giản nhưng rất tốn kém về mặt tính toán.
* **Random Search:** Lấy mẫu ngẫu nhiên các kết hợp siêu tham số. Thường hiệu quả hơn Grid Search trong việc tìm ra bộ siêu tham số tốt.
* **Bayesian Optimization:** Sử dụng các thuật toán thông minh để tìm kiếm các siêu tham số tiềm năng, hiệu quả hơn đáng kể so với Grid/Random Search. Thư viện **Optuna** là một công cụ mạnh mẽ cho phương pháp này.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# Định nghĩa các tham số cần tối ưu
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}

# Sử dụng GridSearchCV để tìm kiếm
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=3,  # Sử dụng 3-fold cross-validation
    scoring='accuracy',
    n_jobs=-1  # Sử dụng tất cả các cores
)

grid_search.fit(X_train, y_train)

print(f"Tham số tốt nhất: {grid_search.best_params_}")
print(f"Độ chính xác tốt nhất: {grid_search.best_score_:.4f}")
```

### **b. Cross-validation (Kiểm định chéo)**

Đây là một kỹ thuật mạnh mẽ để đánh giá mô hình một cách bền vững hơn, tránh việc đánh giá quá phụ thuộc vào cách chia tập dữ liệu ngẫu nhiên. **K-fold cross-validation** chia tập dữ liệu thành `k` phần, huấn luyện `k` lần và tính trung bình kết quả.

### **c. Lựa chọn Đặc trưng (Feature Selection)**

Việc giảm bớt các đặc trưng không quan trọng không chỉ giúp mô hình chạy nhanh hơn mà còn có thể cải thiện hiệu suất.

* **Recursive Feature Elimination (RFE):** Lặp đi lặp lại việc huấn luyện mô hình, loại bỏ đặc trưng kém quan trọng nhất cho đến khi đạt được số lượng mong muốn.
* **SelectKBest:** Chọn ra `k` đặc trưng tốt nhất dựa trên các kiểm định thống kê.
* **SHAP Importance:** Sử dụng thư viện **SHAP** để tính toán mức độ quan trọng của từng đặc trưng, đưa ra cái nhìn sâu sắc và có thể giải thích được.

### **d. Regularization (Chuẩn hóa)**

Kỹ thuật này giúp mô hình chống lại **overfitting** (học thuộc lòng dữ liệu huấn luyện).

* **L1 Regularization (Lasso):** Thêm một số hạng vào hàm mất mát, có xu hướng đưa các trọng số của các đặc trưng không quan trọng về 0.
* **L2 Regularization (Ridge):** Thêm một số hạng khác vào hàm mất mát, làm giảm các trọng số mà không đưa chúng về 0.

## **3. Đánh giá Mô hình: Phân tích kết quả**

Đánh giá mô hình một cách toàn diện là bước cuối cùng và quyết định.

### **a. Các chỉ số quan trọng (Metrics)**

* **Classification:**
  * **Accuracy:** Tỷ lệ dự đoán đúng. Dễ hiểu nhưng có thể gây hiểu lầm với dữ liệu mất cân bằng.
  * **Precision, Recall, F1-score:** Cân bằng giữa các chỉ số này là chìa khóa.
  * **ROC-AUC:** Đo lường khả năng phân biệt giữa các lớp của mô hình, rất hữu ích cho các bài toán phân loại nhị phân.

* **Regression:**
  * **RMSE (Root Mean Squared Error):** Sai số trung bình giữa dự đoán và thực tế. Càng nhỏ càng tốt.
  * **MAE (Mean Absolute Error):** Sai số tuyệt đối trung bình, ít nhạy cảm với các giá trị ngoại lai hơn RMSE.
  * **R² (R-squared):** Đo lường mức độ phù hợp của mô hình với dữ liệu, giá trị càng gần 1 càng tốt.

### **b. Phân tích Chuyên sâu với Confusion Matrix và ROC Curve**

* **Confusion Matrix:** Một bảng tóm tắt giúp ta nhìn rõ các lỗi của mô hình (False Positives và False Negatives).
* **ROC Curve (Receiver Operating Characteristic):** Một đồ thị trực quan cho thấy hiệu suất của mô hình ở mọi ngưỡng phân loại.

```python
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

# Dự đoán trên tập kiểm tra
y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
y_pred = pipeline.predict(X_test)

# In các chỉ số
print(f"Độ chính xác: {accuracy_score(y_test, y_pred):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Vẽ Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.show()

# Vẽ ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label='ROC Curve')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

## **4. Bước cuối cùng: Đưa Mô hình vào Sản xuất**

Sau khi đã có mô hình tối ưu, bước cuối cùng là lưu trữ và triển khai nó. Sử dụng **MLflow** là một giải pháp chuyên nghiệp để làm điều này.

* **Lưu trữ mô hình:** MLflow cho phép bạn lưu toàn bộ pipeline đã được huấn luyện, bao gồm cả các bước tiền xử lý, giúp việc tải và sử dụng lại mô hình trở nên dễ dàng.
* **Triển khai:** MLflow cung cấp các công cụ để đóng gói mô hình thành một API, sẵn sàng cho việc đưa vào môi trường sản xuất.

## **Kết luận**

Việc xây dựng và tối ưu hóa mô hình học máy là một quá trình có hệ thống, không chỉ dựa vào kinh nghiệm mà còn đòi hỏi sự hiểu biết về các công cụ và kỹ thuật chuyên sâu. Nắm vững quy trình này sẽ giúp bạn tạo ra các mô hình không chỉ chính xác mà còn bền vững và đáng tin cậy. Bây giờ bạn đã có một cái nhìn tổng quan và các công cụ cần thiết để bắt đầu. Chúc các bạn thành công! 