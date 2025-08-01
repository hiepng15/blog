---
title: "Explainable AI: Làm cho AI trở nên minh bạch"
date: "2025-01-27"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["explainable ai", "xai", "shap", "lime", "machine learning", "interpretability", "transparency", "python"]
excerpt: "Hướng dẫn chuyên sâu về Explainable AI (XAI) - làm cho các mô hình AI trở nên minh bạch và dễ hiểu, từ lý thuyết đến thực hành với SHAP và LIME."
featured: false
---

# Explainable AI: Làm cho AI trở nên minh bạch

Chào mừng bạn đến với thế giới của **Explainable AI (XAI)**! Trong kỷ nguyên của học máy, việc xây dựng một mô hình đưa ra dự đoán chính xác thôi là chưa đủ. Các mô hình phức tạp thường hoạt động như những "hộp đen", và việc hiểu **tại sao** chúng lại đưa ra một quyết định cụ thể ngày càng trở nên quan trọng.

Bài blog này sẽ đi sâu vào XAI, từ việc phân loại các phương pháp giải thích cho đến việc hướng dẫn sử dụng các công cụ mạnh mẽ như **SHAP** và **LIME** với code ví dụ cụ thể.

## **1. XAI: Tại sao lại cần "Hộp đen" phải lên tiếng?**

**Explainable AI (XAI)** là một lĩnh vực của học máy tập trung vào việc làm cho các mô hình AI trở nên minh bạch và dễ hiểu hơn. Mục tiêu chính là để con người có thể hiểu, tin tưởng và kiểm soát các quyết định của AI.

**Tầm quan trọng của XAI:**

* **Minh bạch và Đạo đức:** Trong các lĩnh vực nhạy cảm như tài chính (quyết định cho vay) hay y tế (chẩn đoán bệnh), việc hiểu lý do mô hình đưa ra một quyết định là bắt buộc để đảm bảo sự công bằng và tuân thủ các quy định.
* **Gỡ lỗi và Cải thiện:** Khi mô hình hoạt động sai, việc biết được các đặc trưng nào đang gây ảnh hưởng tiêu cực sẽ giúp các kỹ sư nhanh chóng gỡ lỗi và cải thiện mô hình.
* **Xây dựng niềm tin:** Người dùng và các bên liên quan sẽ tin tưởng hơn vào một hệ thống AI khi họ có thể hiểu được logic đằng sau các quyết định của nó.

## **2. Phân loại các Phương pháp Giải thích**

Có hai cách tiếp cận chính để giải thích mô hình:

* **Mô hình có thể giải thích nội tại (Interpretable Models):** Đây là những mô hình có cấu trúc đơn giản, cho phép chúng ta trực tiếp hiểu cách chúng hoạt động.

  * **Ví dụ:** Hồi quy tuyến tính (Linear Regression), Cây quyết định (Decision Tree). Các mô hình này được coi là "hộp trắng" vì chúng ta có thể nhìn thấy và hiểu logic bên trong.

* **Phương pháp giải thích hậu kiểm (Post-hoc Explanations):** Đây là các kỹ thuật được áp dụng sau khi mô hình đã được huấn luyện. Chúng hoạt động với các mô hình "hộp đen" phức tạp và đưa ra các giải thích. Các phương pháp này được chia thành:

  * **Giải thích toàn cục (Global Explanations):** Giải thích cách mô hình hoạt động trên toàn bộ tập dữ liệu.
  * **Giải thích cục bộ (Local Explanations):** Giải thích dự đoán của mô hình cho một trường hợp cụ thể.

## **3. Các Kỹ thuật XAI Phổ biến và Ví dụ Code**

Chúng ta sẽ sử dụng một mô hình **Random Forest** (một "hộp đen") để minh họa các kỹ thuật giải thích.

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
import shap

# Tạo dữ liệu giả
X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=42)
feature_names = [f'feature_{i}' for i in range(10)]
X_df = pd.DataFrame(X, columns=feature_names)
y_df = pd.Series(y, name='target')

# Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(X_df, y_df, test_size=0.2, random_state=42)

# Huấn luyện mô hình Random Forest
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)
```

### **3.1. Giải thích Toàn cục (Global Explanations)**

#### **a. Feature Importance (Độ quan trọng của Đặc trưng)**

Đây là một trong những phương pháp giải thích đơn giản và phổ biến nhất, có sẵn trong nhiều mô hình dạng cây.

```python
# Lấy độ quan trọng của đặc trưng từ mô hình
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({
    'feature': feature_names, 
    'importance': importances
}).sort_values('importance', ascending=False)

