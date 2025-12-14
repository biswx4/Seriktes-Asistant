class MotionPlanner:
    def __init__(self):
        self.path = []

    def plan(self, start, goal):
        self.path = [start, goal]
        return self.path

    def get_next(self):
        if not self.path:
            return None
        return self.path.pop(0)
