import bpy


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


clear_scene()


# class MyClass:
#     def __init__(self):
#         self.name = "my name"
#         print(f"hello from init {self.name}")


# a = MyClass()
# a.name = "my new name"
# a.name


# class MyClass:
#     def __init__(self, name=None):
#         if name is None:
#             self.name = "default name"
#         else:
#             self.name = name

#     def print_name(self):
#         print(f"the name is {self.name}")


# a = MyClass()
# a.print_name()

# b = MyClass("Taro")
# b.print_name()


# class MyClass:
#     note = "this class was created by me"
#     instance_count = 0

#     def __init__(self, name=None):
#         MyClass.instance_count += 1
#         if name is None:
#             self.name = "default name"
#         else:
#             self.name = name

#     def print_name(self):
#         print(f"the name is {self.name}")


# a = MyClass()
# a.instance_count
# MyClass.note = "new note"
# a.note


# class SceneManager:
#     def add_cube(self):
#         bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
#     def add_light(self):
#         bpy.ops.object.light_add(type="POINT", location=(5, 5, 5))
#     def add_camera(self):
#         bpy.ops.object.camera_add(location=(0, -10, 5))
#         camera = bpy.context.object
#         camera.rotation_euler = (1.2, 0, 0)
#     def create_default_scene(self):
#         self.add_cube()
#         self.add_light()
#         self.add_camera()

# sm = SceneManager()
# sm.create_default_scene()


class IcoSphereMesh:
    def __init__(self, mesh_object=None):
        if mesh_object and mesh_object.type == "MESH":
            self.mesh_object = mesh_object
        else:
            bpy.ops.mesh.primitive_ico_sphere_add()
            self.mesh_object = bpy.context.object
        self.wireframe_name = None

    def double_scale(self):
        self.mesh_object.scale *= 2

    def add_wireframe_mod(self):
        if self.wireframe_name:
            print("error: can't have more than one wireframe modifier")
            return
        self.wireframe_name = "wireframe"
        self.mesh_object.modifiers.new(name=self.wireframe_name, type="WIREFRAME")
        # bpy.ops.object.select_all(action="DESELECT")
        # self.mesh_object.select_set(True)
        # bpy.ops.object.modifier_add(type="WIREFRAME")
        # self.mesh_object.modifiers.new(name="wireframe", type="WIREFRAME")

    def wireframe_thickness(self, thickness):
        if not self.wireframe_name:
            print("error: no wireframe modifier found")
            return
        self.mesh_object.modifiers[self.wireframe_name].thickness = thickness


my_ico = IcoSphereMesh()
my_ico.double_scale()
my_ico.add_wireframe_mod()
