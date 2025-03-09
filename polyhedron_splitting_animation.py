import bpy
import math
import random
from mathutils import Vector, Euler


def scene_clear():
    """シーンのオブジェクトをデータを含め全削除"""
    # 既存のオブジェクトを削除
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # すべての孤立したデータの削除
    bpy.ops.outliner.orphans_purge(
        do_local_ids=True, do_linked_ids=True, do_recursive=True
    )


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
    emission_node.inputs["Color"].default_value = (0, 1, 0, 1)
    emission_node.inputs["Strength"].default_value = 20

    # ノードを接続
    links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])

    return mat


def add_sphere():
    """発行する球体を追加"""
    mat = create_emission_material()
    bpy.ops.mesh.primitive_uv_sphere_add(scale=(0.2, 0.2, 0.2))
    obj = bpy.context.object
    obj.data.materials.append(mat)


def add_wireframe_polyhedron():
    """ワイヤーフレームの二十面体を追加"""
    # 二十面体を追加(ワイヤーフレーム)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1)
    obj = bpy.context.object
    obj.name = "Wreframe Polyhedron"

    # ワイヤーフレームモディファイアを追加
    bpy.ops.object.modifier_add(type="WIREFRAME")
    bpy.context.object.modifiers["Wireframe"].thickness = 0.01


def set_metallic_material():
    """金属風のマテリアルを設定"""
    mat = bpy.data.materials.new(name="Metal")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.2

    return mat


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


def split_face():
    """オブジェクトを面ごとに分離"""
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="LOOSE")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", center="MEDIAN")

    # すべての分割されたオブジェクトを取得
    return [obj for obj in bpy.context.selected_objects]


def apply_animation(faces, frame_start=1, frame_mid=144, frame_end=288):
    """オブジェクトのばらけるアニメーション"""
    for face in faces:
        initial_location = face.location.copy()

        # 初期位置と回転のキーフレームを設定
        face.keyframe_insert(data_path="location", frame=frame_start)
        face.keyframe_insert(data_path="rotation_euler", frame=frame_start)

        # ランダムな移動方向（法線方向にバラける）
        move_direction = Vector(
            (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        )
        move_direction.normalize()
        move_distance = random.uniform(2.5, 5.0)
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


def setup_scene():
    """カメラとライトを設定"""
    bpy.ops.object.camera_add(location=(-1.5, -7, 3))
    cam = bpy.context.object
    cam.rotation_euler = (math.radians(68.75), 0, math.radians(-12))

    light_positions = [
        (3.8, -2.75, -2),
    ]

    for i in range(3):
        bpy.ops.object.light_add(type="AREA", location=light_positions)
        light = bpy.context.object
        light.data.color = (0.46, 0.78, 1)
        light.data.energy = 1000


scene_clear()

# ブルームの設定オン
bpy.context.scene.eevee.use_bloom = True

add_sphere()
add_wireframe_polyhedron()
add_animation_polyhedron()

faces = split_face()

apply_animation(faces)
setup_scene()
