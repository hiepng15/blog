#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog Update Script
Tự động convert Markdown thành HTML và update blog

Usage: python update_blog.py <markdown_file.md>
Example: python update_blog.py markdown/new-post.md
"""

import os
import re
import json
import sys
from datetime import datetime
import markdown

def parse_front_matter(content):
    """Parse front matter từ Markdown file"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        raise ValueError("Không tìm thấy front matter trong file Markdown")
    
    front_matter = match.group(1)
    metadata = {}
    
    for line in front_matter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"')
            
            # Parse arrays
            if value.startswith('[') and value.endswith(']'):
                value = json.loads(value)
            # Parse booleans
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
                
            metadata[key] = value
    
    return metadata

def convert_markdown_to_html(content):
    """Convert Markdown content thành HTML"""
    # Remove front matter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Use markdown library for conversion
    md = markdown.Markdown(extensions=['extra', 'codehilite'])
    html = md.convert(content)
    
    return html

def get_next_post_number(category):
    """Lấy số thứ tự tiếp theo cho category"""
    index_file = 'blog/index.html'
    
    if not os.path.exists(index_file):
        return 1
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all post numbers for this category
    pattern = rf'data-category="{category}".*?post-number">(\d+)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        return 1
    
    # Get highest number and add 1
    max_num = max(int(num) for num in matches)
    return max_num + 1

def update_index_html(metadata, post_number):
    """Cập nhật index.html với post mới"""
    index_file = 'blog/index.html'
    
    if not os.path.exists(index_file):
        print(f"❌ Không tìm thấy {index_file}")
        return False
    
    # Tạo HTML cho post mới
    post_html = f'''
                <div class="post-card" data-category="{metadata['category']}" onclick="openPost('{metadata['id']}')">
                    <div class="post-number">{post_number:02d}</div>
                    <div class="post-meta">
                        <span class="post-date">{metadata['date']}</span>
                        <span class="category-badge {metadata['category']}">{"My Blog" if metadata['category'] == "blog" else "TIL"}</span>
                    </div>
                    <div class="post-tags">
                        {"".join(f'<span class="post-tag">{tag}</span>' for tag in metadata['tags'])}
                    </div>
                    <h2 class="post-title">{metadata['title']}</h2>
                    <p class="post-excerpt">{metadata['excerpt']}</p>
                </div>
'''
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find insertion point based on category
    if metadata['category'] == 'blog':
        # Insert after "<!-- MY BLOG Category -->"
        insert_pattern = r'(<!-- MY BLOG Category -->)'
        replacement = f'\\1{post_html}'
    else:
        # Insert after "<!-- TIL Category -->"
        insert_pattern = r'(<!-- TIL Category -->)'
        replacement = f'\\1{post_html}'
    
    new_content = re.sub(insert_pattern, replacement, content)
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Đã cập nhật index.html với post #{post_number:02d}")
    return True

def update_metadata_json(metadata):
    """Cập nhật metadata.json"""
    metadata_file = 'blog/metadata.json'
    
    # Load existing metadata
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"posts": []}
    
    # Add new post to beginning
    data["posts"].insert(0, metadata)
    
    # Sort by date (newest first)
    data["posts"].sort(key=lambda x: x['date'], reverse=True)
    
    # Ensure only one featured post
    featured_count = sum(1 for post in data["posts"] if post.get('featured', False))
    if featured_count > 1:
        for i, post in enumerate(data["posts"]):
            if post.get('featured', False) and i > 0:
                post['featured'] = False
    
    # Save updated metadata
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Đã cập nhật metadata.json")

def main():
    if len(sys.argv) != 2:
        print("❌ Usage: python update_blog.py <markdown_file.md>")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    if not os.path.exists(markdown_file):
        print(f"❌ Không tìm thấy file: {markdown_file}")
        sys.exit(1)
    
    print(f"🚀 Đang xử lý: {markdown_file}")
    
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse metadata
    try:
        metadata = parse_front_matter(content)
        print(f"📋 Metadata: {metadata['title']}")
    except ValueError as e:
        print(f"❌ Lỗi parse metadata: {e}")
        sys.exit(1)
    
    # Convert to HTML
    html_content = convert_markdown_to_html(content)
    
    # Create HTML file
    html_file = f"blog/posts/{metadata['id']}.html"
    os.makedirs(os.path.dirname(html_file), exist_ok=True)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Đã tạo: {html_file}")
    
    # Get next post number
    post_number = get_next_post_number(metadata['category'])
    print(f"🔢 Post number: {post_number:02d}")
    
    # Update index.html
    update_index_html(metadata, post_number)
    
    # Update metadata.json
    update_metadata_json(metadata)
    
    print(f"""
🎉 Blog update hoàn thành!

📁 Files được tạo/cập nhật:
   - {html_file}
   - blog/index.html
   - blog/metadata.json

📤 Lệnh deploy tiếp theo:
   git add blog/
   git commit -m "Add new blog post: {metadata['title']}"
   git push blog main

🌐 Test local:
   python -m http.server 8000 --directory blog
   → http://localhost:8000
""")

if __name__ == "__main__":
    main()