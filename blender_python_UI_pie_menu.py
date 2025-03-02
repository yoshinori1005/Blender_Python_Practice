bl_info = {
    "name": "Pie Menu: Template",
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


class VIEW3D_MT_PIE_template(Menu):
    bl_label = "Select Mode"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # operator_enum は利用可能なすべてのオプションを円グラフに表示します
        # 演算子の列挙型を円グラフに表示します
        pie.operator_enum("mesh.select_mode", "type")


global_addon_keymaps = []


# Blenderへのクラス登録関数
def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_template)

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
