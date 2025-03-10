import bpy
import random


# 基本的なクラス
class PrintColor:
    def __init__(self, color="red"):
        self.color = color

    def print_color(self):
        print(f"The color is {self.color}")


my_color = PrintColor()
my_color.print_color()
my_color2 = PrintColor(color="green")
my_color2.print_color()


# クラス変数の利用
class InstanceCount:
    instance_count = 0

    def __init__(self):
        InstanceCount.instance_count += 1

    # クラス変数のようにクラスから直接使用できる書き方
    @classmethod
    def get_instance_count(cls):
        print(f"Instance count:{cls.instance_count}")


# @classmethodを使った際の呼び出し方
a = InstanceCount()
InstanceCount.get_instance_count()
b = InstanceCount()
InstanceCount.get_instance_count()


# オブジェクトの移動
class ObjectMover:
    def add_cube(self):
        bpy.ops.mesh.primitive_cube_add()

    def move_x(self, amount):
        obj = bpy.context.active_object
        obj.location.x = amount

    def move_y(self, amount):
        obj = bpy.context.active_object
        obj.location.y = amount

    def move_z(self, amount):
        obj = bpy.context.active_object
        obj.location.z = amount


create_cube = ObjectMover()
create_cube.add_cube()
create_cube.move_x(2)
create_cube.move_y(5)
create_cube.move_z(3)


# オブジェクトの削除
class ObjectDeleter:
    def delete_object(self):
        bpy.ops.object.delete()


obj_delete = ObjectDeleter()
obj_delete.delete_object()


# シーンをカスタマイズする
class CustomSceneManager:
    def add_sphere(self):
        bpy.ops.mesh.primitive_uv_sphere_add()

    def add_torus(self):
        bpy.ops.mesh.primitive_torus_add()

    def clear_scene(self):
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()


sm = CustomSceneManager()
sm.add_sphere()
sm.add_torus()
sm.clear_scene()


# スケール変更クラス
class ObjectScaler:
    def add_ico_sphere(self):
        bpy.ops.mesh.primitive_ico_sphere_add()

    def double_scale(self):
        obj = bpy.context.active_object
        obj.scale *= 2

    def half_scale(self):
        obj = bpy.context.active_object
        obj.scale *= 0.5


ico_sphere = ObjectScaler()
ico_sphere.add_ico_sphere()
ico_sphere.double_scale()
# ico_sphere.half_scale()


# ランダム位置への移動
class RandomMover:
    def add_monkey(self):
        bpy.ops.mesh.primitive_monkey_add()

    def move_random_x(self):
        obj = bpy.context.active_object
        obj.location.x = random.randint(-10, 10)

    def move_random_y(self):
        obj = bpy.context.active_object
        obj.location.y = random.randint(-10, 10)

    def move_random_z(self):
        obj = bpy.context.active_object
        obj.location.z = random.randint(-10, 10)


random_obj = RandomMover()
random_obj.add_monkey()
random_obj.move_random_x()
random_obj.move_random_y()
random_obj.move_random_z()


# ランダムな色のマテリアルを適用する
class RandomColorMaterial:
    def add_cylinder(self):
        bpy.ops.mesh.primitive_cylinder_add()

    def apply_random_material(self):
        random_material = bpy.data.materials.new("Random Material")
        random_material.diffuse_color = (
            random.random(),
            random.random(),
            random.random(),
            1.0,
        )

        obj = bpy.context.active_object
        obj.data.materials.append(random_material)


cylinder = RandomColorMaterial()
cylinder.add_cylinder()
cylinder.apply_random_material()


# モディファイア適用
class ModifierManager:
    def add_cone(self):
        bpy.ops.mesh.primitive_cone_add()

    def apply_subsurf(self, viewport_lvl, render_lvl):
        bpy.ops.object.modifier_add(type="SUBSURF")
        bpy.context.object.modifiers["Subdivision"].levels = viewport_lvl
        bpy.context.object.modifiers["Subdivision"].render_levels = render_lvl


cone = ModifierManager()
cone.add_cone()
cone.apply_subsurf(2, 3)


# オブジェクトのリスト管理
class SceneObjectList:
    def list_objects(self):
        objects = bpy.data.objects
        for obj in objects:
            print(obj.name)


objects = SceneObjectList()
objects.list_objects()
