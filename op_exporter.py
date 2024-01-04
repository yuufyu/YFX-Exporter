import bpy

from .process import run_export_process


class YFX_EXPORTER_OT_export_fbx(bpy.types.Operator) :
    bl_idname = "yfx_exporter.export_fbx"
    bl_label = "Export FBX"
    bl_description = "Export FBX"

    @classmethod
    def poll(cls, context : bpy.types.Context) -> bool:
        return context.mode == "OBJECT"

    def execute(self, context : bpy.types.Context) -> set:
        run_export_process(context)

        return {"FINISHED"}
