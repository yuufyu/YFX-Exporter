import abc

import bpy

from .exporter import Exporter, ExportError
from .ui_panel import show_popup_message


class Process(metaclass=abc.ABCMeta) :
    @abc.abstractmethod
    def report_info(self, message: str) -> None:
        raise NotImplementedError

class MainProcess(Process) :
    pass

class SubProcess(Process) :
    pass



def run_export_process(context : bpy.types.Context) -> None:
    scn = context.scene
    settings = scn.yfx_exporter_settings

    try :
        exporter = Exporter()
        exporter.export(context, settings)
    except ExportError as e:
        show_popup_message(context = context, message = str(e),
                           title = "Export Error", icon = "ERROR")

def start_background_process() -> None:
    pass
