from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import CollisionBox, CollisionTraverser, CollisionHandlerQueue, CollisionRay, CollisionNode, CollisionSphere, BitMask32, CollisionHandlerGravity
from math import sin, cos, pi
from panda3d.core import Vec3
from panda3d.core import Point3
from direct.interval.IntervalGlobal import LerpPosInterval

class Npc():

    def __init__(self, model_way, cords, direction, size):
        self.model_way = model_way
        self.cords = cords
        self.direction = direction
        self.size = size
        self.character = loader.loadModel(model_way)
        self.character.reparentTo(render)
        self.character.setScale(1)
        self.character.setPos(cords)
        self.character.setHpr(direction)
        self.character.setScale(size)

class Player(Npc):
    def __init__(self, model_way, cords, direction, size, onGround = False):
        super().__init__(model_way, cords, direction)
        self.character.setScale(0.5)
        self.onGround = False
        #self.accept_events_p()

class P(Npc):
    def __init__(self,):
        super().__init__(self,)

class Land():
    
    def __init__(self):
        self.model2 = loader.loadModel('models/location2.glb')
        self.model2.reparentTo(render)
        self.model2.setScale(1)
        self.model2.setPos(0, 0, -30)
        self.model2.setHpr(90, 90, 0)