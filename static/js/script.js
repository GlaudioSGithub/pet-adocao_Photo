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
