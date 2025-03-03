# PythonにBlenderの機能へのアクセスを許可する
import bpy

# Python に Blender のメッシュ編集機能へのアクセスを許可する
import bmesh

# 乱数を生成するための Python 機能の拡張
import random


def get_random_color():
    """ランダムな色を生成する"""
    # 0.0 から 1.0 までの値を作成
    red = random.random()
    green = random.random()
    blue = random.random()
    alpha = 1.0
    color = (red, green, blue, alpha)

    return color


def generate_random_color_materials(obj, count):
    """オブジェクトにマテリアルを作成して割当てる"""
    # メッシュの各面を反復処理
    for i in range(count):
        # 新しいマテリアルを作成する
        mat = bpy.data.materials.new(name=f"material_{i}")
        mat.diffuse_color = get_random_color()

        # オブジェクトにマテリアルを追加する
        obj.data.materials.append(mat)


def add_ico_sphere():
    """ICO 球を追加する"""
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3)

    return bpy.context.active_object


def assign_materials_to_faces(obj):
    """オブジェクトのすべての面を反復処理し、
    面にランダムなマテリアルを割当てる"""

    # 編集モードをオンにする
    bpy.ops.object.editmode_toggle()

    # すべての面の選択を解除
    bpy.ops.mesh.select_all()

    # メッシュオブジェクトからジオメトリデータを取得
    bmesh_obj = bmesh.from_edit_mesh(obj.data)

    # オブジェクトに割り当てられたマテリアルの数を取得
    material_count = len(obj.data.materials)

    # メッシュの各面を反復処理する
    for face in bmesh_obj.faces:
        # ランダムにマテリアルを選択する
        obj.active_material_index = random.randint(0, material_count)

        # 面を選択し、アクティブなマテリアルを割当てる
        face.select = True
        bpy.ops.object.material_slot_assign()
        face.select = False

    # 編集モードをオフにする
    bpy.ops.object.editmode_toggle()


ico_object = add_ico_sphere()


# 作成するマテリアルの数を保持する変数の作成
material_count = 30

# オブジェクトにマテリアルを作成して割当てる
generate_random_color_materials(ico_object, material_count)

assign_materials_to_faces(ico_object)
