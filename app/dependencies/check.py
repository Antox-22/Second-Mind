from app.core.log import log
from app.core.path import *
from app.core.error import safe
from importlib.metadata import distribution, PackageNotFoundError
from app.core.i18n import i18n
from packaging.version import Version
from app.config.config import VERSION_APP
import spacy, requests

def get_dependencies()  -> list[str]:
    _dependencies = []

    with open(ROOT / "requirements.txt", "r") as file:
        for line in file.readlines():

            # Check comment
            if not line or line.startswith("#") or "@" in line:
                continue

            _pkg = line.split(">=")[0].split("==")[0].strip()

            # Check spacy model
            if "http" in _pkg:
                continue

            _dependencies.append(_pkg)

            #DEBUG: Print _pkg added
            log.debug(f"PKG added {_pkg}")

    return _dependencies

def check_dependencies()  -> tuple[bool, list[str]]:
    _dependencies = get_dependencies()
    _missing = []

    for _pkg in _dependencies:
        try:
            distribution(_pkg)
        except PackageNotFoundError:
            _missing.append(_pkg)

            # WARNING: Print missing package
            log.warning(f"Missing *{_pkg}* package")

    return (len(_missing) != 0, _missing)

def check_spacy_model() -> bool:
    _model = i18n().lang_setting.get("spacy-model")

    if not _model: return False

    try:
        spacy.load(_model)
        return True
    except: return False

# TODO: DEBUG - FIX PRODUCTION
@safe()
def check_update(**_) -> tuple[bool, str]:
    url = f"https://api.github.com/repos/Antox-22/Second-Mind/contents/app/debug/__version__.json?ref=main"
    headers = {
        "Accept": "application/vnd.github.raw+json",
        "User-Agent": "check-update/1.0",
    }

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    remote_version = Version(r.json()["version"])

    return (VERSION_APP < remote_version, str(remote_version))