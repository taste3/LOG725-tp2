from pgzero.keyboard import keyboard
import pygame

# Cette classe représente le "Publisher" dans le Patron Observer
# Cette classe est également un Singleton
class InputListener:

    instance = None
    def __init__(self):
        InputListener.instance = self
        # les observateurs une liste de Tuple (code de la touche, callback )
        self.observers = []
        self.previous = set()
        self.current = set()
    
    def update(self):
        self.current = set(keyboard._pressed)
        # touches qui viennent d'être appuyées
        new_keypresses = self.current - self.previous
        for touche, callback in self.observers:
            if touche in new_keypresses:
                # on exécute le callback
                callback()

        self.previous = self.current.copy()
                

    def bind(self, key: str, method: callable):
        keycode = pygame.key.key_code(key)
        self.observers.append((keycode, method))