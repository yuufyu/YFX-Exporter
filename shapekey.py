import bpy

from .merge import get_child_objects


def insert_shapekey(obj: bpy.types.Object, name: str, index: int) -> bpy.types.ShapeKey:
    key_blocks_len = len(obj.data.shape_keys.key_blocks)
    if key_blocks_len <= 1:
        return None

    shapekey = obj.shape_key_add(name=name, from_mix=False)

    stash_active_index = obj.active_shape_key_index
    obj.active_shape_key_index = key_blocks_len

    for _ in range(key_blocks_len - index - 1):
        bpy.ops.object.shape_key_move(type="UP")
    obj.active_shape_key_index = stash_active_index

    return shapekey


def separate_shapekey(
    obj: bpy.types.Object,
    source: str,
    left: str,
    right: str,
    eps: float = 0.0000001,
) -> None:
    key_blocks = obj.data.shape_keys.key_blocks

    source_shapekey_idx = key_blocks.find(source)
    if source_shapekey_idx < 0:
        return
    source_shapekey = key_blocks[source_shapekey_idx]
    right_shapekey = insert_shapekey(obj, right, source_shapekey_idx)  # No error check
    left_shapekey = insert_shapekey(obj, left, source_shapekey_idx)  # No error check
    basis_shapekey = key_blocks[0]

    for i in range(len(source_shapekey.data)):
        co = source_shapekey.data[i].co

        if co.x > eps:
            if left_shapekey:
                left_shapekey.data[i].co = co
        elif co.x < -eps:
            if right_shapekey:
                right_shapekey.data[i].co = co
        else:
            basis_co = basis_shapekey.data[i].co
            center_co = basis_co + ((co - basis_co) / 2)
            if left_shapekey:
                left_shapekey.data[i].co = center_co

            if right_shapekey:
                right_shapekey.data[i].co = center_co


def separate_shapekey_lr(obj: bpy.types.Object) -> None:
    shapekeys = obj.data.shape_keys
    if shapekeys is None or len(shapekeys.key_blocks) == 0:
        return

    remove_keys = []

    key_blocks = shapekeys.key_blocks

    for shape_key in key_blocks:
        name = shape_key.name
        if name.endswith(("_LR", ".LR")):
            left_key_name = name[:-3] + name[-3] + "L"
            right_key_name = name[:-3] + name[-3] + "R"

            separate_shapekey(obj, name, left_key_name, right_key_name)

            remove_keys.append(shape_key)

    for remove_key in remove_keys:
        obj.shape_key_remove(remove_key)


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
            shapekeys = shapekey_settings.shapekeys

            # Add new shapekeys
            shapekey_names = get_collection_shapekeys(collection_setting.collection_ptr)
            for name in shapekey_names:
                if shapekeys.find(name) < 0:
                    shapekey_item = shapekeys.add()
                    shapekey_item.name = name

            # Remove deleted shapekeys
            remove_idx = [
                i
                for i, shapekey in enumerate(shapekeys)
                if shapekey.name not in shapekey_names
            ]
            for i in reversed(remove_idx):
                shapekeys.remove(i)
