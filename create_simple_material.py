# PythonにBlenderの機能へのアクセスを許可する
import bpy

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
    principled_bsdf_node.inputs["Roughness"].default_value = random.uniform(0.1, 1.0)

    return material


def add_mesh():

    # ICO 球を作成する
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5)

    # シェードスムース
    bpy.ops.object.shade_smooth()

    # メッシュオブジェクトへの参照を取得する
    mesh_obj = bpy.context.active_object

    return mesh_obj


def main():

    partially_clean_the_scene()

    name = "My_Generated_Material"
    material = create_material(name)

    mesh_obj = add_mesh()

    # メッシュオブジェクトにマテリアルを適用する
    mesh_obj.data.materials.append(material)


main()
