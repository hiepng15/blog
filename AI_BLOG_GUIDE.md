# 🤖 AI Blog Update Guide

## 📋 Tổng quan
File này hướng dẫn AI cách tự động cập nhật blog từ file Markdown. Khi bạn hoàn thành một bài blog bằng Markdown, AI sẽ đọc file này và tự động:
1. Convert Markdown thành HTML
2. Cập nhật metadata.json
3. Tạo file HTML trong thư mục posts/

## 📁 Cấu trúc thư mục blog
```
blog/
├── index.html              # Trang chủ blog (hardcoded với số thứ tự)
├── metadata.json           # Metadata cho tất cả bài viết  
├── posts/                  # Các file HTML của bài viết
│   ├── my-chilhood.html
│   ├── ai-machine-learning-ai-agent.html
│   ├── nlp-llm-computer-vision.html
│   └── ... (16 posts total)
├── markdown/               # 📝 THƯ MỤC MỚI: Chứa file Markdown
│   ├── my-chilhood.md
│   ├── ai-machine-learning-ai-agent.md
│   └── ... (file .md tương ứng)
└── AI_BLOG_GUIDE.md        # File này
```

### 🏷️ Hệ thống phân loại & số thứ tự:
- **My Blog**: Số thứ tự riêng (01, 02, 03...)
- **TIL**: Số thứ tự riêng (01, 02, 03...)
- **Categories**: "blog" hoặc "til" trong data-category
- **Blog hiện tại**: 1 My Blog + 15 TIL = 16 posts total

## ✍️ Format Markdown cho bài viết

### 📝 Template cơ bản:
```markdown
---
id: "unique-post-id"
title: "Tiêu đề bài viết"
excerpt: "Mô tả ngắn gọn về bài viết (2-3 câu)"
date: "YYYY-MM-DD"
author: "Huy Hiep Nguyen"
category: "blog"                # "blog" hoặc "til"
tags: ["Tag1", "Tag2", "Tag3"]
readTime: "X phút đọc"
featured: false
---

# Tiêu đề chính

Nội dung bài viết bắt đầu từ đây...

## Tiêu đề phụ

Nội dung tiếp theo...

### Tiêu đề nhỏ hơn

- Danh sách bullet points
- Điểm thứ hai
- Điểm thứ ba

**Bold text** và *italic text*.

> Blockquote nếu cần

---

*Kết luận hoặc ghi chú cuối bài*
```

### 📋 Quy tắc quan trọng:

#### 1. **Front Matter (Metadata)**
- **Bắt buộc**: Phải có section `---` ở đầu và cuối metadata
- **id**: Phải unique, không dấu cách, dùng dấu gạch ngang
- **date**: Format YYYY-MM-DD
- **featured**: true/false (chỉ 1 bài có thể featured = true)
- **tags**: Tối đa 5 tags, viết hoa chữ cái đầu

#### 2. **Nội dung Markdown**
- Sử dụng `#` cho tiêu đề chính
- Sử dụng `##` cho tiêu đề phụ
- Sử dụng `###` cho tiêu đề nhỏ
- **Không sử dụng** `####` trở lên (sẽ được convert thành `<h4>`)
- Sử dụng `**text**` cho bold
- Sử dụng `*text*` cho italic
- Sử dụng `- item` cho bullet lists
- Sử dụng `1. item` cho numbered lists

#### 3. **HTML trong Markdown**
- Có thể sử dụng HTML tags: `<strong>`, `<em>`, `<ul>`, `<li>`
- **Không sử dụng**: `<div>`, `<section>`, `<article>` (sẽ bị loại bỏ)
- **Được phép**: `<hr>`, `<br>`, `<p>`

## 🔄 Quy trình AI Update

### Bước 1: Đọc file Markdown
```javascript
// AI sẽ đọc file .md từ thư mục markdown/
const markdownContent = fs.readFileSync('./blog/markdown/new-post.md', 'utf8');
```

### Bước 2: Parse Front Matter
```javascript
// Extract metadata từ section ---
const frontMatter = parseFrontMatter(markdownContent);
// Kết quả: { id, title, excerpt, date, author, tags, readTime, featured }
```

### Bước 3: Convert Markdown to HTML
```javascript
// Convert nội dung Markdown thành HTML
const htmlContent = convertMarkdownToHTML(markdownContent);
```

### Bước 4: Cập nhật metadata.json
```javascript
// Thêm bài viết mới vào đầu array posts[]
// Sắp xếp theo date (mới nhất trước)
// Đảm bảo chỉ có 1 bài featured = true
```

### Bước 5: Tạo file HTML
```javascript
// Tạo file ./blog/posts/{id}.html
// Chỉ chứa nội dung HTML, không có <html>, <head>, <body>
```

### Bước 6: ⚠️ **CẬP NHẬT INDEX.HTML VỚI SỐ THỨ TỰ**
```javascript
// AI PHẢI thực hiện thủ công:
// 1. Thêm post mới vào blog/index.html
// 2. Thêm <div class="post-number">XX</div> với số thứ tự đúng
// 3. My Blog: tiếp tục từ số hiện tại + 1
// 4. TIL: tiếp tục từ số hiện tại + 1
// 5. Category đúng: data-category="blog" hoặc "til"
```

**🔢 Numbering Logic:**
- **My Blog**: Đếm riêng (hiện tại có 01)
- **TIL**: Đếm riêng (hiện tại có 01-15)
- **Post mới**: My Blog → 02, TIL → 16

