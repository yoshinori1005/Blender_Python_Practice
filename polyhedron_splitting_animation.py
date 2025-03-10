# ====================
# 参考:https://www.artstation.com/artwork/nEQ4J4
# ====================

import bpy
import math
import random
from mathutils import Vector, Euler

# ====================
# ユーティリティ関数
# ====================


def create_collection(name):
    """指定した名前のコレクションを作成し、シーンに追加"""
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)

    return collection


def move_to_collection(obj, collection_name):
    """オブジェクトを指定したコレクションへ移動"""
    collection = create_collection(collection_name)
    for col in obj.users_collection:
        col.objects.unlink(obj)
    collection.objects.link(obj)


def scene_clear():
    """シーンのオブジェクトをデータを含め全削除"""
    # 既存のオブジェクトを削除
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # すべての孤立したデータの削除
    bpy.ops.outliner.orphans_purge(
        do_local_ids=True, do_linked_ids=True, do_recursive=True
    )

    # 既存の「Collection」があれば削除
    if "Collection" in bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections["Collection"])


# ===================
# マテリアル作成系
# ===================


def create_emission_material():
    """放射マテリアルの作成"""
    mat = bpy.data.materials.new("Emission")
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
    emission_node.inputs["Color"].default_value = (1, 1, 1, 1)
    emission_node.inputs["Strength"].default_value = 10

    # ノードを接続
    links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])

    return mat


def set_metallic_material():
    """虹色の反社を持つ金属風のマテリアルを設定"""
    if "Metal" in bpy.data.materials:
        return bpy.data.materials["Metal"]

    mat = bpy.data.materials.new(name="Metal")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    node_location_step = 200
    node_location_x = -node_location_step
    node_location_y = 300

    # HSVノードの作成
    hsv_node = nodes.new(type="ShaderNodeHueSaturation")
    hsv_node.location.x = node_location_x
    node_location_x -= node_location_step
    hsv_node.location.y = node_location_y
    hsv_node.inputs["Saturation"].default_value = 0.3
    hsv_node.inputs["Color"].default_value = (1, 0, 0, 1)

    # ベクトル演算ノードの作成(加算)
    vector_math_node = nodes.new(type="ShaderNodeVectorMath")
    vector_math_node.location.x = node_location_x
    node_location_x -= node_location_step
    vector_math_node.location.y = node_location_y
    vector_math_node.operation = "ADD"

    # タンジェントノードの作成
    tangent_node = nodes.new(type="ShaderNodeTangent")
    tangent_node.location.x = node_location_x
    node_location_x -= node_location_step
    tangent_node.location.y = node_location_y
    tangent_node.axis = "Z"

    # ジオメトリノードの作成
    geometry_node = nodes.new(type="ShaderNodeNewGeometry")
    geometry_node.location.x = vector_math_node.location.x - node_location_step
    geometry_node.location.y = node_location_y / 2

    # プリンシプルBSDFノード
    principled_node = mat.node_tree.nodes["Principled BSDF"]
    principled_node.inputs["Metallic"].default_value = 1.0
    principled_node.inputs["Specular"].default_value = 1.0
    principled_node.inputs["Roughness"].default_value = 0.05
    principled_node.inputs["Anisotropic"].default_value = 1.0
    principled_node.inputs["Anisotropic Rotation"].default_value = 0.2

    # ノード接続
    links.new(geometry_node.outputs["Incoming"], vector_math_node.inputs[1])
    links.new(tangent_node.outputs["Tangent"], vector_math_node.inputs[0])
    links.new(vector_math_node.outputs["Vector"], hsv_node.inputs["Hue"])
    links.new(hsv_node.outputs["Color"], principled_node.inputs["Base Color"])

    return mat


# ====================
# オブジェクト作成系
# ====================


def add_sphere():
    """発行する球体を追加"""
    mat = create_emission_material()
    bpy.ops.mesh.primitive_uv_sphere_add(scale=(0.2, 0.2, 0.2))
    obj = bpy.context.object
    obj.data.materials.append(mat)
    obj.name = "Emission Sphere"

    # 「Static Objects」コレクションに追加
    move_to_collection(obj, "Static Objects")


def add_wireframe_polyhedron():
    """ワイヤーフレームの二十面体を追加"""
    # 二十面体を追加(ワイヤーフレーム)
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1, radius=1, scale=(0.98, 0.98, 0.98)
    )
    obj = bpy.context.object
    obj.name = "Wireframe Polyhedron"
    mat = set_metallic_material()
    obj.data.materials.append(mat)

    # ワイヤーフレームモディファイアを追加
    bpy.ops.object.modifier_add(type="WIREFRAME")
    bpy.context.object.modifiers["Wireframe"].thickness = 0.01

    # 「Static Objects」コレクションに追加
    move_to_collection(obj, "Static Objects")


