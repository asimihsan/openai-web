#!/usr/bin/env python3

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import starlette.websockets

import vopenai

app = FastAPI()


@app.get("/ping")
def ping():
    return "healthy"


class CompletionRequest(BaseModel):
    prompt: str


class CompletionResponse(BaseModel):
    success: bool
    error: str
    completion: str


openaiWrapper = vopenai.OpenAIWrapper()

@app.websocket("/ws/completion")
async def completion_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except starlette.websockets.WebSocketDisconnect:
            break
        request = CompletionRequest.parse_raw(data)
        for text in openaiWrapper.complete(request.prompt):
            await websocket.send_text(text)
