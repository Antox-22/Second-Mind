from app.config.config import get_config, VERSION_APP
from app.core.i18n import i18n
from app.dependencies.check import check_dependencies, check_spacy_model
from app.dependencies.install import install_packages, install_spacy_model
from enum import Enum
from webview import Window

MODULE = "dependencies"
window: Window = None

class Stage(Enum):
    FULL_INSTALL = 0
    ONLY_CONFIG = 1
    DEPENDENCIES = 2
    SPACY = 3
    CHECK_UPDATE = 4


def set_window(_window):
    global window
    window = _window

class Api:
    def __init__(self):
        self._config = get_config()
        self.config = self._config.config
        self.i18n = i18n()

    def get_stage(self):
        """
            Determines the installation state to be performed:

            - 0: Full installation required; the application has just been installed.
            - 1: Dependencies have been installed; proceed with standard configuration.
            - 2: Configuration has been completed, but dependencies are missing.
            - 3: Install Spacy Model.
            - 4: Check only for available updates.
        """
        self._missing_pack = check_dependencies()

        if self.config.app.language and self.config.user.name:
            if (self._missing_pack[0]):
                window.resize(800, 600)
                return (Stage.DEPENDENCIES.value, self._missing_pack[1])
            else:
                if (check_spacy_model()):
                    window.resize(450, 200)
                    return (Stage.CHECK_UPDATE.value, VERSION_APP)
                window.resize(800, 600)
                return (Stage.SPACY.value, self.i18n.lang_setting.get("spacy-model"))

        window.resize(800, 600)
        if (not self._missing_pack[0]):
            return (Stage.ONLY_CONFIG.value, None)

        return (Stage.FULL_INSTALL.value, self._missing_pack[1])

    def get_language(self):
        return self.i18n.get_translations(MODULE)

    def get_languages(self):
        return self.i18n.get_languages()

    def reload_language(self):
        self.i18n.reload()
        return self.i18n.get_translations(MODULE)

    def install_package(self):
        return install_packages(check_dependencies()[1], window)

    def install_spacy_model(self):
        return install_spacy_model(self.i18n.lang_setting.get("spacy-model"), window)

    def save_config(self, name, age, lang):
        self.config.user.name = name
        self.config.user.age = int(age)
        self.config.app.language = lang

        self._config.save_and_reload()