from pgzero.actor import Actor
from constants import *
from utils import is_horizontal, inverse_direction, cell2pos
from systems.game_state import GameState

# SEGMENT MOVEMENT
# The code below creates several constants used in the Segment class in relation to movement and directions

# Each myriapod segment moves in relation to its current grid cell.
# A segment enters a cell from a particular edge (stored in 'in_edge' in the Segment class)
# After five frames it decides which edge it's going leave that cell through (stored in out_edge).
# For example, it might carry straight on and leave through the opposite edge from the one it started at.
# Or it might turn 90 degrees and leave through an edge to its left or right.
# In this case it initially turn 45 degrees and continues along that path for 8 frames. It then turns another
# 45 degrees, at which point they are heading directly towards the next grid cell.
# A segment spends a total of 16 frames in each cell. Within the update method, the variable 'phase' refers to
# where it is in that cycle - 0 meaning it's just entered a grid cell, and 15 meaning it's about to leave it.

# Let's imagine the case where a segment enters from the left edge of a cell and then turns to leave from the
# bottom edge. The segment will initially move along the horizontal (X) axis, and will end up moving along the
# vertical (Y) axis. In this case we'll call the X axis the primary axis, and the Y axis the secondary axis.
# The lists SECONDARY_AXIS_SPEED and SECONDARY_AXIS_POSITIONS are used to determine the movement of the segment.
# This is explained in more detail in the Segment.update method.

