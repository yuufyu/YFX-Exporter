import bpy


class YFX_EXPORTER_PG_warning_settings(bpy.types.PropertyGroup):
    check_warnings : bpy.props.BoolProperty(default = False) # WIP
    check_armature_exist : bpy.props.BoolProperty(default = True)
    check_vertices_with_no_weights : bpy.props.BoolProperty(default = True)

class YFX_EXPORTER_PG_shapekey_settings(bpy.types.PropertyGroup):
    separate_shapekey : bpy.props.BoolProperty(default = True)
    separate_mmd_shapekey : bpy.props.BoolProperty(default = True)

class YFX_EXPORTER_PG_transform_settings(bpy.types.PropertyGroup):
    apply_transform : bpy.props.BoolProperty(default = True)

class YFX_EXPORTER_PG_vertex_group_settings(bpy.types.PropertyGroup):
    delete_vertex_group : bpy.props.BoolProperty(default = True)

class YFX_EXPORTER_PG_collection_settings(bpy.types.PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    collection_ptr: bpy.props.PointerProperty(
        name="Collection",
        type=bpy.types.Collection)
    transform_settings : bpy.props.PointerProperty(
        type = YFX_EXPORTER_PG_transform_settings)
    shapekey_settings : bpy.props.PointerProperty(
        type = YFX_EXPORTER_PG_shapekey_settings)
    warning_settings : bpy.props.PointerProperty(
        type = YFX_EXPORTER_PG_warning_settings)
    vertex_group_settings : bpy.props.PointerProperty(
        type = YFX_EXPORTER_PG_vertex_group_settings)

class YFX_EXPORTER_PG_export_settings(bpy.types.PropertyGroup):
    collections : bpy.props.CollectionProperty(
        type = YFX_EXPORTER_PG_collection_settings)
    collection_index : bpy.props.IntProperty()
    export_path : bpy.props.StringProperty()
    temp_path : bpy.props.StringProperty(subtype = "DIR_PATH")

class YFX_EXPORTER_PG_settings(bpy.types.PropertyGroup):
    export_settings : bpy.props.PointerProperty(type = YFX_EXPORTER_PG_export_settings)
    is_subprocess : bpy.props.BoolProperty()

def register() -> None:
    bpy.types.Scene.yfx_exporter_settings = bpy.props.PointerProperty(
        type = YFX_EXPORTER_PG_settings)

def unregister() -> None:
    del bpy.types.Scene.yfx_exporter_settings
