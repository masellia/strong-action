// This script runs in the document head to avoid a light-theme flash.
let medium_zoom;

const determineThemeSetting = () => {
  const setting = localStorage.getItem("theme");
  return ["system", "light", "dark"].includes(setting) ? setting : "system";
};

const determineComputedTheme = () => {
  const setting = determineThemeSetting();
  if (setting !== "system") return setting;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
};

const applyTheme = () => {
  const theme = determineComputedTheme();
  document.documentElement.setAttribute("data-theme", theme);

  document.querySelectorAll("table").forEach((table) => {
    table.classList.toggle("table-dark", theme === "dark");
  });

  const search = document.querySelector("ninja-keys");
  if (search) search.classList.toggle("dark", theme === "dark");

  if (medium_zoom) {
    const background = getComputedStyle(document.documentElement).getPropertyValue("--global-bg-color") + "ee";
    medium_zoom.update({ background });
  }
};

const setThemeSetting = (setting) => {
  localStorage.setItem("theme", setting);
  document.documentElement.setAttribute("data-theme-setting", setting);
  applyTheme();
};

const toggleThemeSetting = () => {
  const setting = determineThemeSetting();
  setThemeSetting(setting === "system" ? "light" : setting === "light" ? "dark" : "system");
};

const initTheme = () => {
  document.documentElement.setAttribute("data-theme-setting", determineThemeSetting());
  document.documentElement.setAttribute("data-theme", determineComputedTheme());

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (determineThemeSetting() === "system") applyTheme();
  });

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("light-toggle")?.addEventListener("click", toggleThemeSetting);
    applyTheme();
  });
};
