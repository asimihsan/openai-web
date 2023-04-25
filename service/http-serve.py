#!/usr/bin/env python3

import base64
import json
import os

import starlette.websockets
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from nacl.public import PrivateKey, PublicKey, Box, EncryptedMessage

import vopenai

load_dotenv()
APP_PUBLIC_KEY: bytes = base64.b64decode(os.getenv("APP_PUBLIC_KEY"))
SERVER_PUBLIC_KEY: bytes = base64.b64decode(os.getenv("SERVER_PUBLIC_KEY"))
SERVER_PRIVATE_KEY: bytes = base64.b64decode(os.getenv("SERVER_PRIVATE_KEY"))

app = FastAPI()


@app.get("/ping")
def ping():
    return "healthy"


class CompletionRequest(BaseModel):
    prompt: str


class CryptoWrapper:
    def __init__(self):
        self.box = Box(PrivateKey(SERVER_PRIVATE_KEY), PublicKey(APP_PUBLIC_KEY))

    def encrypt(self, data: bytes) -> bytes:
        encrypted_message: EncryptedMessage = self.box.encrypt(data)
        return encrypted_message.nonce + encrypted_message.ciphertext

    def decrypt(self, data: bytes) -> bytes:
        return self.box.decrypt(data)


crypto_wrapper = CryptoWrapper()


class Message:
    d: str

    # from bytes, base64 encode to d
    def __init__(self, data: bytes):
        self.d = base64.b64encode(data).decode("utf-8")

    # from d, base64 decode to bytes
    def __bytes__(self):
        return base64.b64decode(self.d.encode("utf-8"))

    @staticmethod
    def parse_raw(data: str):
        return Message(base64.b64decode(data.encode("utf-8")))


openaiWrapper = vopenai.OpenAIWrapper()


@app.websocket("/ws/completion")
async def completion_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        serialized: str = await websocket.receive_text()
        data: bytes = base64.b64decode(json.loads(serialized)["d"])
        plaintext: bytes = crypto_wrapper.decrypt(data)
        request = CompletionRequest.parse_raw(plaintext)
        print(f"received request: {request}")

        for text in openaiWrapper.complete(request.prompt):
            ciphertext = crypto_wrapper.encrypt(text.encode("utf-8"))
            message = Message(ciphertext)
            await websocket.send_text(json.dumps({"d": message.d}))

        await websocket.close(code=1000, reason="success")
    except starlette.websockets.WebSocketDisconnect:
        print("websocket disconnected")
        return
