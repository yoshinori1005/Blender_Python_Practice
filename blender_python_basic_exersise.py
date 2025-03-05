import bpy
import math
import random


def clear_scene():
    # オブジェクトの削除
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # すべての孤立したデータの削除
    bpy.ops.outliner.orphans_purge(
        do_local_ids=True, do_linked_ids=True, do_recursive=True
    )


clear_scene()

# オブジェクトの追加
bpy.ops.mesh.primitive_cube_add()

# オブジェクトの移動
bpy.context.object.location = (2, 3, 1)

# オブジェクトの回転
bpy.context.object.rotation_euler.x = math.radians(90)

# オブジェクトのスケール変更
bpy.context.object.scale *= 2

# 複数のオブジェクトの追加
for i in range(5):
    bpy.ops.mesh.primitive_uv_sphere_add()
    obj = bpy.context.active_object
    obj.location.x = i * 2

# オブジェクトの一覧表示
for obj in bpy.data.objects:
    print(obj.name)

# 特定のオブジェクトを選択して移動
cube = bpy.data.objects.get("Cube")
if cube:
    cube.location = (5, 0, 0)

# アクティブオブジェクトの複製
obj = bpy.context.active_object
for i in range(3):
    new_obj = obj.copy()
    new_obj.location.x += (i + 1) * 2
    bpy.context.collection.objects.link(new_obj)

# ランダムな位置にオブジェクトを配置
for i in range(10):
    bpy.ops.mesh.primitive_cylinder_add()
    cylinder = bpy.context.active_object
    cylinder.location = (random.randint(-5, 5), 0, 0)

# マテリアルを追加
red_material = bpy.data.materials.new("Red Material")
red_material.diffuse_color = (1, 0, 0, 1)
obj = bpy.context.active_object
obj.data.materials.append(red_material)

# ランダムな色のマテリアルを適用
random_material = bpy.data.materials.new("Random Material")
random_r = random.uniform(0.0, 1.0)
random_g = random.uniform(0.0, 1.0)
random_b = random.uniform(0.0, 1.0)
random_material.diffuse_color = (random_r, random_g, random_b, 1.0)
obj = bpy.context.active_object
obj.data.materials.append(random_material)

# モディファイアの追加
bpy.ops.object.modifier_add(type="SUBSURF")
bpy.context.object.modifiers["Subdivision"].levels = 2

# すべてのモディファイアを削除
bpy.context.object.modifiers.clear()

# カメラの追加と配置
bpy.ops.object.camera_add(location=(0, -10, 5))
camera = bpy.context.object
camera.rotation_euler = (math.radians(60), 0, 0)

# ライトの追加
positions = [(3, 0, 2), (-3, 3, 2), (0, -3, 2)]
for pos in positions:
    bpy.ops.object.light_add(type="POINT", location=pos)


# カスタムオペレーターの作成
class AddCube(bpy.types.Operator):
    bl_idname = "object.add_cube"
    bl_label = "Add Cube"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {"FINISHED"}


bpy.utils.register_class(AddCube)


class GetObjectListScene(bpy.types.Operator):
    bl_idname = "object.get_object_list"
    bl_label = "Get Object List Scene"

    def execute(self, context):
        for obj in bpy.data.objects:
            print(obj.name)
        return {"FINISHED"}


bpy.utils.register_class(GetObjectListScene)

clear_scene()

# オブジェクトが移動するアニメーションの作成
bpy.ops.mesh.primitive_cube_add()
cube = bpy.context.active_object
cube.location = (0, 0, 0)
cube.keyframe_insert(data_path="location", frame=1)
cube.location = (5, 0, 0)
cube.keyframe_insert(data_path="location", frame=50)

# オブジェクトの回転アニメーション
cube.rotation_euler.z = math.radians(0)
cube.keyframe_insert(data_path="rotation_euler", frame=1, index=2)
cube.rotation_euler.z = math.radians(360)
cube.keyframe_insert(data_path="rotation_euler", frame=100, index=2)
bpy.context.scene.frame_end = 100
bpy.ops.action.interpolation_type(type="LINEAR")
