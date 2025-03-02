import bpy


class SimpleOperator(bpy.types.Operator):
    """This is a the doc"""

    bl_idname = "object.simple_operator"
    bl_label = "Simple Operator"

    def execute(self, context):
        # print("Operator executed")
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.object.modifier_add(type="EDGE_SPLIT")
        bpy.ops.object.modifier_add(type="DISPLACE")
        bpy.ops.object.modifier_add(type="SOLIDIFY")
        bpy.context.object.modifiers["Solidify"].thickness = 0.1
        return {"FINISHED"}


bpy.utils.register_class(SimpleOperator)
