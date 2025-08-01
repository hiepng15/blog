#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đơn giản để convert 1 file Markdown sang HTML
Sử dụng: python convert_markdown.py markdown/your-file.md
"""

import sys
import re
import json
import os
from datetime import datetime

try:
    from markdown import Markdown
except ImportError:
    print("Loi: Khong the import module markdown")
    print("Hay cai dat: pip install markdown")
    sys.exit(1)

def parse_front_matter(content):
    """Parse front matter từ Markdown"""
    pattern = r'^---\n(.*?)\n---\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        raise ValueError("Không tìm thấy front matter")
    
    front_matter_text = match.group(1)
    markdown_content = match.group(2)
    
    # Parse front matter
    metadata = {}
    for line in front_matter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"')
            
            if key == 'tags':
                # Parse tags array
                value = [tag.strip().strip('"\'') for tag in value.strip('[]').split(',')]
            elif key == 'featured':
                value = value.lower() == 'true'
            
            metadata[key] = value
    
    return metadata, markdown_content

def convert_markdown_to_html(markdown_content):
    """Convert Markdown sang HTML với custom extensions"""
    try:
        md = Markdown(extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc'
        ])
    except AttributeError:
        # Fallback for older versions
        md = Markdown()
    
    html = md.convert(markdown_content)
    
    # Custom processing
    # 1. Fix paragraphs (exclude img, div, and table tags)
    html = re.sub(r'^(?!<[h|u|o]|<li|<blockquote|<p|<img|<div|<table|</table)(.+)$', r'<p>\1</p>', html, flags=re.MULTILINE)
    
    # 2. Clean up table structure - remove unnecessary <p> tags inside tables
    html = re.sub(r'<p>(<thead>|<tbody>|<tr>|<th[^>]*>|<td[^>]*>|</thead>|</tbody>|</tr>|</th>|</td>)</p>', r'\1', html)
    
    # 3. Additional cleanup for table cells - remove <p> tags around table content
    # Remove <p> tags that are inside table cells (more comprehensive)
    html = re.sub(r'<td[^>]*><p>([^<]*(?:<[^>]+>[^<]*)*)</p></td>', r'<td\1></td>', html)
    html = re.sub(r'<th[^>]*><p>([^<]*(?:<[^>]+>[^<]*)*)</p></th>', r'<th\1></th>', html)
    
    # 2. Process code blocks with language detection
    def process_code_block(match):
        language = match.group(1) or 'text'
        code_content = match.group(2)
        
        # Count lines to determine if we need line numbers
        lines = code_content.strip().split('\n')
        has_line_numbers = len(lines) > 10  # Show line numbers for code with more than 10 lines
        
        # Escape HTML entities in code content
        code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Add copy button and line numbers if needed
        copy_button = '<button class="copy-button" onclick="copyCode(this)">Copy</button>'
        line_class = ' long-code' if has_line_numbers else ''
        
        return f'<div class="code-block{line_class}" data-language="{language}">{copy_button}<pre><code>{code_content}</code></pre></div>'
    
    # Process both raw markdown code blocks and fenced code blocks
    html = re.sub(r'```(\w+)?\n([\s\S]*?)```', process_code_block, html)
    
    # Also process fenced code blocks that were already converted by markdown extension
    def process_fenced_code(match):
        language = match.group(1) or 'text'
        code_content = match.group(2)
        
        # Remove <p> tags that might be inside the code
        code_content = re.sub(r'<p>(.*?)</p>', r'\1', code_content)
        
        # Count lines to determine if we need line numbers
        lines = code_content.strip().split('\n')
        has_line_numbers = len(lines) > 10
        
        # Add copy button and line numbers if needed
        copy_button = '<button class="copy-button" onclick="copyCode(this)">Copy</button>'
        line_class = ' long-code' if has_line_numbers else ''
        
        return f'<div class="code-block{line_class}" data-language="{language}">{copy_button}<pre><code>{code_content}</code></pre></div>'
    
    html = re.sub(r'<pre><code class="language-(\w+)">(.*?)</code></pre>', process_fenced_code, html, flags=re.DOTALL)
    
    # 3. Process inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 4. Process images with caption
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<div class="post-image-container"><img src="\2" alt="\1" class="post-image"><div class="post-image-caption">\1</div></div>', html)
    
    return html

def create_html_template(metadata, html_content):
    """Tạo HTML template hoàn chỉnh"""
    category_label = "Blog" if metadata['category'] == 'blog' else "TIL"
    
    template = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']} - Blog của Hiệp</title>
    <meta name="description" content="{metadata['excerpt']}">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- MathJax for mathematical formulas -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }},
            svg: {{
                fontCache: 'global'
            }}
        }};
    </script>
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: #1f1f1f;
            background-image: 
                radial-gradient(circle at 25% 25%, rgba(255,255,255,0.04) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(255,255,255,0.04) 0%, transparent 50%);
            color: #ffffff;
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            flex: 1;
        }}
        
        /* Navigation */
        .nav-back {{
            margin-bottom: 40px;
        }}
        
        .back-button {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #64ffda;
            text-decoration: none;
            font-weight: 500;
            padding: 10px 20px;
            border: 1px solid #64ffda;
            border-radius: 25px;
            transition: all 0.3s ease;
            background: rgba(100, 255, 218, 0.1);
        }}
        
        .back-button:hover {{
            background: #64ffda;
            color: #1f1f1f;
            transform: translateY(-2px);
        }}
        
        /* Post Header */
        .post-header {{
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 1px solid #233554;
        }}
        
        .post-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .post-date {{
            color: #8892b0;
            font-size: 0.9rem;
        }}
        
        .post-category {{
            background: #64ffda;
            color: #1f1f1f;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        
        .post-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 20px;
            line-height: 1.2;
        }}
        
        .post-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
        }}
        
        .post-tag {{
            background: rgba(100, 255, 218, 0.1);
            color: #64ffda;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            border: 1px solid rgba(100, 255, 218, 0.2);
        }}
        
        .post-author {{
            color: #64ffda;
            font-weight: 500;
            font-size: 1.1rem;
        }}
        
        /* Post Content */
        .post-content {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #e6e6e6;
        }}
        
        .post-content h1, .post-content h2, .post-content h3, .post-content h4, .post-content h5, .post-content h6 {{
            color: #ffffff;
            margin: 40px 0 20px 0;
            font-weight: 600;
        }}
        
        .post-content h1 {{
            font-size: 2rem;
        }}
        
        .post-content h2 {{
            font-size: 1.8rem;
        }}
        
        .post-content h3 {{
            font-size: 1.5rem;
        }}
        
        .post-content p {{
            margin-bottom: 20px;
        }}
        
        .post-content ul, .post-content ol {{
            margin: 20px 0;
            padding-left: 30px;
        }}
        
        .post-content li {{
            margin-bottom: 10px;
        }}
        
        .post-content strong {{
            color: #64ffda;
            font-weight: 600;
        }}
        
        .post-content em {{
            color: #8892b0;
            font-style: italic;
        }}
        
        .post-content hr {{
            border: none;
            border-top: 1px solid #233554;
            margin: 40px 0;
        }}
        
        .post-content blockquote {{
            border-left: 4px solid #64ffda;
            padding-left: 20px;
            margin: 20px 0;
            color: #8892b0;
            font-style: italic;
        }}
        
        /* Math and Image styles */
        .math-formula {{
            margin: 20px 0;
            text-align: center;
            overflow-x: auto;
        }}
        
        .math-formula.inline {{
            display: inline;
            margin: 0 5px;
        }}
        
        .post-image {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .post-image-container {{
            text-align: center;
            margin: 20px 0;
        }}
        
        .post-image-caption {{
            font-size: 0.9rem;
            color: #8892b0;
            margin-top: 8px;
            font-style: italic;
        }}
        
        .code-block {{
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 12px;
            margin: 16px 0;
            overflow-x: auto;
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', monospace;
            font-size: 0.85rem;
            line-height: 1.4;
            position: relative;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }}
        
        .code-block::before {{
            content: attr(data-language);
            position: absolute;
            top: 0;
            right: 12px;
            background: #30363d;
            color: #8b949e;
            padding: 2px 8px;
            font-size: 0.75rem;
            border-radius: 0 0 4px 4px;
            text-transform: uppercase;
            font-weight: 500;
        }}
        
        .code-block pre {{
            margin: 0;
            color: #c9d1d9;
        }}
        
        .code-block code {{
            color: #c9d1d9;
        }}
        
        /* Syntax highlighting colors */
        .code-block .keyword {{
            color: #ff7b72;
        }}
        
        .code-block .string {{
            color: #a5d6ff;
        }}
        
        .code-block .comment {{
            color: #8b949e;
            font-style: italic;
        }}
        
        .code-block .function {{
            color: #d2a8ff;
        }}
        
        .code-block .number {{
            color: #79c0ff;
        }}
        
        .code-block .operator {{
            color: #ff7b72;
        }}
        
        /* Inline code */
        .post-content code:not(.code-block code) {{
            background: rgba(110, 118, 129, 0.4);
            color: #c9d1d9;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.85em;
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', monospace;
        }}
        
        /* Table Styles */
        .post-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .post-content thead {{
            background: rgba(100, 255, 218, 0.1);
        }}
        
        .post-content th {{
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: #64ffda;
            border-bottom: 2px solid rgba(100, 255, 218, 0.3);
        }}
        
        .post-content td {{
            padding: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: #e0e0e0;
        }}
        
        .post-content tr:hover {{
            background: rgba(255, 255, 255, 0.02);
        }}
        
        .post-content tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        /* Copy button for code blocks */
        .code-block {{
            position: relative;
        }}
        
        .copy-button {{
            position: absolute;
            top: 8px;
            right: 40px;
            background: #30363d;
            color: #8b949e;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.2s ease;
        }}
        
        .code-block:hover .copy-button {{
            opacity: 1;
        }}
        
        .copy-button:hover {{
            background: #484f58;
            color: #c9d1d9;
        }}
        
        /* Line numbers for long code blocks */
        .code-block.long-code {{
            counter-reset: line;
        }}
        
        .code-block.long-code pre {{
            display: flex;
        }}
        
        .code-block.long-code code {{
            counter-increment: line;
            display: block;
            padding-left: 3.5em;
            position: relative;
        }}
        
        .code-block.long-code code::before {{
            content: counter(line);
            position: absolute;
            left: 0;
            width: 2.5em;
            text-align: right;
            color: #484f58;
            font-size: 0.9em;
            padding-right: 1em;
            border-right: 1px solid #30363d;
        }}
        
        .highlight-box {{
            background: rgba(100, 255, 218, 0.1);
            border-left: 4px solid #64ffda;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .warning-box {{
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .info-box {{
            background: rgba(13, 202, 240, 0.1);
            border-left: 4px solid #0dcaf0;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        /* Footer */
        .footer {{
            background: #1f1f1f;
            background-image: 
                radial-gradient(circle at 25% 25%, rgba(255,255,255,0.04) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(255,255,255,0.04) 0%, transparent 50%);
            border-top: 1px solid rgba(255, 255, 255, 0.03);
            padding: 40px 0;
            margin-top: 60px;
            text-align: center;
            position: relative;
            width: 100vw;
            margin-left: calc(-50vw + 50%);
        }}
        
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 8vw;
            text-align: center;
        }}
        
        .footer-text {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            align-items: center;
        }}
        
        .copyright {{
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            letter-spacing: 0.5px;
        }}
        
        .tagline {{
            font-size: 16px;
            color: #888;
            font-style: italic;
            margin: 4px 0;
        }}
        
        .version {{
            font-size: 14px;
            color: #666;
            font-family: 'Courier New', monospace;
            letter-spacing: 0.3px;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .container {{
                padding: 20px 15px;
            }}
            
            .post-title {{
                font-size: 2rem;
            }}
            
            .post-content {{
                font-size: 1rem;
            }}
            
            .post-content h1 {{
                font-size: 1.8rem;
            }}
            
            .post-content h2 {{
                font-size: 1.6rem;
            }}
            
            .post-content h3 {{
                font-size: 1.4rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            .post-title {{
                font-size: 1.8rem;
            }}
            
            .post-content {{
                font-size: 0.95rem;
            }}
            
            .post-content h1 {{
                font-size: 1.6rem;
            }}
            
            .post-content h2 {{
                font-size: 1.4rem;
            }}
            
            .post-content h3 {{
                font-size: 1.2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Navigation -->
        <nav class="nav-back">
            <a href="../index.html" class="back-button">
                ← Quay lại trang chủ
            </a>
        </nav>
        
        <!-- Post Header -->
        <header class="post-header">
            <div class="post-meta">
                <span class="post-date">{metadata['date']}</span>
                <span class="post-category">{category_label}</span>
            </div>
            
            <h1 class="post-title">{metadata['title']}</h1>
            
            <div class="post-tags">
                {''.join([f'<span class="post-tag">{tag}</span>' for tag in metadata['tags']])}
            </div>
            
            <div class="post-author">Bởi {metadata['author']}</div>
        </header>
        
        <!-- Post Content -->
        <article class="post-content">
            {html_content}
        </article>
    </div>
    
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-text">
                <div class="copyright">© 2025 Hiep Nguyen</div>
                <div class="tagline">Vietnamese soul, global impact</div>
                <div class="version">Est. 1997 | Version 27.0 (and counting!)</div>
            </div>
        </div>
    </footer>
    
    <script>
        // Copy code functionality
        function copyCode(button) {{
            const codeBlock = button.parentElement;
            const code = codeBlock.querySelector('code').textContent;
            
            navigator.clipboard.writeText(code).then(function() {{
                // Change button text temporarily
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                button.style.background = '#238636';
                button.style.color = '#ffffff';
                
                setTimeout(function() {{
                    button.textContent = originalText;
                    button.style.background = '#30363d';
                    button.style.color = '#8b949e';
                }}, 2000);
            }}).catch(function(err) {{
                console.error('Could not copy text: ', err);
                button.textContent = 'Failed';
                button.style.background = '#da3633';
                button.style.color = '#ffffff';
            }});
        }}
        
        // Disable syntax highlighting to avoid conflicts
        // Code blocks will display with basic styling only
    </script>
</body>
</html>'''
    
    return template

def process_markdown_file(markdown_file_path):
    """Xử lý file Markdown và tạo HTML"""
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse front matter
    metadata, markdown_content = parse_front_matter(content)
    
    # Validate required fields
    required_fields = ['title', 'excerpt', 'date', 'author', 'category', 'tags']
    for field in required_fields:
        if field not in metadata:
            raise ValueError(f"Thiếu field bắt buộc: {field}")
    
    # Validate category
    if metadata['category'] not in ['blog', 'til']:
        raise ValueError("Category phải là 'blog' hoặc 'til'")
    
    # Convert to HTML
    html_content = convert_markdown_to_html(markdown_content)
    
    # Create complete HTML template
    html_template = create_html_template(metadata, html_content)
    
    # Generate filename
    filename = markdown_file_path.split('/')[-1].replace('.md', '.html')
    output_path = f"posts/{filename}"
    
    # Ensure posts directory exists
    os.makedirs('posts', exist_ok=True)
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return metadata, output_path

def update_index_html(metadata, html_file):
    """Tạo JavaScript code để thêm vào index.html"""
    post_id = html_file.replace('posts/', '').replace('.html', '')
    
    js_code = f'''    {{
        id: '{post_id}',
        title: '{metadata['title']}',
        excerpt: '{metadata['excerpt']}',
        date: '{metadata['date']}',
        author: '{metadata['author']}',
        category: '{metadata['category']}',
        tags: {metadata['tags']},
        featured: {str(metadata.get('featured', False)).lower()},
        file: '{html_file}'
    }}'''
    
    return js_code

def main():
    if len(sys.argv) != 2:
        print("Sử dụng: python convert_markdown.py markdown/your-file.md")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    if not os.path.exists(markdown_file):
        print(f"File không tồn tại: {markdown_file}")
        sys.exit(1)
    
    try:
        # Process markdown file
        metadata, html_file = process_markdown_file(markdown_file)
        
        print(f"✅ Đã tạo thành công: {html_file}")
        print(f"📝 Metadata:")
        for key, value in metadata.items():
            print(f"   {key}: {value}")
        
        # Generate JavaScript code for index.html
        js_code = update_index_html(metadata, html_file)
        print(f"\n📋 Thêm vào mảng posts trong index.html:")
        print(js_code)
        
        print(f"\n🎉 Hoàn thành! Bây giờ bạn cần:")
        print(f"1. Thêm JavaScript code trên vào mảng posts trong index.html")
        print(f"2. Test locally bằng cách mở index.html")
        print(f"3. Commit changes")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 