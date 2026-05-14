import { loadLanguage } from "../core/lang.js";

window.addEventListener("pywebviewready", async () => {
    await loadLanguage();
});