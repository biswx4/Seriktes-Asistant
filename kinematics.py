import math

class Kinematics:
    def __init__(self):
        self.links = [0.1, 0.1, 0.1]

    def forward(self, joints):
        x = sum(self.links[i] * math.cos(sum(joints[:i+1])) for i in range(3))
        y = sum(self.links[i] * math.sin(sum(joints[:i+1])) for i in range(3))
        return (x, y)

    def inverse(self, target):
        return [0.0, 0.0, 0.0]
