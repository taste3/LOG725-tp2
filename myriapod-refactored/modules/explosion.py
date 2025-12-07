from pgzero.actor import Actor

class Explosion(Actor):
    def __init__(self, pos, type):
        super().__init__("blank", pos)

        self.type = type
        self.timer = 0

    def update(self):
        self.timer += 1

        # Set sprite based on explosion type and timer - update to a new image
        # every four frames
        self.image = "exp" + str(self.type) + str(self.timer // 4)