from fastapi import APIRouter, WebSocket
import logging as log

current_ws = None
log.basicConfig(level=log.DEBUG)
router = APIRouter()

@router.get("/")
async def root():
    return {"status": "ok"}

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global current_ws

    if current_ws is not None:
        await ws.close(
            code=1008,
            reason="Only one WebSocket connection allowed at a time."
        )

        return;

    await ws.accept()
    current_ws = ws

    try:
        while True:
            data = await ws.receive_text()

            # DEBUG: Print received data to console
            log.debug(f"Received data from WS: {data}")

            # await ws.send_text()
    except: pass
    finally:
        current_ws = None