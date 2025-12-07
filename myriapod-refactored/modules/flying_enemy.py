from pgzero.actor import Actor
from random import choice, randint


class FlyingEnemy(Actor):
    def __init__(self, player_x):
        # Choose which side of the screen we start from. Don't start right next to the player as that would be
        # unfair - if not near player, start on a random side
        side = 1 if player_x < 160 else 0 if player_x > 320 else randint(0, 1)

        super().__init__("blank", (550*side-35, 688))

        # Always moves in the same X direction, but randomly pauses to just fly straight up or down
        self.moving_x = 1       # 0 if we're currently moving only vertically, 1 if moving along x axis (as well as y axis)
        self.dx = 1 - 2 * side  # Move left or right depending on which side of the screen we're on
        self.dy = choice([-1, 1])   # Start moving either up or down
        self.type = randint(0, 2)   # 3 different colours

        self.health = 1

        self.timer = 0

    def update(self):
        self.timer += 1

        # Move
        self.x += self.dx * self.moving_x * (3 - abs(self.dy))
        self.y += self.dy * (3 - abs(self.dx * self.moving_x))

        if self.y < 592 or self.y > 784:
            # Gone too high or low - reverse y direction
            self.moving_x = randint(0, 1)
            self.dy = -self.dy

        anim_frame = str([0, 2, 1, 2][(self.timer // 4) % 4])
        self.image = "meanie" + str(self.type) + anim_frame