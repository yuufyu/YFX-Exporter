from typing import Generator

import bpy
import bpy_types

from .modifier import main_apply_modifiers


def convert_to_mesh(context: bpy_types.Context, obj: bpy.types.Object) -> None:
    context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(state=True)
    bpy.ops.object.convert(target="MESH")


def get_child_objects(collection: bpy.types.Collection) -> list:
    collections = [
        obj for obj in collection.objects if obj.visible_get() and obj.type == "MESH"
    ]
    for c in collection.children:
        children = get_child_objects(c)
        collections.extend(children)

    return collections


def merge_objects(context: bpy_types.Context, collection: bpy.types.Collection) -> None:
    merge_targets = get_child_objects(collection)

    if len(merge_targets) == 1:
        merge_targets[0].name = collection.name
    elif len(merge_targets) > 1:
        context.view_layer.objects.active = merge_targets[0]
        bpy.ops.object.select_all(action="DESELECT")

        for obj in merge_targets:
            print(f"obj:{obj.name}")
            obj.select_set(state=True)
        bpy.ops.object.join()
        context.view_layer.objects.active.name = collection.name


def apply_objects(context: bpy_types.Context) -> None:
    scn = context.scene
    for obj in scn.objects:
        if obj.visible_get():
            # Convert object to mesh
            if obj.type == "CURVE":  # noqa: SIM114
                convert_to_mesh(context, obj)
            elif obj.type == "FONT":
                convert_to_mesh(context, obj)

            if obj.type == "MESH":
                main_apply_modifiers(obj)


def get_merge_parents(
    collection_names: set,
    parent_collection: bpy.types.Collection,
) -> Generator[bpy.types.Collection, None, None]:
    if parent_collection.name in collection_names:
        # Ignore nested collections
        yield parent_collection
    else:
        for child in parent_collection.children:
            yield from get_merge_parents(collection_names, child)


def main_merge_objects(
    context: bpy_types.Context,
    collection_names: set,
) -> None:
    scn = context.scene

    # Select collection for working
    context.view_layer.active_layer_collection = context.view_layer.layer_collection

    # Convert object to mesh and Apply modifiers
    apply_objects(context)

    # Merge objects
    for c in get_merge_parents(collection_names, scn.collection):
        merge_objects(context, c)
