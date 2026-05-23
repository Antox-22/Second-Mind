export let translation = {};

export async function loadLanguage() {
    var langsTags = document.querySelectorAll("lang");

    translation = await window.pywebview.api.get_language();

    langsTags.forEach(element => {
        var key = element.dataset.key;
        var value = translation[key];

        element.textContent = value ?? `[${key}]`;

    });
}

export async function reloadLanguage() {
    await window.pywebview.api.reload_language();
    await loadLanguage();
}

export function format(str, values) {
    return str.replace(/\{(.*?)\}/g, (_, key) => {
        return values[key] ?? `{${key}}`;
    });
}