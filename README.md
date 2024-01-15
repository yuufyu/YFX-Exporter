# YFX Exporter

[![GitHub license](https://img.shields.io/github/license/yuufyu/YFX-Exporter)](https://github.com/yuufyu/YFX-Exporter/blob/main/LICENSE)
[![Blender Version](https://img.shields.io/badge/Blender-4.0.2-blue)](https://www.blender.org/)

## Overview
A plugin for FBX export with additional processing like applying modifiers and merging objects in a non-destructive way.

## Features
When the user presses the "Export FBX" button, the addon copies the current scene and performs the export process in the background. The application of modifiers and the merging of objects are reflected only in the exported FBX file, leaving the current scene undisturbed. The processes executed during export include:

- **Apply Constraint:** Applies Object Constraints visible in the current scene.

- **Convert to Mesh:** Converts Curve, Surface, and Text objects to Mesh. (Note: Modifiers attached to Curve, Surface, Text objects are removed.)

- **Apply Modifier:** Applies Modifiers to Mesh objects visible in the current scene. Modifiers attached to Mesh objects with Shapekeys are also applicable. Modifiers without viewport display settings are removed.

- **Merge Mesh:** Merges all objects within the specified "Merge Collection" hierarchy. Replaces the merged objects with the name of the collection.

- **Apply Transform(\*1):** Applies the Transform of merged objects. Sets the origin of the applied objects to the world coordinate origin.

- **Separate Shapekey(\*1):** Allows setting a specified Shapekey as the source for separation. Splits the source Shapekey along the X-axis passing through the object's origin. Adds the separated Shapekey below the source Shapekey, names the separated Shapekey as specified, and allows deletion of the source Shapekey.

- **Sort Shapekey(\*1):** Specifies the order of Shapekeys applied to objects merged using Merge Mesh.

- **Delete Unused Vertex Group(\*1):** Deletes unnecessary vertex groups in Mesh objects. Considers vertex groups with names not included in the deformation bones of the Armature modifier and vertex groups with weights of 0 as unnecessary.

- **Export FBX:** Exports the currently visible models in the scene to FBX format.

(*1) Features set for each Merge Collection.

## Installation
1. Download the plugin ZIP file from the [Code > Download ZIP](https://github.com/yuufyu/YFX-Exporter/archive/refs/heads/main.zip) page.
2. Open Blender and go to Edit > Preferences > Add-ons.
3. Click on "Install" and select the downloaded ZIP file.
4. Enable the "YFX Exporter" addon.

## Usage
"View 3D > SidePanel > YFX > YFX Exporter"  
Access export processing initiation and configuration through the "YFX" tab in the Side Panel of the Viewport 3D screen.

## Known Issues
If a Mesh object within the "Merge Collection" has Auto Smooth enabled, the normals may change after exporting.

## License
This plugin is licensed under the GNU General Public License (GPL) version 3. For details, see the [LICENSE](https://github.com/yuufyu/YFX-Exporter/blob/main/LICENSE) file.

## Author
yuufyu

## Feedback and Contributions
Feedback and contributions are welcome! Feel free to open issues or submit pull requests.

