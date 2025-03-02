import bpy
import random


# 基本のオペレーター作成
class SimpleOperator(bpy.types.Operator):
    """Add Modifier"""

    bl_idname = "mesh.add_modifier"
    bl_label = "Add Modifier"

    def execute(self, context):

        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.object.modifier_add(type="SUBSURF")
        bpy.ops.object.modifier_add(type="WIREFRAME")
        bpy.context.object.modifiers["Wireframe"].thickness = 0.05
        return {"FINISHED"}


bpy.utils.register_class(SimpleOperator)


# オブジェクトの移動オペレーター
class MoveObjectOperator(bpy.types.Operator):
    #     """Random Move Selected Object Along Y-Axis"""

    bl_idname = "object.move_random_y"
    bl_label = "Random Move Object Along Y-Axis"

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({"WARNING"}, "オブジェクトがありません")
            return {"CANCELLED"}

        obj.location = (0, random.randint(-5, 5), 0)
        self.report({"INFO"}, "オブジェクトを移動させました")
        return {"FINISHED"}


bpy.utils.register_class(MoveObjectOperator)


# オブジェクトのスケール変更
class ScaleChangeObject(bpy.types.Operator):
    """Scale Change Selected Object"""

    bl_idname = "object.scale_change"
    bl_label = "Scale Change Selected Object"

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({"WARNING"}, "オブジェクトがありません")
            return {"CANCELLED"}

        obj.scale *= 1.5
        self.report({"INFO"}, "Object scaled by 1.5")
        return {"FINISHED"}


bpy.utils.register_class(ScaleChangeObject)


# ライトを追加し、ランダムな色を設定する
class AddRandomColorLights(bpy.types.Operator):
    """Add 3 Random Color Lights Around the Active Object"""

    bl_idname = "object.add_random_color_light"
    bl_label = "Add Random Color Lights Around Object"

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({"WARNING"}, "No active selected object")
            return {"CANCELLED"}

        positions = {
            (random.randint(-3, 3), random.randint(-3, 3), obj.location.z + 2),
            (random.randint(-3, 3), random.randint(-3, 3), obj.location.z + 2),
            (random.randint(-3, 3), random.randint(-3, 3), obj.location.z + 2),
        }

        for pos in positions:
            bpy.ops.object.light_add(type="POINT", location=pos)
            light_obj = context.active_object.data
            light_obj.color = (random.random(), random.random(), random.random())

        self.report({"INFO"}, "Added 3 random colored lights")
        return {"FINISHED"}


bpy.utils.register_class(AddRandomColorLights)


# カメラを特定の位置に配置
class AddCameraOperator(bpy.types.Operator):
    """Add Camera in the scene"""

    bl_idname = "object.add_camera"
    bl_label = "Add Camera Scene"

    def execute(self, context):
        camera_obj = context.active_object
        if camera_obj:
            self.report({"WARNING"}, "This scene has Camera already")
            return {"CANCELLED"}

        bpy.ops.object.camera_add()
        camera_obj = context.active_object
        camera_obj.location = (0, -5, 3)
        camera_obj.rotation_euler = (0, 0, 0)

        self.report({"INFO"}, "Camera positioned at (0,-5,3)")
        return {"FINISHED"}


bpy.utils.register_class(AddCameraOperator)


# モディファイアの一喝削除
class ObjectRemoveModifier(bpy.types.Operator):
    """Selected Object Remove All Modifier"""

    bl_idname = "object.remove_all_modifier"
    bl_label = "Object Remove Modifier"

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({"WARNING"}, "No active selected object")
            return {"CANCELLED"}

        if obj.type != "MESH":
            self.report({"WARNING"}, "Select the mesh object")
            return {"CANCELLED"}

        if not obj.modifiers:
            self.report({"WARNING"}, "Selected object don't have Modifier")
            return {"CANCELLED"}

        obj.modifiers.clear()
        return {"FINISHED"}


bpy.utils.register_class(ObjectRemoveModifier)

# オブジェクトの複製
class ObjectDuplicate(bpy.types.Operator):
    """Object Duplicate Operation"""
    bl_idname="mesh.object_duplicate"
    bl_label="Object Duplicate"
    
    def execute(self, context):
        obj=context.active_object
        
        if not obj:
            self.report({"WARNING"},"No active selected object")
            return{"CANCELLED"}
        
        for i in range(3):
            new_obj=obj.copy()
            new_obj.location.x+=(i+1)*2
            context.collection.objects.link(new_obj)
        return {"FINISHED"}

bpy.utils.register_class(ObjectDuplicate)

# マテリアルをランダムに設定
class RandomMaterialSet(bpy.types.Operator):
    """Random Material Set to Selected Object"""
    bl_idname="object.random_material_set"
    bl_label="Random Material Set to Object"
    
    def execute(self, context):
        obj=context.active_object
        if not obj:
            self.report({"WARNING"},"No active selected object")
            return{"CANCELLED"}
        
        random_color_material=bpy.data.materials.new(name="Random Color Material")
        random_color_material.diffuse_color=(
            random.random(),
            random.random(),
            random.random(),1.0
            )
        obj.data.materials.append(random_color_material)
        
        self.report({"INFO"},"Applied random material")
        return {"FINISHED"}
bpy.utils.register_class(RandomMaterialSet)