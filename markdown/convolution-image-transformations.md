---
title: "Convolution và các phép biến đổi hình ảnh"
date: "2025-01-25"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["Convolution", "Image Processing", "Signal Processing", "Fourier Transform", "Computer Vision", "Mathematics"]
excerpt: "Tìm hiểu về phép toán Convolution - nền tảng của xử lý tín hiệu và hình ảnh. Hiểu rõ các công thức toán học, định lý Convolution và ứng dụng trong Computer Vision."
featured: false
---

# Convolution và các phép biến đổi hình ảnh

## 1. Giới thiệu về Convolution

**Convolution** là một phép toán toán học cơ bản trong xử lý tín hiệu và hình ảnh. Nó mô tả cách hai hàm số "trộn lẫn" với nhau để tạo ra một hàm số thứ ba. Trong ngữ cảnh của Computer Vision, convolution được sử dụng để lọc, làm mịn, phát hiện cạnh và thực hiện nhiều phép biến đổi hình ảnh khác.

### 1.1. Định nghĩa toán học

Với hai hàm số f(t) và g(t), phép convolution được định nghĩa như sau:

$$(f * g)(t) = \int_{-\infty}^{\infty} f(\tau) \cdot g(t - \tau) d\tau$$

Trong đó:
- **f(t)**: Tín hiệu đầu vào
- **g(t)**: Kernel (bộ lọc)
- **τ**: Biến tích phân
- **t**: Thời gian hoặc vị trí

### 1.2. Convolution rời rạc (Discrete Convolution)

Đối với tín hiệu số và hình ảnh, chúng ta sử dụng convolution rời rạc:

$$(f * g)[n] = \sum_{k=-\infty}^{\infty} f[k] \cdot g[n - k]$$

Với hình ảnh 2D, công thức trở thành:

$$(f * g)[i, j] = \sum_{m=-\infty}^{\infty} \sum_{n=-\infty}^{\infty} f[m, n] \cdot g[i - m, j - n]$$

## 2. Định lý Convolution và miền tần số

### 2.1. Định lý Convolution

Một trong những định lý quan trọng nhất trong xử lý tín hiệu là **Định lý Convolution**:

**Convolution trong miền thời gian tương đương với phép nhân trong miền tần số**

$$f(t) * g(t) \leftrightarrow F(\omega) \cdot G(\omega)$$

Trong đó:
- **F(ω)**: Biến đổi Fourier của f(t)
- **G(ω)**: Biến đổi Fourier của g(t)

### 2.2. Ý nghĩa thực tế

Định lý này có ý nghĩa rất quan trọng:

1. **Tính toán hiệu quả**: Thay vì thực hiện convolution trực tiếp (phức tạp), ta có thể:
   - Chuyển sang miền tần số bằng FFT
   - Thực hiện phép nhân đơn giản
   - Chuyển ngược về miền thời gian bằng IFFT

2. **Hiểu biết sâu sắc**: Giúp hiểu cách các bộ lọc hoạt động trong miền tần số

## 3. Các loại Kernel phổ biến trong xử lý hình ảnh

### 3.1. Kernel làm mịn (Smoothing Kernels)

**Kernel trung bình (Average Filter)**:
```
1/9 * [1 1 1]
      [1 1 1]
      [1 1 1]
```

**Kernel Gaussian**:
```
1/16 * [1 2 1]
       [2 4 2]
       [1 2 1]
```

### 3.2. Kernel phát hiện cạnh (Edge Detection)

**Kernel Sobel (phát hiện cạnh theo hướng X)**:
```
[-1  0  1]
[-2  0  2]
[-1  0  1]
```

**Kernel Sobel (phát hiện cạnh theo hướng Y)**:
```
[-1 -2 -1]
[ 0  0  0]
[ 1  2  1]
```

**Kernel Laplacian**:
```
[ 0 -1  0]
[-1  4 -1]
[ 0 -1  0]
```

### 3.3. Kernel làm sắc nét (Sharpening)

**Kernel Unsharp Masking**:
```
[ 0 -1  0]
[-1  5 -1]
[ 0 -1  0]
```

## 4. Ứng dụng trong Computer Vision

### 4.1. Lọc nhiễu (Noise Reduction)

Convolution với kernel làm mịn giúp loại bỏ nhiễu trong hình ảnh:

$$I_{filtered}(x, y) = \sum_{i=-k}^{k} \sum_{j=-k}^{k} I(x+i, y+j) \cdot K(i, j)$$

Trong đó K(i,j) là kernel làm mịn.

### 4.2. Phát hiện cạnh (Edge Detection)

Sử dụng các kernel như Sobel, Canny để phát hiện cạnh:

$$G_x = \frac{\partial I}{\partial x}, \quad G_y = \frac{\partial I}{\partial y}$$

$$G = \sqrt{G_x^2 + G_y^2}$$

### 4.3. Convolutional Neural Networks (CNN)

Trong Deep Learning, convolution được sử dụng để:

1. **Trích xuất đặc trưng**: Tự động học các kernel tối ưu
2. **Giảm tham số**: Chia sẻ trọng số giữa các vị trí
3. **Bất biến với dịch chuyển**: Nhận dạng đối tượng ở các vị trí khác nhau

## 5. Các phép biến đổi hình ảnh nâng cao

### 5.1. Morphological Operations

**Dilation (Giãn nở)**:
$$(A \oplus B)(x, y) = \max_{(i,j) \in B} A(x-i, y-j)$$

**Erosion (Co lại)**:
$$(A \ominus B)(x, y) = \min_{(i,j) \in B} A(x+i, y+j)$$

### 5.2. Geometric Transformations

**Affine Transformation**:
$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} + \begin{bmatrix} t_x \\ t_y \end{bmatrix}$$

### 5.3. Frequency Domain Filtering

Sử dụng định lý convolution để lọc trong miền tần số:

1. **Low-pass filter**: Loại bỏ tần số cao (nhiễu)
2. **High-pass filter**: Giữ lại tần số cao (cạnh)
3. **Band-pass filter**: Giữ lại dải tần cụ thể

## 6. Tối ưu hóa và hiệu suất

### 6.1. Separable Convolution

Nếu kernel có thể tách thành tích của hai vector 1D:

$$K = v \cdot h^T$$

Thì convolution 2D có thể được thực hiện bằng hai convolution 1D liên tiếp, giảm độ phức tạp từ O(n²) xuống O(2n).

### 6.2. FFT-based Convolution

Với kernel lớn, sử dụng FFT có thể hiệu quả hơn:

1. Chuyển cả hình ảnh và kernel sang miền tần số
2. Thực hiện phép nhân
3. Chuyển ngược về miền không gian

## 7. Kết luận

Convolution là một công cụ mạnh mẽ trong xử lý hình ảnh và Computer Vision. Hiểu rõ các nguyên lý toán học và ứng dụng thực tế giúp chúng ta:

- **Thiết kế bộ lọc hiệu quả** cho các ứng dụng cụ thể
- **Tối ưu hóa hiệu suất** trong các thuật toán xử lý hình ảnh
- **Phát triển các mô hình Deep Learning** hiệu quả hơn
- **Giải quyết các bài toán thực tế** trong Computer Vision

Việc nắm vững convolution không chỉ giúp hiểu sâu về xử lý hình ảnh mà còn là nền tảng để tiếp cận các kỹ thuật nâng cao trong AI và Machine Learning. 