// dashboard.js

document.addEventListener("DOMContentLoaded", () => {
  const fills = document.querySelectorAll(".progress-fill");

  fills.forEach(fill => {
    const width = fill.style.width;
    fill.style.width = "0%";

    setTimeout(() => {
      fill.style.width = width;
    }, 100);
  });
});
