import random

class ObjectTracker:
    def __init__(self):
        self.tracks = {}

    def update(self, detections):
        updated = []
        for d in detections:
            cls, conf, bbox = d
            tid = random.randint(1000, 9999)
            updated.append((tid, cls, conf, bbox))
        return updated
