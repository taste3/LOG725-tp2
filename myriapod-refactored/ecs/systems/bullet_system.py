from pgzero.actor import Actor
from utils import pos2cell
from modules.explosion import Explosion
from modules.segment import Segment
from modules.rock import Rock
from random import random
from systems.game_state import GameState
from systems.sound_system import play_sound
from utils import pos2cell
from modules.explosion import Explosion
from modules.segment import Segment
from modules.rock import Rock
from ecs.components.actor_component import ActorComponent
from ecs.components.bullet_data import BulletData
from ecs.components.rigidbody import Rigidbody
from ecs.entity import Entity


class BulletSystem:
    instance = None

    def __init__(self):
        BulletSystem.instance = self
        self.bullets = []

    def shoot_bullet(self, x, y):
        bullet_entity = Entity()
        bullet_entity.add_component(ActorComponent(Actor("bullet", pos=(x, y - 8))))
        bullet_entity.add_component(Rigidbody(0, -24))
        bullet_entity.add_component(BulletData())

        GameState.game.bullets.append(bullet_entity)
        self.bullets.append(bullet_entity)

    def update(self):
        for bullet in self.bullets[:]:
            rigidbody = bullet.get_component(Rigidbody)
            data = bullet.get_component(BulletData)
            actor = bullet.get_component(ActorComponent).actor
            x, y = actor.pos

            # Move bullet acording to Rigidbody
            x += rigidbody.speed_x
            y += rigidbody.speed_y
            actor.pos = (x, y)

            # On vérifie les collisions comme avant dans Bullet
            cell = pos2cell(x, y)
            if GameState.game.damage(*cell, 1, True):
                data.done = True
            else:
                for obj in GameState.game.segments + [GameState.game.flying_enemy]:
                    if obj and obj.collidepoint((x, y)):
                        GameState.game.explosions.append(Explosion(obj.pos, 2))

                        obj.health -= 1

                        if isinstance(obj, Segment):
                            if obj.health == 0 and not GameState.game.grid[obj.cell_y][obj.cell_x] and \
                               GameState.game.allow_movement(GameState.game.player.x, GameState.game.player.y, obj.cell_x, obj.cell_y):
                                GameState.game.grid[obj.cell_y][obj.cell_x] = Rock(obj.cell_x, obj.cell_y, random() < .2)

                            play_sound("segment_explode")
                            GameState.game.score += 10
                        else:
                            play_sound("meanie_explode")
                            GameState.game.score += 20

                        data.done = True
                        break

            # Si le data de la balle est done ou qu'elle est sortie de l'écran on retire du système
            if data.done or y < 0:
                self.bullets.remove(bullet)

    def draw(self):
        for bullet in self.bullets:
            bullet.get_component(ActorComponent).actor.draw()