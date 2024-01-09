from typing import Generator

import bpy
import bpy_types

from .merge import merge_objects
from .modifier import main_apply_modifiers


def make_all_unlink() -> None:
    bpy.ops.object.duplicates_make_real(use_hierarchy=True)
    bpy.ops.object.make_local(type="ALL")
    bpy.ops.object.make_single_user(
        type="ALL",
        object=True,
        obdata=True,
        material=False,
        animation=False,
        obdata_animation=False,
    )


def apply_all_objects(context: bpy_types.Context) -> None:
    scn = context.scene

    bpy.ops.object.select_all(action="SELECT")
    make_all_unlink()

    for obj in scn.objects:
        if obj.visible_get():
            if obj.type in ("CURVE", "FONT", "SURFACE"):
                # Convert object to mesh
                context.view_layer.objects.active = obj
                bpy.ops.object.select_all(action="DESELECT")
                obj.select_set(state=True)
                bpy.ops.object.convert(target="MESH")

            if obj.type == "MESH":
                main_apply_modifiers(obj)


def get_merge_collections(
    collection_settings: dict,  # readonly
    parent_collection: bpy.types.Collection,
) -> Generator[bpy.types.AnyType, None, None]:
    name = parent_collection.name
    if name in collection_settings:
        # Ignore nested collections
        yield collection_settings[name]
    else:
        for child in parent_collection.children:
            yield from get_merge_collections(collection_settings, child)


class ExportError(Exception):
    pass


class Exporter:
    """Preprocess and Export file"""

    def __init__(self) -> None:
        pass

    def export(self, context: bpy_types.Context, settings: bpy.types.AnyType) -> None:
        scn = context.scene
        export_settings = settings.export_settings

        # Check file path error
        if export_settings.export_path == "":
            error_msg = "Invalid path"
            raise ExportError(error_msg)

        # Convert object to mesh and Apply modifiers
        apply_all_objects(context)

        # Merge objects
        collection_settings_dict = {
            c.collection_ptr.name: c for c in export_settings.collections
        }

        merge_collections = get_merge_collections(
            collection_settings_dict,
            scn.collection,
        )

        for c in merge_collections:
            merge_objects(context, c.collection_ptr)

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
