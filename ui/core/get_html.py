from app.core.error import safe

@safe()
def get_html(paths: list[str]):
    _html = []
    _style = []
    _script = []
    _text = ""

    for file in paths:
        with open(file, "r") as f:
            if file.endswith(".html"):
                _html.append(f.read())
            elif file.endswith(".css"):
                _style.append(f.readd())
            elif file.endswith(".js"):
                _script.append(f.readd())

    _text = "\n".join(_style)
    _text += "\n".join(_html)
    _text += "\n".join(_script)

    return _text