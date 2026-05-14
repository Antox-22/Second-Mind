from app.config.config import Config
from app.core.path import ROOT
from app.core.error import safe
import json

DEFAULT_LANGUAGE = "it"

class i18n:
    def __init__(self):
        self.config = Config()
        self.lang = self.config.language if self.config.language else DEFAULT_LANGUAGE
        self.translations: dict = None

        self._load(self.lang)

    @safe()
    def _load(self, lang: str, **_):
        path = ROOT / "app" / "lang" / lang / "strings.json"
        with open(path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

    def t(self, module: str, key: str):
        _mod = self.translations.get(module)
        return _mod.get(key)

    def get_translations(self, module: str):
        return self.translations.get(module, None)


    def reload(self):
        self._load(self.lang)