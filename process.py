import abc

import bpy

from .exporter import Exporter


class Process(metaclass=abc.ABCMeta) :
    @abc.abstractmethod
    def report_info(self, message: str) -> None:
        raise NotImplementedError

class MainProcess(Process) :
    def report_info(self, message: str) -> None:
        print(message)

class SubProcess(Process) :
    def report_info(self, message: str) -> None:
        print(message)

def run_export_process(context : bpy.types.Context) -> None:
    scn = context.scene
    exporter = Exporter()
    process = MainProcess()

    settings = scn.yfx_exporter_settings
    process.report_info(f"path : {settings.export_settings.export_path}")

    exporter.export(context, settings)

def run_background_process() -> None:
    pass
