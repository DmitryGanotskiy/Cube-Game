from ursina import *

class Game(Ursina):
    def __init__(self):
        super().__init__() 
        window.fullscreen = True
        Entity(model='sphere', scale=100, texture='textures/sky1', double_sided=True)
        EditorCamera()
        camera.world_position=(0,0,-15)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.loadGame()

    def loadGame(self):
        self.createPosition()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
        self.cube_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT, 'FACE': self.FACE,
                                    'BACK': self.BACK, 'TOP': self.TOP}
        self.animation_time = 0.2
        self.action_trigger = True

    def rotate(self, side_name):
        if not self.action_trigger:
            return

        self.action_trigger = False
        cube_positions = self.cube_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
        invoke(self.animation_trigger, delay=self.animation_time + 0.11)

    def animation_trigger(self):
        self.action_trigger = True

    def to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def createPosition(self):
        self.LEFT = {Vec3(-1,y,z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x,-1,z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x,y,-1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x,y,1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1,y,z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x,1,z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP

    def input(self, key, *args):
        if key:
            keys = dict(zip('asdwqe', 'LEFT BOTTOM RIGHT TOP FACE BACK'.split()))
            if key in keys and self.action_trigger:
                self.rotate(keys[key])
        super().input(key, *args)


if __name__ == "__main__":
    game = Game()
    game.run()
