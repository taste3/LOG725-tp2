from pgzero.actor import Actor
from random import randint
from constants import CENTRE_ANCHOR
from utils import cell2pos
from entities.explosion import Explosion
from systems.gamestate import GameState
from systems.soundsystem import play_sound

class Rock(Actor):
    def __init__(self, x, y, totem=False):
        # Use a custom anchor point for totem rocks, which are taller than other rocks
        anchor = (24, 60) if totem else CENTRE_ANCHOR
        super().__init__("blank", cell2pos(x, y), anchor=anchor)

        self.type = randint(0, 3)

        if totem:
            # Totem rocks take five hits and give bonus points
            play_sound("totem_create")
            self.health = 5
            self.show_health = 5
        else:
            # Non-totem rocks are initially displayed as if they have one health, and animate until they
            # show the actualy sprite for their health level - resulting in a 'growing' animation.
            self.health = randint(3, 4)
            self.show_health = 1

        self.timer = 1

    def damage(self, amount, damaged_by_bullet=False):
        # Damage can occur by being hit by bullets, or by being destroyed by a segment, or by being cleared from the
        # player's respawn location. Points can be earned by hitting special "totem" rocks, which have 5 health, but
        # this should only happen when they are hit by a bullet.
        if damaged_by_bullet and self.health == 5:
            play_sound("totem_destroy")
            GameState.game.score += 100
        else:
            if amount > self.health - 1:
                play_sound("rock_destroy")
            else:
                play_sound("hit", 4)

        GameState.game.explosions.append(Explosion(self.pos, 2 * (self.health == 5)))
        self.health -= amount
        self.show_health = self.health

        self.anchor, self.pos = CENTRE_ANCHOR, self.pos

        # Return False if we've lost all our health, otherwise True
        return self.health < 1

    def update(self):
        self.timer += 1

        # Every other frame, update the growing animation
        if self.timer % 2 == 1 and self.show_health < self.health:
            self.show_health += 1

        if self.health == 5 and self.timer > 200:
            # Totem rocks turn into normal rocks if not shot within 200 frames
            self.damage(1)

        colour = str(max(GameState.game.wave, 0) % 3)
        health = str(max(self.show_health - 1, 0))
        self.image = "rock" + colour + str(self.type) + health