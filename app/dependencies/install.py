from app.core.log import log
from app.core.error import safe
from app.dependencies.check import check_dependencies
from importlib.metadata import distribution, PackageNotFoundError
import subprocess
import sys


@safe()
def _install_packages(packages: list[str], window,  **_) -> None:
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
        subprocess.check_call(cmd)

        try:
            distribution(pkg)
            window.evaluate_js(f"window.checkPkgLog(\"{pkg}\", 1)")
        except PackageNotFoundError:
            window.evaluate_js(f"window.checkPkgLog(\"{pkg}\", -1)")
            _missing = True

    if not _missing:
        window.evaluate_js("window.loadStage()")