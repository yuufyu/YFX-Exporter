import bpy
import bpy_types


def show_popup_message(
    context: bpy_types.Context,
    message: str = "",
    title: str = "Message Box",
    icon: str = "INFO",
) -> None:
    def draw(self: bpy.types.Panel, context: bpy_types.Context) -> None:
        self.layout.label(text=message)

    context.window_manager.popup_menu(draw, title=title, icon=icon)


class View3dSidePanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "YFX"


class YFX_EXPORTER_MT_collection_list_context(bpy.types.Menu):
    bl_label = "Collection list context menu"

    def draw(self, context: bpy_types.Context) -> None:
        layout = self.layout
        layout.separator()
        layout.operator("yfx_exporter.clear_list", icon="X")


class YFX_EXPORTER_UL_colllection(bpy.types.UIList):
    def draw_item(
        self,
        context: bpy_types.Context,
        layout: bpy.types.UILayout,
        data: bpy.types.AnyType,
        item: bpy.types.AnyType,
        icon: int,
        active_data: bpy.types.AnyType,
        active_propname: str,
        index: int,
    ) -> None:
        row = layout.row()
        row.prop(
            item.collection_ptr,
            "name",
            text="",
            emboss=False,
            icon="OUTLINER_COLLECTION",
        )

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> None:
        pass


class YFX_EXPORTER_PT_export_panel(View3dSidePanel, bpy.types.Panel):
    bl_label = "YFX Exporter"
    bl_idname = "YFX_EXPORTER_PT_export_panel"

    def draw(self, context: bpy_types.Context) -> None:
        layout = self.layout
        scn = context.scene
        settings = scn.yfx_exporter_settings.export_settings

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.scale_y = 1.5
        row.operator("yfx_exporter.export_fbx", text="Export FBX", icon="CUBE")

        row = layout.row(align=True)
        if settings.export_path == "":
            row.alert = True

        row.prop(settings, "export_path", text="")

        row = row.row(align=True)
        row.operator(
            "yfx_exporter.select_file",
            text="",
            icon="FILE_FOLDER",
        ).filepath = settings.export_path


class YFX_EXPORTER_PT_fbx_export_settings_main_panel(View3dSidePanel, bpy.types.Panel):
    bl_label = "FBX settings"
    bl_idname = "YFX_EXPORTER_PT_fbx_export_settings_main_panel"
    bl_parent_id = "YFX_EXPORTER_PT_export_panel"
    bl_options = {"DEFAULT_CLOSED"}  # noqa: RUF012

    def draw(self, context: bpy_types.Context) -> None:
        scn = context.scene
        settings = scn.yfx_exporter_settings
        fbx_export_settings = settings.export_settings.fbx_export_settings

        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        row = layout.row(align=True)
        row.prop(fbx_export_settings, "path_mode")
        sub = row.row(align=True)
        sub.enabled = fbx_export_settings.path_mode == "COPY"
        sub.prop(
            fbx_export_settings,
            "embed_textures",
            text="",
            icon="PACKAGE" if fbx_export_settings.embed_textures else "UGLYPACKAGE",
        )


class YFX_EXPORTER_PT_fbx_export_settings_include_panel(
    View3dSidePanel,
    bpy.types.Panel,
):
    bl_label = "Include"
    bl_idname = "YFX_EXPORTER_PT_fbx_export_settings_include_panel"
    bl_parent_id = "YFX_EXPORTER_PT_fbx_export_settings_main_panel"

    def draw(self, context: bpy_types.Context) -> None:
        scn = context.scene
        settings = scn.yfx_exporter_settings
        fbx_export_settings = settings.export_settings.fbx_export_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.column().prop(fbx_export_settings, "object_types")
        layout.prop(fbx_export_settings, "use_custom_props")


class YFX_EXPORTER_PT_fbx_export_settings_transform_panel(
    View3dSidePanel,
    bpy.types.Panel,
):
    bl_label = "Transform"
    bl_idname = "YFX_EXPORTER_PT_fbx_export_settings_transform_panel"
    bl_parent_id = "YFX_EXPORTER_PT_fbx_export_settings_main_panel"

    def draw(self, context: bpy_types.Context) -> None:
        scn = context.scene
        settings = scn.yfx_exporter_settings
        fbx_export_settings = settings.export_settings.fbx_export_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(fbx_export_settings, "global_scale")
        layout.prop(fbx_export_settings, "apply_scale_options")

        layout.prop(fbx_export_settings, "axis_forward")
        layout.prop(fbx_export_settings, "axis_up")

        layout.prop(fbx_export_settings, "apply_unit_scale")
        layout.prop(fbx_export_settings, "use_space_transform")
        row = layout.row()
        row.prop(fbx_export_settings, "bake_space_transform")
        row.label(text="", icon="ERROR")


class YFX_EXPORTER_PT_fbx_export_settings_geometry_panel(
    View3dSidePanel,
    bpy.types.Panel,
):
    bl_label = "Geometry"
    bl_idname = "YFX_EXPORTER_PT_fbx_export_settings_geometry_panel"
    bl_parent_id = "YFX_EXPORTER_PT_fbx_export_settings_main_panel"

    def draw(self, context: bpy_types.Context) -> None:
        scn = context.scene
        settings = scn.yfx_exporter_settings
        fbx_export_settings = settings.export_settings.fbx_export_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(fbx_export_settings, "mesh_smooth_type")
        layout.prop(fbx_export_settings, "use_subsurf")
        layout.prop(fbx_export_settings, "use_mesh_modifiers")
        layout.prop(fbx_export_settings, "use_mesh_edges")
        layout.prop(fbx_export_settings, "use_triangles")
        sub = layout.row()
        # ~ sub.enabled = operator.mesh_smooth_type in {'OFF'}
        sub.prop(fbx_export_settings, "use_tspace")
        layout.prop(fbx_export_settings, "colors_type")
        layout.prop(fbx_export_settings, "prioritize_active_color")


