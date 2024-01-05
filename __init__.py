# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""YFX Exporter.

FBX exporter for character modeling.
"""

from . import auto_load

bl_info = {
    "name": "YFX Exporter",
    "author": "yuufyu",
    "description": "",
    "blender": (4, 0, 2),
    "version": (0, 0, 1),
    "location": "View 3D > SidePanel > YFX(panel) > YFX Exporter",
    "warning": "",
    "category": "Import-Export",
}

auto_load.init()


def register() -> None:
    auto_load.register()


def unregister() -> None:
    auto_load.unregister()
