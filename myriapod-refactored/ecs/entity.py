# L'entité est un conteneur permettant d’y attacher des composants.

class Entity:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def get_component(self, component_type):
        # on regarde dans la liste de composants et on retourne le premier qui est une instance de ce que l'on à spécifié en paramêtre
        # (j'aurais pu aussi empêché d'avoir plus d'un composant d'un même type)
        for comp in self.components:
            if isinstance(comp, component_type):
                return comp
        return None