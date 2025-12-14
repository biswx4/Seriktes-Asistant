class NavigationCore:
    def __init__(self):
        self.state = "idle"
        self.target = None
        self.path = []
        self.index = 0

    def set_target(self, target):
        self.target = target
        self.index = 0
        self.path = [target]

    def update(self):
        if self.target is None:
            self.state = "idle"
            return None

        if self.index >= len(self.path):
            self.state = "arrived"
            return None

        self.state = "moving"
        return self.path[self.index]
