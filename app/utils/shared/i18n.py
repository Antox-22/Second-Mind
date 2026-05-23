from app.config.config import get_config
from app.utils.path import ROOT
from app.utils.shared.error import safe
import json, os

DEFAULT_LANGUAGE = "it"

class i18n:
    def __init__(self):
        self.config = get_config().config
        self.lang = self.config.app.language if self.config.app.language else DEFAULT_LANGUAGE
        self.translations: dict = None
        self.lang_setting:dict = None

        self._load()

    @safe()
    def _load(self, **_):
        self.lang = self.config.app.language if self.config.app.language else DEFAULT_LANGUAGE
        path = ROOT / "app" / "lang" / self.lang / "strings.json"

        with open(path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

        path = ROOT / "app" / "lang" / self.lang / "config.json"
        with open(path, "r", encoding="utf-8") as f:
            self.lang_setting = json.load(f)

        return self.translations

    def t(self, module: str, key: str):
        _mod = self.translations.get(module)
        return _mod.get(key)

    def get_translations(self, module: str):
        return self.translations.get(module, None)

    def reload(self):
        return self._load()

    @safe()
    def get_languages(self, **_):
        _list = [ROOT / "app" / "lang" / f for f in os.listdir(ROOT / "app" / "lang") if os.path.isdir(ROOT / "app" / "lang" / f)]
        _lngs = []

        for p in _list:
            try:
                with open(p / "config.json", "r") as f:
                    _js = json.load(f)
                    _lngs.append((_js["name"], _js["prefix"]))
            except: pass

        return _lngs