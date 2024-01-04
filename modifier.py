import bpy


def _transfer_shapekey(obj : bpy.types.Object, blendshape : bpy.types.Object) -> None :
    bpy.ops.object.select_all(action="DESELECT")
    blendshape.select_set(state = True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.join_shapes()

def _apply_shapekey(obj : bpy.types.Object, index : int) -> None :
    shapekeys = obj.data.shape_keys.key_blocks
    if index < 0 or index > len(shapekeys):
        return

    for i in reversed(range(len(shapekeys))):
        if i != index:
            obj.shape_key_remove(shapekeys[i])

    obj.shape_key_remove(shapekeys[0])

def _apply_modifiers(obj : bpy.types.Object) -> None :
    for m in obj.modifiers :
        if m.show_viewport :
            if m.type != "ARMATURE" :
                bpy.context.view_layer.objects.active = obj
                try :
                    bpy.ops.object.modifier_apply(modifier = m.name)
                except RuntimeError :
                    # Error applying {m.name} to {obj.name}, removing it instead.
                    obj.modifiers.remove(m)
        else :
            obj.modifiers.remove(m)

def _apply_modifiers_shapekey(obj : bpy.types.Object) -> None:
    # Temp object that will contain all collapsed shapekeys
    temp_obj = obj.copy()
    temp_obj.data = obj.data.copy()
    #temp_obj.name = "temp_yfx_exporter_apply_modifiers"

    _apply_shapekey(obj, 0)
    _apply_modifiers(obj)

    shapekeys = temp_obj.data.shape_keys

    for i in range(1, len(shapekeys.key_blocks)) :
        blendshape_obj = temp_obj.copy()
        blendshape_obj.data = temp_obj.data.copy()

        _apply_shapekey(blendshape_obj, i)
        _apply_modifiers(blendshape_obj)

        # Transfer shapekey to original object
        _transfer_shapekey(obj, blendshape_obj)

        # Rename shapekey
        obj.data.shape_keys.key_blocks[i].name \
            = temp_obj.data.shape_keys.key_blocks[i].name

        # Delete the blendshape donor
        mesh_data = blendshape_obj.data
        bpy.data.objects.remove(blendshape_obj)
        bpy.data.meshes.remove(mesh_data)

    # Delete temp object
    mesh_data = temp_obj.data
    bpy.data.objects.remove(temp_obj)
    bpy.data.meshes.remove(mesh_data)


def apply_modifiers(obj : bpy.types.Object) -> None :
    if len(obj.modifiers) < 1 :
         return
    shapekeys = obj.data.shape_keys
    if shapekeys is not None and len(shapekeys.key_blocks) > 0 :
        _apply_modifiers_shapekey(obj)
    else :
        _apply_modifiers(obj)