class YFX_EXPORTER_PT_fbx_export_settings_armature_panel(
    View3dSidePanel,
    bpy.types.Panel,
):
    bl_label = "Armature"
    bl_idname = "YFX_EXPORTER_PT_fbx_export_settings_armature_panel"
    bl_parent_id = "YFX_EXPORTER_PT_fbx_export_settings_main_panel"

    def draw(self, context: bpy_types.Context) -> None:
        scn = context.scene
        settings = scn.yfx_exporter_settings
        fbx_export_settings = settings.export_settings.fbx_export_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(fbx_export_settings, "primary_bone_axis")
        layout.prop(fbx_export_settings, "secondary_bone_axis")
        layout.prop(fbx_export_settings, "armature_nodetype")
        layout.prop(fbx_export_settings, "use_armature_deform_only")
        layout.prop(fbx_export_settings, "add_leaf_bones")


class YFX_EXPORTER_PT_fbx_export_settings_bake_animation_panel(
    View3dSidePanel,
    bpy.types.Panel,
):
    bl_label = "Bake Animation"
    bl_idname = "YFX_EXPORTER_PT_fbx_export_settings_bake_animation_panel"
    bl_parent_id = "YFX_EXPORTER_PT_fbx_export_settings_main_panel"

    def draw_header(self, context: bpy_types.Context) -> None:
        scn = context.scene
        settings = scn.yfx_exporter_settings
        fbx_export_settings = settings.export_settings.fbx_export_settings

        self.layout.prop(fbx_export_settings, "bake_anim", text="")

    def draw(self, context: bpy_types.Context) -> None:
        scn = context.scene
        settings = scn.yfx_exporter_settings
        fbx_export_settings = settings.export_settings.fbx_export_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.enabled = fbx_export_settings.bake_anim
        layout.prop(fbx_export_settings, "bake_anim_use_all_bones")
        layout.prop(fbx_export_settings, "bake_anim_use_nla_strips")
        layout.prop(fbx_export_settings, "bake_anim_use_all_actions")
        layout.prop(fbx_export_settings, "bake_anim_force_startend_keying")
        layout.prop(fbx_export_settings, "bake_anim_step")
        layout.prop(fbx_export_settings, "bake_anim_simplify_factor")


class YFX_EXPORTER_PT_collection_panel(View3dSidePanel, bpy.types.Panel):
    bl_label = "Merge Collections"
    bl_idname = "YFX_EXPORTER_PT_collection_panel"
    bl_parent_id = "YFX_EXPORTER_PT_export_panel"

    def draw(self, context: bpy_types.Context) -> None:
        layout = self.layout
        scn = context.scene
        settings = scn.yfx_exporter_settings.export_settings

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator_menu_enum(
            "YFX_EXPORTER_OT_add_collection",
            "user_collections",
            text="Add Collection",
            icon="ADD",
        )

        row = layout.row()
        row.template_list(
            "YFX_EXPORTER_UL_colllection",
            "",
            settings,
            "collections",
            settings,
            "collection_index",
            rows=5,
        )

        col = row.column(align=True)
        col.operator("yfx_exporter.list_action", icon="X", text="").action = "REMOVE"
        col.separator()
        col.operator("yfx_exporter.list_action", icon="TRIA_UP", text="").action = "UP"
        col.operator(
            "yfx_exporter.list_action",
            icon="TRIA_DOWN",
            text="",
        ).action = "DOWN"


class YFX_EXPORTER_PT_collection_setting_panel(View3dSidePanel, bpy.types.Panel):
    bl_label = "Collection Settings"
    bl_idname = "YFX_EXPORTER_PT_collection_setting_panel"
    bl_parent_id = "YFX_EXPORTER_PT_collection_panel"

    def draw(self, context: bpy_types.Context) -> None:
        layout = self.layout
        scn = context.scene
        settings = scn.yfx_exporter_settings.export_settings

        idx = settings.collection_index
        try:
            item = settings.collections[idx]
        except IndexError:
            pass
        else:
            row = layout.row(align=True)
            col = row.column(align=True)

            if False:
                col.box().label(text="error", icon="ERROR")
            else:
                col.prop(
                    item.transform_settings,
                    "apply_all_transform",
                    text="Apply All Transform",
                )

                col.separator()

                col.prop(
                    item.vertex_group_settings,
                    "delete_vertex_group",
                    text="Delete Unused Vertex Group",
                )

                col.separator()

                col.prop(
                    item.shapekey_settings,
                    "separate_shapekey",
                    text="Separate Shapekeys L/R",
                )
                col.prop(
                    item.shapekey_settings,
                    "separate_mmd_shapekey",
                    text="Separate MMD Shapekeys",
                )

                col.separator()

                col.prop(
                    item.warning_settings,
                    "check_warnings",
                    text="Check for Warnings",
                )

                if item.warning_settings.check_warnings:
                    col.prop(
                        item.warning_settings,
                        "check_armature_exist",
                        text="Check if Armature Exists",
                    )
                    col.prop(
                        item.warning_settings,
                        "check_vertices_with_no_weights",
                        text="Check Vertices with No Weights",
                    )
