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


# 既存のオブジェクトを削除
def ObjectDeleter():
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_by_type(type="MESH")
    bpy.ops.object.delete()
    bpy.ops.object.select_by_type(type="CURVE")
    bpy.ops.object.delete()


# clear_scene()

# ランダムなオブジェクトの追加
# オブジェクトタイプの作成
object_types = ["CUBE", "SPHERE", "CYLINDER"]

for i in range(10):
    # リストからランダム抽出
    obj_type = random.choice(object_types)
    if obj_type == "CUBE":
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.active_object
        cube.location.x = random.randint(-5, 5)
    elif obj_type == "SPHERE":
        bpy.ops.mesh.primitive_uv_sphere_add()
        sphere = bpy.context.active_object
        sphere.location.x = random.randint(-5, 5)
    elif obj_type == "CYLINDER":
        bpy.ops.mesh.primitive_cylinder_add()
        cylinder = bpy.context.active_object
        cylinder.location.x = random.randint(-5, 5)

# 親子関係の設定
cube = bpy.data.objects.get("Cube")
sphere = bpy.data.objects.get("Sphere")

if cube and sphere:
    sphere.parent = cube

# 親子関係の解除
if sphere:
    sphere.parent = None

# オブジェクトの整列
for i, obj in enumerate(bpy.data.objects):
    obj.location.x = i

# オブジェクトのスナップ
obj = bpy.context.object
obj.location.x = round(obj.location.x)
obj.location.y = round(obj.location.y)
obj.location.z = round(obj.location.z)


# グラデーションマテリアルの適用
# ランダムなテクスチャの適用
def create_node():
    node_location_x_step = 300
    node_location_x = -node_location_x_step
    node_location_y = 300

    # カラーランプノード作成
    color_ramp_node = gradient_material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].color = (1, 0, 0, 1)
    color_ramp_node.color_ramp.elements[1].color = (0, 0, 1, 1)
    color_ramp_node.location.x = node_location_x
    node_location_x -= node_location_x_step
    color_ramp_node.location.y = node_location_y

    # ノイズテクスチャノード作成
    noise_texture_node = gradient_material.node_tree.nodes.new(
        type="ShaderNodeTexNoise"
    )
    noise_texture_node.inputs["Scale"].default_value = random.uniform(1.0, 20.0)
    noise_texture_node.location.x = node_location_x
    node_location_x -= node_location_x_step
    noise_texture_node.location.y = node_location_y

    # マッピングノード作成
    mapping_node = gradient_material.node_tree.nodes.new(type="ShaderNodeMapping")
    mapping_node.location.x = node_location_x
    node_location_x -= node_location_x_step
    mapping_node.location.y = node_location_y

    # テクスチャ座標ノード作成
    texture_coordinate_node = gradient_material.node_tree.nodes.new(
        type="ShaderNodeTexCoord"
    )
    texture_coordinate_node.location.x = node_location_x
    node_location_x -= node_location_x_step
    texture_coordinate_node.location.y = node_location_y

    # ノイズテクスチャノードからカラーランプノードへ接続
    gradient_material.node_tree.links.new(
        noise_texture_node.outputs["Color"], color_ramp_node.inputs["Fac"]
    )

    # マッピングノードからノイズテクスチャノードへ接続
    gradient_material.node_tree.links.new(
        mapping_node.outputs["Vector"], noise_texture_node.inputs["Vector"]
    )

    # テクスチャ座標ノードからマッピングノードへ接続
    gradient_material.node_tree.links.new(
        texture_coordinate_node.outputs["Generated"], mapping_node.inputs["Vector"]
    )

    return color_ramp_node


gradient_material = bpy.data.materials.new("Gradient Material")
gradient_material.use_nodes = True

principled_bsdf_node = gradient_material.node_tree.nodes["Principled BSDF"]

color_ramp_node = create_node()

gradient_material.node_tree.links.new(
    color_ramp_node.outputs["Color"], principled_bsdf_node.inputs["Base Color"]
)

obj = bpy.context.object
obj.data.materials.append(gradient_material)

# すべてのオブジェクトのマテリアルを変更
for obj in bpy.data.objects:
    if obj.type == "MESH":
        material = bpy.data.materials.new(f"Material_{obj.name}")
        material.diffuse_color = (1, 1, 0, 1)
        obj.data.materials.append(material)

# マテリアルの透過設定
transparent_material = bpy.data.materials.new("Transparent Material")
transparent_material.diffuse_color = (0, 1, 1, 0.3)
bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 3))
monkey = bpy.context.active_object
monkey.data.materials.append(transparent_material)
monkey.active_material.blend_method = "BLEND"

