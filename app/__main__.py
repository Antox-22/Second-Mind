from app.config.config import get_config
from ui.dependencies.ui import start_ui
import argparse

argv = argparse.ArgumentParser()
argv.add_argument(
    "--skip-check",
    action="store_true",
    help="Salta il controllo"
)

args = argv.parse_args()
config = get_config()

if not args.skip_check:
    check_status = start_ui()

    print(check_status)