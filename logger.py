import time

class Logger:
    def __init__(self, name="Seriktes"):
        self.name = name

    def log(self, msg):
        t = time.strftime("%H:%M:%S")
        print(f"[{t}] [{self.name}] {msg}")
