from app.config.config import get_config
from app.core.i18n import i18n
from app.dependencies.check import check_dependencies, get_dependencies
from app.dependencies.install import install_packages

MODULE = "dependencies"
window = None



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
            - 3: Check only for available updates.
        """
        self._missing_pack = check_dependencies()

        print(self._missing_pack)

        if self.config.app.language and self.config.user.name:
            if (self._missing_pack[0]):
                return (2, self._missing_pack[1])
            else: return (3, None)

        if (not self._missing_pack[0]):
            return (1, None)

        return (0, self._missing_pack[1])

    def get_language(self):
        return self.i18n.get_translations(MODULE)

    def reload_language(self):
        self.i18n.reload()
        return self.i18n.get_translations(MODULE)

    def install_package(self):
        return install_packages(check_dependencies()[1], window)