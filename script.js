const root = document.documentElement;
const landscape = document.querySelector(".landscape");
const themeToggle = document.querySelector("#theme-toggle");
const parallaxLayers = document.querySelectorAll(".parallax");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

function updateThemeButton() {
  const isDark = root.dataset.theme === "dark";
  themeToggle.setAttribute("aria-pressed", String(isDark));
  themeToggle.setAttribute(
    "aria-label",
    isDark ? "Switch to light colour theme" : "Switch to dark colour theme",
  );
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute("content", isDark ? "#17211e" : "#e7d6bb");
}

themeToggle?.addEventListener("click", () => {
  root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
  localStorage.setItem("theme", root.dataset.theme);
  updateThemeButton();
});

function moveScene(event) {
  if (reduceMotion.matches || !landscape) return;

  const bounds = landscape.getBoundingClientRect();
  const x = (event.clientX - bounds.left) / bounds.width - 0.5;
  const y = (event.clientY - bounds.top) / bounds.height - 0.5;

  parallaxLayers.forEach((layer) => {
    if (layer.classList.contains("cloud")) return;
    const depth = Number(layer.dataset.depth ?? 0);
    layer.style.setProperty("--parallax-x", `${x * depth * -12}px`);
    layer.style.setProperty("--parallax-y", `${y * depth * -7}px`);
  });
}

function resetScene() {
  parallaxLayers.forEach((layer) => {
    layer.style.removeProperty("--parallax-x");
    layer.style.removeProperty("--parallax-y");
  });
}

landscape?.addEventListener("pointermove", moveScene);
landscape?.addEventListener("pointerleave", resetScene);

updateThemeButton();
