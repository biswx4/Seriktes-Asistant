class DiffDrive:
    def __init__(self):
        self.left_speed = 0.0
        self.right_speed = 0.0

    def forward(self, speed):
        self.left_speed = speed
        self.right_speed = speed

    def stop(self):
        self.left_speed = 0.0
        self.right_speed = 0.0

    def turn_left(self, speed):
        self.left_speed = -speed
        self.right_speed = speed

    def turn_right(self, speed):
        self.left_speed = speed
        self.right_speed = -speed
