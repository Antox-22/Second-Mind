import { loadLanguage, reloadLanguage, translation } from "../core/lang.js";

const PROGRESS = document.querySelector(".progress");
const PROGRESSLOG = document.querySelector(".footer .log lang");
const MAXSTAGE = 4;
var STAGE = 0;

// Add step progress bar
function setStep(stage) {
    var percent = (stage / MAXSTAGE) * 100;
    PROGRESS.style.width = percent + "%";

    PROGRESSLOG.textContent = translation[`stage_log_${stage}`] ?? `[stage_log_${stage}]`;
    PROGRESSLOG.dataset.key = `stage_log_${stage}`;
}

function loadStage(stage) {
    setStep(stage)

}


// ! Start Eventi
window.addEventListener("pywebviewready", async () => {
    await loadLanguage();
    STAGE = await window.pywebview.api.get_stage();
    loadStage(STAGE[0]);
});




// DEBUG: RELOAD LANGUAGE
document.getElementById("reloadBtn").addEventListener("click", async () => {
    await reloadLanguage();
});