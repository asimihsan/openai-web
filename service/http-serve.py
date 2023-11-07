#!/usr/bin/env python3

import asyncio
import base64
import dataclasses
import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from nacl.public import PrivateKey, PublicKey, Box, EncryptedMessage
from pydantic import BaseModel

import vopenai
from generated.proto.prompt.v1 import StartCompletionRequest, CompletionResponse, Role
from generated.proto.secure_connection.v1 import EncryptedData, ClientEphemeralKey, ServerEphemeralKey

load_dotenv()
APP_PUBLIC_KEY: bytes = base64.b64decode(os.getenv("APP_PUBLIC_KEY"))
SERVER_PUBLIC_KEY: bytes = base64.b64decode(os.getenv("SERVER_PUBLIC_KEY"))
SERVER_PRIVATE_KEY: bytes = base64.b64decode(os.getenv("SERVER_PRIVATE_KEY"))

app = FastAPI()


@app.get("/p/ping")
def ping():
    return "healthy"


class CompletionRequest(BaseModel):
    prompt: str


@dataclasses.dataclass
class EncryptionResult:
    nonce: bytes
    ciphertext: bytes


class CryptoWrapper:
    def __init__(self):
        self.box = Box(PrivateKey(SERVER_PRIVATE_KEY), PublicKey(APP_PUBLIC_KEY))

    def encrypt(self, data: bytes) -> EncryptionResult:
        encrypted_message: EncryptedMessage = self.box.encrypt(data)
        return EncryptionResult(nonce=encrypted_message.nonce, ciphertext=encrypted_message.ciphertext)

    def decrypt(self, ciphertext: bytes, nonce: bytes) -> bytes:
        return self.box.decrypt(ciphertext, nonce=nonce)


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


async def async_enumerate(aiterable, start=0):
    i = start
    async for x in aiterable:
        yield i, x
        i += 1


async def receive_data(request, queue):
    converted_request = convert_start_completion_response_to_messages(request)
    async for i, text in async_enumerate(openaiWrapper.complete(converted_request)):
        completion_response = CompletionResponse()

        # TODO conversation IDs
        completion_response.conversation_id = ""
        completion_response.text = text
        completion_response.counter = i
        completion_response.is_final = False

        await queue.put(completion_response)

    completion_response = CompletionResponse()
    # TODO conversation IDs
    completion_response.conversation_id = ""
    completion_response.is_final = True
    await queue.put(completion_response)


async def send_data(websocket, queue):
    while True:
        try:
            completion_response = await queue.get()
            if completion_response.is_final:
                break
            ciphertext = crypto_wrapper.encrypt(bytes(completion_response))
            message = EncryptedData()
            message.nonce = ciphertext.nonce
            message.ciphertext = ciphertext.ciphertext
            await websocket.send_bytes(bytes(message))
        except Exception as e:
            print(f"error sending data: {e}")
            break

    try:
        await websocket.close(code=1000, reason="success")
    except Exception as e:
        print(f"error closing websocket: {e}")


@app.websocket("/p/ws/completion")
async def completion_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("connection accepted")

    # server_ephemeral_private_key = PrivateKey.generate()
    # server_ephemeral_public_key = server_ephemeral_private_key.public_key
    # service_nonce: bytes = os.urandom(16)
    #
    # client_ephemeral_public_key_serialized: bytes = await websocket.receive_bytes()
    # client_ephemeral_public_key: ClientEphemeralKey = ClientEphemeralKey().parse(
    #     data=client_ephemeral_public_key_serialized
    # )

    serialized: bytes = await websocket.receive_bytes()
    data: EncryptedData = EncryptedData().parse(data=serialized)
    plaintext: bytes = crypto_wrapper.decrypt(ciphertext=data.ciphertext, nonce=data.nonce)
    request = StartCompletionRequest().parse(data=plaintext)

    queue = asyncio.Queue()
    receive_task = asyncio.create_task(receive_data(request, queue))
    send_task = asyncio.create_task(send_data(websocket, queue))

    await asyncio.gather(receive_task, send_task)


def convert_start_completion_response_to_messages(response: StartCompletionRequest) -> list[dict]:
    result = []
    for message in response.stanzas:
        role: str
        if message.role == Role.USER:
            role = "user"
        elif message.role == Role.ASSISTANT:
            role = "assistant"
        else:
            raise Exception(f"unknown role: {message.role}")
        result.append({"role": role, "content": message.content})
    return result
