import bpy

from .exporter import Exporter
from .process import MainProcess


class YFX_EXPORTER_OT_export_fbx(bpy.types.Operator) :
    bl_idname = "yfx_exporter.export_fbx"
    bl_label = "Export FBX"
    bl_description = "Export FBX"

    @classmethod
    def poll(cls, context : bpy.types.Context) -> bool:
        return context.mode == "OBJECT"

    def execute(self, context : bpy.types.Context) -> set:
        exporter = Exporter(MainProcess())

        # TODO(yuufyu): Add run in background process
        # https://yuufyu.atlassian.net/browse/YUUFYU-21?atlOrigin=eyJpIjoiNGFmZGZiM2I4MWVlNDk5ZGI2Mjc1ZTc2YjE1NWJlNjEiLCJwIjoiaiJ9
        exporter.export(context)

        return {"FINISHED"}
