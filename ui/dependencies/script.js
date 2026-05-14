import { format, loadLanguage, reloadLanguage, translation } from "../core/lang.js";

const PROGRESS = document.querySelector(".progress");
const PROGRESSLOG = document.querySelector(".footer .log lang");
const PKGSECTION = document.querySelector(".pkg-section")
const PKGCARD = document.querySelector(".pkg-section .card")
const MAXSTAGE = 4;
var STAGE = 0;

// Add step progress bar
function setStep(stage) {
    var percent = (stage / MAXSTAGE) * 100;
    PROGRESS.style.width = percent + "%";

    PROGRESSLOG.textContent = translation[`stage_log_${stage}`] ?? `[stage_log_${stage}]`;
    PROGRESSLOG.dataset.key = `stage_log_${stage}`;
}

function addPkgLog(pkgs) {
    // <span class="log"><input type="checkbox" disabled></input><lang>hbfdhbdhh</lang></span>
    pkgs.forEach(pkg => {
        var span = document.createElement("span");
        span.classList.add("log")
        span.id = pkg;

        var input = document.createElement("input");
        input.type = "checkbox";
        input.disabled = true;

        var lang = document.createElement("lang");
        lang.dataset.key = "pkg_log";
        lang.textContent = format(translation[`pkg_log`] ?? "[pkg_log]", {pkg: pkg});

        span.appendChild(input);
        span.appendChild(lang);

        PKGCARD.appendChild(span);
    });
}

function loadStage(stage) {
    setStep(stage[0])

    if (stage[0] == 0) {
        PKGSECTION.style.display = "flex";
        addPkgLog(stage[1])
    }
}


// ! Start Eventi
window.addEventListener("pywebviewready", async () => {
    await loadLanguage();
    STAGE = await window.pywebview.api.get_stage();
    loadStage(STAGE);
});