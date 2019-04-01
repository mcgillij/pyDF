
class Renderable:
    def __init__(self, image, pos_x, pos_y, depth=0):
        self.image = image
        self.depth = depth
        self.x = pos_x
        self.y = pos_y
        self.w = image.get_width()
        self.h = image.get_height()

class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Health:
    def __init__(self, current, max_health):
        self.current = current
        self.max_health = max_health
