from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from birdseye import eye

app = Ursina()

Sky()

@eye
def update():
    global pick
    if held_keys['1']: pick = 1
    if held_keys['2']: pick = 2
    if held_keys['3']: pick = 3
    if held_keys['4']: pick = 4
    if held_keys['5']: pick = 5
    if held_keys['6']: pick = 6

class Shootable(Button):
    def __init__(self, position=(0,0,0), texture='Bomb', color=color.rgb(229,0,0), radius=3):
        super().__init__(
            model='Bomb',
            texture=texture,
            position=position,
            color=color,
            parent=scene,
            collider='box',
            scale=.5
        )
        self.radius=radius
    
    def explode(self):
        camera.shake(.5,1,.05)
        for e in scene.entities:
            if e != self and distance(e.position, self.position) < self.radius:
                destroy(e)
        destroy(self)

    def input(self, key):
        if key == 'left mouse down':
            destroy(self)

    def update(self):
        if self.intersects():
            self.explode()
        if self.hovered:
            if held_keys['f']:
                try:
                    bomb = Shootable(position=self.position - mouse.normal / 5, texture='noise', color=color.rgb(229,0,0))
                    destroy(self)
                except:
                    pass

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='PixGrass', color=color.rgb(150,150,150), model='PixGrass'):
        super().__init__(
            model=model,
            texture=texture,
            position=position,
            color=color,
            parent=scene,
            collider='box',
            scale=.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                if pick == 1:
                    voxel=Voxel(position=self.position + mouse.normal, texture='PixGrass', color=color.rgb(150,150,150))
                if pick == 2:
                    voxel=Voxel(position=self.position + mouse.normal, texture='Brick', color=color.rgb(229,0,0), model='Brick')
                if pick == 3:
                    bomb = Shootable(position=self.position + mouse.normal, texture='Bomb', color=color.rgb(229,0,0))
                if pick == 4:
                    voxel=Voxel(position=self.position + mouse.normal, texture='Cobble', color=color.rgb(150,150,150), model='Cobble')
                if pick == 5:
                    voxel=Voxel(position=self.position + mouse.normal, texture='Glass', color=color.rgb(150,150,150), model='Glass')
                if pick == 6:
                    voxel=Voxel(position=self.position + mouse.normal, texture='Wood', color=color.rgb(150,150,150), model='Wood')
            if key == 'left mouse down':
                destroy(self)

for z in range(30):
    for x in range(30):
        voxel=Voxel(position=(x,-1,z))

class Main(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = FirstPersonController(position=(4, 2, 4), speed=5)
        self.blocks = []
        self.flashlight = Entity(parent=self.player, position=(0, 0, 0), rotation=(-90, 0, 0))
        self.flashlight_light = DirectionalLight(parent=self.flashlight, color=color.white, direction=(0, 1, 0), shadows=True)
        window.fullscreen = True
    def menu(self):
        self.wood = Entity(
            model='Wood',
            texture='Wood',
            color=color.rgb(150,150,150),
            position=Vec3(.4,-.1,1),
            rotation=(0,0,0),
            scale=.2,
            parent=camera.ui,
            visible=False
        )
        self.glass = Entity(
            model='Glass',
            texture='Glass',
            color=color.rgb(150,150,150),
            position=Vec3(.4,-.1,1),
            rotation=(0,0,0),
            scale=.2,
            parent=camera.ui,
            visible=False
        )
        self.cobble = Entity(
            model='Cobble',
            texture='Cobble',
            color=color.rgb(150,150,150),
            position=Vec3(.4,-.1,1),
            rotation=(0,0,0),
            scale=.2,
            parent=camera.ui,
            visible=False
        )
        self.bomb = Entity(
            model='Bomb',
            texture='Bomb',
            color=color.rgb(229,0,0),
            position=Vec3(.4,-.1,1),
            rotation=(0,0,0),
            scale=.2,
            parent=camera.ui,
            visible=False
        )
        self.brick = Entity(
            model='Brick',
            texture='Brick',
            color=color.rgb(229,0,0),
            position=Vec3(.4,-.1,1),
            rotation=(0,0,0),
            scale=.2,
            parent=camera.ui,
            visible=False
        )
        self.cube1 = Entity(
            model='PixGrass',
            texture='PixGrass',
            color=color.rgb(150,150,150),
            position=Vec3(.4,-.1,1),
            rotation=(0,0,0),
            scale=.2,
            parent=camera.ui,
            visible=False
        )
        self.hand = Entity(
            model='Hand',
            texture='Hand',
            color=color.rgb(255,229,180),
            position=Vec3(.75,-.6,1),
            rotation=Vec3(0,45,-45),
            parent=camera.ui,
            scale=.3,
            visible=True
        )

        self.slots = [self.cube1, self.brick, self.bomb, self.cobble, self.glass, self.wood]
        self.choice = 0
        self.swap()

    def swap(self):
        for x,y in enumerate(self.slots):
            if x == self.choice:
                y.visible = True
            else:
                y.visible = False

    def input(self,key):
        if key == '1':self.choice = 0;self.swap()
        if key == '2':self.choice = 1;self.swap()
        if key == '3':self.choice = 2;self.swap()
        if key == '4':self.choice = 3;self.swap()
        if key == '5':self.choice = 4;self.swap()
        if key == '6':self.choice = 5;self.swap()

DirectionalLight(position=(0,50,0))

pick = 1

if __name__ == '__main__':
    main = Main()
    main.menu()

app.run()