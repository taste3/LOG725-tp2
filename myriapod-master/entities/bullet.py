from pgzero.actor import Actor
from utils import pos2cell
from entities.explosion import Explosion
from entities.segment import Segment
from entities.rock import Rock
from random import random
from systems.gamestate import GameState
from systems.soundsystem import play_sound

class Bullet(Actor):
    def __init__(self, pos):
        super().__init__("bullet", pos)
        self.done = False

    def update(self):
        # Move up the screen, 24 pixels per frame
        self.y -= 24

        # game.damage checks to see if there is a rock at the given position - if so, it damages
        # the rock and returns True
        # An asterisk before a list or tuple will unpack the contents into separate values
        grid_cell = pos2cell(*self.pos)
        if GameState.game.damage(*grid_cell, 1, True):
            # Hit a rock - destroy self
            self.done = True
        else:
            # Didn't hit a rock
            # Check each myriapod segment, and the flying enemy, to see if this bullet collides with them
            for obj in GameState.game.segments + [GameState.game.flying_enemy]:
                # Is this a valid object reference, and if so, does this bullet's location overlap with the
                # object's rectangle? (collidepoint is a method from Pygame's Rect class)
                if obj and obj.collidepoint(self.pos):
                    # Create explosion
                    GameState.game.explosions.append(Explosion(obj.pos, 2))

                    obj.health -= 1

                    # Is the object an instance of the Segment class?
                    if isinstance(obj, Segment):
                        # Should we create a new rock in the segment's place? Health must be zero, there must be no
                        # rock there already, and the player sprite must not overlap with the location
                        if obj.health == 0 and not GameState.game.grid[obj.cell_y][obj.cell_x] and GameState.game.allow_movement(GameState.game.player.x, GameState.game.player.y, obj.cell_x, obj.cell_y):
                            # Create new rock - 20% chance of being a totem
                            GameState.game.grid[obj.cell_y][obj.cell_x] = Rock(obj.cell_x, obj.cell_y, random() < .2)

                        play_sound("segment_explode")
                        GameState.game.score += 10
                    else:
                        # If it's not a segment, it must be the flying enemy
                        play_sound("meanie_explode")
                        GameState.game.score += 20

                    self.done = True    # Destroy self

                    # Don't continue the for loop, this bullet has hit something so shouldn't hit anything else
                    return