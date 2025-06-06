// Initialize mobile sidebar toggle
document.addEventListener('DOMContentLoaded', function() {
  // Mobile sidebar toggle
  const mobileToggle = document.querySelector('.sidebar-toggle-mobile');
  const mainWrapper = document.querySelector('.main-wrapper');
  
  if (mobileToggle) {
    mobileToggle.addEventListener('click', function() {
      document.querySelector('.sidebar').classList.toggle('collapsed');
      mainWrapper.classList.toggle('collapsed');
    });
  }
  
  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', function(event) {
    if (window.innerWidth <= 768) {
      const sidebar = document.querySelector('.sidebar');
      const isClickInsideSidebar = sidebar.contains(event.target);
      const isClickOnToggle = event.target.closest('.sidebar-toggle-mobile');
      
      if (!isClickInsideSidebar && !isClickOnToggle && !sidebar.classList.contains('collapsed')) {
        sidebar.classList.add('collapsed');
        mainWrapper.classList.add('collapsed');
      }
    }
  });
  
  // Active link highlighting
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});