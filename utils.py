import bpy

from .shapekey import (
    update_active_collection_shapekeys,
    update_all_collection_shapekeys,
)

exclusive_active_update_setting_items = False
exclusive_all_update_setting_items = False


def remove_invalid_collection_settings(context: bpy.types.Context) -> None:
    if context and context.scene.yfx_exporter_settings:
        export_settings = context.scene.yfx_exporter_settings.export_settings
        items = export_settings.collections
        remove_indices = [
            i
            for i, item in enumerate(items)
            if item is None or item.collection_ptr is None
        ]
        for i in remove_indices:
            items.remove(i)
        current_index = export_settings.collection_index
        export_settings.collection_index = max(
            0,
            current_index - len(remove_indices),
        )


def update_active_setting_items(
    self: bpy.types.AnyType,
    context: bpy.types.Context,
) -> None:
    if context and context.scene.yfx_exporter_settings:
        global exclusive_active_update_setting_items  # noqa: PLW0603
        if exclusive_active_update_setting_items is False:
            exclusive_active_update_setting_items = True

            remove_invalid_collection_settings(context)
            update_active_collection_shapekeys(context)

            exclusive_active_update_setting_items = False


def update_all_setting_items(context: bpy.types.Context) -> None:
    if context and context.scene.yfx_exporter_settings:
        global exclusive_all_update_setting_items  # noqa: PLW0603
        if exclusive_all_update_setting_items is False:
            exclusive_all_update_setting_items = True

            remove_invalid_collection_settings(context)
            update_all_collection_shapekeys(context)

            exclusive_all_update_setting_items = False
