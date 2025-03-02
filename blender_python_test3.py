import bpy
import random


# class MoveObjectOperator(bpy.types.Operator):
#     """Move Selected Object Along X-Axis"""

#     bl_idname = "object.move_x"
#     bl_label = "Move Object Along X-Axis"

#     def execute(self, context):
#         obj = context.active_object
#         if not obj:
#             self.report({"WARNING"}, "No active object found")
#             return {"FINISHED"}

#         obj.location.x += 2
#         self.report({"INFO"}, "Object moved by 2 units on X-axis")

#         return {"FINISHED"}


# bpy.utils.register_class(MoveObjectOperator)


# class AddLightsOperator(bpy.types.Operator):
#     """Add 3 Lights Around the Active Object"""

#     bl_idname = "object.add_light"
#     bl_label = "Add Lights Around Object"

#     def execute(self, context):
#         obj = context.active_object
#         if not obj:
#             self.report({"WARNING"}, "No active selected object")
#             return {"CANCELLED"}

#         positions = {
#             (obj.location.x + 3, obj.location.y, obj.location.z + 2),
#             (obj.location.x - 3, obj.location.y + 3, obj.location.z + 2),
#             (obj.location.x, obj.location.y - 3, obj.location.z + 2),
#         }

#         index = 0
#         for pos in positions:
#             index += 1
#             bpy.ops.object.light_add()
#             light_obj = context.active_object
#             light_obj.location = pos

#         self.report({"INFO"}, "Added 3 lights,around the object")
#         return {"FINISHED"}


# bpy.utils.register_class(AddLightsOperator)


class AddCameraTrackObject(bpy.types.Operator):
    """Add Camera Track to Selected Active Object"""

    bl_idname = "object.add_camera"
    bl_label = "Add Camera Track to Object"

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({"WARNING"}, "No active selected object")
            return {"CANCELLED"}

        bpy.ops.object.camera_add()
        camera_obj = context.active_object
        camera_obj.location = (
            random.randint(-3, 3),
            random.randint(-3, 3),
            random.randint(-3, 3),
        )
        bpy.ops.object.constraint_add(type="TRACK_TO")
        context.object.constraints["Track To"].target = obj

        self.report({"INFO"}, "Added camera track to object")
        return {"FINISHED"}


bpy.utils.register_class(AddCameraTrackObject)
