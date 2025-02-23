import bpy


def scene_clear():
    """シーンをクリアする"""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


scene_clear()


def create_tree(x, y, is_pine=False):
    """通常の木または松の木を作成し、市松模様に並べる"""

    if is_pine:
        # 松の木の幹
        pine_trunk_material = bpy.data.materials.new(name="Pine_Trunk")
        pine_trunk_material.diffuse_color = (0.36, 0.22, 0.05, 1)
        bpy.ops.mesh.primitive_cone_add(radius1=0.2, depth=1)
        pine_trunk = bpy.context.active_object
        pine_trunk.location = (x, y, 0.5)
        pine_trunk.data.materials.append(pine_trunk_material)

        # 松の木の葉（3段）
        pine_crown_material = bpy.data.materials.new(name="Pine_Crown")
        pine_crown_material.diffuse_color = (0.53, 0.59, 0.44, 1)

        for i in range(3):
            bpy.ops.mesh.primitive_cone_add(radius1=0.5, depth=1)
            pine_crown = bpy.context.active_object
            pine_crown.location = (x, y, 0.8 + i * 0.5)
            pine_crown.data.materials.append(pine_crown_material)

    else:
        # 通常の木の幹
        trunk_material = bpy.data.materials.new(name="Trunk")
        trunk_material.diffuse_color = (0.16, 0.075, 0.025, 1)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1)
        trunk = bpy.context.active_object
        trunk.location = (x, y, 0.5)
        trunk.data.materials.append(trunk_material)

        # 通常の木の葉
        tree_crown_material = bpy.data.materials.new(name="Tree_Crown")
        tree_crown_material.diffuse_color = (0, 1, 0, 1)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.8)
        tree_crown = bpy.context.active_object
        tree_crown.location = (x, y, 1)
        tree_crown.data.materials.append(tree_crown_material)


# 木を市松模様に並べる
for i in range(6):
    for j in range(6):
        create_tree(i * 2, j * 2, is_pine=(i + j) % 2 == 1)
