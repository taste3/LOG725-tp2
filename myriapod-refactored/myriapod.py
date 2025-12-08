import pgzero, pgzrun, pygame, sys
import pgzero.music
from pgzero.loaders import images, sounds
from pgzero.keyboard import keyboard
from systems.state import State
from modules.game import Game
from modules.player import Player
from constants import WIDTH, HEIGHT, TITLE
from systems.game_state import GameState
from systems.input_listener import InputListener

# Music path
pgzero.music.searchpath = ["assets/music"]
# Image path
images.subpath = "assets/images"
# Sound path
sounds.subpath = "assets/sounds"

# Check Python version number. sys.version_info gives version as a tuple, e.g. if (3,7,2,'final',0) for version 3.7.2.
# Unlike many languages, Python can compare two tuples in the same way that you can compare numbers.


# Check Pygame Zero version. This is a bit trickier because Pygame Zero only lets us get its version number as a string.
# So we have to split the string into a list, using '.' as the character to split on. We convert each element of the
# version number into an integer - but only if the string contains numbers and nothing else, because it's possible for
# a component of the version to contain letters as well as numbers (e.g. '2.0.dev0')
# We're using a Python feature called list comprehension - this is explained in the Bubble Bobble/Cavern chapter.



def on_space_pressed():
    global state

    if state == State.MENU:
        state = State.PLAY
        GameState.create_game(Game(screen, Player((240, 768))))

    elif state == State.GAME_OVER:
        state = State.MENU
        GameState.create_game(Game(screen))


# Pygame Zero calls the update and draw functions each frame
def update():
    global state
    InputListener.instance.update()

    if GameState.game is None:
        GameState.create_game(Game(screen))

    if state == State.MENU:
        GameState.game.update()

    elif state == State.PLAY:
        if GameState.game.player.lives == 0 and GameState.game.player.timer == 100:
            sounds.gameover.play()
            state = State.GAME_OVER
        else:
            GameState.game.update()

def draw():
    # Draw the game, which covers both the game during gameplay but also the game displaying in the background
    # during the main menu and game over screens
    GameState.game.draw()

    if state == State.MENU:
        # Display logo
        screen.blit("title", (0, 0))

        # 14 frames of animation for "Press space to start", updating every 4 frames
        screen.blit("space" + str((GameState.game.time // 4) % 14), (0, 420))

    elif state == State.PLAY:
        # Display number of lives
        for i in range(GameState.game.player.lives):
            screen.blit("life", (i*40+8, 4))

        # Display score
        score = str(GameState.game.score)
        for i in range(1, len(score)+1):
            # In Python, a negative index into a list (or in this case, into a string) gives you items in reverse order,
            # e.g. 'hello'[-1] gives 'o', 'hello'[-2] gives 'l', etc.
            digit = score[-i]
            screen.blit("digit"+digit, (468-i*24, 5))

    elif state == State.GAME_OVER:
        # Display "Game Over" image
        screen.blit("over", (0, 0))

def play_music():
    pygame.mixer.music.load("assets\\music\\theme.ogg")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.4)

def launch():
    global state
    
    if sys.version_info < (3,5):
        print("This game requires at least version 3.5 of Python. Please download it from www.python.org")
        return

    pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
    if pgzero_version < [1,2]:
        print("This game requires at least version 1.2 of Pygame Zero. You have version {0}. Please upgrade using the command 'pip3 install --upgrade pgzero'".format(pgzero.__version__))
        sys.exit()

    state = State.MENU
    InputListener()
    InputListener.instance.bind("space", on_space_pressed)
    play_music()
    pgzrun.go()

launch()
