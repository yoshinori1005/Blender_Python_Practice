import bpy
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
output_node.location = (400, 0)

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
