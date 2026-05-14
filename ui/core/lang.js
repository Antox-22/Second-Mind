export async function loadLanguage() {
    var langsTags = document.querySelectorAll("lang");

    var translation = await window.pywebview.api.get_language();

    langsTags.forEach(element => {
        var key = element.textContent;
        var value = translation[key];

        element.textContent = value;

    });
}