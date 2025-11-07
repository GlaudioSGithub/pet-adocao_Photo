document.addEventListener("DOMContentLoaded", function() {
    const elements = document.querySelectorAll(".fade-in-title, .fade-in-banner, .fade-in-buttons");

    elements.forEach((el, index) => {
        el.style.opacity = 0;
        setTimeout(() => {
            el.style.transition = "opacity 1s ease, transform 1s ease";
            el.style.opacity = 1;
            el.style.transform = "translateY(0)";
        }, 200 * index);
    });
});


self.addEventListener('install', event => {
  console.log('Service Worker instalado.');
});

self.addEventListener('fetch', event => {
  // Aqui você poderia adicionar cache, se quiser PWA offline
});