## 🛠️ Hàm chuyển đổi Markdown

### Convert Markdown to HTML:
```javascript
function convertMarkdownToHTML(markdown) {
  let html = markdown;
  
  // Loại bỏ front matter
  html = html.replace(/^---[\s\S]*?---\n/, '');
  
  // Convert headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  
  // Convert paragraphs
  html = html.replace(/^(?!<[h|u|o]|<li|<blockquote)(.+)$/gim, '<p>$1</p>');
  
  // Convert lists
  html = html.replace(/^- (.+)$/gim, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
  
  // Convert bold and italic
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  
  // Convert horizontal rule
  html = html.replace(/^---$/gim, '<hr>');
  
  // Clean up empty paragraphs
  html = html.replace(/<p><\/p>/g, '');
  
  return html;
}
```

### Parse Front Matter:
```javascript
function parseFrontMatter(content) {
  const frontMatterMatch = content.match(/^---([\s\S]*?)---/);
  if (!frontMatterMatch) return null;
  
  const frontMatter = frontMatterMatch[1];
  const metadata = {};
  
  // Parse từng dòng
  frontMatter.split('\n').forEach(line => {
    const [key, ...valueParts] = line.split(':');
    if (key && valueParts.length > 0) {
      let value = valueParts.join(':').trim();
      
      // Remove quotes if present
      if (value.startsWith('"') && value.endsWith('"')) {
        value = value.slice(1, -1);
      }
      
      // Parse arrays
      if (value.startsWith('[') && value.endsWith(']')) {
        value = JSON.parse(value);
      }
      
      // Parse booleans
      if (value === 'true') value = true;
      if (value === 'false') value = false;
      
      metadata[key.trim()] = value;
    }
  });
  
  return metadata;
}
```

## 📝 Ví dụ file Markdown hoàn chỉnh

### File: `blog/markdown/example-post.md`
```markdown
---
id: "example-post"
title: "Ví dụ bài viết mẫu"
excerpt: "Đây là một bài viết mẫu để minh họa cách viết Markdown cho blog."
date: "2025-02-01"
author: "Huy Hiep Nguyen"
tags: ["Ví dụ", "Markdown", "Hướng dẫn"]
readTime: "5 phút đọc"
featured: false
---

# Tiêu đề chính của bài viết

Đây là đoạn mở đầu của bài viết. Bạn có thể viết bất kỳ nội dung gì ở đây.

## Tiêu đề phụ đầu tiên

Nội dung của phần này có thể bao gồm:

- **Điểm quan trọng**: Được highlight bằng bold
- *Ghi chú phụ*: Được viết nghiêng
- Danh sách các ý chính

### Tiêu đề nhỏ hơn

Đây là nội dung của phần nhỏ hơn. Bạn có thể sử dụng:

1. Danh sách đánh số
2. Để liệt kê các bước
3. Hoặc các ý theo thứ tự

> Đây là một blockquote để nhấn mạnh ý quan trọng.

---

*Kết luận: Đây là cách viết Markdown cho blog của bạn.*
```

## 🚀 Quy trình hoàn chỉnh

### Khi bạn có file Markdown mới, AI sẽ thực hiện:

```bash
# 1. Đọc file Markdown từ blog/markdown/
# 2. Parse metadata và convert to HTML
# 3. Tạo file posts/{id}.html
# 4. Update metadata.json
# 5. ⚠️ CẬP NHẬT INDEX.HTML (thủ công)
# 6. Test local: python -m http.server 8000 --directory blog
```

### 📤 Deployment Guide (cho lần push tiếp theo):

```bash
# A. Commit local changes
git add blog/
git commit -m "Add new blog post: [title]"

# B. Push to hiepng15/blog repository
git remote add blog https://github.com/hiepng15/blog.git
git push blog main

# C. GitHub Actions sẽ tự động:
# - Copy blog content từ hiepng15/blog
# - Paste vào hiepng15.github.io/blog/
# - Deploy to hiepng15.github.io/blog/
```

### 🔄 Workflow tự động:
1. **Viết blog** → `blog/markdown/new-post.md`
2. **AI update** → Tạo HTML + update index.html
3. **Push** → `hiepng15/blog` repository
4. **GitHub Actions** → Auto-deploy to live website

## ⚠️ Lưu ý quan trọng

1. **Backup**: Luôn backup file Markdown gốc
2. **Validation**: Kiểm tra HTML output trước khi commit
3. **Testing**: Test blog trên local trước khi push
4. **Metadata**: Đảm bảo id unique và date format đúng
5. **Featured**: Chỉ có 1 bài viết có featured = true

## 🔧 Troubleshooting

### Lỗi thường gặp:
- **Front matter không đúng format**: Kiểm tra dấu `---`
- **ID trùng lặp**: Đổi id trong metadata
- **Date format sai**: Sử dụng YYYY-MM-DD
- **HTML không render**: Kiểm tra syntax Markdown

### Debug:
```javascript
// Kiểm tra metadata
console.log(parsedMetadata);

// Kiểm tra HTML output
console.log(htmlContent);

// Validate JSON
JSON.parse(metadataJson);
```

---

**📞 Khi cần AI update blog, chỉ cần cung cấp file Markdown và nói: "Hãy update blog theo hướng dẫn trong AI_BLOG_GUIDE.md"** 