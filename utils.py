import bpy


def remove_all_invalid_items(
    self: bpy.types.AnyType,
    context: bpy.types.Context,
) -> None:
    if context and context.yfx_exporter_settings:
        scn = context.scene
        export_settings = scn.yfx_exporter_settings.export_settings
        items = export_settings.collections
        remove_indices = [
            i
            for i, item in enumerate(items)
            if item is None or item.collection_ptr is None
        ]
        for i in remove_indices:
            items.remove(i)
        current_index = export_settings.collection_index
        export_settings.collection_index = max(0, current_index - len(remove_indices))
