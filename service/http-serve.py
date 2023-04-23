#!/usr/bin/env python3

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        await websocket.send_text("pong")

openaiWrapper = vopenai.OpenAIWrapper()


@app.post("/completion")
async def completion(request: CompletionRequest) -> CompletionResponse:
    response = await openaiWrapper.complete(request.prompt)
    return CompletionResponse(success=True, error="", completion=response)
