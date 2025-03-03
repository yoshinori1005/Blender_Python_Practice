# PythonにBlenderの機能へのアクセスを許可する
import bpy

# Python に Blender のメッシュ編集機能へのアクセスを許可する
import bmesh

# 乱数を生成するための Python 機能の拡張
import random

# ICO球を追加
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3)
ico_object = bpy.context.active_object

# 編集モードをオンにする
bpy.ops.object.editmode_toggle()

# すべての面の選択を解除
bpy.ops.mesh.select_all()

# メッシュオブジェクトからジオメトリデータを取得
ico_bmesh = bmesh.from_edit_mesh(ico_object.data)

# メッシュの各面を反復処理
for face in ico_bmesh.faces:

    # ランダムな色を生成する
    # 0.0 から 1.0 までの値を作成
    red = random.random()
    green = random.random()
    blue = random.random()
    alpha = 1.0
    color = (red, green, blue, alpha)

    # 新しいマテリアルを作成する
    mat = bpy.data.materials.new(name=f"face_{face.index}")
    mat.diffuse_color = color

    # オブジェクトにマテリアルを追加する
    ico_object.data.materials.append(mat)

    # アクティブなマテリアルを設定する
    ico_object.active_material_index = face.index

    # 面を選択し、アクティブなマテリアルを割当てる
    face_select = True
    bpy.ops.object.material_slot_assign()
    face_select = False

# 編集モードをオフにする
bpy.ops.object.editmode_toggle()
