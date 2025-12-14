class PID:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev = 0.0
        self.integral = 0.0

    def compute(self, error, dt):
        p = self.kp * error
        self.integral += error * dt
        i = self.ki * self.integral
        d = self.kd * (error - self.prev) / dt if dt > 0 else 0.0
        self.prev = error
        return p + i + d
