import bpy
import random
import math


def clear_scene():
    # オブジェクトの削除
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # すべての孤立したデータの削除
    bpy.ops.outliner.orphans_purge(
        do_local_ids=True, do_linked_ids=True, do_recursive=True
    )


clear_scene()

# 複数のオブジェクトを追加
for i in range(10):
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    cube.location.x += i

# オブジェクトを特定の位置に移動
bpy.ops.mesh.primitive_uv_sphere_add()
sphere = bpy.context.active_object
sphere.name = "Sphere"
sphere.location = (0, 5, 2)

# オブジェクトの削除（特定の名前）
cube = bpy.data.objects.get("Cube")
if cube:
    bpy.data.objects.remove(cube, do_unlink=True)

# シーンの特定の名前のオブジェクトをすべて削除
object_name = "Cube"
for obj in bpy.data.objects:
    if object_name in obj.name:
        bpy.data.objects.remove(obj, do_unlink=True)

print(f"{object_name}を含むオブジェクトを削除しました")
# オブジェクトの複製とランダム移動
# 元のオブジェクトを取得
original = bpy.data.objects.get("Sphere")
if original:
    for i in range(5):
        # オブジェクトを複製
        obj = original.copy()
        # メッシュデータも複製
        obj.data = original.data.copy()
        obj.location = (random.randint(-5, 5), 0, 0)
        # シーンにリンク
        bpy.context.collection.objects.link(obj)

# 選択したオブジェクトをスケール変更
for obj in bpy.data.objects:
    obj.scale *= 1.5

# 新しいマテリアルを作成
blue_material = bpy.data.materials.new("Blue Material")
blue_material.diffuse_color = (0, 0, 1, 0)
bpy.context.object.data.materials.append(blue_material)

# マテリアルの変更
bpy.context.object.active_material.diffuse_color = (0, 1, 0, 1)

# オブジェクトごとに異なるマテリアルを適用
for obj in bpy.data.objects:
    random_material = bpy.data.materials.new(f"Random Material {obj.name}")
    random_material.diffuse_color = (
        random.uniform(0.0, 1.0),
        random.uniform(0.0, 1.0),
        random.uniform(0.0, 1.0),
        1.0,
    )
    obj.data.materials.append(random_material)

# 透明なマテリアルを適用
transparent_material = bpy.data.materials.new("Transparent Material")
transparent_material.diffuse_color = (1, 0, 0, 0.5)
bpy.ops.mesh.primitive_ico_sphere_add(location=(-5, 0, 0))
ico_sphere = bpy.context.active_object
ico_sphere.data.materials.append(transparent_material)
ico_sphere.active_material.blend_method = "BLEND"

# マテリアルのリストを取得
for mat in bpy.data.materials:
    print(mat.name)

# ベベルモディファイアを適用
bpy.ops.mesh.primitive_cone_add(location=(3, 4, 5))
bpy.ops.object.modifier_add(type="BEVEL")
bpy.context.object.modifiers["Bevel"].offset_type = "WIDTH"
bpy.context.object.modifiers["Bevel"].width = 0.1
# mod = bpy.context.object.modifiers.new(name="Bevel", type="BEVEL")
# mod.width = 0.1

# ワイヤーフレームモディファイアを追加
bpy.ops.object.modifier_add(type="WIREFRAME")
bpy.context.object.modifiers["Wireframe"].thickness = 0.05
# mod = bpy.context.object.modifiers.new(name="Wireframe", type="WIREFRAME")
# mod.thickness = 0.05

# カーブオブジェクトの作成
bpy.ops.curve.primitive_bezier_circle_add(location=(0, 0, 5))

# カーブに沿ってオブジェクトを配置
bezier_circle = bpy.context.active_object
bpy.ops.mesh.primitive_cylinder_add(scale=(0.5, 0.5, 0.5))
bpy.ops.object.modifier_add(type="ARRAY")
bpy.context.object.modifiers["Array"].fit_type = "FIT_CURVE"
bpy.context.object.modifiers["Array"].curve = bezier_circle

# 特定のモディファイアの削除
# 操作するオブジェクトの名前
object_name = "Cone"
# 削除したいモディファイアの名前
modifier_name = "Bevel"

# オブジェクトがシーンに存在するかの確認
if object_name in bpy.data.objects:
    obj = bpy.data.objects[object_name]

    # モディファイアがオブジェクトに存在するかの確認
    if modifier_name in obj.modifiers:
        obj.modifiers.remove(obj.modifiers[modifier_name])
        print(f"{modifier_name}を削除しました")
    else:
        print(f"{modifier_name}はオブジェクトにありません")
else:
    print(f"{object_name}は見つかりません")

# カメラの移動と回転
bpy.ops.object.camera_add(location=(0, -8, 5))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, 0)

# 複数のカメラを追加
# 既存のカメラを削除
for obj in bpy.data.objects:
    if obj.type == "CAMERA":
        bpy.data.objects.remove(obj, do_unlink=True)
# 位置と角度のリストを作成
camera_settings = [
    ((0, -4, 3), (math.radians(60), 0, 0)),
    ((3, 2, 4), (math.radians(45), 0, math.radians(120))),
    ((-4, 6, 4), (math.radians(45), 0, math.radians(-150))),
]
# 第一に位置、第二に角度を指定して設定
for pos, rot in camera_settings:
    bpy.ops.object.camera_add(location=pos, rotation=rot)

# レンダリングの設定変更
bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.cycles.samples = 100

# 特定のカメラをアクティブにする
bpy.context.scene.camera = bpy.data.objects.get("Camera")

# レンダリングを実行し画像を保存
# bpy.context.scene.render.filepath = "//render_output.png"
# bpy.ops.render.render(write_still=False)
