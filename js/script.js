// Blog functionality
class BlogManager {
  constructor() {
    this.metadata = null;
    this.currentPage = 'home';
    this.init();
  }

  async init() {
    try {
      await this.loadMetadata();
      this.setupEventListeners();
      this.renderPage();
    } catch (error) {
      console.error('Error initializing blog:', error);
      this.showError('Failed to load blog content');
    }
  }

  async loadMetadata() {
    try {
      const response = await fetch('./metadata.json');
      if (!response.ok) {
        throw new Error('Failed to load metadata');
      }
      this.metadata = await response.json();
    } catch (error) {
      console.error('Error loading metadata:', error);
      throw error;
    }
  }

  setupEventListeners() {
    // Handle navigation
    document.addEventListener('click', (e) => {
      if (e.target.matches('.nav a')) {
        e.preventDefault();
        const href = e.target.getAttribute('href');
        this.navigateTo(href);
      }
      
      if (e.target.closest('.post-card')) {
        e.preventDefault();
        const postId = e.target.closest('.post-card').dataset.postId;
        this.navigateTo(`./posts/${postId}.html`);
      }
    });

    // Handle back button
    window.addEventListener('popstate', (e) => {
      this.handleRouteChange();
    });
  }

  navigateTo(url) {
    if (url === './' || url === './index.html') {
      this.currentPage = 'home';
      window.history.pushState({ page: 'home' }, '', './');
    } else if (url.includes('./posts/')) {
      const postId = url.split('/').pop().replace('.html', '');
      this.currentPage = 'post';
      this.currentPostId = postId;
      window.history.pushState({ page: 'post', postId }, '', url);
    }
    this.renderPage();
  }

  handleRouteChange() {
    const path = window.location.pathname;
    if (path === '/blog/' || path === '/blog/index.html' || path.endsWith('/blog/')) {
      this.currentPage = 'home';
    } else if (path.includes('/posts/')) {
      const postId = path.split('/').pop().replace('.html', '');
      this.currentPage = 'post';
      this.currentPostId = postId;
    }
    this.renderPage();
  }

  renderPage() {
    const mainContent = document.getElementById('main-content');
    if (!mainContent) return;

    if (this.currentPage === 'home') {
      this.renderHomePage(mainContent);
    } else if (this.currentPage === 'post') {
      this.renderPostPage(mainContent);
    }
  }

  renderHomePage(container) {
    if (!this.metadata) {
      container.innerHTML = '<div class="loading">Đang tải bài viết...</div>';
      return;
    }

    const { posts, site } = this.metadata;
    
    // Sort posts by date (newest first)
    const sortedPosts = posts.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    // Separate featured and regular posts
    const featuredPost = sortedPosts.find(post => post.featured);
    const regularPosts = sortedPosts.filter(post => !post.featured);

    let html = `
      <div class="header">
        <h1>${site.title}</h1>
        <p>${site.description}</p>
      </div>
      
      <nav class="nav">
        <a href="./" class="active">Trang chủ</a>
        <a href="https://hiepng15.github.io">Website chính</a>
      </nav>
      
      <div class="posts-grid">
    `;

    // Add featured post first
    if (featuredPost) {
      html += this.renderPostCard(featuredPost, true);
    }

    // Add regular posts
    regularPosts.forEach(post => {
      html += this.renderPostCard(post, false);
    });

    html += `
      </div>
      
      <footer class="footer">
        <p>&copy; 2025 ${site.author}. Được xây dựng với ❤️ và nhiều ☕</p>
        <p><a href="https://hiepng15.github.io">Về website chính</a></p>
      </footer>
    `;

    container.innerHTML = html;
  }

  renderPostCard(post, isFeatured = false) {
    const date = new Date(post.date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    const tagsHtml = post.tags.map(tag => 
      `<span class="post-tag">${tag}</span>`
    ).join('');

    return `
      <article class="post-card ${isFeatured ? 'featured' : ''}" data-post-id="${post.id}">
        <div class="post-meta">
          <span class="post-date">${date}</span>
          <span class="post-read-time">${post.readTime}</span>
        </div>
        
        <div class="post-tags">
          ${tagsHtml}
        </div>
        
        <h2 class="post-title">${post.title}</h2>
        <p class="post-excerpt">${post.excerpt}</p>
        <div class="post-author">Bởi ${post.author}</div>
      </article>
    `;
  }

  async renderPostPage(container) {
    if (!this.metadata) {
      container.innerHTML = '<div class="loading">Đang tải bài viết...</div>';
      return;
    }

    const post = this.metadata.posts.find(p => p.id === this.currentPostId);
    
    if (!post) {
      container.innerHTML = `
        <div class="error">
          <h2>Không tìm thấy bài viết</h2>
          <p>Không thể tìm thấy bài viết yêu cầu.</p>
          <a href="./" class="back-link">← Về trang chủ</a>
        </div>
      `;
      return;
    }

    try {
      // Load post content
      const response = await fetch(`./posts/${post.id}.html`);
      if (!response.ok) {
        throw new Error('Post content not found');
      }
      
      const postContent = await response.text();
      
      const date = new Date(post.date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });

      const tagsHtml = post.tags.map(tag => 
        `<span class="post-tag">${tag}</span>`
      ).join('');

      container.innerHTML = `
        <a href="./" class="back-link">← Về blog</a>
        
        <article class="post-content">
          <header class="post-header">
            <h1>${post.title}</h1>
            <div class="post-meta">
              <span class="post-date">${date}</span>
              <span class="post-read-time">${post.readTime}</span>
            </div>
            <div class="post-tags">
              ${tagsHtml}
            </div>
            <div class="post-author">Bởi ${post.author}</div>
          </header>
          
          <div class="post-body">
            ${postContent}
          </div>
        </article>
        
        <footer class="footer">
          <p>&copy; 2025 ${this.metadata.site.author}</p>
          <p><a href="./">← Về blog</a> | <a href="https://hiepng15.github.io">Website chính</a></p>
        </footer>
      `;
    } catch (error) {
      console.error('Error loading post:', error);
      container.innerHTML = `
        <div class="error">
          <h2>Lỗi tải bài viết</h2>
          <p>Xin lỗi, có lỗi xảy ra khi tải bài viết này.</p>
          <a href="./" class="back-link">← Về trang chủ</a>
        </div>
      `;
    }
  }

  showError(message) {
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      mainContent.innerHTML = `
        <div class="error">
          <h2>Error</h2>
          <p>${message}</p>
          <a href="./" class="back-link">← Back to home</a>
        </div>
      `;
    }
  }
}

// Initialize blog when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new BlogManager();
});

// Handle direct navigation to posts
if (window.location.pathname.includes('/posts/')) {
  const postId = window.location.pathname.split('/').pop().replace('.html', '');
  window.history.replaceState({ page: 'post', postId }, '', window.location.pathname);
} 