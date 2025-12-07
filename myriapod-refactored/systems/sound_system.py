from systems.game_state import GameState
from pgzero.builtins import sounds
from random import randint

def play_sound(name, count=1):
    # Some sounds have multiple varieties. If count > 1, we'll randomly choose one from those
    # We don't play any sounds if there is no player (e.g. if we're on the menu)
    if GameState.game.player:
        try:
            # Pygame Zero allows you to write things like 'sounds.explosion.play()'
            # This automatically loads and plays a file named 'explosion.wav' (or .ogg) from the sounds folder (if
            # such a file exists)
            # But what if you have files named 'explosion0.ogg' to 'explosion5.ogg' and want to randomly choose
            # one of them to play? You can generate a string such as 'explosion3', but to use such a string
            # to access an attribute of Pygame Zero's sounds object, we must use Python's built-in function getattr
            sound = getattr(sounds, name + str(randint(0, count - 1)))
            sound.play()
        except Exception as e:
            # If no such sound file exists, print the name
            print(e)
