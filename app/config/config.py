from app.core.path import ROOT
from app.core.error import safe
from typing import Optional
from pydantic import BaseModel
from app.core.log import log
import json

VERSION_APP = " 0.1.5"
NAME_APP = "Second Mind"
config = None

class App(BaseModel):
    name: str
    version: str
    language: Optional[str] = None

class User(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

class _Config(BaseModel):
    app: App
    user: User

class Config:
    def __init__(self):
        self.language = None
        self.config: _Config = None

        # Load
        self._load()

    @safe(retry=True)
    def _load(self, was_error=False, exception=None):
        global config
        if was_error:
            self.config = _Config(
                app=App(name=NAME_APP, version=VERSION_APP, language=None),
                user=User(name=None, age=None)
            )

            with open(ROOT / "app" / "config" / "settings.json", "w") as f:
                json.dump(self.config.model_dump(), f, indent=2)

            # DEBUG: Creata settings file
            log.info("Create settings file")
        else:
            with open(ROOT / "app" / "config" / "settings.json", "r") as f:
                self._config = json.load(f)

            self.config = _Config(**self._config)
        config = self

        # DEBUG: Config loaded
        log.info("Settings loaded.")

    @safe()
    def _save(self):
        with open(ROOT / "config" / "settings.json", "w") as f:
            f.write(self.config.model_dump_json(indent=2))

        # DEBUG: Config saved
        log.debug("Settings saved.")

    def save_and_reload(self):
        self._save()
        self._load()

def get_config():
    global config
    if not config:
        config = Config()

    return config