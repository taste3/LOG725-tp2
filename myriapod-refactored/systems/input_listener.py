from pgzero.keyboard import keyboard

# Cette classe représente le "Publisher" dans le Patron Observer
class InputListener:
    def __init__(self):
        self.observers = {}
        self.previous = set()
        self.current = set()
    
    def update(self):
        self.current = {k for k, v in keyboard.__dict__.items() if v}
        for observer in self.observers:
            observer_key = observer.key
            return key in self.current and key not in self.previous

    def add_observer(key: str, ):
        pass

    def pressed(self, key):
        """Edge: key was NOT down but is NOW down."""
        