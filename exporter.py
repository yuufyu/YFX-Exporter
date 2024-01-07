import bpy
import bpy_types

from .merge_processor import main_merge_objects


class ExportError(Exception):
    pass


class Exporter:
    """Preprocess and Export file"""

    def __init__(self) -> None:
        pass

    def export(self, context: bpy_types.Context, settings: bpy.types.AnyType) -> None:
        export_settings = settings.export_settings

        # Check file path error
        if export_settings.export_path == "":
            error_msg = "Invalid path"
            raise ExportError(error_msg)

        # Merge objects
        if len(export_settings.collections) > 0:
            collection_names = {
                c.collection_ptr.name for c in export_settings.collections
            }
            main_merge_objects(context, collection_names)

        # Export to fbx
        fbx_export_settings = export_settings.fbx_export_settings
        keyargs_dict = {
            key: getattr(fbx_export_settings, key, None)
            for key in fbx_export_settings.__annotations__
        }
        bpy.ops.export_scene.fbx(
            filepath=export_settings.export_path,
            **keyargs_dict,
        )
