from pgzero.actor import Actor
#from modules.bullet import Bullet
from modules.explosion import Explosion
from pgzero.builtins import keyboard
from systems.game_state import GameState
from systems.sound_system import play_sound

from ecs.systems.bullet_system import BulletSystem

class Player(Actor):

    INVULNERABILITY_TIME = 100
    RESPAWN_TIME = 100
    RELOAD_TIME = 10

    def __init__(self, pos):
        super().__init__("blank", pos)

        # These determine which frame of animation the player sprite will use
        self.direction = 0
        self.frame = 0

        self.lives = 3
        self.alive = True

        # timer is used for animation, respawning and for ensuring the player is
        # invulnerable immediately after respawning
        self.timer = 0

        # When the player shoots, this is set to RELOAD_TIME - it then counts
        # down - when it reaches zero the player can shoot again
        self.fire_timer = 0

    def move(self, dx, dy, speed):
        # dx and dy will each be either 0, -1 or 1. speed is an integer indicating
        # how many pixels we should move in the specified direction.
        for i in range(speed):
            # For each pixel we want to move, we must first check if it's a valid place to move to
            if GameState.game.allow_movement(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy

    def update(self):
        self.timer += 1

        if self.alive:
            # Get keyboard input. dx and dy represent the direction the player is facing on each axis
            dx = 0
            if keyboard.left:
                dx = -1
            elif keyboard.right:
                dx = 1

            dy = 0
            if keyboard.up:
                dy = -1
            elif keyboard.down:
                dy = 1

            # Move in the relevant directions by the specified number of pixels. The purpose of 3 - abs(dy) is to
            # generate vectors which look either like (3,0) (which is 3 units long) or (2, 2) (which is sqrt(8) long)
            # so we move roughly the same distance regardless of whether we're travelling straight along the x or y axis.
            # or at 45 degrees. Without this, we would move noticeably faster when travelling diagonally.
            self.move(dx, 0, 3 - abs(dy))
            self.move(0, dy, 3 - abs(dx))

            # When the player presses a key to start handing in a new direction, we don't want the sprite to just
            # instantly change to facing in that new direction. That would look wrong, since in the real world vehicles
            # can't just suddenly change direction in the blink of an eye.
            # Instead, we want the vehicle to turn to face the new direction over several frames. If the vehicle is
            # currently facing down, and the player presses the left arrow key, the vehicle should first turn to face
            # diagonally down and to the left, and then turn to face left.

            # Each number in the following list corresponds to a direction - 0 is up, 1 is up and to the right, and
            # so on in clockwise order. -1 means no direction.
            # Think of it as a grid, as follows:
            # 7  0  1
            # 6 -1  2
            # 5  4  3
            directions = [7,0,1,6,-1,2,5,4,3]

            # But! If you look at the values that self.direction actually takes on during the game, you only see
            # numbers from 0 to 3. This is because although there are eight possible directions of travel, there are
            # only four orientations of the player vehicle. The same sprite, for example, is used if the player is
            # travelling either left or right. This is why the direction is ultimately clamped to a range of 0 to 4.
            # 0 = facing up or down
            # 1 = facing top right or bottom left
            # 2 = facing left or right
            # 3 = facing bottom right or top left

            # # It can be useful to think of the vehicle as being able to drive both forwards and backwards.

            # Choose the relevant direction from the above list, based on dx and dy
            dir = directions[dx+3*dy+4]

            # Every other frame, if the player is pressing a key to move in a particular direction, update the current
            # direction to rotate towards facing the new direction
            if self.timer % 2 == 0 and dir >= 0:

                # We first calculate the difference between the desired direction and the current direction.
                difference = (dir - self.direction)

                # We use the following list to decide how much to rotate by each frame, based on difference.
                # It's easiest to think about this by just considering the first four direction values - 0 to 3,
                # corresponding to facing up, to fit into the bottom right. However, because of the symmetry of the
                # player sprites as described above, these calculations work for all possible directions.
                # If there is no difference, no rotation is required.
                # If the difference is 1, we rotate by 1 (clockwise)
                # If the difference is 2, then the target direction is at right angles to the current direction,
                # so we have a free choice as to whether to turn clockwise or anti-clockwise to align with the
                # target direction. We choose clockwise.
                # If the difference is three, the symmetry of the player sprites means that we can reach the desired
                # animation frame by rotating one unit anti-clockwise.
                rotation_table = [0, 1, 1, -1]

                rotation = rotation_table[difference % 4]
                self.direction = (self.direction + rotation) % 4


            self.fire_timer -= 1

            # Fire cannon (or allow firing animation to finish)
            if self.fire_timer < 0 and (self.frame > 0 or keyboard.space):
                if self.frame == 0:
                    # Create a bullet
                    play_sound("laser")

                    BulletSystem.instance.shoot_bullet(self.x, self.y)

                self.frame = (self.frame + 1) % 3
                self.fire_timer = Player.RELOAD_TIME

            # Check to see if any enemy segments collide with the player, as well as the flying enemy.
            # We create a list consisting of all enemy segments, and append another list containing only the
            # flying enemy.
            all_enemies = GameState.game.segments + [GameState.game.flying_enemy]
            for enemy in all_enemies:
                # The flying enemy might not exist, in which case its value
                # will be None. We cannot call a method or access any attributes
                # of a 'None' object, so we must first check for that case.
                # "if object:" is shorthand for "if object != None".
                if enemy and enemy.collidepoint(self.pos):
                    # Collision has occurred, check to see whether player is invulnerable
                    if self.timer > Player.INVULNERABILITY_TIME:
                        play_sound("player_explode")
                        GameState.game.explosions.append(Explosion(self.pos, 1))
                        self.alive = False
                        self.timer = 0
                        self.lives -= 1
        else:
            # Not alive
            # Wait a while before respawning
            if self.timer > Player.RESPAWN_TIME:
                # Respawn
                self.alive = True
                self.timer = 0
                self.pos = (240, 768)
                GameState.game.clear_rocks_for_respawn(*self.pos)     # Ensure there are no rocks at the player's respawn position

        # Display the player sprite if alive - BUT, if player is currently invulnerable, due to having just respawned,
        # switch between showing and not showing the player sprite on alternate frames
        invulnerable = self.timer > Player.INVULNERABILITY_TIME
        if self.alive and (invulnerable or self.timer % 2 == 0):
            self.image = "player" + str(self.direction) + str(self.frame)
        else:
            self.image = "blank"