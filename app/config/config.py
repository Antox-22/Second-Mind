from app.core.path import ROOT
import json

# Read Settings
with open(ROOT / "config" / "settings.json", "r") as f:
    settings = json.load(f)

# Get Language
LANGUAGE = settings.get("language", "en")