from app.utils.path import ROOT

BASE_DIR = ROOT / "test"


def _read(name: str) -> str:
    return (BASE_DIR / name).read_text(
        encoding="utf-8"
    )


NOTE_1 = _read("nota_01.txt")
NOTE_2 = _read("nota_02.txt")
NOTE_3 = _read("nota_03.txt")
NOTE_4 = _read("nota_04.txt")
NOTE_5 = _read("nota_05.txt")

ALL_NOTES = [
    NOTE_1,
    NOTE_2,
    NOTE_3,
    NOTE_4,
    NOTE_5,
]