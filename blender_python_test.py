import random
import math

import bpy


def scene_clear():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def add_cube(name,bevel=False):
    x = random.randint(-10, 10)
    y = random.randint(-10, 10)
    z = random.randint(-10, 10)

    degree_X = random.randint(0, 90)
    degree_Y = random.randint(0, 90)
    degree_Z = random.randint(0, 90)

    radians_X = math.radians(degree_X)
    radians_Y = math.radians(degree_Y)
    radians_Z = math.radians(degree_Z)

    bpy.ops.mesh.primitive_cube_add(
        location=(x, y, z), 
        rotation=(radians_X, radians_Y, radians_Z)
    )
    
    obj= bpy.context.active_object
    obj.name = name
    
    if bevel:
        bpy.ops.object.modifier_add(type='BEVEL')    


scene_clear()

add_cube("Cube_1")
add_cube("Cube_2",True)
add_cube("Cube_3")
add_cube("Cube_4",True)
