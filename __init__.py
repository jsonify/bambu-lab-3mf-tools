# Bambu Lab 3MF Tools - Blender add-on for Bambu Lab 3D printer workflows.
# 3MF import/export based on original work by Ghostkeeper (2020).
# Copyright (C) 2025 jsonify
#
# This add-on is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# This add-on is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for
# details.
# You should have received a copy of the GNU Affero General Public License along with this plug-in. If not, see
# <https://gnu.org/licenses/>.

# <pep8 compliant>

bl_info = {
    "name": "Bambu Lab 3MF Tools",
    "author": "jsonify (based on 3MF addon by Ghostkeeper)",
    "version": (2, 0, 0),
    "blender": (5, 0, 0),
    "location": "File > Import-Export, View3D > Sidebar > Bambu Lab",
    "description": "3MF import/export with Bambu Lab printer setup tools",
    "support": 'COMMUNITY',
    "category": "Import-Export"
}

"""
Bambu Lab 3MF Tools - Blender add-on for Bambu Lab 3D printer workflows.

3MF import/export functionality based on original work by Ghostkeeper (2020).
Extended and maintained by jsonify (2025).

Features:
- Import/export 3MF files with unit scale options
- Bambu Lab printer setup (build volume, build plate visualization)
- Model fit checking and centering for supported printers
- Millimeter workflow configuration
"""

import bpy

# Reload functionality.
if "bpy" in locals():
    import importlib
    if "import_3mf" in locals():
        importlib.reload(import_3mf)
    if "export_3mf" in locals():
        importlib.reload(export_3mf)
    if "bambu_lab" in locals():
        importlib.reload(bambu_lab)

import bpy.utils  # To (un)register the add-on.
import bpy.types  # To (un)register the add-on as an import/export function.

from .import_3mf import Import3MF  # Imports 3MF files.
from .export_3mf import Export3MF  # Exports 3MF files.
from .bambu_lab import (  # Bambu Lab printer integration.
    BambuProperties,
    BAMBU_OT_setup_scene,
    BAMBU_OT_create_build_volume,
    BAMBU_OT_create_build_plate,
    BAMBU_OT_full_setup,
    BAMBU_OT_check_model_fit,
    BAMBU_OT_center_on_plate,
    BAMBU_OT_import_stl,
    BAMBU_OT_import_3mf,
    BAMBU_OT_export_stl,
    BAMBU_OT_export_3mf,
    BAMBU_PT_main_panel,
)


def menu_import(self, _):
    """
    Calls the 3MF import operator from the menu item.
    """
    self.layout.operator(Import3MF.bl_idname, text="3D Manufacturing Format (.3mf)")


def menu_export(self, _):
    """
    Calls the 3MF export operator from the menu item.
    """
    self.layout.operator(Export3MF.bl_idname, text="3D Manufacturing Format (.3mf)")


classes = (
    BambuProperties,  # Must be first (PropertyGroup)
    Import3MF,
    Export3MF,
    BAMBU_OT_setup_scene,
    BAMBU_OT_create_build_volume,
    BAMBU_OT_create_build_plate,
    BAMBU_OT_full_setup,
    BAMBU_OT_check_model_fit,
    BAMBU_OT_center_on_plate,
    BAMBU_OT_import_stl,
    BAMBU_OT_import_3mf,
    BAMBU_OT_export_stl,
    BAMBU_OT_export_3mf,
    BAMBU_PT_main_panel,  # Panel last
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bambu_props = bpy.props.PointerProperty(type=BambuProperties)

    bpy.types.TOPBAR_MT_file_import.append(menu_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_export)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bambu_props

    bpy.types.TOPBAR_MT_file_import.remove(menu_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export)


# Allow the add-on to be ran directly without installation.
if __name__ == "__main__":
    register()
