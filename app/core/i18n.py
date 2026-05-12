from app.config.config import Config
from app.core.path import ROOT
from app.core.error import safe
import json

DEFAULT_LANGUAGE = "it"

class i18n:
    def __init__(self):
        self.config = Config()
        self.lang = self.config.language if self.config.language else DEFAULT_LANGUAGE
        self.translations: dict = self._load(self.lang)

    @safe()
    def _load(self, lang):
        path = ROOT / "app" / lang / "strings.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def t(self, module, key):
        _mod = self.translations.get(module)
        return _mod.get(key)

    def reload(self):
        self._load(self.lang)