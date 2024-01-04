import bpy
import bpy_types

from .merge_processor import main_merge_objects


class Exporter :
    """ Preprocess and Export file """
    def __init__(self) -> None:
        pass

    def export(self, context : bpy_types.Context, settings : bpy.types.AnyType) -> None:
        export_settings = settings.export_settings

        # Check file path error
        if settings.export_settings == "" :
            return

        # Merge objects
        main_merge_objects(context, export_settings.collections)

        # Export to fbx
