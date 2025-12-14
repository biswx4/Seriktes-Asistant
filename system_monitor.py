import psutil
import time

class SystemMonitor:
    def __init__(self):
        self.cpu = 0.0
        self.ram = 0.0
        self.fps = 0.0
        self.last_time = time.time()

    def update(self):
        now = time.time()
        dt = now - self.last_time
        self.fps = 1.0 / dt if dt > 0 else 0
        self.last_time = now
        self.cpu = psutil.cpu_percent()
        self.ram = psutil.virtual_memory().percent

    def get_status(self):
        return {
            "cpu": self.cpu,
            "ram": self.ram,
            "fps": self.fps
        }
