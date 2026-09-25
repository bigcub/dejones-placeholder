const root = document.documentElement;
const landscape = document.querySelector(".landscape");
const themeToggle = document.querySelector("#theme-toggle");
const sceneToggle = document.querySelector("#scene-toggle");
const sceneNext = document.querySelector("#scene-next");
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
  const nextScene = { meadow: "coast", ocean: "Blea Tarn", tarn: "Kielder Forest", forest: "Merthyr Mawr", desert: "Manchester canal", canal: "meadow" }[root.dataset.scene];
  // The pill carries its own visible label, so name the destination in the
  // tooltip rather than overriding what the button says.
  if (sceneNext) sceneNext.title = `Switch to the ${nextScene} scene`;
  // Notes pages carry the header control so the header keeps its shape, but
  // there is no landscape there to change; the markup explains why it is off.
  if (!sceneToggle || sceneToggle.disabled) return;
  sceneToggle.setAttribute("aria-label", `Switch to ${nextScene} scene`);
  sceneToggle.title = `Switch to ${nextScene} scene`;
  const descriptions = {
    meadow: "A quiet landscape at the edge of evening",
    ocean: "A quiet sea with a sailing boat at the edge of evening",
    tarn: "A stone bothy beside a still mountain tarn",
    forest: "A timber lookout among the pines of Kielder Forest",
    desert: "A small observatory among the Merthyr Mawr dunes",
    canal: "A narrowboat moored on a Manchester canal at dusk",
  };
  landscape?.setAttribute("aria-label", descriptions[root.dataset.scene]);
}

function cycleScene(step = 1) {
  const scenes = ["meadow", "ocean", "tarn", "forest", "desert", "canal"];
  const index = scenes.indexOf(root.dataset.scene);
  root.dataset.scene = scenes[(index + step + scenes.length) % scenes.length];
  localStorage.setItem("scene", root.dataset.scene);
  resetScene();
  updateSceneButton();
}

sceneToggle?.addEventListener("click", () => cycleScene());
sceneNext?.addEventListener("click", () => cycleScene());

// Left and right arrows step through the scenes on the homepage.
document.addEventListener("keydown", (event) => {
  if (!landscape || (sceneToggle && sceneToggle.disabled)) return;
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  if (event.target.closest?.("input, textarea, select, [contenteditable]")) return;
  if (event.key === "ArrowRight") cycleScene(1);
  else if (event.key === "ArrowLeft") cycleScene(-1);
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
