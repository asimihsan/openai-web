#!/usr/bin/env python3

import base64
import json
import logging

import dissononce
import starlette.websockets
from dissononce.cipher.chachapoly import ChaChaPolyCipher
from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.hash.sha256 import SHA256Hash
from dissononce.processing.handshakepatterns.interactive.XX import XXHandshakePattern
from dissononce.processing.impl.cipherstate import CipherState
from dissononce.processing.impl.handshakestate import HandshakeState
from dissononce.processing.impl.symmetricstate import SymmetricState
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

import vopenai

app = FastAPI()


dissononce.logger.setLevel(logging.DEBUG)


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

    bob_s = X25519DH().generate_keypair()
    bob_handshakestate = HandshakeState(
        SymmetricState(
            CipherState(
                ChaChaPolyCipher()
            ),
            SHA256Hash()
        ),
        X25519DH()
    )
    bob_handshakestate.initialize(
        handshake_pattern=XXHandshakePattern(),
        initiator=False,
        prologue=b"",
        s=bob_s,
    )

    # -> e
    data: str = await websocket.receive_text()
    serialized: dict[str, str] = json.loads(data)
    message: bytes = base64.b64decode(serialized["d"])
    message_buffer = bytearray()
    bob_handshakestate.read_message(message=message, payload_buffer=message_buffer)

    # <- e, ee, s, es
    message_buffer = bytearray()
    bob_handshakestate.write_message(payload=b'', message_buffer=message_buffer)
    message: str = base64.b64encode(message_buffer).decode("utf-8")
    serialized: dict[str, str] = {
        "d": message,
    }
    data: str = json.dumps(serialized)
    await websocket.send_text(data)

    # -> s, se
    message_buffer = bytearray()
    data: str = await websocket.receive_text()
    serialized: dict[str, str] = json.loads(data)
    message: bytes = base64.b64decode(serialized["d"])
    bob_cipherstates = bob_handshakestate.read_message(
        message=message, payload_buffer=message_buffer)

    try:
        data = await websocket.receive_text()
        serialized: dict[str, str] = json.loads(data)
        message: bytes = base64.b64decode(serialized["d"])
        plaintext = bob_cipherstates[0].decrypt_with_ad(ad=b'', ciphertext=message)
        request = CompletionRequest.parse_raw(plaintext)

        for text in openaiWrapper.complete(request.prompt):
            ciphertext: bytes = bob_cipherstates[0].encrypt_with_ad(ad=b'', plaintext=text)
            serialized: dict[str, str] = {
                "d": base64.b64encode(ciphertext).decode("utf-8"),
            }
            text = json.dumps(serialized)
            await websocket.send_text(text)
        await websocket.close(code=1000, reason="success")

    except starlette.websockets.WebSocketDisconnect:
        return

