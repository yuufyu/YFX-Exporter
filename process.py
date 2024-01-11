import abc
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import bpy


class Process(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def report_info(self, message: str) -> None:
        raise NotImplementedError


class MainProcess(Process):
    pass


class SubProcess(Process):
    pass


def run_export_process(context: bpy.types.Context) -> None:
    from .exporter import Exporter

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

        process = subprocess.run(
            blender_args,
            text=True,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(process.stdout)
        print(f"-- export end --- : {blender_args}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str)

    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])
    output = args.output
    print(f"output path {output}")

    if bpy.app.background:
        context = bpy.context
        settings = context.scene.yfx_exporter_settings
        export_settings = settings.export_settings
        export_settings.export_path = output

        settings.export(context)
