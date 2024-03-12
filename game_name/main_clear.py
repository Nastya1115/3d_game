from classes import *

def degToRad(degrees):
    return degrees * (pi / 180.0)

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.set_background_color(0.5, 0.5, 1, 1)

        self.first_view = False
        self.CameraSwingActivated = False

        self.f1_cam()
        self.setup_camera()

        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        self.gravityHandler = CollisionHandlerGravity()

        self.land = Land()

        self.setup_controls()
        self.mouse_contorls()

        taskMgr.add(self.update, 'update')

        base.camLens.setFov(90)

    def setup_camera(self):
        self.camera.setPos(0, 0, 3)

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

    def update(self, task):
        dt = globalClock.getDt()

        self.cTrav.traverse(render)

        if self.CameraSwingActivated == True:

            playerMoveSpeed = 1.5

            x_movement = 0
            y_movement = 0
            z_movement = 0

            if self.keyMap['forward'] == True:
                x_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
                y_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            if self.keyMap['back'] == True:
                x_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
                y_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            if self.keyMap['left'] == True:
                x_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
                y_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            if self.keyMap['right'] == True:
                x_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
                y_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))

            self.camera.setPos(
                camera.getX() + x_movement,
                camera.getY() + y_movement,
                camera.getZ() + z_movement,
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