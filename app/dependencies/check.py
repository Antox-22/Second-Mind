from app.core.log import log
from app.core.path import *
from importlib.metadata import distribution, PackageNotFoundError

def get_dependencies():
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

def check_dependencies():
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