# エミッションマテリアルを適用
bpy.context.scene.eevee.use_bloom = True
mat = bpy.data.materials.new("Green Emission")
# ノードベースのマテリアルにする
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
# 既存のノードを削除
for node in nodes:
    nodes.remove(node)
# ノードの作成
output_node = nodes.new(type="ShaderNodeOutputMaterial")
output_node.location = (200, 0)

emission_node = nodes.new(type="ShaderNodeEmission")
emission_node.location = (0, 0)
emission_node.inputs["Color"].default_value = (0, 1, 0, 1)
emission_node.inputs["Strength"].default_value = 5

# ノードを接続
links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])

bpy.ops.mesh.primitive_cone_add(location=(-5, 0, 0))
obj = bpy.context.active_object

if obj and obj.type == "MESH":
    # 既存のマテリアルスロットがあるか確認し、なければ追加
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
else:
    print("アクティブオブジェクトが見つからないか、メッシュではありません")

clear_scene()

# カーブを作成し、メッシュを沿わせる
# 円形のカーブを作成
bpy.ops.curve.primitive_bezier_circle_add(radius=3)
curve = bpy.context.object
curve.name = "Circle_Curve"

# 立方体を作成
bpy.ops.mesh.primitive_cube_add(size=1)
cube = bpy.context.object
cube.name = "Cube"

# カーブモディファイアを追加
modifier = cube.modifiers.new(name="CurveFollow", type="CURVE")
modifier.object = curve
# X軸方向に沿わせる
modifier.deform_axis = "POS_X"

# 立方体の位置をカーブの始点に調整
cube.location = (3, 0, 0)

# ランダムなモディファイアの適用
modifier_types = ["SUBSURF", "SOLIDIFY", "WIREFRAME"]

for i in range(1):
    bpy.ops.mesh.primitive_torus_add()
    torus = bpy.context.active_object
    modifier_type = random.choice(modifier_types)
    if modifier_type == "SUBSURF":
        bpy.ops.object.modifier_add(type=modifier_types[0])
    elif modifier_type == "SOLIDIFY":
        bpy.ops.object.modifier_add(type=modifier_types[1])
    elif modifier_type == "WIREFRAME":
        bpy.ops.object.modifier_add(type=modifier_types[2])

# すべてのオブジェクトのモディファイアを適用
bpy.ops.object.select_all()
for obj in bpy.data.objects:
    if obj.type == "MESH":
        for mod in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)

# オブジェクトをカーブに沿ってアニメーション
frame_start = 1
frame_end = 100
cube = bpy.data.objects.get("Cube")
cube.location = (0, 0, 0)
cube.keyframe_insert("location", frame=frame_start, index=0)
cube.location = (18.8, 0, 0)
cube.keyframe_insert("location", frame=frame_end, index=0)

# Fカーブの取得と補間設定（リニア補間）
action = cube.animation_data.action
if action:
    for fcurve in action.fcurves:
        fcurve.modifiers.new(type="CYCLES")
        # X軸の動き
        if fcurve.data_path == "location" and fcurve.array_index == 0:
            for kp in fcurve.keyframe_points:
                # 補間をリニアに変更
                kp.interpolation = "LINEAR"

# ボリュームを持つオブジェクトの作成
# bpy.ops.mesh.primitive_cube_add(size=3)
# cube_2 = bpy.context.object
# cube_2.name = "Volume_Cube"

# ボリュームオブジェクトを作成
# bpy.ops.object.volume_add()
# volume = bpy.context.object
# volume.name = "Volume_Object"

# VDBファイルをボリュームに適用(事前にVDBファイルのパスを指定)
# Blenderの相対パス
# vdb_filepath="ファイル名.vdb"
# volume.data.filepath=vdb_filepath
# VDBがアニメーションシーケンスでない場合
# volume.data.is_sequence=False

# 立方体にボリュームモディファイアを追加
# modifier = cube_2.modifiers.new(name="VolumeModifier", type="VOLUME_TO_MESH")
# modifier.object = volume

# ボリュームの設定調整
# modifier.threshold = 0.1
# modifier.density = 1.0

# ランダムな回転アニメーション
# モンキーを追加
bpy.ops.mesh.primitive_monkey_add()
monkey = bpy.context.active_object


# ランダムな回転値の範囲を設定
monkey.rotation_euler = (
    random.uniform(0, math.radians(360)),
    random.uniform(0, math.radians(360)),
    random.uniform(0, math.radians(360)),
)

