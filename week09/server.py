"""One-process shared scene, bound only to this laptop. Stop with Ctrl+C."""

import argparse
import asyncio
import json
from pathlib import Path

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from scene import Scene

HERE = Path(__file__).resolve().parent


def create_app():
    app = FastAPI()
    scene = Scene()
    clients = set()
    lock = asyncio.Lock()

    async def broadcast():
        for client in tuple(clients):
            try:
                await client.send_json(scene.snapshot())
            except (WebSocketDisconnect, RuntimeError, OSError):
                clients.discard(client)

    @app.get("/", response_class=HTMLResponse)
    async def index():
        return (HERE / "index.html").read_text()

    @app.get("/state")
    async def state():
        return scene.snapshot()

    @app.post("/action")
    async def action(request: Request):
        try:
            message = await request.json()
        except (ValueError, UnicodeError):
            return JSONResponse({"type": "rejected", "error": "Send valid JSON."}, status_code=400)
        async with lock:
            try:
                ack = scene.apply(message)
            except ValueError as error:
                return JSONResponse({"type": "rejected", "error": str(error)}, status_code=422)
            await broadcast()
            return ack

    @app.websocket("/ws")
    async def updates(client: WebSocket):
        await client.accept()
        try:
            async with lock:
                clients.add(client)
                await client.send_json(scene.snapshot())
            while True:
                incoming = await client.receive()
                if incoming["type"] == "websocket.disconnect":
                    break
                try:
                    if "text" not in incoming:
                        raise ValueError("Send a JSON text message, not binary.")
                    message = json.loads(incoming["text"])
                    async with lock:
                        ack = scene.apply(message)
                        # Shared state changes even if this client never observes its ack.
                        await broadcast()
                        await client.send_json(ack)
                except (ValueError, UnicodeError) as error:
                    await client.send_json({"type": "rejected", "error": str(error)})
        except (WebSocketDisconnect, RuntimeError, OSError):
            pass
        finally:
            clients.discard(client)

    return app


app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8009)
    args = parser.parse_args()
    uvicorn.run(app, host="127.0.0.1", port=args.port, ws_max_size=4096)
