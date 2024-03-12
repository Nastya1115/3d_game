from classes import *

def degToRad(degrees):
    return degrees * (pi / 180.0)

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.set_background_color(0.5, 0.5, 1, 1)

        self.npc = Npc('models/npc_pig_male.glb', (-4, -6, -3.9), (50, 90, 90), 0.3)
        self.apples = Npc('models/basket_and_apple.glb', (-1.3, 0, -2.6), (50, 90, 90), 0.05)

        self.first_view = False
        self.CameraSwingActivated = False
        self.onGround = False

        self.f1_cam()
        self.setup_controls()
        self.mouse_contorls()

        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        self.collision_handler = CollisionHandlerQueue()

        self.land = Land()
        '''
        landSolid = CollisionBox((-1000, 27.2, -1000), (1000, 0, 1000))
        landNode = CollisionNode('land-collision-node')
        landNode.addSolid(landSolid)
        self.land_collider = self.land.model2.attachNewNode(landNode)
        self.land_collider.setPythonTag('owner', self.land.model2)
        self.land_collider.show()
        self.cTrav.addCollider(self.land_collider, self.collision_handler)
        '''

        self.setup_camera()

        taskMgr.add(self.update_gravity, 'update')
        taskMgr.add(self.update, 'update')

        base.camLens.setFov(90)

    def setup_camera(self):
        self.camera.setPos(-1, 0, 20)

        cameraCollider = CollisionNode('camera_collider')
        cameraCollider.setIntoCollideMask(BitMask32.bit(0))
        cameraCollider.setIntoCollideMask(BitMask32.allOff())
        colliderSphere = CollisionSphere(0, 0, 20, 1)
        cameraCollider.addSolid(colliderSphere)
        cameraColliderNodePath = self.camera.attachNewNode(cameraCollider)
        self.cTrav.addCollider(cameraColliderNodePath, self.collision_handler)

    def free_cam(self):
        self.release_mouse()
        self.enableMouse()

    def f1_cam(self):
        self.first_view = True
        self.disable_mouse()
        self.capture_mouse()
        self.mouse_contorls()

    def mouse_contorls(self):
        self.accept('n', self.f1_cam)
        self.accept('m', self.free_cam)

    def jump(self):
        self.onGround = False
        new_z = self.camera.getZ() + 3
        camera_interval = LerpPosInterval(self.camera, duration=0.2, pos=(self.camera.getX(), self.camera.getY(), new_z))
        camera_interval.start()

    def setup_controls(self):
        self.keyMap = {
            "forward": False,
            "back": False,
            "left": False,
            "right": False,
        }

        self.accept('w', self.update_controls, ['forward', True])
        self.accept('w-up', self.update_controls, ['forward', False])
        self.accept('s', self.update_controls, ['back', True])
        self.accept('s-up', self.update_controls, ['back', False])
        self.accept('a', self.update_controls, ['right', True])
        self.accept('a-up', self.update_controls, ['right', False])
        self.accept('d', self.update_controls, ['left', True])
        self.accept('d-up', self.update_controls, ['left', False])

    def update_controls(self, key, value):
        self.keyMap[key] = value

    def capture_mouse(self):
        self.CameraSwingActivated = True

        md = self.win.getPointer(0)
        self.last_mouseX = md.getX()
        self.last_mouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_relative)
        properties.setFullscreen(True)
        self.win.requestProperties(properties)

    def release_mouse(self):
        self.CameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_relative)
        properties.setFullscreen(False)
        self.win.requestProperties(properties)

    def update_gravity(self, task):
        dt = globalClock.getDt()

        gravity = 9.81
        gravity_vector = Vec3(0, 0, -gravity)

        if self.onGround == True:
            self.accept('space', self.jump)

        if self.camera.getZ() <= -1.5:
            self.onGround = True
       
        if self.onGround == False:
            self.camera.setPos(self.camera.getPos() + gravity_vector * dt)

        '''
        self.cTrav.traverse(render)
        collisions = self.collision_handler.getEntries()

        if collisions:
            self.onGround = True
        '''

        return task.cont

    def update(self, task):
        dt = globalClock.getDt()

        if self.CameraSwingActivated:
            playerMoveSpeed = 1.5

            x_movement = 0
            y_movement = 0
            z_movement = 0

            if self.keyMap['forward']:
                x_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
                y_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            if self.keyMap['back']:
                x_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
                y_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            if self.keyMap['left']:
                x_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
                y_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            if self.keyMap['right']:
                x_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
                y_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))

            self.camera.setPos(
                self.camera.getX() + x_movement,
                self.camera.getY() + y_movement,
                self.camera.getZ() + z_movement,
            )

            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()
            mouse_changeX = mouseX - self.last_mouseX
            mouse_changeY = mouseY - self.last_mouseY

            self.cameraSwingFactor = 90
            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouse_changeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouse_changeY * dt * self.cameraSwingFactor)),
                0
            )

            self.last_mouseX = mouseX
            self.last_mouseY = mouseY

        return task.cont

game = Game()
game.run()