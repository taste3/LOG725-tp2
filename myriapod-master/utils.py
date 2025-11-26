from constants import *

# Convert a position in pixel units to a position in grid units. In this game, a grid square is 32 pixels.
def pos2cell(x, y):
    return ((int(x)-16)//32, int(y)//32)

# Convert grid cell position to pixel coordinates, with a given offset
def cell2pos(cell_x, cell_y, x_offset=0, y_offset=0):
    # If the requested offset is zero, returns the centre of the requested cell, hence the +16. In the case of the
    # X axis, there's a 16 pixel border at the left and right of the screen, hence +16 becomes +32.
    return ((cell_x * 32) + 32 + x_offset, (cell_y * 32) + 16 + y_offset)


def inverse_direction(dir):
    if dir == DIRECTION_UP:
        return DIRECTION_DOWN
    elif dir == DIRECTION_RIGHT:
        return DIRECTION_LEFT
    elif dir == DIRECTION_DOWN:
        return DIRECTION_UP
    elif dir == DIRECTION_LEFT:
        return DIRECTION_RIGHT

def is_horizontal(dir):
    return dir == DIRECTION_LEFT or dir == DIRECTION_RIGHT