def add_animation_polyhedron():
    """アニメーション用の二十面体を追加"""
    # 二十面体を追加(アニメーション部分)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1)
    obj = bpy.context.object
    obj.name = "Polyhedron"

    mat = set_metallic_material()
    obj.data.materials.append(mat)

    # 辺分離モディファイアを適用
    bpy.ops.object.modifier_add(type="EDGE_SPLIT")
    bpy.context.object.modifiers["EdgeSplit"].split_angle = 0
    bpy.ops.object.modifier_apply(modifier="EdgeSplit")

    # ソリッド化モディファイアを追加
    bpy.ops.object.modifier_add(type="SOLIDIFY")
    bpy.context.object.modifiers["Solidify"].thickness = 0.02

    move_to_collection(obj, "Animated_Polyhedra")


def split_face():
    """オブジェクトを面ごとに分離"""
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="LOOSE")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", center="MEDIAN")

    # すべての分割されたオブジェクトを取得
    return [obj for obj in bpy.context.selected_objects]


# ====================
# アニメーション系
# ====================


def set_linear_interpolation(obj):
    """アニメーションを線形補間に設定"""
    action = obj.animation_data.action
    if action:
        for fcurve in action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = "LINEAR"


def apply_animation(faces, frame_start=1, frame_mid=144, frame_end=288):
    """オブジェクトのばらけるアニメーション"""
    for i, face in enumerate(faces, start=1):
        face.name = f"Polyhedron_{i}"
        # move_to_collection(face, "Animated_Polyhedra")

        initial_location = face.location.copy()
        # 初期位置と回転のキーフレームを設定
        face.keyframe_insert(data_path="location", frame=frame_start)
        face.keyframe_insert(data_path="rotation_euler", frame=frame_start)

        # ランダムな移動方向（法線方向にバラける）
        move_direction = Vector(
            (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        )
        move_direction.normalize()
        move_distance = random.uniform(2.0, 3.0)
        face.location = initial_location + move_direction * move_distance

        # ランダムな回転（XYZ回転）
        face.rotation_euler = Euler(
            (
                random.uniform(3.14, 6.28),
                random.uniform(3.14, 6.28),
                random.uniform(3.14, 6.28),
            ),
            "XYZ",
        )

        # 中間のキーフレームの設定
        face.keyframe_insert(data_path="location", frame=frame_mid)
        face.keyframe_insert(data_path="rotation_euler", frame=frame_mid)

        # 最終キーフレームの設定(元に戻す)
        face.location = initial_location
        face.rotation_euler = (0, 0, 0)
        face.keyframe_insert(data_path="location", frame=frame_end)
        face.keyframe_insert(data_path="rotation_euler", frame=frame_end)

        # set_linear_interpolation(face)


# ====================
# シーン設定系
# ====================


def set_scene_properties(
    resolution_value=2048,
    frame_range=288,
    shadow_cube_size="2048",
    shadow_cascade_size="4096",
):
    """シーンのプロパティ"""
    # 解像度の設定
    bpy.context.scene.render.resolution_x = resolution_value
    bpy.context.scene.render.resolution_y = resolution_value

    # ワールド背景カラー
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
        0.051,
        0.051,
        0.051,
        1,
    )

    # 影の設定
    bpy.context.scene.eevee.shadow_cube_size = shadow_cube_size
    bpy.context.scene.eevee.shadow_cascade_size = shadow_cascade_size

    # ブルームの設定オン
    bpy.context.scene.eevee.use_bloom = True
    bpy.context.scene.view_settings.view_transform = "Filmic"

    bpy.context.scene.frame_end = frame_range


def set_light_scene():
    """ライトの設定"""
    light_names = ["Key Light", "Fill Light", "Back Light"]
    light_positions = [(1.3, -4.7, -1.8), (-4, 3.9, 1.5), (5.1, 6.2, 0)]
    light_rotations = [
        (math.radians(-161), math.radians(-64), math.radians(-95)),
        (0, math.radians(-60), math.radians(-57)),
        (math.radians(-90), 0, math.radians(-38)),
    ]
    colors = [(0.46, 0.78, 1), (1, 0.6, 0.12), (1, 1, 1)]
    energies = [1000, 500, 500]

    for i in range(3):
        bpy.ops.object.light_add(
            type="AREA", location=light_positions[i], rotation=light_rotations[i]
        )
        light = bpy.context.object
        light.name = light_names[i]
        light.data.size = 6
        light.data.color = colors[i]
        light.data.energy = energies[i]
        move_to_collection(light, "Camera_Light")


def setup_scene():
    """シーンの設定"""
    set_scene_properties()

    bpy.ops.object.camera_add(location=(-1.5, -7, 3))
    cam = bpy.context.object
    cam.rotation_euler = (math.radians(68.75), 0, math.radians(-12))
    cam.data.type = "ORTHO"
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 7.5
    cam.data.dof.aperture_fstop = 5
    move_to_collection(cam, "Camera_Light")

    set_light_scene()


# ====================
# 実行処理
# ====================

scene_clear()

add_sphere()
add_wireframe_polyhedron()
add_animation_polyhedron()

faces = split_face()

apply_animation(faces)
setup_scene()
