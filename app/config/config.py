from app.core.path import ROOT
from app.core.error import safe
from pydantic import BaseModel
from app.core.log import log
import json

class App(BaseModel):
    name: str
    version: str
    language: str

class User(BaseModel):
    name: str
    age: int

class _Config(BaseModel):
    app: App

class Config:
    def __init__(self):
        self.language = None
        self.config: _Config = None

        # Load
        self._load()

    @safe()
    def _load(self):
        with open(ROOT / "config" / "settings.json", "r") as f:
            self._config = json.load(f)

        self.config = _Config(**self._config)

        # DEBUG: Config loaded
        log.debug("Settings loaded.")

    @safe()
    def _save(self):
        with open(ROOT / "config" / "settings.json", "w") as f:
            f.write(self.config.model_dump_json(indent=2))

        # DEBUG: Config saved
        log.debug("Settings saved.")

    def save_and_reload(self):
        self._save()
        self._load()