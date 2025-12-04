game_instance = None

def game(screen=None):
  global game_instance
  if game_instance is None and screen is None:
    print("error screen has not been initialized")
  elif game_instance is None:
    game_instance = Game(screen)
  else:
    return game_instance