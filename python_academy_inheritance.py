import bpy


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


clear_scene()


# class MyClassA:
#     def __init__(self):
#         self.name = "default name"

#     def print_name(self):
#         print(f"Here is the name {self.name}")


# class MyClassB(MyClassA):
#     pass


# a = MyClassB()
# a.name
# a.print_name()


# class MyClassA:
#     def __init__(self, name):
#         self.name = name

#     def print_name(self):
#         print(f"Here is the name {self.name}")


# class MyClassB(MyClassA):
#     def __init__(self, name, number):
#         super().__init__(name)
#         self.number = number


# a = MyClassB("Taro", 44)
# a.print_name()
# print(a.number)


class LightTypes:
    PointLight = "POINT"
    Sun = "SUN"
    SpotLight = "SPOT"
    AreaLight = "AREA"


class BaseLight:
    def __init__(self, name, light_type, location, energy=1000, color=(1, 1, 1)):
        self.name = name
        self.light_type = light_type
        self.location = location
        self.energy = energy
        self.color = color
        self.light_object = None

    def create_light(self):
        bpy.ops.object.light_add(type=self.light_type, location=self.location)
        self.light_object = bpy.context.active_object
        self.set_properties()

    def set_properties(self):
        if not self.light_object:
            return
        self.light_object.name = self.name
        self.light_object.data.energy = self.energy
        self.light_object.data.color = self.color

    def move_light(self, new_location):
        if not self.light_object:
            return
        self.light_object.location = new_location


class PointLight(BaseLight):
    def __init__(self, name="Point_Light", location=(0, 0, 3), energy=1000):
        super().__init__(name, LightTypes.PointLight, location, energy)


class SpotLight(BaseLight):
    def __init__(
        self,
        name="Spot_Light",
        location=(2, 2, 3),
        energy=1000,
        spot_size=0.785,
        spot_blend=0.2,
    ):
        super().__init__(name, LightTypes.SpotLight, location, energy)
        self.spot_size = spot_size
        self.spot_blend = spot_blend

    def set_properties(self):
        super().set_properties()
        if not self.light_object:
            return
        self.light_object.data.spot_size = self.spot_size
        self.light_object.data.spot_blend = self.spot_blend


class SunLight(BaseLight):
    def __init__(
        self,
        name="Sun_Light",
        location=(0, 0, 3),
        energy=1000,
        angle=0.0714,
        color=(1, 1, 1),
    ):
        super().__init__(name, LightTypes.Sun, location, energy, color)
        self.angle = angle

    def set_properties(self):
        super().set_properties()
        if not self.light_object:
            return
        self.light_object.data.angle = self.angle


class AreaLightShapes:
    Ellipse = "ELLIPSE"
    Disc = "DISC"
    Rectangle = "RECTANGLE"
    Square = "SQUARE"


class AreaLight(BaseLight):
    def __init__(
        self,
        name="Area_Light",
        location=(0, 0, 3),
        energy=1000,
        color=(1, 1, 1),
        shape=AreaLightShapes.Rectangle,
        size=1,
        size_y=1,
    ):
        super().__init__(name, LightTypes.AreaLight, location, energy, color)
        self.shape = shape
        self.size = size
        self.size_y = size_y

    def set_properties(self):
        super().set_properties()
        if not self.light_object:
            return
        self.light_object.data.shape = self.shape
        if self.shape in [AreaLightShapes.Rectangle, AreaLightShapes.Ellipse]:
            self.light_object.data.size = self.size
            self.light_object.data.size_y = self.size_y
        elif self.shape in [AreaLightShapes.Disc, AreaLightShapes.Square]:
            self.light_object.data.size = self.size


# l = BaseLight("my light", LightTypes.SpotLight, (0, 8, 5))
# l.create_light()

# pl = PointLight()
# pl.create_light()

# sl = SpotLight()
# sl.create_light()

# s = SunLight(color=(1, 0, 0))
# s.create_light()

al = AreaLight(shape=AreaLightShapes.Ellipse, size=2, size_y=1)
al.create_light()
