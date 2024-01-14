import bpy


def copy_object(obj: bpy.types.Object) -> bpy.types.Object:
    copy_obj = obj.copy()
    copy_obj.data = obj.data.copy()
    bpy.context.collection.objects.link(copy_obj)
    return copy_obj


def remove_object(obj: bpy.types.Object) -> None:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(state=True)
    bpy.ops.object.delete(use_global=False, confirm=False)


def transfer_shapekey(obj: bpy.types.Object, blendshape: bpy.types.Object) -> None:
    bpy.ops.object.select_all(action="DESELECT")
    blendshape.select_set(state=True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.join_shapes()


def reset_shapekey_value(obj: bpy.types.Object) -> None:
    for shapekey in obj.data.shape_keys.key_blocks:
        shapekey.value = 0


def apply_shapekey(obj: bpy.types.Object, index: int) -> None:
    shapekeys = obj.data.shape_keys.key_blocks
    if 0 <= index < len(shapekeys):
        shapekeys[index].value = 1
        obj.shape_key_add(name="temp_apply_shape_key", from_mix=True)
        for s in shapekeys[:]:
            obj.shape_key_remove(s)


def apply_all_modifiers(obj: bpy.types.Object) -> None:
    for m in obj.modifiers:
        if m.show_viewport:
            if m.type != "ARMATURE":
                bpy.context.view_layer.objects.active = obj
                try:
                    bpy.ops.object.modifier_apply(modifier=m.name)
                except RuntimeError:
                    obj.modifiers.remove(m)
        else:
            obj.modifiers.remove(m)


def apply_modifiers_with_shapekeys(obj: bpy.types.Object) -> None:
    reset_shapekey_value(obj)

    # Temp object that will contain all collapsed shapekeys
    temp_obj = copy_object(obj)

    apply_shapekey(obj, 0)
    apply_all_modifiers(obj)

    shapekeys_blocks = temp_obj.data.shape_keys.key_blocks
    basis_name = shapekeys_blocks[0].name

    for i in range(1, len(shapekeys_blocks)):
        blendshape_obj = copy_object(temp_obj)

        apply_shapekey(blendshape_obj, i)
        apply_all_modifiers(blendshape_obj)

        # Transfer shapekey to the original object
        transfer_shapekey(obj, blendshape_obj)

        # Rename shapekey
        obj.data.shape_keys.key_blocks[i].name = shapekeys_blocks[i].name

        # Delete the blendshape donor
        remove_object(blendshape_obj)

    # Keep Basis name
    obj.data.shape_keys.key_blocks[0].name = basis_name

    # Delete temp object
    remove_object(temp_obj)


def main_apply_modifiers(obj: bpy.types.Object) -> None:
    """
    Main function to apply modifiers to the target object.

    Args:
        obj (bpy.types.Object): The target object.
    """
    if sum(m.type != "ARMATURE" for m in obj.modifiers) == 0:
        return
    shapekeys = obj.data.shape_keys
    if shapekeys is not None and len(shapekeys.key_blocks) > 0:
        apply_modifiers_with_shapekeys(obj)
    else:
        apply_all_modifiers(obj)
