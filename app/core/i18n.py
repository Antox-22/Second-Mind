from app.config.config import LANGUAGE
from app.core.path import ROOT
import json

class i18n:
    def __init__(self):
        self.lang = LANGUAGE if LANGUAGE else "it"
        self.translations: dict = self._load(self.lang)

    def _load(self, lang):
        path = ROOT / "app" / lang / "strings.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def t(self, module, key):
        _mod = self.translations.get(module)
        return _mod.get(key)