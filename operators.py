from enum import Enum
from typing import ClassVar

import bpy
import bpy_extras
import bpy_types

from .process import run_export_process


def list_actions_move(items: bpy.types.AnyType, index: int, action: str) -> str:
    idx = index

    try:
        item = items[idx]
    except IndexError:
        info = "Out of range"
    else:
        if action == "DOWN" and idx < len(items) - 1:
            items.move(idx, idx + 1)
            index += 1
            info = 'Item "%s" moved to position %d' % (item.name, index + 1)

        elif action == "UP" and idx >= 1:
            items.move(idx, idx - 1)
            index -= 1
            info = 'Item "%s" moved to position %d' % (item.name, index + 1)

        elif action == "REMOVE":
            info = 'Item "%s" removed from list' % (items[idx].name)
            index -= 1
            items.remove(idx)
        else:
            info = "Unknown action"

    return info


class YFX_EXPORTER_OT_list_actions(bpy.types.Operator):
    """Move items up and down, add and remove"""

    bl_idname = "yfx_exporter.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options: ClassVar[set] = {"REGISTER"}

    action: bpy.props.EnumProperty(
        items=(
            ("UP", "Up", ""),
            ("DOWN", "Down", ""),
            ("REMOVE", "Remove", ""),
            ("ADD", "Add", ""),
        ),
    )

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> set:
        scn = context.scene
        settings = scn.yfx_exporter_settings.export_settings

        info = list_actions_move(
            settings.collections,
            settings.collection_index,
            self.action,
        )

        self.report({"INFO"}, info)

        return {"FINISHED"}


class YFX_EXPORTER_OT_clear_list(bpy.types.Operator):
    # Clear all items of the list
    bl_idname = "yfx_exporter.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options: ClassVar[set] = {"INTERNAL"}

    @classmethod
    def poll(cls, context: bpy_types.Context) -> None:
        return bool(context.scene.yfx_exporter_settings.export_settings.collections)

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> Enum:
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context: bpy_types.Context) -> None:
        collections = context.scene.yfx_exporter_settings.export_settings.collections
        if bool(collections):
            collections.clear()
            self.report({"INFO"}, "All items removed")
        else:
            self.report({"INFO"}, "Nothing to remove")
        return {"FINISHED"}


class YFX_EXPORTER_OT_add_viewport_selection(bpy.types.Operator):
    """Add all items currently selected in the viewport"""

    bl_idname = "yfx_exporter.add_viewport_selection"
    bl_label = "Add Viewport Selection to List"
    bl_description = "Add all items currently selected in the viewport"
    bl_options: ClassVar[set] = {"REGISTER", "UNDO"}

    def execute(self, context: bpy_types.Context) -> set:
        scn = context.scene
        selected_objs = context.selected_objects
        if selected_objs:
            new_objs = []
            for i in selected_objs:
                item = scn.yfx_exporter_settings.export_settings.collections.add()
                item.name = i.name
                item.obj = i
                new_objs.append(item.name)
            info = ", ".join(map(str, new_objs))
            self.report({"INFO"}, 'Added: "%s"' % (info))
        else:
            self.report({"INFO"}, "Nothing selected in the Viewport")
        return {"FINISHED"}


class YFX_EXPORTER_OT_select_file(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "yfx_exporter.select_file"
    bl_label = "Select file in browser"

    # ExportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: bpy.props.StringProperty(
        default="*.fbx",
        options={"HIDDEN"},
    )

    def execute(self, context: bpy_types.Context) -> set:
        scn = context.scene
        settings = scn.yfx_exporter_settings.export_settings

        settings.export_path = self.filepath

        return {"FINISHED"}


def get_collection_list_callback(
    operator: bpy.types.Operator,
    context: bpy_types.Context,
) -> list:
    scn = context.scene
    export_settings = scn.yfx_exporter_settings.export_settings
    custom_collections = [c[1].name for c in export_settings.collections.items()]
    return [
        (
            c.name,
            c.name + " ",  # Append a space for non-translatable version
            c.name,
            "OUTLINER_COLLECTION",
            idx,
        )
        for idx, c in enumerate(bpy.data.collections)
        if c.name not in custom_collections and bpy.context.scene.user_of_id(c)
    ]


def get_collection_by_name(
    name: str,
    context: bpy_types.Context,
) -> bpy.types.Collection:
    for collection in bpy.data.collections:
        if collection.name == name:
            return collection
    return None


class YFX_EXPORTER_OT_add_collection(bpy.types.Operator):
    bl_idname = "yfx_exporter.add_collection"
    bl_label = "Add Collection"

    user_collections: bpy.props.EnumProperty(items=get_collection_list_callback)

    def execute(self, context: bpy_types.Context) -> set:
        scn = context.scene
        settings = scn.yfx_exporter_settings.export_settings
        act_coll = get_collection_by_name(self.user_collections, context)

        if act_coll.name in [c[1].name for c in settings.collections.items()]:
            info = '"%s" already in the list' % (act_coll.name)
        else:
            item = settings.collections.add()
            item.collection_ptr = act_coll
            item.name = item.collection_ptr.name
            settings.collection_index = len(settings.collections) - 1
            info = "%s added to list" % (item.name)

        self.report({"INFO"}, info)

        return {"FINISHED"}


class YFX_EXPORTER_OT_export_fbx(bpy.types.Operator):
    bl_idname = "yfx_exporter.export_fbx"
    bl_label = "Export FBX"
    bl_description = "Export FBX"

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return context.mode == "OBJECT"

    def execute(self, context: bpy.types.Context) -> set:
        run_export_process(context)

        return {"FINISHED"}
