import bpy


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
