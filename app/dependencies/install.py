from app.utils.log import log
from app.utils.error import safe, showError
from app.dependencies.check import check_spacy_model
from importlib.metadata import distribution, PackageNotFoundError
import subprocess
import sys


@safe()
def install_packages(packages: list[str], window,  **_) -> None:
    """
    State
    0: Installing
    1: Ok
    -1: Error
    """
    if not packages:
        return

    _missing = False

    for pkg in packages:

        window.evaluate_js(f"window.checkPkgLog(\"{pkg}\", 0)")

        cmd = [
            sys.executable, "-m", "pip", "install",
            "--disable-pip-version-check",
            "--no-input",
            pkg
        ]

        log.info("Installing packages: %s", packages)
        try:
            subprocess.check_call(cmd)
        except:
            log.exception("Error installing package: %s", pkg)
            window.evaluate_js(f"window.checkPkgLog(\"{pkg}\", -1)")

        try:
            distribution(pkg)
            window.evaluate_js(f"window.checkPkgLog(\"{pkg}\", 1)")
        except PackageNotFoundError:
            window.evaluate_js(f"window.checkPkgLog(\"{pkg}\", -1)")
            _missing = True

    if not _missing:
        window.evaluate_js("window.loadStage()")
        return

    showError(window, "pkg_error");

@safe()
def install_spacy_model(model: str, window, **_) -> bool:
    cmd = [
            sys.executable, "-m", "spacy", "download",
            model
    ]

    log.info("Installing model: %s", model)
    try:
        subprocess.check_call(cmd)
    except:
        log.exception("Error installing model: %s", model)
        window.evaluate_js("window.errorSpacy()")
        showError(window, "error_log_spacy", {"cmd": f"python -m spacy download {model}"});
        return False

    if check_spacy_model():
        window.evaluate_js("window.loadStage()")
        return True

    log.exception("Error checking model: %s", model)
    window.evaluate_js("window.errorSpacy()")
    showError(window, "error_log_spacy", {"cmd": f"python -m spacy download {model}"});
    return False