class Segment(Actor):
    def __init__(self, cx, cy, health, fast, head):
        super().__init__("blank")

        # Grid cell positions
        self.cell_x = cx
        self.cell_y = cy

        self.health = health

        # Determines whether the 'fast' version of the sprite is used. Note that the actual speed of the myriapod is
        # determined by how much time is included in the State.update method
        self.fast = fast

        self.head = head        # Should this segment use the head sprite?

        # Each myriapod segment moves in a defined pattern within its current cell, before moving to the next one.
        # It will start at one of the edges - represented by a number, where 0=down,1=right,2=up,3=left
        # self.in_edge stores the edge through which it entered the cell.
        # Several frames after entering a cell, it chooses which edge to leave through - stored in out_edge
        # The path it follows is explained in the update and rank methods
        self.in_edge = DIRECTION_LEFT
        self.out_edge = DIRECTION_RIGHT

        self.disallow_direction = DIRECTION_UP      # Prevents segment from moving in a particular direction
        self.previous_x_direction = 1               # Used to create winding/snaking motion

    def rank(self):
        # The rank method creates and returns a function. Don't worry if this seems a strange concept - it is
        # fairly advanced stuff. The returned function is passed to Python's 'min' function in the update method,
        # as the 'key' optional parameter. min then calls this function with the numbers 0 to 3, representing the four
        # directions

        def inner(proposed_out_edge):
            # proposed_out_edge is a number between 0 and 3, representing a possible direction to move - see DIRECTION_UP etc and DX/DY above
            # This function returns a tuple consisting of a series of factors determining which grid cell the segment should try to move into next.
            # These are not absolute rules - rather they are used to rank the four directions in order of preference,
            # i.e. which direction is the best (or at least, least bad) to move in. The factors are boolean (True or False)
            # values. A value of False is preferable to a value of True.
            # The order of the factors in the returned tuple determines their importance in deciding which way to go,
            # with the most important factor coming first.
            new_cell_x = self.cell_x + DX[proposed_out_edge]
            new_cell_y = self.cell_y + DY[proposed_out_edge]

            # Does this direction take us to a cell which is outside the grid?
            # Note: when the segments start, they are all outside the grid so this would be True, except for the case of
            # walking onto the top-left cell of the grid. But the end result of this and the following factors is that
            # it will still be allowed to continue walking forwards onto the screen.
            out = new_cell_x < 0  or new_cell_x > num_grid_cols - 1 or new_cell_y < 0 or new_cell_y > num_grid_rows - 1

            # We don't want it to to turn back on itself..
            turning_back_on_self = proposed_out_edge == self.in_edge

            # ..or go in a direction that's disallowed (see comments in update method)
            direction_disallowed = proposed_out_edge == self.disallow_direction

            # Check to see if there's a rock at the proposed new grid cell.
            # rock will either be the Rock object at the new grid cell, or None.
            # It will be set to None if there is no Rock object is at the new location, or if the new location is
            # outside the grid. We also have to account for the special case where the segment is off the left-hand
            # side of the screen on the first row, where it is initially created. We mustn't try to access that grid
            # cell (unlike most languages, in Python trying to access a list index with negative value won't necessarily
            # result in a crash, but it's still not a good idea)
            if out or (new_cell_y == 0 and new_cell_x < 0):
                rock = None
            else:
                rock = GameState.game.grid[new_cell_y][new_cell_x]

            rock_present = rock != None

            # Is new cell already occupied by another segment, or is another segment trying to enter my cell from
            # the opposite direction?
            occupied_by_segment = (new_cell_x, new_cell_y) in GameState.game.occupied or (self.cell_x, self.cell_y, proposed_out_edge) in GameState.game.occupied

            # Prefer to move horizontally, unless there's a rock in the way.
            # If there are rocks both horizontally and vertically, prefer to move vertically
            if rock_present:
                horizontal_blocked = is_horizontal(proposed_out_edge)
            else:
                horizontal_blocked = not is_horizontal(proposed_out_edge)

            # Prefer not to go in the previous horizontal direction after we move up/down
            same_as_previous_x_direction = proposed_out_edge == self.previous_x_direction

            # Finally we create and return a tuple of factors determining which cell segment should try to move into next.
            # Most important first - e.g. we shouldn't enter a new cell if if's outside the grid
            return (out, turning_back_on_self, direction_disallowed, occupied_by_segment, rock_present, horizontal_blocked, same_as_previous_x_direction)

        return inner

    def update(self):
        # Segments take either 16 or 8 frames to pass through each grid cell, depending on the amount by which
        # game.time is updated each frame. phase will be a number between 0 and 15 indicating where we're at
        # in that cycle.
        phase = GameState.game.time % 16

        if phase == 0:
            # At this point, the segment is entering a new grid cell. We first update our current grid cell coordinates.
            self.cell_x += DX[self.out_edge]
            self.cell_y += DY[self.out_edge]

            # We then need to update in_edge. If, for example, we left the previous cell via its right edge, that means
            # we're entering the new cell via its left edge.
            self.in_edge = inverse_direction(self.out_edge)

            # During normal gameplay, once a segment reaches the bottom of the screen, it starts moving up again.
            # Once it reaches row 18, it starts moving down again, so that it remains a threat to the player.
            # During the title screen, we allow segments to go all the way back up to the top of the screen.
            if self.cell_y == (18 if GameState.game.player else 0):
                self.disallow_direction = DIRECTION_UP
            if self.cell_y == num_grid_rows-1:
                self.disallow_direction = DIRECTION_DOWN

        elif phase == 4:
            # At this point we decide which new cell we're going to go into (and therefore, which edge of the current
            # cell we will leave via - to be stored in out_edge)
            # range(4) generates all the numbers from 0 to 3 (corresponding to DIRECTION_UP etc)
            # Python's built-in 'min' function usually chooses the lowest number, so would usually return 0 as the result.
            # But if the optional 'key' argument is specified, this changes how the function determines the result.
            # The rank function (see above) returns a function (named 'inner' in rank), which min calls to decide
            # how the items should be ordered. The argument to inner represents a possible direction to move in.
            # The 'inner' function returns a tuple of boolean values - for example: (True,False,False,True,etc..)
            # When Python compares two such tuples, it considers values of False to be less than values of True,
            # and values that come earlier in the sequence are more significant than later values. So (False,True)
            # would be considered less than (True,False).
            self.out_edge = min(range(4), key = self.rank())

            if is_horizontal(self.out_edge):
                self.previous_x_direction = self.out_edge

            new_cell_x = self.cell_x + DX[self.out_edge]
            new_cell_y = self.cell_y + DY[self.out_edge]
            
            # Destroy any rock that might be in the new cell
            if new_cell_x >= 0 and new_cell_x < num_grid_cols:
                GameState.game.damage(new_cell_x, new_cell_y, 5)

            # Set new cell as occupied. It's a case of whichever segment is processed first, gets first dibs on a cell
            # The second line deals with the case where two segments are moving towards each other and are in
            # neighbouring cells. It allows a segment to tell if another segment trying to enter its cell from
            # the opposite direction
            GameState.game.occupied.add((new_cell_x, new_cell_y))
            GameState.game.occupied.add((new_cell_x, new_cell_y, inverse_direction(self.out_edge)))

        # turn_idx tells us whether the segment is going to be making a 90 degree turn in the current cell, or moving
        # in a straight line. 1 = anti-clockwise turn, 2 = straight ahead, 3 = clockwise turn, 0 = leaving through same
        # edge from which we entered (unlikely to ever happen in practice)
        turn_idx = (self.out_edge - self.in_edge) % 4

        # Calculate segment offset in the cell, measured from the cell's centre
        # We start off assuming that the segment is starting from the top of the cell - i.e. self.in_edge being DIRECTION_UP,
        # corresponding to zero. The primary and secondary axes, as described under "SEGMENT MOVEMENT" above, are Y and X.
        # We then apply a calculation to rotate these X and Y offsets, based on the actual direction the segment is coming from.
        # Let's take as an example the case where the segment is moving in a straight line from top to bottom.
        # We calculate offset_x by multiplying SECONDARY_AXIS_POSITIONS[phase] by 2-turn_idx. In this case, turn_idx
        # will be 2.  So 2 - turn_idx will be zero. Multiplying anything by zero gives zero, so we end up with no
        # movement on the X axis - which is what we want in this case.
        # The starting point for the offset_y calculation is that the segment starts at an offset of -16 and must cover
        # 32 pixels over the 16 phases - therefore we must multiply phase by 2. We then subtract the result of the
        # previous line, in which stolen_y_movement was calculated by multiplying SECONDARY_AXIS_POSITIONS[phase] by
        # turn_idx % 2.  mod 2 gives either zero (if turn_idx is 0 or 2), or 1 if it's 1 or 3. In the case we're looking
        # at, turn_idx is 2, so stolen_y_movement is zero.
        # The end result of all this is that in the case where the segment is moving in a straight line through a cell,
        # it just moves at 2 pixels per frame along the primary axis. If it's turning, it starts out moving at 2px
        # per frame on the primary axis, but then starts moving along the secondary axis based on the values in
        # SECONDARY_AXIS_POSITIONS. In this case we don't want it to continue moving along the primary axis - it should
        # initially slow to moving at 1px per phase, and then stop moving completely. Effectively, the secondary axis
        # is stealing movement from the primary axis - hence the name 'stolen_y_movement'
        offset_x = SECONDARY_AXIS_POSITIONS[phase] * (2 - turn_idx)
        stolen_y_movement = (turn_idx % 2) * SECONDARY_AXIS_POSITIONS[phase]
        offset_y = -16 + (phase * 2) - stolen_y_movement

        # A rotation matrix is a set of numbers which, when multiplied by a set of coordinates, result in those
        # coordinates being rotated. Recall that the code above  makes the assumption that segment is starting from the
        # top edge of the cell and moving down. The code below chooses the appropriate rotation matrix based on the
        # actual edge the segment started from, and then modifies offset_x and offset_y based on this rotation matrix.
        rotation_matrix = [[1,0,0,1],[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0]][self.in_edge]
        offset_x, offset_y = offset_x * rotation_matrix[0] + offset_y * rotation_matrix[1], offset_x * rotation_matrix[2] + offset_y * rotation_matrix[3]

        # Finally, we can calculate the segment's position on the screen. See cell2pos function above.
        self.pos = cell2pos(self.cell_x, self.cell_y, offset_x, offset_y)

        # We now need to decide which image the segment should use as its sprite.
        # Images for segment sprites follow the format 'segABCDE' where A is 0 or 1 depending on whether this is a
        # fast-moving segment, B is 0 or 1 depending on whether we currently have 1 or 2 health, C is whether this
        # is the head segment of a myriapod, D represents the direction we're facing (0 = up, 1 = top right,
        # up to 7 = top left) and E is how far we are through the walking animation (0 to 3)

        # Three variables go into the calculation of the direction. turn_idx tells us if we're making a turn in this
        # cell - and if so, whether we're turning clockwise or anti-clockwise. self.in_edge tells us which side of the
        # grid cell we entered from. And we can use SECONDARY_AXIS_SPEED[phase] to find out whether we should be facing
        # along the primary axis, secondary axis or diagonally between them.
        # (turn_idx - 2) gives 0 if straight, -1 if turning anti-clockwise, 1 if turning clockwise
        # Multiplying this by SECONDARY_AXIS_SPEED[phase] gives 0 if we're not doing a turn in this cell, or if
        # we are going to be turning but have not yet begun to turn. If we are doing a turn in this cell, and we're
        # at a phase where we should be showing a sprite with a new rotation, the result will be -1 or 1 if we're
        # currently in the first (45°) part of a turn, or -2 or 2 if we have turned 90°.
        # The next part of the calculation multiplies in_edge by 2 and then adds the result to the result of the previous
        # part. in_edge will be a number from 0 to 3, representing all possible directions in 90° increments.
        # It must be multiplied by two because the direction value we're calculating will be a number between 0 and 7,
        # representing all possible directions in 45° increments.
        # In the sprite filenames, the penultimate number represents the direction the sprite is facing, where a value
        # of zero means it's facing up. But in this code, if, for example, in_edge were zero, this means the segment is
        # coming from the top edge of its cell, and therefore should be facing down. So we add 4 to account for this.
        # After all this, we may have ended up with a number outside the desired range of 0 to 7. So the final step
        # is to MOD by 8.
        direction = ((SECONDARY_AXIS_SPEED[phase] * (turn_idx - 2)) + (self.in_edge * 2) + 4) % 8

        leg_frame = phase // 4  # 16 phase cycle, 4 frames of animation

        # Converting a boolean value to an integer gives 0 for False and 1 for True. We then need to convert the
        # result to a string, as an integer can't be appended to a string.
        self.image = "seg" + str(int(self.fast)) + str(int(self.health == 2)) + str(int(self.head)) + str(direction) + str(leg_frame)