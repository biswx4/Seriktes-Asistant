import asyncio
import websockets
import base64
import sounddevice as sd
import numpy as np
from openai import OpenAI
import time

class InteractionManager:
    def __init__(self, did_key, openai_key, robot):
        self.did_key = did_key
        self.client = OpenAI(api_key=openai_key)
        self.robot = robot
        self.ws_url = "wss://api.d-id.com/rt/stream"
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(f'{did_key}:'.encode()).decode()}"
        }

    def record(self, duration=2, samplerate=16000):
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
        return self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"Ты Seriktes, ассистент робота. Интерпретируй команды пользователя."},
                      {"role":"user","content":text}]
        ).choices[0].message.content

    def synthesize(self, text):
        speech = self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )
        return speech.read()

    async def send_emotion(self, ws, emotion):
        await ws.send(emotion)

    async def speak(self, audio_bytes):
        async with websockets.connect(self.ws_url, extra_headers=self.headers) as ws:
            await ws.send(base64.b64encode(audio_bytes).decode())

    def handle_hotword(self, text):
        return "сериктес" in text.lower()

    def parse_command(self, text):
        t = text.lower()
        if "подними руку" in t:
            return "raise_arm"
        if "опусти руку" in t:
            return "lower_arm"
        if "отъедь назад" in t:
            return "move_back"
        if "вперед" in t:
            return "move_forward"
        if "стоп" in t:
            return "stop"
        return None

    async def run(self):
        while True:
            audio = self.record()
            text = self.transcribe(audio)
            msg = str(text)

            if self.handle_hotword(msg):
                self.robot.drive.stop()
                reply = "Слушаю."
                voice = self.synthesize(reply)
                await self.speak(voice)
                audio2 = self.record()
                cmd_text = self.transcribe(audio2)
                cmd = str(cmd_text)
                action = self.parse_command(cmd)

                if action == "raise_arm":
                    self.robot.arm.set_joint_positions([0.0, -0.5, 0.4, 0.0])
                elif action == "lower_arm":
                    self.robot.arm.set_joint_positions([0.0, 0.0, 0.0, 0.0])
                elif action == "move_back":
                    self.robot.drive.forward(-0.3)
                elif action == "move_forward":
                    self.robot.drive.forward(0.3)
                elif action == "stop":
                    self.robot.drive.stop()

                answer = self.synthesize("Команда выполнена.")
                await self.speak(answer)
            else:
                pass

            time.sleep(0.1)
