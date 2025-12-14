import random

class Sensor:
    def __init__(self, name):
        self.name = name

    def read(self):
        return random.random()

class SensorSuite:
    def __init__(self):
        self.sensors = {
            "distance_front": Sensor("distance_front"),
            "distance_left": Sensor("distance_left"),
            "distance_right": Sensor("distance_right"),
        }

    def get(self, name):
        return self.sensors[name].read()
