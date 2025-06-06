const sidebarWrapper = document.querySelector('.sidebar-wrapper');
const toggleBtn = document.getElementById('sidebarToggleBtn');
const mainWrapper = document.querySelector('.main-wrapper');


if (toggleBtn && sidebarWrapper) {
  toggleBtn.addEventListener('click', () => {
    sidebarWrapper.classList.toggle('active');
    mainWrapper.classList.toggle('active');
  });
}
