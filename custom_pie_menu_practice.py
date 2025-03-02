bl_info = {
    "name": "Pie Menu: Example",
    "description": "Description of this addon",
    "author": "Authors name",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Development",
}


import bpy
from bpy.types import Menu


def add_subdivide_modifier(subdivide_viewport_levels, subdivide_render_levels):
    obj = bpy.context.active_object

    # アクティブなオブジェクトがなかった場合
    if obj is None:
        print("Warning: no active object")
        return

    # アクティブなオブジェクトがメッシュでなかった場合
    if obj.type != "MESH":
        print("Warning: the active object need to be a mesh")
        return

    # 細分化モディファイアを追加
    bpy.ops.object.modifier_add(type="SUBSURF")
    bpy.context.object.modifiers["Subdivision"].levels = subdivide_viewport_levels
    bpy.context.object.modifiers["Subdivision"].render_levels = subdivide_render_levels


class MESH_OT_add_subdivide_mod(bpy.types.Operator):
    bl_idname = "mesh.add_subdivide_mod"
    bl_label = "Add Subdivision Surf Modifier to the Active Mesh Object"
    bl_options = {"REGISTER", "UNDO"}

    # 細分化モディファイアのビューポートプロパティ
    subdivide_viewport_lvl: bpy.props.IntProperty(
        name="Subdivision Viewport",
        default=1,
        min=1,
        max=3,
        description="The Subdivision Levels applied the Viewport",
    )

    # 細分化モディファイアのレンダープロパティ
    subdivide_render_lvl: bpy.props.IntProperty(
        name="Subdivide Render",
        default=3,
        min=3,
        max=7,
        description="The Subdivision Levels applied during the Viewport ",
    )

    # 実行処理
    def execute(self, context):

        add_subdivide_modifier(subdivide_viewport_levels=3, subdivide_render_levels=5)

        return {"FINISHED"}


class VIEW3D_MT_PIE_template(Menu):
    bl_label = "Pie Menu: Example"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        # Pieメニューの列を作成
        column = pie.split().column()
        # メッシュ追加操作
        column.operator("mesh.primitive_torus_add", text="Add Torus", icon="MESH_TORUS")
        column.operator("mesh.primitive_plane_add", text="Add Plane", icon="MESH_PLANE")

        column = pie.split().column()
        column.operator(
            "mesh.add_subdivide_mod", text="Add Subdivision Mod", icon="MOD_SUBSURF"
        )
        column.operator("object.shade_smooth", text="Shade Smooth", icon="MOD_SMOOTH")

        # bpy.ops.mesh.primitive_plane_add(
        #     size=2,
        #     enter_editmode=False,
        #     align="WORLD",
        #     location=(0, 0, 0),
        #     scale=(1, 1, 1),
        # )
        # bpy.ops.mesh.primitive_torus_add(
        #     align="WORLD",
        #     location=(0, 0, 0),
        #     rotation=(0, 0, 0),
        #     major_radius=1,
        #     minor_radius=0.25,
        #     abso_major_rad=1.25,
        #     abso_minor_rad=0.75,
        # )


global_addon_keymaps = []


# Blenderへのクラス登録関数
def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_template)
    bpy.utils.register_class(MESH_OT_add_subdivide_mod)

    # キーマップ登録のコード
    window_manager = bpy.context.window_manager
    # アドオン用のキーマップが登録されていなかった場合
    if window_manager.keyconfigs.addon:
        # どのエディターで使うキーマップかを定義
        keymap = window_manager.keyconfigs.addon.keymaps.new(
            "3D View", space_type="VIEW_3D"
        )

        # 使用するボタンの定義
        keymap_item = keymap.keymap_items.new(
            "wm.call_menu_pie", "A", "PRESS", ctrl=True, alt=True
        )
        # キーマップでアドオンの呼び出し
        keymap_item.properties.name = "VIEW3D_MT_PIE_template"

        # キーマップへの登録（リストに追加）
        global_addon_keymaps.append((keymap, keymap_item))


# Blenderからの登録解除関数
def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_template)
    bpy.utils.unregister_class(MESH_OT_add_subdivide_mod)

    # キーマップ解除のコード
    window_manager = bpy.context.window_manager
    # キーマップが登録されているかの確認
    if window_manager and window_manager.keyconfigs and window_manager.keyconfigs.addon:
        # 登録されているキーマップを全てチェック
        for keymap, keymap_item in global_addon_keymaps:
            # キーマップを解除
            keymap.keymap_items.remove(keymap_item)

    # キーマップのリストを空にする
    global_addon_keymaps.clear()


if __name__ == "__main__":
    register()

    bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_template")
