# PythonにBlenderの機能へのアクセスを許可する
import bpy

# Python の数学機能を拡張する
import math

# 乱数を生成するための Python 機能を拡張する
import random


# シーンのすべてのオブジェクトを削除する関数
def partially_clean_the_scene():

    # シーン内のすべてのオブジェクトを選択
    bpy.ops.object.select_all(action="SELECT")

    # シーン内の選択されたオブジェクトをすべて削除する
    bpy.ops.object.delete()

    # 削除したオブジェクトに関連付けられていたデータを確実に削除する
    bpy.ops.outliner.orphans_purge(
        do_local_ids=True, do_linked_ids=True, do_recursive=True
    )


# ノイズ マスクを作成する関数
def create_noise_mask(material):
    """次のノードを使用して、ノイズ マスクを作成するためのノード セットを追加する
    * テクスチャ座標ノード
    * マッピングノード
    * ノイズテクスチャノード
    * カラーランプノード
    """

    node_location_x_step = 300
    node_location_x = -node_location_x_step

    # カラーランプノードの作成
    # https://docs.blender.org/api/current/bpy.types.ShaderNodeValToRGB.html
    color_ramp_node = material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].position = 0.45
    color_ramp_node.color_ramp.elements[1].position = 0.5
    color_ramp_node.location.x = node_location_x
    node_location_x -= node_location_x_step

    # ノイズテクスチャノードの作成
    # https://docs.blender.org/api/current/bpy.types.ShaderNodeTexNoise.html#bpy.types.ShaderNodeTexNoise
    noise_texture_node = material.node_tree.nodes.new(type="ShaderNodeTexNoise")
    noise_texture_node.inputs["Scale"].default_value = random.uniform(1.0, 20.0)
    noise_texture_node.location.x = node_location_x
    node_location_x -= node_location_x_step

    # マッピングノードの作成
    # https://docs.blender.org/api/current/bpy.types.ShaderNodeMapping.html#bpy.types.ShaderNodeMapping
    mapping_node = material.node_tree.nodes.new(type="ShaderNodeMapping")
    mapping_node.inputs["Rotation"].default_value.x = math.radians(
        random.uniform(0.0, 360.0)
    )
    mapping_node.inputs["Rotation"].default_value.y = math.radians(
        random.uniform(0.0, 360.0)
    )
    mapping_node.inputs["Rotation"].default_value.z = math.radians(
        random.uniform(0.0, 360.0)
    )
    mapping_node.location.x = node_location_x
    node_location_x -= node_location_x_step

    # テクスチャ座標ノードの作成
    texture_coordinate_node = material.node_tree.nodes.new(type="ShaderNodeTexCoord")
    texture_coordinate_node.location.x = node_location_x
    node_location_x -= node_location_x_step

    # ノードを接続
    # https://docs.blender.org/api/current/bpy.types.NodeTree.html#bpy.types.NodeTree
    # https://docs.blender.org/api/current/bpy.types.NodeLinks.html#bpy.types.NodeLinks

    # ノイズテクスチャノードからカラーランプノードへの接続
    material.node_tree.links.new(
        noise_texture_node.outputs["Color"], color_ramp_node.inputs["Fac"]
    )
    # マッピングノードからノイズテクスチャノードへの接続
    material.node_tree.links.new(
        mapping_node.outputs["Vector"], noise_texture_node.inputs["Vector"]
    )
    # テクスチャ座標ノードからマッピングノードへの接続
    material.node_tree.links.new(
        texture_coordinate_node.outputs["Generated"], mapping_node.inputs["Vector"]
    )

    return color_ramp_node


# マテリアルを作成する関数
def create_material(name):

    # 新しいマテリアルを作成する
    material = bpy.data.materials.new(name=name)

    # ノード経由でマテリアルを作成できるようにする
    # materialはbpy.context.object.active_materialを参照しているため省略できる
    material.use_nodes = True

    # Principled BSDFシェーダーノードへの参照を取得する
    principled_bsdf_node = material.node_tree.nodes["Principled BSDF"]

    # マテリアルの基本色を設定する
    # bpy.data.materials["My_Generated_"].node_tree.nodes["Principled BSDF"]
    # .inputs[0].default_value = (R,G,B,A)で取得する（上記の変数で一部を定義し、省略）
    principled_bsdf_node.inputs["Base Color"].default_value = (0.8, 0.12, 0.0075, 1)

    # マテリアルのメタリック値を設定する
    principled_bsdf_node.inputs["Metallic"].default_value = 1.0

    # マテリアルの粗さの値を設定する
    # principled_bsdf_node.inputs["Roughness"].default_value = random.uniform(0.1, 1.0)

    color_ramp_node = create_noise_mask(material)

    # カラーランプノードからプリンシプルBSDFの粗さへの接続
    material.node_tree.links.new(
        color_ramp_node.outputs["Color"], principled_bsdf_node.inputs["Roughness"]
    )

    return material


# シーンにICO 球を追加する関数
def add_mesh():

    # ICO 球を作成する
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5)

    # シェードスムース
    bpy.ops.object.shade_smooth()

    # メッシュオブジェクトへの参照を取得する
    mesh_obj = bpy.context.active_object

    return mesh_obj


# メイン関数
def main():

    partially_clean_the_scene()

    name = "My_Generated_Material"
    material = create_material(name)

    mesh_obj = add_mesh()

    # メッシュオブジェクトにマテリアルを適用する
    mesh_obj.data.materials.append(material)


main()
