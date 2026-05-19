import { format, loadLanguage, reloadLanguage, translation } from "../core/lang.js";

const PROGRESS = document.querySelector(".progress");
const PROGRESSLOG = document.querySelector(".footer .log lang");
const PKGSECTION = document.querySelector(".section")
const PKGCARD = document.querySelector(".section #pkg")
const CONFCARD = document.querySelector(".section #conf")
const LANGSELECT = document.querySelector("#language")
const SUBMITCONF = document.querySelector("#submit")
const ICON = document.querySelector(".icon")
const HEADER = document.querySelector(".header")
const VERSIONSECTION = document.querySelector(".version-section")
const OLDVERSION = document.querySelector("#oldVersionNumber")
const SPACYSPAN = document.querySelectorAll(".loader span")
const SPACYSUBTITLE = document.querySelector("#span-subtitle")
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

async function addLangSelect(lngs) {
    lngs.forEach(element => {
        // <option value="it" selected>Italiano</option>
        var option = document.createElement("option")
        option.value = element[1]
        option.textContent = element[0]

        LANGSELECT.appendChild(option)

    });
}

// TODO:
function setCorrectVersion(versionName) {
    const box = document.getElementById('newVersionBox');
    const numberSpan = document.getElementById('newVersionNumber');

    // numberSpan.textContent = versionName;

    box.classList.remove('loading');
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

function errorSpacy() {
    SPACYSPAN.forEach(span => {
        span.id = "error"
    });

    console.log(translation)
    SPACYSUBTITLE.textContent = translation["error_spacy"] ?? "[error_spacy]";
}

errorSpacy()

// Export to Python
window.checkPkgLog = checkPkgLog

async function loadStage() {
    await new Promise(r => setTimeout(r, 500));
    STAGE = await window.pywebview.api.get_stage();
    await setStep(STAGE[0])

    if (STAGE[0] === 0 || STAGE[0] === 2) {
        PKGCARD.style.display = "flex";
        VERSIONSECTION.style.display = "none";
        CONFCARD.style.display = "none";
        HEADER.style.display = "flex";
        await addPkgLog(STAGE[1])

        window.pywebview.api.install_package();
    }

    if (STAGE[0] === 1) {
        PKGCARD.style.display = "none";
        VERSIONSECTION.style.display = "none";
        CONFCARD.style.display = "flex";
        HEADER.style.display = "flex";

        var lngs = await window.pywebview.api.get_languages();

        console.log(lngs)

        await addLangSelect(lngs);
    }

    if (STAGE[0] === 3) {
        PKGCARD.style.display = "none";
        CONFCARD.style.display = "none";
        VERSIONSECTION.style.display = "none";
        HEADER.style.display = "flex";

        await reloadLanguage();
    }

    if (STAGE[0] === 4) {
        VERSIONSECTION.style.display = "flex";
        PKGCARD.style.display = "none";
        CONFCARD.style.display = "none";
        HEADER.style.display = "none";

        OLDVERSION.textContent = STAGE[1];
    }
}

window.loadStage = loadStage;


SUBMITCONF.addEventListener("click", async () => {
    var name = document.querySelector("#name").value
    var age = document.querySelector("#age").value
    var language = LANGSELECT.value
    if (name && age) {
        await window.pywebview.api.save_config(name, age, language);
        await loadStage();
    }
})

// ! Start Eventi
window.addEventListener("pywebviewready", async () => {
    await loadLanguage();
    loadStage();
});