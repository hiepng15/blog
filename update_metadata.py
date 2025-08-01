#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đơn giản để quản lý metadata.json
Sử dụng: python update_metadata.py [list|add|remove]
"""

import json
import sys
import os
from datetime import datetime

def load_metadata():
    """Load metadata từ file JSON"""
    try:
        with open('metadata.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_metadata(metadata):
    """Lưu metadata vào file JSON"""
    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def add_post(post_id, title, excerpt, date, category, tags, author="Huy Hiep Nguyen", featured=False):
    """Thêm bài viết mới vào metadata"""
    metadata = load_metadata()
    
    # Tạo số thứ tự mới (bài mới nhất là số 1)
    new_stt = 1
    for post in metadata:
        post['stt'] += 1
    
    # Tạo bài viết mới
    new_post = {
        "id": post_id,
        "stt": new_stt,
        "title": title,
        "excerpt": excerpt,
        "date": date,
        "author": author,
        "category": category,
        "tags": tags.split(',') if isinstance(tags, str) else tags,
        "featured": featured,
        "file": f"posts/{post_id}.html"
    }
    
    # Thêm vào đầu mảng (bài mới nhất)
    metadata.insert(0, new_post)
    
    # Lưu lại
    save_metadata(metadata)
    
    print(f"Da them bai viet: {title}")
    print(f"So thu tu: {new_stt}")
    print(f"File: posts/{post_id}.html")
    
    return new_post

def remove_post(post_id):
    """Xóa bài viết khỏi metadata"""
    metadata = load_metadata()
    
    # Tìm và xóa bài viết
    for i, post in enumerate(metadata):
        if post['id'] == post_id:
            removed_post = metadata.pop(i)
            
            # Cập nhật lại số thứ tự
            for j, post in enumerate(metadata):
                post['stt'] = j + 1
            
            save_metadata(metadata)
            print(f"Da xoa bai viet: {removed_post['title']}")
            return removed_post
    
    print(f"Khong tim thay bai viet voi ID: {post_id}")
    return None

def list_posts():
    """Liệt kê tất cả bài viết"""
    metadata = load_metadata()
    
    if not metadata:
        print("Chua co bai viet nao")
        return
    
    print(f"Tong cong {len(metadata)} bai viet:")
    print("-" * 80)
    
    for post in metadata:
        try:
            title = post['title']
            tags = ', '.join(post['tags'])
            print(f"#{post['stt']:2d} | {post['date']} | {post['category']:4s} | {title}")
            print(f"     ID: {post['id']}")
            print(f"     Tags: {tags}")
            print()
        except Exception as e:
            print(f"Loi khi hien thi bai viet: {e}")
            print(f"Post data: {post}")
            print()

def generate_template(post_id, title, excerpt, date, category, tags):
    """Tạo template cho bài viết mới"""
    template = f'''---
title: "{title}"
excerpt: "{excerpt}"
date: "{date}"
author: "Huy Hiep Nguyen"
category: "{category}"
tags: [{', '.join([f'"{tag.strip()}"' for tag in tags.split(',')])}]
featured: false
---

# {title}

{excerpt}

## Mở đầu

Viết nội dung mở đầu của bài viết ở đây...

## Nội dung chính

### Phần 1

Viết nội dung phần 1...

### Phần 2

Viết nội dung phần 2...

## Kết luận

Viết phần kết luận...

---
*Bài viết được viết vào {date}*
'''
    
    # Tạo thư mục markdown nếu chưa có
    os.makedirs('markdown', exist_ok=True)
    
    # Lưu template
    template_file = f"markdown/{post_id}.md"
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"Da tao template: {template_file}")
    return template_file

def main():
    if len(sys.argv) < 2:
        print("Sử dụng:")
        print("  python update_metadata.py add <id> <title> <excerpt> <date> <category> <tags>")
        print("  python update_metadata.py remove <id>")
        print("  python update_metadata.py list")
        print("  python update_metadata.py template <id> <title> <excerpt> <date> <category> <tags>")
        print("\nVí dụ:")
        print("  python update_metadata.py add my-new-post 'Tiêu đề bài viết' 'Mô tả ngắn' 'January 30, 2025' blog 'AI, Machine Learning'")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 7:
            print("Thieu tham so. Su dung: python update_metadata.py add <id> <title> <excerpt> <date> <category> <tags>")
            sys.exit(1)
        
        post_id = sys.argv[2]
        title = sys.argv[3]
        excerpt = sys.argv[4]
        date = sys.argv[5]
        category = sys.argv[6]
        tags = sys.argv[7] if len(sys.argv) > 7 else ""
        
        add_post(post_id, title, excerpt, date, category, tags)
        
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Thieu ID bai viet. Su dung: python update_metadata.py remove <id>")
            sys.exit(1)
        
        post_id = sys.argv[2]
        remove_post(post_id)
        
    elif command == "list":
        list_posts()
        
    elif command == "template":
        if len(sys.argv) < 7:
            print("Thieu tham so. Su dung: python update_metadata.py template <id> <title> <excerpt> <date> <category> <tags>")
            sys.exit(1)
        
        post_id = sys.argv[2]
        title = sys.argv[3]
        excerpt = sys.argv[4]
        date = sys.argv[5]
        category = sys.argv[6]
        tags = sys.argv[7] if len(sys.argv) > 7 else ""
        
        template_file = generate_template(post_id, title, excerpt, date, category, tags)
        print(f"\nHoan thanh! Bay gio ban co the:")
        print(f"1. Chinh sua file {template_file}")
        print(f"2. Chay: python convert_markdown.py {template_file}")
        print(f"3. Chay: python update_metadata.py add {post_id} '{title}' '{excerpt}' '{date}' {category} '{tags}'")
        
    else:
        print(f"Lenh khong hop le: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main() 