print("Độ quan trọng của đặc trưng (Feature Importance):")
print(feature_importance_df)
```

**Giải thích:** Kết quả cho thấy đặc trưng nào có ảnh hưởng lớn nhất đến dự đoán của mô hình trên toàn bộ tập dữ liệu.

#### **b. Partial Dependence Plots (PDP) và Individual Conditional Expectation (ICE)**

* **PDP:** Cho chúng ta biết một đặc trưng ảnh hưởng trung bình đến dự đoán của mô hình như thế nào.
* **ICE:** Tương tự PDP nhưng vẽ một đường riêng cho mỗi mẫu dữ liệu, giúp phát hiện các mối quan hệ phức tạp mà PDP có thể bỏ qua.

```python
from sklearn.inspection import partial_dependence, plot_partial_dependence
import matplotlib.pyplot as plt

# Vẽ PDP cho 2 đặc trưng quan trọng nhất
fig, ax = plt.subplots(figsize=(10, 5))
plot_partial_dependence(model, X_train, features=['feature_4', 'feature_7'], ax=ax)
fig.suptitle("Partial Dependence Plots (PDP)")
plt.show()
```

**Giải thích:** Đồ thị trên cho thấy khi giá trị của `feature_4` tăng lên, xác suất dự đoán là lớp 1 cũng tăng.

### **3.2. Giải thích Cục bộ (Local Explanations)**

#### **a. SHAP (SHapley Additive exPlanations)**

SHAP là một kỹ thuật mạnh mẽ dựa trên lý thuyết trò chơi, gán một giá trị cho mỗi đặc trưng cho biết mức độ đóng góp của nó vào dự đoán. SHAP có thể giải thích cả cục bộ và toàn cục.

```python
# Sử dụng TreeExplainer của SHAP cho mô hình cây
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Giải thích dự đoán cho một mẫu cụ thể (mẫu thứ 5 trong tập kiểm tra)
sample_index = 5
print(f"Dự đoán của mô hình cho mẫu {sample_index}: {model.predict(X_test.iloc[[sample_index]])[0]}")
shap.initjs()
shap.force_plot(explainer.expected_value[1], shap_values[1][sample_index], X_test.iloc[[sample_index]])
```

**Giải thích:** **Force Plot** trên cho thấy các đặc trưng màu đỏ (`feature_7`, `feature_4`) đang "đẩy" dự đoán của mô hình về phía lớp 1, trong khi các đặc trưng màu xanh (`feature_5`, `feature_8`) đang "đẩy" về phía lớp 0.

#### **b. LIME (Local Interpretable Model-agnostic Explanations)**

LIME hoạt động bằng cách tạo ra một mô hình đơn giản (như hồi quy tuyến tính) xung quanh một điểm dữ liệu cụ thể để giải thích dự đoán của mô hình phức tạp.

```python
from lime.lime_tabular import LimeTabularExplainer

# Tạo đối tượng LIME explainer
explainer = LimeTabularExplainer(
    training_data=np.array(X_train),
    feature_names=feature_names,
    class_names=['Class 0', 'Class 1'],
    mode='classification'
)

# Giải thích dự đoán cho cùng một mẫu
exp = explainer.explain_instance(
    data_row=X_test.iloc[sample_index].values,
    predict_fn=model.predict_proba,
    num_features=5
)

# Hiển thị kết quả trên giao diện
exp.show_in_notebook(show_table=True)
```

**Giải thích:** LIME sẽ chỉ ra những đặc trưng nào có ảnh hưởng nhất đến quyết định của mô hình đối với một mẫu cụ thể, kèm theo trọng số (trọng số càng lớn, ảnh hưởng càng mạnh).

## **4. Thách thức khi áp dụng XAI**

1. **Hiệu suất và Khả năng mở rộng:** Các kỹ thuật như SHAP rất tốn kém về mặt tính toán, đặc biệt với các mô hình phức tạp và tập dữ liệu lớn.
2. **Sự hiểu nhầm (Misinterpretation):** Các giải thích của XAI có thể bị hiểu nhầm. Ví dụ, một giải thích cục bộ không thể suy rộng ra toàn bộ mô hình.
3. **Thiên vị (Bias):** Nếu mô hình ban đầu đã có bias, các công cụ XAI có thể chỉ giải thích cách bias đó hoạt động, chứ không tự động loại bỏ nó.
4. **Tính ổn định (Stability):** Một số phương pháp giải thích có thể không ổn định, đưa ra các kết quả khác nhau cho cùng một mẫu dữ liệu.

## **Kết luận**

XAI không phải là một viên thuốc thần kỳ để làm cho mọi mô hình trở nên hoàn hảo, mà là một công cụ mạnh mẽ để chúng ta có thể làm việc hiệu quả hơn với các hệ thống AI phức tạp. Nắm vững các kỹ thuật như SHAP và LIME sẽ giúp bạn không chỉ xây dựng được các mô hình chính xác mà còn có thể giải thích, gỡ lỗi và xây dựng niềm tin cho người dùng.

Trong tương lai, XAI sẽ tiếp tục là một yếu tố không thể thiếu trong mọi quy trình phát triển học máy, hướng tới một kỷ nguyên AI minh bạch và đáng tin cậy hơn. 