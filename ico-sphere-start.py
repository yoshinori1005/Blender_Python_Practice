import bpy


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


clear_scene()


class BaseMesh:
    def __init__(self, mesh_object=None):
        if mesh_object and mesh_object.type == "MESH":
            self.mesh_object = mesh_object
        else:
            bpy.ops.mesh.primitive_ico_sphere_add()
            self.mesh_object = bpy.context.object

        self.wireframe_name = None

    def create_mesh(self):
        pass

    def double_scale(self):
        if not self.mesh_object:
            return
        self.mesh_object.scale *= 2

    def add_wireframe_mod(self):
        if self.wireframe_name:
            print("error: can't have more than one wireframe mod")
            return
        self.wireframe_name = "wireframe"
        self.mesh_object.modifiers.new(name=self.wireframe_name, type="WIREFRAME")

    def set_wireframe_thickness(self, thickness):
        if not self.wireframe_name:
            print("error: no wireframe mod found")
            return
        self.mesh_object.modifiers[self.wireframe_name].thickness = thickness


class IcoSphereMesh(BaseMesh):
    def __init__(self, mesh_object=None):
        super().__init__(mesh_object)

    def create_mesh(self):
        bpy.ops.mesh.primitive_ico_sphere_add()
        return bpy.context.object


i = IcoSphereMesh()
# i.create_mesh()
i.double_scale()
i.add_wireframe_mod()
