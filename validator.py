from dataclasses import dataclass
from enum import Enum

import bpy
import bpy_types


class ErrorCategory(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class ErrorInfo:
    code: int
    category: ErrorCategory
    message: str


def check_fbx_path(path: str) -> bool:
    """
    Check the validity of the provided FBX file path.

    Parameters:
    - path (str): The file path of the FBX file.

    Returns:
    - bool: If True is returned, it indicates a potential error due to an invalid path.
    """
    min_path_length = 5
    return len(path) < min_path_length  # <>.fbx


def check_multiple_collections(obj: bpy.types.Object) -> bool:
    """
    Check multiple collections.

    Parameters:
    - obj (bpy.types.Object): Object

    Returns:
    - bool: If True is returned, it indicates a potential error due to
            object in multiple collections.
    """
    return len(obj.users_collection) > 1


# nest
def get_nest_collections(
    collection_settings: dict,  # readonly
    parent_collection: bpy.types.Collection,
    in_merge_collection: bool,
) -> list:
    nest_collection_names = []
    name = parent_collection.name
    is_merge_collection = name in collection_settings

    if is_merge_collection and in_merge_collection:
        nest_collection_names.append(name)

    for child in parent_collection.children:
        nested = get_nest_collections(
            collection_settings,
            child,
            in_merge_collection=is_merge_collection or in_merge_collection,
        )
        if len(nested) > 0:
            nest_collection_names.extend(nested)

    return nest_collection_names


def check_nest_collections(
    collection_settings: bpy.types.AnyType,
    collection: bpy.types.Collection,
) -> list:
    if len(collection_settings) <= 1:
        return []

    collection_settings_dict = {c.collection_ptr.name: c for c in collection_settings}
    return get_nest_collections(
        collection_settings_dict,
        collection,
        in_merge_collection=False,
    )


def validate(context: bpy_types.Context) -> list:
    error_list = []

    scn = context.scene
    export_settings = scn.yfx_exporter_settings.export_settings
    collection_settings = export_settings.collections

    # Check file path error
    if check_fbx_path(export_settings.export_path):
        err = ErrorInfo(
            code=2,
            category=ErrorCategory.ERROR,
            message="Invalid FBX output path.",
        )
        error_list.append(err)

    # Check nestd collection
    nested_collections = check_nest_collections(collection_settings, scn.collection)
    if len(nested_collections) > 0:
        nested_collections_str = ",".join(nested_collections)

        err = ErrorInfo(
            code=17,
            category=ErrorCategory.WARNING,
            message=f"Merging collections with parent-child relationships.\
Settings of child collections will be ignored.({nested_collections_str})",
        )
        error_list.append(err)

    return error_list
