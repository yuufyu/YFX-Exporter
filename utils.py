import bpy

exclusive_remove_all_invalid_items = False


def remove_all_invalid_items(
    self: bpy.types.AnyType,
    context: bpy.types.Context,
) -> None:
    global exclusive_remove_all_invalid_items  # noqa: PLW0603
    if exclusive_remove_all_invalid_items is False:
        exclusive_remove_all_invalid_items = True

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

        exclusive_remove_all_invalid_items = False
