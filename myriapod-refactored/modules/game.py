from constants import *
from utils import pos2cell
from modules.flying_enemy import FlyingEnemy
from modules.explosion import Explosion
from modules.segment import Segment
from modules.rock import Rock
from random import randint, random
from systems.game_state import GameState
from pgzero.builtins import sounds
from systems.sound_system import play_sound

class Game:
    def __init__(self, screen, player=None):
        self.screen = screen
        self.player = player

        self.wave = -1
        self.time = 0

        # Create empty grid of 14 columns, 25 rows, each element intially just containing the value 'None'
        # Rocks will be added to the grid later
        self.grid = [[None] * num_grid_cols for y in range(num_grid_rows)]

        self.bullets = []
        self.explosions = []
        self.segments = []

        self.flying_enemy = None

        self.score = 0

    def damage(self, cell_x, cell_y, amount, from_bullet=False):
        # Find the rock at this grid cell (or None if no rock here)
        rock = self.grid[cell_y][cell_x]

        if rock != None:
            # rock.damage returns False if the rock has lost all its health - in this case, the grid cell will be set
            # to None, overwriting the rock object reference
            if rock.damage(amount, from_bullet):
                self.grid[cell_y][cell_x] = None

        # Return whether or not there was a rock at this position
        return rock != None

    def allow_movement(self, x, y, ax=-1, ay=-1):
        # ax/ay are only supplied when a segment is being destroyed, and we check to see if we should create a new
        # rock in the segment's place. They indicate a grid cell location where we're planning to create the new rock,
        # we need to ensure the new rock would not overlap with the player sprite

        # Don't go off edge of screen or above the player zone
        if x < 40 or x > 440 or y < 592 or y > 784:
            return False

        # Get coordinates of corners of player sprite's collision rectangle
        x0, y0 = pos2cell(x-18, y-10)
        x1, y1 = pos2cell(x+18, y+10)

        # Check each corner against grid
        for yi in range(y0, y1+1):
            for xi in range(x0, x1+1):
                if self.grid[yi][xi] or xi == ax and yi == ay:
                    return False

        return True

    def clear_rocks_for_respawn(self, x, y):
        # Destroy any rocks that might be overlapping with the player when they respawn
        # Could be more than one rock, hence the loop
        x0, y0 = pos2cell(x-18, y-10)
        x1, y1 = pos2cell(x+18, y+10)

        for yi in range(y0, y1+1):
            for xi in range(x0, x1+1):
                self.damage(xi, yi, 5)

    def update(self):
        # Increment time - used by segments. Time moves twice as fast every fourth wave.
        self.time += (2 if self.wave % 4 == 3 else 1)

        # At the start of each frame, we reset occupied to be an empty set. As each individual myriapod segment is
        # updated, it will create entries in the occupied set to indicate that other segments should not attempt to
        # enter its current grid cell. There are two types of entries that are created in the occupied set. One is a
        # tuple consisting of a pair of numbers, representing grid cell coordinates. The other is a tuple consisting of
        # three numbers - the first two being grid cell coordinates, the third representing an edge through which a
        # segment is trying to enter a cell.
        # It is only used for myriapod segments - not rocks. Those are stored in self.grid.
        self.occupied = set()

        # Call update method on all objects. grid is a list of lists, equivalent to a 2-dimensional array,
        # so sum can be used to produce a single list containing all grid objects plus the contents of the other
        # Actor lists. The player and flying enemy, which are object references rather than lists, are appended as single-item lists.
        all_objects = sum(self.grid, self.bullets + self.segments + self.explosions + [self.player] + [self.flying_enemy])
        for obj in all_objects:
            if obj:
                obj.update()

        # Recreate the bullets list, which will contain all existing bullets except those which have gone off the screen or have hit something
        self.bullets = [b for b in self.bullets if b.y > 0 and not b.done]

        # Recreate the explosions list, which will contain all existing explosions except those which have completed their animations
        self.explosions = [e for e in self.explosions if not e.timer == 31]

        # Recreate the segments list, which will contain all existing segments except those whose health is zero
        self.segments = [s for s in self.segments if s.health > 0]

        if self.flying_enemy:
            # Destroy flying enemy if it goes off the left or right sides of the screen, or health is zero
            if self.flying_enemy.health <= 0 or self.flying_enemy.x < -35 or self.flying_enemy.x > 515:
                self.flying_enemy = None
        elif random() < .01:    # If there is no flying enemy, small chance of creating one each frame
            self.flying_enemy = FlyingEnemy(self.player.x if self.player else 240)

        if self.segments == []:
            # No myriapod segments - start a new wave
            # First, ensure there are enough rocks. Count the number of rocks in the grid and if there aren't enough,
            # create one per frame. Initially there should be 30 rocks - each wave, this goes up by one.
            num_rocks = 0
            for row in self.grid:
                for element in row:
                    if element != None:
                        num_rocks += 1
            if num_rocks < 31+self.wave:
                while True:
                    x, y = randint(0, num_grid_cols-1), randint(1, num_grid_rows-3)     # Leave last 2 rows rock-free
                    if self.grid[y][x] == None:
                        self.grid[y][x] = Rock(x, y)
                        break
            else:
                # New wave and enough rocks - create a new myriapod
                play_sound("wave")
                self.wave += 1
                self.time = 0
                self.segments = []
                num_segments = 8 + self.wave // 4 * 2   # On the first four waves there are 8 segments - then 10, and so on
                for i in range(num_segments):
                    if DEBUG_TEST_RANDOM_POSITIONS:
                        cell_x, cell_y = randint(1, 7), randint(1, 7)
                    else:
                        cell_x, cell_y = -1-i, 0
                    # Determines whether segments take one or two hits to kill, based on the wave number.
                    # e.g. on wave 0 all segments take one hit; on wave 1 they alternate between one and two hits
                    health = [[1,1],[1,2],[2,2],[1,1]][self.wave % 4][i % 2]
                    fast = self.wave % 4 == 3   # Every fourth myriapod moves faster than usual
                    head = i == 0           # The first segment of each myriapod is the head
                    self.segments.append(Segment(cell_x, cell_y, health, fast, head))

        return self

    def draw(self):
        self.screen.blit("bg" + str(max(self.wave, 0) % 3), (0, 0))

        # Create a list of all grid locations and other objects which need to be drawn
        # (Most grid locations will be set to None as they are unoccupied, hence the check "if obj:" further down)
        all_objs = sum(self.grid, self.bullets + self.segments + self.explosions + [self.player])

        # We want to draw objects in order based on their Y position. Objects further down the screen should be drawn
        # after (and therefore in front of) objects higher up the screen. We can use Python's built-in sort function
        # to put the items in the desired order, before we draw them. The following function specifies the criteria
        # used to decide how the objects are sorted.
        def sort_key(obj):
            # Returns a tuple consisting of two elements. The first is whether the object is an instance of the
            # Explosion class (True or False). A value of true means it will be displayed in front of other objects.
            # The second element is a number - either the objects why position, or zero if obj is 'None'
            return (isinstance(obj, Explosion), obj.y if obj else 0)

        # Sort list using the above function to determine order
        all_objs.sort(key=sort_key)

        # Draw the flying enemy on top of everything else
        all_objs.append(self.flying_enemy)

        # Draw the objects
        for obj in all_objs:
            if obj:
                obj.draw()

