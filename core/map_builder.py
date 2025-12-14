class MapBuilder:
    def __init__(self):
        self.map = {}

    def update(self, position, obstacles):
        self.map[position] = obstacles

    def get_map(self):
        return self.map
