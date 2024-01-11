from typing import Generator

import bpy
import bpy_types

from .merge import merge_objects
from .modifier import main_apply_modifiers
from .shapekey import separate_shapekey_lr, sort_shapekey


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


def apply_constraints(obj: bpy.types.Object) -> None:
    names = [constraint.name for constraint in obj.constraints]
    for name in names:
        bpy.ops.constraint.apply(constraint=name)


def apply_all_objects(context: bpy_types.Context) -> None:
    scn = context.scene

    bpy.ops.object.select_all(action="SELECT")
    make_all_unlink()

    for obj in scn.objects:
        if obj.visible_get() and obj.type in ("CURVE", "FONT", "SURFACE", "MESH"):
            context.view_layer.objects.active = obj
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(state=True)

            apply_constraints(obj)

            if obj.type in ("CURVE", "FONT", "SURFACE"):
                # Convert object to mesh
                bpy.ops.object.convert(target="MESH")

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


def delete_unused_vertex_group(obj: bpy.types.Object) -> None:
    if len(obj.vertex_groups) == 0:
        return

    max_weights = [0] * len(obj.vertex_groups)

    # Survey Zero Weights
    for vertex in obj.data.vertices:
        for vertex_group_element in vertex.groups:
            group_index = vertex_group_element.group
            weight = vertex_group_element.weight
            if max_weights[group_index] < weight:
                max_weights[group_index] = weight

    # Deform vertex groups
    deform_bone_names = []
    armature = obj.find_armature()
    if armature:
        deform_bone_names = [bone.name for bone in armature.data.bones]

    for index, weight in reversed(list(enumerate(max_weights))):
        vertex_group = obj.vertex_groups[index]
        if vertex_group.name not in deform_bone_names or weight == 0:
            obj.vertex_groups.remove(obj.vertex_groups[index])


class ExportError(Exception):
    pass


class Exporter:
    """Preprocess and Export file"""

    def __init__(self) -> None:
        pass

    def export(self, context: bpy_types.Context, settings: bpy.types.AnyType) -> None:
        scn = context.scene
        export_settings = settings.export_settings
        collection_settings = export_settings.collections

        # Check file path error
        if export_settings.export_path == "":
            error_msg = "Invalid path"
            raise ExportError(error_msg)

        # Convert object to mesh and Apply modifiers
        apply_all_objects(context)

        # Merge objects
        collection_settings_dict = {
            c.collection_ptr.name: c for c in collection_settings
        }

        merge_collections = get_merge_collections(
            collection_settings_dict,
            scn.collection,
        )

        for c in merge_collections:
            merge_objects(context, c.collection_ptr)

            obj = context.view_layer.objects.active

            # Post merge process
            if c.transform_settings.apply_all_transform:
                bpy.ops.object.transform_apply(
                    location=True,
                    rotation=True,
                    scale=True,
                    properties=False,
                )

            sort_shapekey(obj, c.shapekey_settings)

            separate_shapekey_lr(obj, c.shapekey_settings)

            if c.vertex_group_settings.delete_vertex_group:
                delete_unused_vertex_group(obj)

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
