from app.core.path import ROOT
from app.core.log import log
from ui.api.dependencies import Api, set_window
import webview


html = ROOT / "ui" / "dependencies" / "index.html"
close_count = False

def on_closing():
    global close_count
    # window.evaluate_js("window.onClose()")
    if close_count: return True
    log.debug("Closing window event.")
    close_count = True
    return False

window = webview.create_window(
    title = "Second Mind - Package Manager",
    js_api=Api(),
    width=500,
    height=300,
    frameless=True,
    easy_drag=True,
    resizable=False,
    url= "file://" + str(html)
)

window.events.closing += on_closing

def start_ui():
    webview.start(
        func=set_window,
        args=(window,),
        icon=ROOT / "assets" / "icons" / "icon.ico",
        debug=True
    )

if __name__ == "__main__":
    start_ui()