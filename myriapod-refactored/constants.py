WIDTH = 480
HEIGHT = 800
TITLE = "Myriapod"

DEBUG_TEST_RANDOM_POSITIONS = False

# Pygame Zero allows you to access and change sprite positions based on various
# anchor points
CENTRE_ANCHOR = ("center", "center")

num_grid_rows = 25
num_grid_cols = 14

# In Python, multiplying a list by a number creates a list where the contents
# are repeated the specified number of times. So the code below is equivalent to:
# SECONDARY_AXIS_SPEED = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1 , 1, 2, 2, 2, 2]
# This list represents how much the segment moves along the secondary axis, in situations where it makes two 45° turns
# as described above. For the first four frames it doesn't move at all along the secondary axis. For the next eight
# frames it moves at one pixel per frame, then for the last four frames it moves at two pixels per frame.
SECONDARY_AXIS_SPEED = [0]*4 + [1]*8 + [2]*4


# The code below creates a list of 16 elements, where each element is the sum of all the equivalent elements in the
# SECONDARY_AXIS_SPEED list up to that point.
# It is equivalent to writing:
# SECONDARY_AXIS_POSITIONS = [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14]
# This list stores the total secondary axis movement that will have occurred at each phase in the segment's movement
# through the current grid cell (if the segment is turning)
SECONDARY_AXIS_POSITIONS = [sum(SECONDARY_AXIS_SPEED[:i]) for i in range(16)]


# Constants representing directions
DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3

# X and Y directions indexed into by in_edge and out_edge in Segment
# The indices correspond to the direction numbers above, i.e. 0 = up, 1 = right, 2 = down, 3 = left
DX = [0,1,0,-1]
DY = [-1,0,1,0]