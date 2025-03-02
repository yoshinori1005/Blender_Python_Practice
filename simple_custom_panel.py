bl_info = {
    "name": "My Custom Panel",
    "description": "My custom operator buttons",
    "author": "Yoshinori Serizawa",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "3D Viewport > Sidebar > My Custom Panel Category",
    "warning": "This addon is still in development.",
    "category": "Development",
}


# Python に Blender の機能へのアクセスを許可する
import bpy


class VIEW3D_OT_scene_clear(bpy.types.Operator):
    """シーン内のオブジェクトを全て削除する"""

    bl_idname = "view3d.scene_clear"
    bl_label = "Clear Scene"

    def execute(self, context):
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

        return {"FINISHED"}


def add_subdiv_monkey_obj(size, suvdiv_viewport, subdiv_render_levels, shade_smooth):
    bpy.ops.mesh.primitive_monkey_add(size=size)

    bpy.ops.object.modifier_add(type="SUBSURF")
    bpy.context.object.modifiers["Subdivision"].levels = suvdiv_viewport
    bpy.context.object.modifiers["Subdivision"].render_levels = subdiv_render_levels

    if shade_smooth:
        bpy.ops.object.shade_smooth()


class MESH_OT_add_subdiv_monkey(bpy.types.Operator):
    """細分化とスムースシェードをかけたモンキーを新しく生成する"""

    bl_idname = "mesh.add_subdiv_monkey"
    bl_label = "Add Subdivided Monkey Mesh Object"
    bl_options = {"REGISTER", "UNDO"}

    mesh_size: bpy.props.FloatProperty(
        name="Size",
        default=2.0,
        description="The size of the monkey",
    )

    subdiv_viewport_lvl: bpy.props.IntProperty(
        name="Subdiv Viewport",
        default=1,
        min=1,
        max=3,
        description="The Subdivision Levels applied in the Viewport",
    )

    subdiv_render_lvl: bpy.props.IntProperty(
        name="Subdiv Render",
        default=3,
        min=3,
        max=7,
        description="The Subdivision Levels applied during the Render",
    )

    shade_smooth: bpy.props.BoolProperty(
        name="Shade Smooth",
        default=True,
        description="Apply Smooth Shading to the mesh",
    )

    def execute(self, context):

        add_subdiv_monkey_obj(
            self.mesh_size,
            self.subdiv_viewport_lvl,
            self.subdiv_render_lvl,
            self.shade_smooth,
        )

        return {"FINISHED"}


# クラスの名前のめい命名規則は「CATEGORY_PT_name」である必要がある
# この例では「VIEW3D_PT_my_custom_panel」
class VIEW3D_PT_my_custom_panel(bpy.types.Panel):
    # UI 内にパネルを追加する場所
    # 3D ビューポートの領域
    # 参照https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items)
    bl_space_type = "VIEW_3D"
    # パネルが表示される場所
    # サイドバーの領域
    # 参照https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#bpy.types.Panel.bl_region_type
    bl_region_type = "UI"

    # ラベルを追加する
    # UI に追加した時にサイドバー上に表示される名前
    bl_category = "My Custom Panel Category"
    # UI に追加した時にパネルの上部に表示される
    bl_label = "My Custom Panel Label"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        """パネルのレイアウトを定義する"""
        # 基本オブジェクトの追加
        row = self.layout.row()
        row.operator("mesh.primitive_cube_add", text="Add Cube")
        row = self.layout.row()
        row.operator("mesh.primitive_ico_sphere_add", text="Add IcoSphere")
        row = self.layout.row()
        row.operator("object.shade_smooth", text="Shade Smooth")

        # パネルの表示を分類するメソッド
        self.layout.separator()

        # モンキー追加
        row = self.layout.box()
        row.label(text="Add Subdivided Monkey")
        row.operator("mesh.add_subdiv_monkey", text="Add Subdivided Monkey")
        row=self.layout.row()
        row.operator("mesh.add_subdiv_monkey",text="Test Label")

        self.layout.separator()

        # シーン内のオブジェクトを全て削除
        row = self.layout.box()
        row.label(text="Clear Scene")
        row.operator("view3d.scene_clear", text="Scene Clear")


# パネルを Blender に登録する
def register():
    bpy.utils.register_class(VIEW3D_PT_my_custom_panel)
    bpy.utils.register_class(MESH_OT_add_subdiv_monkey)
    bpy.utils.register_class(VIEW3D_OT_scene_clear)


# パネルを Blender から登録解除する
def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_my_custom_panel)
    bpy.utils.unregister_class(MESH_OT_add_subdiv_monkey)
    bpy.utils.unregister_class(VIEW3D_OT_scene_clear)


# 登録する関数を呼び出す
if __name__ == "__main__":
    register()
