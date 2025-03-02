import bpy
import random


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


clear_scene()

# used_materials = set()
# for obj in bpy.context.selected_objects:
#     for mat in obj.data.materials:
#         used_materials.add(mat.name)

# all_materials = set()
# for mat in bpy.data.materials:
#     all_materials.add(mat.name)

# unused_materials = all_materials - used_materials
# print(f"Unused materials: + {unused_materials}")

# def get_object_dimensions(obj_name):
#     obj = bpy.data.objects.get(obj_name)
#     if obj:
#         return obj.dimensions.x, obj.dimensions.y, obj.dimensions.z
#     else:
#         return None

# dimensions=get_object_dimensions("Cube")


# def list_unique_modifiers():
#     unique_modifier = set()
#     for obj in bpy.context.scene.objects:
#         for mod in obj.modifiers:
#             unique_modifier.add(mod.type)

#     print(f"Unique modifier types in the scene {unique_modifier}")


# list_unique_modifiers()


# def get_random_xyz(range_tuple):
#     x = random.randint(range_tuple[0], range_tuple[1])
#     y = random.randint(range_tuple[0], range_tuple[1])
#     z = random.randint(range_tuple[0], range_tuple[1])
#     return (x, y, z)


# random_range = (-5, 3)
# random_location = get_random_xyz(random_range)
# bpy.ops.mesh.primitive_cube_add(location=random_location)
# print(f"Added cube at location {random_location}")


def add_random_colored_light(location=(0, 0, 0)):
    colors = [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 1.0, 0.0),
        (0.0, 1.0, 1.0),
        (1.0, 0.0, 1.0),
        (1.0, 1.0, 1.0),
    ]

    random_color = random.choice(colors)

    bpy.ops.object.light_add(type="POINT", location=location)
    obj = bpy.context.active_object
    obj.data.color = random_color


add_random_colored_light((1, 1, 1))
