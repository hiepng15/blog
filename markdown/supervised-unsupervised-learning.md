---
title: "Supervised Learning và Unsupervised Learning: Khám phá các loại hình Học máy"
date: "2025-01-27"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["supervised learning", "unsupervised learning", "semi-supervised learning", "clustering", "dimensionality reduction", "anomaly detection", "machine learning", "python", "scikit-learn"]
excerpt: "Hướng dẫn chuyên sâu về các loại hình học máy: Supervised, Unsupervised và Semi-supervised Learning, từ lý thuyết đến ứng dụng thực tế với các thuật toán clustering, dimensionality reduction và anomaly detection."
featured: false
---

# Supervised Learning và Unsupervised Learning: Khám phá các loại hình Học máy

Sau khi đi một vòng để trang bị những kiến thức cơ bản nhất, giờ là lúc chúng ta sẽ quay lại với các thuật toán ML. Trong khi học máy có giám sát (supervised learning) đã trở nên quen thuộc, học máy không giám sát (unsupervised learning) và học máy bán giám sát (semi-supervised learning) lại mở ra những cánh cửa mới để khám phá các mối quan hệ ẩn trong dữ liệu.

Bài blog này sẽ đi sâu vào các kỹ thuật và ứng dụng của hai lĩnh vực này, từ việc phân cụm dữ liệu cho đến việc tận dụng một lượng nhãn hạn chế để xây dựng các mô hình mạnh mẽ.

## **1. Phân biệt các loại hình Học máy**

Để hiểu rõ hơn về unsupervised và semi-supervised learning, chúng ta hãy đặt chúng vào bối cảnh của ba loại hình học máy chính:

* **Học có giám sát (Supervised Learning):** Dữ liệu huấn luyện có đầy đủ các cặp **đầu vào-đầu ra (features-labels)**. Mục tiêu là học một hàm ánh xạ từ đầu vào đến đầu ra.

  * **Ví dụ:** Phân loại email spam, dự đoán giá nhà.

* **Học không giám sát (Unsupervised Learning):** Dữ liệu huấn luyện **không có nhãn (labels)**. Mục tiêu là khám phá cấu trúc, các mối quan hệ ẩn hoặc các mẫu (patterns) trong dữ liệu.

  * **Ví dụ:** Phân cụm khách hàng, giảm chiều dữ liệu để trực quan hóa.

* **Học bán giám sát (Semi-supervised Learning):** Kết hợp cả hai loại trên, sử dụng một lượng nhỏ dữ liệu **có nhãn** và một lượng lớn dữ liệu **không nhãn** để huấn luyện mô hình.

  * **Ví dụ:** Phân loại văn bản khi chỉ có một vài tài liệu được gán nhãn thủ công.

## **2. Học máy không giám sát: Khám phá cấu trúc dữ liệu**

Các kỹ thuật học không giám sát giúp chúng ta tìm ra các nhóm, các điểm bất thường hoặc cách biểu diễn dữ liệu tốt hơn.

### **a. Phân cụm (Clustering)**

Mục tiêu của phân cụm là nhóm các mẫu dữ liệu tương tự nhau lại với nhau.

* **K-Means:** Thuật toán phổ biến và dễ hiểu. Nó chia dữ liệu thành $k$ cụm, trong đó $k$ được xác định trước. Thuật toán hoạt động bằng cách lặp lại hai bước:

  1. Gán mỗi điểm dữ liệu cho tâm cụm gần nhất.
  2. Cập nhật vị trí của tâm cụm bằng giá trị trung bình của tất cả các điểm trong cụm đó.

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# Tạo dữ liệu giả
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# Phân cụm K-Means với k=4
kmeans = KMeans(n_clusters=4, random_state=0, n_init=10)
kmeans.fit(X)
labels = kmeans.labels_

print("Các nhãn cụm được gán:")
print(labels[:10])  # In ra 10 nhãn đầu tiên
```

* **DBSCAN:** Một thuật toán phân cụm dựa trên mật độ. DBSCAN không yêu cầu số cụm được xác định trước và có khả năng tìm ra các cụm có hình dạng phức tạp. Nó hoạt động bằng cách tìm ra các vùng có mật độ cao và phân loại các điểm còn lại là nhiễu (outliers).

* **Hierarchical Clustering:** Tạo ra một cây phân cấp các cụm. Kết quả có thể được trực quan hóa bằng một biểu đồ Dendrogram, giúp chúng ta dễ dàng lựa chọn số cụm phù hợp.

### **b. Giảm chiều dữ liệu (Dimensionality Reduction)**

Giảm chiều dữ liệu là quá trình biến đổi dữ liệu từ không gian có nhiều chiều sang không gian có ít chiều hơn.

* **PCA (Principal Component Analysis):** Một kỹ thuật giảm chiều tuyến tính, tìm ra các trục (principal components) mà tại đó phương sai của dữ liệu là lớn nhất. PCA rất hữu ích để loại bỏ các biến có tương quan cao và trực quan hóa dữ liệu.

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data

# Giảm chiều dữ liệu về 2 chiều
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

print("Dữ liệu sau khi giảm chiều với PCA:")
print(X_pca[:5])
```

