# PythonにBlenderの機能へのアクセスを許可する
import bpy

# Pythonの数学機能の拡張
import math


# 16進数カラーコードをRGBAに変換する関数
def hex_color_to_rgba(hex_color):
    # 先頭の「#」記号を削除
    hex_color = hex_color[1:]

    # 赤色成分を抽出
    red = int(hex_color[:2], base=16)
    # 255 で割って 0.0 から 1.0 の間の数値を取得
    srgb_red = red / 255
    linear_red = convert_srgb_to_linear_rgb(srgb_red)

    # 緑色成分を抽出
    green = int(hex_color[2:4], base=16)
    # 255 で割って 0.0 から 1.0 の間の数値を取得
    srgb_green = green / 255
    linear_green = convert_srgb_to_linear_rgb(srgb_green)

    # 青色成分を抽出
    blue = int(hex_color[4:6], base=16)
    # 255 で割って 0.0 から 1.0 の間の数値を取得
    srgb_blue = blue / 255
    linear_blue = convert_srgb_to_linear_rgb(srgb_blue)

    return tuple([linear_red, linear_green, linear_blue, 1.0])


# sRGBからリニアRGBへ変換する関数
def convert_srgb_to_linear_rgb(srgb_color_component: float) -> float:
    """
    sRGBからリニアRGBへの変換
    参照:https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)

    return linear_color_component


hex_color = "#FFD43B"
rgba_color = hex_color_to_rgba(hex_color)


# シーンに平面を追加
bpy.ops.mesh.primitive_plane_add()

# 新しいマテリアルの作成
material = bpy.data.materials.new(name=f"hex_color_{hex_color}")
material.diffuse_color = rgba_color

# オブジェクトにマテリアルを追加
bpy.context.active_object.data.materials.append(material)
