import asyncio
import websockets
import base64
import sounddevice as sd
import numpy as np
from openai import OpenAI

class VoiceInterface:
    def __init__(self, did_key, openai_key):
        self.did_key = did_key
        self.client = OpenAI(api_key=openai_key)
        self.ws_url = "wss://api.d-id.com/rt/stream"
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(f'{did_key}:'.encode()).decode()}"
        }

    def record(self, duration=3, samplerate=16000):
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
        sd.wait()
        return np.squeeze(audio)

    def transcribe(self, audio):
        wav = audio.astype(np.float32).tobytes()
        return self.client.audio.transcriptions.create(
            model="whisper-1",
            file=wav,
            response_format="text"
        )

    def ask(self, text):
        out = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        )
        return out.choices[0].message.content

    def synthesize(self, text):
        speech = self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )
        return speech.read()

    async def send_to_avatar(self, audio_bytes):
        async with websockets.connect(self.ws_url, extra_headers=self.headers) as ws:
            await ws.send(base64.b64encode(audio_bytes).decode())

    async def interact(self):
        audio = self.record()
        text = self.transcribe(audio)
        reply = self.ask(text)
        voice = self.synthesize(reply)
        await self.send_to_avatar(voice)
        return reply
