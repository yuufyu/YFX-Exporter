import bpy

from .merge import get_child_objects


def get_collection_shapekeys(collection: bpy.types.Collection) -> list:
    objects = get_child_objects(collection)
    total_shapekeys = []
    for obj in objects:
        shapekeys = obj.data.shape_keys
        if shapekeys is not None and len(shapekeys.key_blocks) > 1:
            shapekey_names = [key.name for key in shapekeys.key_blocks]
            total_shapekeys.extend(shapekey_names[1:])

    return list(dict.fromkeys(total_shapekeys))


def update_collection_shapekeys(context: bpy.types.Context) -> None:
    if context and context.scene.yfx_exporter_settings:
        export_settings = context.scene.yfx_exporter_settings.export_settings
        collection_settings = export_settings.collections
        collection_index = export_settings.collection_index
        len_collections = len(collection_settings)

        if len_collections > 0 and 0 <= collection_index < len_collections:
            collection_setting = collection_settings[collection_index]
            shapekey_settings = collection_setting.shapekey_settings
            shapekey_names = get_collection_shapekeys(collection_setting.collection_ptr)
            shapekeys = shapekey_settings.shapekeys
            for name in shapekey_names:
                if shapekeys.find(name) < 0:
                    shapekey_item = shapekeys.add()
                    shapekey_item.name = name
