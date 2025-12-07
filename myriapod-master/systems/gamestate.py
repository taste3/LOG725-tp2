
# Singleton qui contient mon instance de Game
class GameState:

  # Instance de Game qui peut être accédée de partout dans le jeu
  game = None

  # Méthode de classe (statique) qui permet la création d'une nouvelle partie
  @classmethod
  def create_game(cls, new_game):
    cls.game = new_game

