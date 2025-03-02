bl_info = {
    "name": "Custom Panel Practice",
    "description": "Development practice for custom panels.",
    "author": "Yoshinori Serizawa",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "3D Viewport > Sidebar > My Custom Panel CategoryView3D",
    "warning": "This addon is still in development.",
    "category": "Object",
}


import bpy


def add_wireframe(thickness, offset):
    bpy.ops.object.modifier_add(type="WIREFRAME")
    bpy.context.object.modifiers["Wireframe"].thickness = thickness
    bpy.context.object.modifiers["Wireframe"].offset = offset


class VIEW3D_PT_add_wireframe(bpy.types.Operator):
    """Add Wireframe Modifier to selected object"""

    bl_idname = "mesh.add_wireframe"
    bl_label = "Add Wireframe Modifier"
    bl_options = {"REGISTER", "UNDO"}

    thickness: bpy.props.FloatProperty(
        name="Thickness",
        default=0.01,
    )

    offset: bpy.props.FloatProperty(
        name="Offset",
        default=0.0,
    )

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != "MESH":
            self.report({"WARNING"}, "Select the mesh object")
            return {"CANCELLED"}

        for mod in obj.modifiers:
            if mod.type == "WIREFRAME":
                self.report({"INFO"}, "Already has wireframe modifier added")
                return {"CANCELLED"}

        add_wireframe(self.thickness, self.offset)

        self.report({"INFO"}, "Add Wireframe Modifier")
        return {"FINISHED"}


def add_subdivision(suvdiv_viewport, subdiv_render_levels):
    bpy.ops.object.modifier_add(type="SUBSURF")
    bpy.context.object.modifiers["Subdivision"].levels = suvdiv_viewport
    bpy.context.object.modifiers["Subdivision"].render_levels = subdiv_render_levels


class VIEW3D_PT_add_subdivide(bpy.types.Operator):
    """Add Subdivision Modifier to selected object"""

    bl_idname = "mesh.add_subdivision"
    bl_label = "Add Subdivision Modifier"
    bl_options = {"REGISTER", "UNDO"}

    viewport_level: bpy.props.IntProperty(
        name="Viewport Level",
        default=1,
        min=1,
        max=6,
    )

    render_level: bpy.props.IntProperty(
        name="Render Level",
        default=2,
        min=2,
        max=6,
    )

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != "MESH":
            self.report({"WARNING"}, "Select the mesh object")
            return {"CANCELLED"}

        add_subdivision(self.viewport_level, self.render_level)

        self.report({"INFO"}, "Add Subdivision Modifier")
        return {"FINISHED"}


class VIEW3D_PT_flip_normal(bpy.types.Operator):
    """Detect and fix inverted faces of selected objects"""

    bl_idname = "object.flip_normals_operator"
    bl_label = "Fix inverted faces of selected object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != "MESH":
            self.report({"WARNING"}, "Select the mesh object")
            return {"CANCELLED"}

        # Switch to mesh edit mode
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")

        self.report({"INFO"}, "Fixed the inverted side")
        return {"FINISHED"}


class VIEW3D_PT_clean_up_mesh(bpy.types.Operator):
    """Remove orphaned mesh data"""

    bl_idname = "mesh.clean_up"
    bl_label = "Clean Mesh Data"

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != "MESH":
            self.report({"WARNING"}, "Select the mesh object")
            return {"CANCELLED"}

        # 現在のモードを取得
        current_mode = obj.mode

        # オブジェクトモードの場合編集モードへ
        if current_mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")

        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.delete_loose()
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")

        # self.report({"INFO"}, "Cleaned up orphaned mesh data")
        return {"FINISHED"}


class VIEW3D_PT_scene_clear(bpy.types.Operator):
    """All Objects in the Scene will be Deleted"""

    bl_idname = "view3d.scene_clear"
    bl_label = "Clear Scene"

    def execute(self, context):
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

        return {"FINISHED"}


class VIEW3D_PT_add_mesh_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CP Practice"
    bl_label = "Add Primitive Mesh"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        """define the layout of the panel"""
        layout = self.layout.row()
        layout.operator("mesh.primitive_cube_add", text="Add Cube")
        layout = self.layout.row()
        layout.operator("mesh.primitive_ico_sphere_add", text="Add IcoSphere")
        layout = self.layout.row()
        layout.operator("mesh.primitive_uv_sphere_add", text="Add UVSphere")
        layout = self.layout.row()
        layout.operator("mesh.primitive_monkey_add", text="Add Monkey")


class VIEW3D_PT_add_modifier_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CP Practice"
    bl_label = "Add Modifier"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout.row()
        layout.operator("object.shade_smooth", text="Shade Smooth")
        layout = self.layout.row()
        layout.operator("mesh.add_wireframe", text="Wireframe")
        layout = self.layout.row()
        layout.operator("mesh.add_subdivision", text="Subdivision")


class VIEW3D_PT_mesh_optimization_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CP Practice"
    bl_label = "Mesh Optimization"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout.row()
        layout.operator("object.flip_normals_operator", text="Flip Normal")
        layout = self.layout.row()
        layout.operator("mesh.clean_up", text="Mesh Clean")


class VIEW3D_PT_scene_clear_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CP Practice"
    bl_label = "Scene Clear"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout.row()
        layout.operator("view3d.scene_clear", text="Clear Scene")


def register():
    bpy.utils.register_class(VIEW3D_PT_add_mesh_panel)
    bpy.utils.register_class(VIEW3D_PT_add_modifier_panel)
    bpy.utils.register_class(VIEW3D_PT_mesh_optimization_panel)
    bpy.utils.register_class(VIEW3D_PT_scene_clear_panel)
    bpy.utils.register_class(VIEW3D_PT_add_wireframe)
    bpy.utils.register_class(VIEW3D_PT_add_subdivide)
    bpy.utils.register_class(VIEW3D_PT_flip_normal)
    bpy.utils.register_class(VIEW3D_PT_clean_up_mesh)
    bpy.utils.register_class(VIEW3D_PT_scene_clear)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_add_mesh_panel)
    bpy.utils.unregister_class(VIEW3D_PT_add_modifier_panel)
    bpy.utils.unregister_class(VIEW3D_PT_mesh_optimization_panel)
    bpy.utils.unregister_class(VIEW3D_PT_scene_clear_panel)
    bpy.utils.unregister_class(VIEW3D_PT_add_wireframe)
    bpy.utils.unregister_class(VIEW3D_PT_add_subdivide)
    bpy.utils.unregister_class(VIEW3D_PT_flip_normal)
    bpy.utils.unregister_class(VIEW3D_PT_clean_up_mesh)
    bpy.utils.unregister_class(VIEW3D_PT_scene_clear)


if __name__ == "__main__":
    register()