* **t-SNE và UMAP:** Các kỹ thuật giảm chiều phi tuyến tính, được thiết kế đặc biệt để trực quan hóa. Chúng cố gắng bảo toàn khoảng cách cục bộ giữa các điểm dữ liệu, giúp các cụm dễ dàng hiển thị trên một mặt phẳng 2D hoặc 3D.

### **c. Phát hiện bất thường (Anomaly Detection)**

Mục tiêu là tìm ra các điểm dữ liệu khác biệt đáng kể so với phần còn lại của dữ liệu.

* **Isolation Forest:** Một thuật toán hiệu quả dựa trên cây quyết định. Nó hoạt động bằng cách "cô lập" các điểm bất thường, vốn ít và dễ bị cô lập hơn so với các điểm bình thường.
* **One-Class SVM:** Một phiên bản của Support Vector Machine, được huấn luyện trên một tập dữ liệu chỉ chứa các điểm bình thường. Sau đó, nó sẽ phân loại bất kỳ điểm mới nào không thuộc "vùng" này là bất thường.

## **3. Học máy bán giám sát: Khi nhãn dữ liệu là một "tài sản hiếm có"**

Trong nhiều tình huống thực tế, việc thu thập dữ liệu không có nhãn thì dễ, nhưng việc gán nhãn lại rất tốn kém. Học bán giám sát giúp chúng ta tận dụng tối đa lượng dữ liệu có nhãn hạn chế.

### **a. Các phương pháp chính**

* **Self-training:** Đây là một phương pháp đơn giản nhưng hiệu quả.

  1. Huấn luyện một mô hình ban đầu trên tập dữ liệu có nhãn nhỏ.
  2. Sử dụng mô hình đó để dự đoán trên tập dữ liệu không nhãn.
  3. Lựa chọn những dự đoán có độ tin cậy cao, gán nhãn cho chúng, và thêm vào tập huấn luyện ban đầu.
  4. Lặp lại quá trình này cho đến khi mô hình hội tụ.

* **Label Propagation:** Một thuật toán dựa trên đồ thị, lan truyền các nhãn đã biết đến các điểm dữ liệu không nhãn. Các điểm gần nhau trên đồ thị có xu hướng nhận cùng một nhãn.

* **Consistency Training:** Đây là một phương pháp tiên tiến hơn, thường được sử dụng trong học sâu. Nó huấn luyện mô hình để đưa ra cùng một dự đoán cho một điểm dữ liệu, ngay cả khi điểm đó được làm nhiễu nhẹ.

### **b. Ví dụ Code với Scikit-learn**

Scikit-learn cung cấp một số công cụ cho học bán giám sát.

```python
from sklearn.semi_supervised import LabelSpreading
from sklearn.datasets import make_moons
import numpy as np

# Tạo dữ liệu giả hình trăng lưỡi liềm
X, y = make_moons(n_samples=200, noise=0.1, random_state=0)

# Giả lập dữ liệu bán giám sát
# Chỉ giữ lại 20 nhãn, còn lại là -1 (không nhãn)
n_labeled = 20
rng = np.random.RandomState(0)
unlabeled_indices = rng.rand(len(X)) > (n_labeled / len(X))
y_unlabeled = np.copy(y)
y_unlabeled[unlabeled_indices] = -1

# Sử dụng Label Spreading
label_spread_model = LabelSpreading(kernel='knn', alpha=0.2)
label_spread_model.fit(X, y_unlabeled)
y_pred = label_spread_model.predict(X)

print("Độ chính xác trên toàn bộ tập dữ liệu:")
print(f"Accuracy: {np.mean(y_pred == y):.4f}")
```

## **4. Ứng dụng thực tế**

* **Phát hiện gian lận (Anomaly Detection):** Một trong những ứng dụng phổ biến nhất của học không giám sát. Chúng ta có thể huấn luyện một mô hình trên dữ liệu giao dịch bình thường để phát hiện các giao dịch bất thường, tiềm ẩn nguy cơ gian lận.
* **Phân cụm khách hàng (Customer Segmentation):** Phân cụm giúp các doanh nghiệp chia khách hàng thành các nhóm dựa trên hành vi mua sắm, sở thích, v.v., từ đó đưa ra các chiến lược marketing phù hợp.
* **Phân loại văn bản (Text Classification):** Trong các ứng dụng như phân loại cảm xúc hay phân loại tin tức, việc gán nhãn cho hàng ngàn tài liệu là không khả thi. Học bán giám sát giúp chúng ta xây dựng mô hình phân loại hiệu quả chỉ với một lượng nhỏ dữ liệu được gán nhãn.

## **Kết luận**

Học máy không giám sát và bán giám sát là những công cụ mạnh mẽ, giúp chúng ta tận dụng tối đa dữ liệu thô và giải quyết các bài toán mà học có giám sát không thể giải quyết được. Hiểu rõ các thuật toán này sẽ mở rộng đáng kể bộ công cụ của bạn, cho phép bạn khám phá những khía cạnh mới của dữ liệu và xây dựng các hệ thống AI thông minh hơn, hiệu quả hơn. 