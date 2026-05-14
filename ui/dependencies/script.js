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
    if (percent === 0) percent = 10
    PROGRESS.style.width = percent + "%";

    PROGRESSLOG.textContent = translation[`stage_log_${stage}`] ?? `[stage_log_${stage}]`;
    PROGRESSLOG.dataset.key = `stage_log_${stage}`;
}

async function addPkgLog(pkgs) {
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

async function checkPkgLog(pkg, state) {
    var lang = document.querySelector(`#${pkg} lang`)
    if (state === 0) lang.style.fontWeight = "bold";
    if (state === 1) {
        lang.style.fontStyle = "italic"
        lang.style.fontWeight = "unset"
        lang.textContent = format(translation[`pkg_log_installed`] ?? "[pkg_log_installed]", {pkg: pkg});
    };
    if (state === -1) {
        lang.style.fontStyle = "normal"
        lang.style.fontWeight = "unset"
        lang.style.color = "red";
        lang.textContent = format(translation[`pkg_log_error`] ?? "[pkg_log_error]", {pkg: pkg});
    };

    var input = document.querySelector(`#${pkg} input`)
    if (state === 1) input.checked = true;
}

// Export to Python
window.checkPkgLog = checkPkgLog

async function loadStage() {
    await new Promise(r => setTimeout(r, 2000));
    STAGE = await window.pywebview.api.get_stage();
    await setStep(STAGE[0])

    if (STAGE[0] === 0) {
        PKGSECTION.style.display = "flex";
        await addPkgLog(STAGE[1])

        window.pywebview.api.install_package();
    }

    if (STAGE[0] === 1) {
        PKGSECTION.style.display = "none";
    }
}

window.loadStage = loadStage;


// ! Start Eventi
window.addEventListener("pywebviewready", async () => {
    await loadLanguage();
    loadStage();
});