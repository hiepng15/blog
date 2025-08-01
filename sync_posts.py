#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đồng bộ dữ liệu từ metadata.json vào index.html
Sử dụng: python sync_posts.py
"""

import json
import re

def load_metadata():
    """Load metadata từ file JSON"""
    try:
        with open('metadata.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Khong tim thay metadata.json")
        return []

def update_index_html(posts_data):
    """Cập nhật posts data trong index.html"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert posts data thành JavaScript
        js_posts = "const posts = " + json.dumps(posts_data, ensure_ascii=False, indent=12)[:-1] + "        ];"
        
        # Tìm và thay thế posts array
        pattern = r'const posts = \[.*?\];'
        new_content = re.sub(pattern, js_posts, content, flags=re.DOTALL)
        
        # Ghi lại file
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Da cap nhat index.html voi {len(posts_data)} bai viet")
        
    except Exception as e:
        print(f"Loi: {e}")

def main():
    print("Dong bo metadata.json -> index.html...")
    metadata = load_metadata()
    if metadata:
        update_index_html(metadata)
    else:
        print("Khong co du lieu de dong bo")

if __name__ == "__main__":
    main()