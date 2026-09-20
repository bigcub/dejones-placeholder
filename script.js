const root = document.documentElement;
const landscape = document.querySelector(".landscape");
const themeToggle = document.querySelector("#theme-toggle");
const sceneToggle = document.querySelector("#scene-toggle");
const parallaxLayers = document.querySelectorAll(".parallax");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

function updateThemeButton() {
  if (!themeToggle) return;
  const isDark = root.dataset.theme === "dark";
  themeToggle.setAttribute("aria-pressed", String(isDark));
  themeToggle.setAttribute(
    "aria-label",
    isDark ? "Switch to light colour theme" : "Switch to dark colour theme",
  );
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute("content", document.body.classList.contains("notes-page")
      ? (isDark ? "#1c282c" : "#f5f1e8")
      : (isDark ? "#171d38" : "#a96670"));
}

themeToggle?.addEventListener("click", () => {
  root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
  localStorage.setItem("theme", root.dataset.theme);
  updateThemeButton();
});

function updateSceneButton() {
  if (!sceneToggle) return;
  const nextScene = { meadow: "coast", ocean: "Blea Tarn", tarn: "Kielder Forest", forest: "meadow" }[root.dataset.scene];
  sceneToggle.setAttribute("aria-label", `Switch to ${nextScene} scene`);
  sceneToggle.title = `Switch to ${nextScene} scene`;
  const descriptions = {
    meadow: "A quiet landscape at the edge of evening",
    ocean: "A quiet sea with a sailing boat at the edge of evening",
    tarn: "A stone bothy beside a still mountain tarn",
    forest: "A timber lookout among the pines of Kielder Forest",
  };
  landscape?.setAttribute("aria-label", descriptions[root.dataset.scene]);
}

sceneToggle?.addEventListener("click", () => {
  const scenes = ["meadow", "ocean", "tarn", "forest"];
  root.dataset.scene = scenes[(scenes.indexOf(root.dataset.scene) + 1) % scenes.length];
  localStorage.setItem("scene", root.dataset.scene);
  resetScene();
  updateSceneButton();
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
updateSceneButton();

// Always show the writing on arrival; hiding it is a temporary viewing choice.
const articlesToggle = document.querySelector("#articles-toggle");
const articleShelf = document.querySelector("#article-shelf");
articlesToggle?.addEventListener("click", () => {
  articleShelf.hidden = !articleShelf.hidden;
  articlesToggle.setAttribute("aria-expanded", String(!articleShelf.hidden));
  articlesToggle.querySelector("span").textContent = articleShelf.hidden ? "Show notes" : "Hide notes";
  root.dataset.articlesHidden = String(articleShelf.hidden);
});
