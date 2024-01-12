import abc
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import bpy

from yfx_exporter.exporter import Exporter, ExportError


class Process(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def report_info(self, message: str) -> None:
        raise NotImplementedError


class MainProcess(Process):
    pass


class SubProcess(Process):
    pass


def run_export_process(context: bpy.types.Context) -> None:
    scn = context.scene
    settings = scn.yfx_exporter_settings

    exporter = Exporter()
    exporter.export(context, settings)


def start_foreground_export(context: bpy.types.Context) -> None:
    pass


def start_background_export(context: bpy.types.Context) -> None:
    export_settings = context.scene.yfx_exporter_settings.export_settings
    abs_export_path = bpy.path.abspath(export_settings.export_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = str(Path(temp_dir) / "___yfx_exporter_temp___.blend")
        bpy.ops.wm.save_as_mainfile(filepath=temp_file, copy=True, check_existing=False)

        exec_script_path = __file__
        exec_script_dir = Path(exec_script_path).parent

        blender_args = [
            bpy.app.binary_path,
            "--factory-startup",
            "--addons",
            __package__.split(".")[0],
            "--background",
            temp_file,
            "--python",
            exec_script_path,
            "--",
            "--output",
            abs_export_path,
        ]
        with subprocess.Popen(
            blender_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="UTF-8",
            cwd=str(exec_script_dir),
        ) as proc:
            print(proc.stdout.read())

            msg_stderr = proc.stderr.read()
            if msg_stderr:
                raise ExportError(msg_stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str)

    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])
    output = args.output

    context = bpy.context
    settings = context.scene.yfx_exporter_settings
    export_settings = settings.export_settings
    export_settings.export_path = output
    run_export_process(context)