monkey.keyframe_insert("rotation_euler", frame=frame_start)

monkey.rotation_euler = (
    random.uniform(0, math.radians(360)),
    random.uniform(0, math.radians(360)),
    random.uniform(0, math.radians(360)),
)

monkey.keyframe_insert("rotation_euler", frame=frame_end)

monkey_action = monkey.animation_data.action

if monkey_action:
    # ループモディファイアを追加してループアニメーション化
    for fcurve in monkey_action.fcurves:
        fcurve.modifiers.new(type="CYCLES")

        # 線形補間設定
        if fcurve.data_path.startswith("rotation_euler"):
            for kp in fcurve.keyframe_points:
                kp.interpolation = "LINEAR"

# 複数のオブジェクトをランダムに動かす
for i in range(5):
    bpy.ops.mesh.primitive_cone_add()
    cone = bpy.context.object
    cone.location.x += i * 3

frame_start = 1
frame_end = 100
move_range = 5

# シーン内のすべてのオブジェクトから MESH タイプで
# アニメーションのついてないものを取得
objects = [
    obj
    for obj in bpy.context.scene.objects
    if obj.type == "MESH" and obj.animation_data is None
]

# 各オブジェクトに対してアニメーションを適用
for obj in objects:
    # オブジェクトの初期位置
    start_location = obj.location.copy()

    # ランダムな移動先を設定
    end_location = (
        start_location.x + random.uniform(-move_range, move_range),
        start_location.y + random.uniform(-move_range, move_range),
        start_location.z + random.uniform(-move_range, move_range),
    )

    # キーフレームの設定
    obj.location = start_location
    obj.keyframe_insert("location", frame=frame_start)

    obj.location = end_location
    obj.keyframe_insert("location", frame=frame_end)

    # アニメーションデータの作成
    obj.animation_data_create()
    obj_action = obj.animation_data.action

    if obj_action:
        for fcurve in obj_action.fcurves:
            if fcurve.data_path.startswith("location"):
                # ループアニメーション(CYCLESモディファイアを追加)
                fcurve.modifiers.new(type="CYCLES")

                # 線形補間設定
                for kp in fcurve.keyframe_points:
                    kp.interpolation = "LINEAR"

# シェイプキーを使ったアニメーション
bpy.ops.mesh.primitive_monkey_add(location=(-3, 0, 0))
obj = bpy.context.active_object

if obj and obj.type == "MESH" and obj.animation_data is None:
    # シェイプキーの作成(ベースキーがない場合は追加)
    if obj.data.shape_keys is None:
        # デフォルト形状の追加
        obj.shape_key_add(name="Basis")

    # 新しいシェイプキーの作成
    shape_key = obj.shape_key_add(name="ShapeKey_1")

    # シェイプキーの変形を適用
    for vert in obj.data.vertices:
        shape_key.data[vert.index].co.x += 0.5

    # アニメーションの設定
    frame_start = 1
    frame_end = 100

    # シェイプキーの影響度のキーフレーム設定
    shape_key.value = 0.0
    shape_key.keyframe_insert(data_path="value", frame=frame_start)

    shape_key.value = 1.0
    shape_key.keyframe_insert(data_path="value", frame=frame_end / 2)

    shape_key.value = 0.0
    shape_key.keyframe_insert(data_path="value", frame=frame_end)

    # アニメーションデータの作成
    obj.animation_data_create()
    obj_action = obj.animation_data.action

    if obj_action:
        for fcurve in obj_action.fcurves:
            if fcurve.data_path == f'key_block["{shape_key.name}"].value':
                # ループアニメーション
                fcurve.modifier.new(type="CYCLES")

                # 線形補間設定
                for kp in fcurve.keyframe_points:
                    kp.interpolation = "LINEAR"


# オブジェクトを制御するオペレーター
class ObjectDeleter(bpy.types.Operator):
    bl_idname = "object.delete_selected"
    bl_label = "Delete Selected Objects"

    def execute(self, context):
        bpy.ops.object.delete()
        return {"FINISHED"}


bpy.utils.register_class(ObjectDeleter)


# モディファイアを適用するオペレーター
class ApplyModifier(bpy.types.Operator):
    bl_idname = "object.apply_modifiers"
    bl_label = "Apply Modifier"

    def execute(self, context):
        obj = context.object
        for mod in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        return {"FINISHED"}


bpy.utils.register_class(ApplyModifier)
