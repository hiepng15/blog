# Hiep's Blog

A static blog built with HTML, CSS, and JavaScript that can be deployed directly to GitHub Pages.

## 📁 Structure

```
blog/
├── index.html              # Main blog page
├── styles.css              # Main stylesheet
├── metadata.json           # Blog posts metadata
├── js/
│   └── script.js           # Blog functionality
├── posts/                  # Individual blog posts
│   ├── ai-computer-vision-research.html
│   ├── mechatronics-engineering.html
│   └── signal-processing-mastery.html
└── README.md               # This file
```

## 🚀 Features

- **Static Site**: No server required, runs entirely in the browser
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern UI**: Clean, minimalist design inspired by Apple and Medium
- **Easy to Update**: Just add new HTML files to the `posts/` directory
- **SEO Friendly**: Proper meta tags and semantic HTML
- **Fast Loading**: Optimized for performance

## ✏️ Adding New Posts

### Method 1: Manual (Recommended)

1. **Create a new HTML file** in the `posts/` directory
   - Use a descriptive filename (e.g., `my-new-post.html`)
   - Only include the content (no HTML structure needed)

2. **Add metadata** to `metadata.json`:
   ```json
   {
     "id": "my-new-post",
     "title": "My New Post Title",
     "excerpt": "A brief description of the post...",
     "date": "2025-01-31",
     "author": "Huy Hiep Nguyen",
     "tags": ["Tag1", "Tag2"],
     "readTime": "5 min read",
     "featured": false
   }
   ```

3. **Write your content** in the HTML file:
   ```html
   <p>Your blog post content here...</p>
   <h2>Section Title</h2>
   <p>More content...</p>
   ```

### Method 2: Using a Generator (Future Enhancement)

You can create a simple script to automate post creation:

```bash
# Example script (not included)
./create-post.sh "My Post Title" "my-post-id"
```

## 🎨 Customization

### Colors and Theme

Edit `styles.css` to customize:
- Background colors
- Text colors
- Accent colors
- Typography

### Layout

The blog uses CSS Grid and Flexbox for layout. Key classes:
- `.container`: Main content wrapper
- `.post-card`: Individual blog post cards
- `.featured-post`: Featured post styling
- `.nav`: Navigation menu

### Fonts

The blog uses Inter font from Google Fonts. To change:
1. Update the Google Fonts link in `index.html`
2. Modify the `font-family` in `styles.css`

## 📱 Responsive Design

The blog is fully responsive with breakpoints at:
- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: 480px - 767px
- **Small Mobile**: < 480px

## 🔧 Technical Details

### JavaScript Features

- **Dynamic Loading**: Posts are loaded from `metadata.json`
- **Client-side Routing**: Navigation without page reloads
- **Error Handling**: Graceful fallbacks for missing content
- **SEO Support**: Proper meta tags and structured data

### Performance Optimizations

- **Minimal Dependencies**: Only Google Fonts external dependency
- **Efficient Loading**: Lazy loading of post content
- **Optimized CSS**: Minimal, focused stylesheets
- **Fast Rendering**: Vanilla JavaScript for maximum performance

## 🌐 Deployment

### GitHub Pages

1. Push your code to GitHub
2. Enable GitHub Pages in repository settings
3. Set source to main branch
4. Your blog will be available at `https://username.github.io/repository-name/blog/`

### Other Platforms

The blog can be deployed to any static hosting service:
- Netlify
- Vercel
- AWS S3
- Any web server

## 📊 Analytics (Optional)

To add analytics, include tracking code in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🔍 SEO Optimization

The blog includes:
- Proper meta tags
- Open Graph tags for social sharing
- Twitter Card support
- Semantic HTML structure
- Clean URLs

## 🛠️ Development

### Local Development

1. Clone the repository
2. Open `blog/index.html` in a browser
3. For live reloading, use a local server:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Node.js
   npx serve blog/
   ```

### Testing

- Test on different devices and browsers
- Validate HTML and CSS
- Check accessibility
- Test performance with Lighthouse

## 📝 Content Guidelines

### Writing Style

- Use clear, concise language
- Include code examples when relevant
- Add images and diagrams for complex topics
- Keep paragraphs short for readability

### HTML Structure

- Use semantic HTML tags (`<h1>`, `<h2>`, `<p>`, `<ul>`, etc.)
- Avoid inline styles
- Keep content focused and well-structured

### Images

- Optimize images for web (compress, resize)
- Use descriptive alt text
- Consider lazy loading for large images

## 🤝 Contributing

To contribute to the blog:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This blog template is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check the browser console for errors
2. Verify all files are in the correct locations
3. Ensure `metadata.json` is valid JSON
4. Test with a different browser

## 🔮 Future Enhancements

Potential improvements:
- Search functionality
- Category/tag filtering
- Comment system
- RSS feed
- Dark/light theme toggle
- Reading time estimation
- Social sharing buttons
- Related posts
- Newsletter signup

---

**Built with ❤️ by Huy Hiep Nguyen** # Blog Integration Complete
