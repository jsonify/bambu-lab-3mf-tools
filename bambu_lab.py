# Bambu Lab 3MF Tools - Printer setup and workflow functionality.
# Provides sidebar panel for Bambu Lab printer configuration.
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

import bpy
import mathutils
from bpy.props import EnumProperty, BoolProperty, FloatProperty

# Printer build volumes (X, Y, Z in mm)
PRINTER_VOLUMES = {
    'A1_MINI': (180, 180, 180),
    'A1': (256, 256, 256),
    'P1S': (256, 256, 256),
    'P1P': (256, 256, 256),
    'X1C': (256, 256, 256),
    'X1E': (256, 256, 256),
}

PRINTER_NAMES = {
    'A1_MINI': "A1 Mini (180×180×180)",
    'A1': "A1 (256×256×256)",
    'P1S': "P1S (256×256×256)",
    'P1P': "P1P (256×256×256)",
    'X1C': "X1 Carbon (256×256×256)",
    'X1E': "X1E (256×256×256)",
}


class BambuProperties(bpy.types.PropertyGroup):
    printer_model: EnumProperty(
        name="Printer",
        description="Select your Bambu Lab printer model",
        items=[
            ('A1_MINI', "A1 Mini (180×180×180)", "Bambu Lab A1 Mini"),
            ('A1', "A1 (256×256×256)", "Bambu Lab A1"),
            ('P1S', "P1S (256×256×256)", "Bambu Lab P1S"),
            ('P1P', "P1P (256×256×256)", "Bambu Lab P1P"),
            ('X1C', "X1 Carbon (256×256×256)", "Bambu Lab X1 Carbon"),
            ('X1E', "X1E (256×256×256)", "Bambu Lab X1E"),
        ],
        default='A1_MINI'
    )


class BAMBU_OT_setup_scene(bpy.types.Operator):
    """Set up the scene for Bambu Lab printer workflow"""
    bl_idname = "bambu.setup_scene"
    bl_label = "Setup Scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.bambu_props

        # Set units to millimeters
        context.scene.unit_settings.system = 'METRIC'
        context.scene.unit_settings.scale_length = 0.001
        context.scene.unit_settings.length_unit = 'MILLIMETERS'

        # Set viewport clipping for all 3D views
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.clip_start = 0.1
                        space.clip_end = 10000

        self.report({'INFO'}, f"Scene configured for millimeter workflow")
        return {'FINISHED'}


class BAMBU_OT_create_build_volume(bpy.types.Operator):
    """Create a wireframe cube representing the printer's build volume"""
    bl_idname = "bambu.create_build_volume"
    bl_label = "Create Build Volume"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.bambu_props
        volume = PRINTER_VOLUMES[props.printer_model]

        # Remove existing build volume if present
        old_volume = bpy.data.objects.get("Build Volume")
        if old_volume:
            bpy.data.objects.remove(old_volume, do_unlink=True)

        # Create cube
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        obj = context.active_object
        obj.name = "Build Volume"

        # Set dimensions
        obj.dimensions = (volume[0], volume[1], volume[2])

        # Position so bottom is at Z=0, centered on X and Y
        obj.location = (volume[0] / 2, volume[1] / 2, volume[2] / 2)

        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Set display properties
        obj.display_type = 'WIRE'
        obj.show_in_front = True
        obj.hide_select = True
        obj.hide_render = True

        # Set color
        obj.color = (0.2, 0.6, 1.0, 0.5)  # Light blue

        # Lock transformations
        obj.lock_location = (True, True, True)
        obj.lock_rotation = (True, True, True)
        obj.lock_scale = (True, True, True)

        # Deselect and set cursor to origin
        obj.select_set(False)
        context.scene.cursor.location = (0, 0, 0)

        self.report({'INFO'}, f"Created {volume[0]}×{volume[1]}×{volume[2]}mm build volume")
        return {'FINISHED'}


class BAMBU_OT_create_build_plate(bpy.types.Operator):
    """Create a flat plane representing the build plate"""
    bl_idname = "bambu.create_build_plate"
    bl_label = "Create Build Plate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.bambu_props
        volume = PRINTER_VOLUMES[props.printer_model]

        # Remove existing build plate if present
        old_plate = bpy.data.objects.get("Build Plate")
        if old_plate:
            bpy.data.objects.remove(old_plate, do_unlink=True)

        # Create plane
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
        obj = context.active_object
        obj.name = "Build Plate"

        # Set dimensions
        obj.dimensions = (volume[0], volume[1], 0)

        # Position centered
        obj.location = (volume[0] / 2, volume[1] / 2, 0)

        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Create material
        mat = bpy.data.materials.get("Build Plate Material")
        if not mat:
            mat = bpy.data.materials.new(name="Build Plate Material")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Base Color"].default_value = (0.15, 0.15, 0.15, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.8

        obj.data.materials.append(mat)

        # Set properties
        obj.hide_select = True

        # Lock transformations
        obj.lock_location = (True, True, True)
        obj.lock_rotation = (True, True, True)
        obj.lock_scale = (True, True, True)

        # Deselect
        obj.select_set(False)

        self.report({'INFO'}, f"Created {volume[0]}×{volume[1]}mm build plate")
        return {'FINISHED'}


class BAMBU_OT_full_setup(bpy.types.Operator):
    """Complete setup: configure scene, create build volume and plate"""
    bl_idname = "bambu.full_setup"
    bl_label = "Full Printer Setup"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.bambu.setup_scene()
        bpy.ops.bambu.create_build_volume()
        bpy.ops.bambu.create_build_plate()

        # Frame the view to see the build volume
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        with context.temp_override(area=area, region=region):
                            bpy.ops.view3d.view_all()

        self.report({'INFO'}, "Full printer setup complete!")
        return {'FINISHED'}


class BAMBU_OT_check_model_fit(bpy.types.Operator):
    """Check if selected objects fit within the build volume"""
    bl_idname = "bambu.check_model_fit"
    bl_label = "Check Model Fit"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.bambu_props
        volume = PRINTER_VOLUMES[props.printer_model]

        selected = context.selected_objects
        if not selected:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        # Calculate bounding box of all selected objects
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')

        for obj in selected:
            if obj.type != 'MESH':
                continue

            # Get world-space bounding box
            bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
            for corner in bbox:
                min_x = min(min_x, corner.x)
                min_y = min(min_y, corner.y)
                min_z = min(min_z, corner.z)
                max_x = max(max_x, corner.x)
                max_y = max(max_y, corner.y)
                max_z = max(max_z, corner.z)

        size_x = max_x - min_x
        size_y = max_y - min_y
        size_z = max_z - min_z

        fits = size_x <= volume[0] and size_y <= volume[1] and size_z <= volume[2]

        if fits:
            self.report({'INFO'}, f"Model fits! Size: {size_x:.1f}x{size_y:.1f}x{size_z:.1f}mm")
        else:
            self.report({'WARNING'}, f"Model too large! Size: {size_x:.1f}x{size_y:.1f}x{size_z:.1f}mm (max: {volume[0]}x{volume[1]}x{volume[2]}mm)")

        return {'FINISHED'}


class BAMBU_OT_center_on_plate(bpy.types.Operator):
    """Center selected objects on the build plate"""
    bl_idname = "bambu.center_on_plate"
    bl_label = "Center on Build Plate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.bambu_props
        volume = PRINTER_VOLUMES[props.printer_model]

        selected = context.selected_objects
        if not selected:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        for obj in selected:
            if obj.type != 'MESH':
                continue

            # Get bounding box in world space
            bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]

            min_x = min(c.x for c in bbox)
            max_x = max(c.x for c in bbox)
            min_y = min(c.y for c in bbox)
            max_y = max(c.y for c in bbox)
            min_z = min(c.z for c in bbox)

            # Calculate center offset
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2

            # Move to center of build plate and sit on Z=0
            obj.location.x += (volume[0] / 2) - center_x
            obj.location.y += (volume[1] / 2) - center_y
            obj.location.z -= min_z  # Sit on build plate

        self.report({'INFO'}, "Objects centered on build plate")
        return {'FINISHED'}


class BAMBU_OT_import_stl(bpy.types.Operator):
    """Import STL file with correct scale for millimeter workflow"""
    bl_idname = "bambu.import_stl"
    bl_label = "Import STL"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default="*.stl", options={'HIDDEN'})

    def execute(self, context):
        props = context.scene.bambu_props
        volume = PRINTER_VOLUMES[props.printer_model]

        # Import STL at 1:1 scale (assuming file is in mm, scene is in mm)
        bpy.ops.wm.stl_import(filepath=self.filepath, global_scale=1.0)

        # Get the imported object(s)
        imported = context.selected_objects

        if imported:
            obj = imported[0]
            # Calculate size for reporting
            size_x = obj.dimensions.x
            size_y = obj.dimensions.y
            size_z = obj.dimensions.z

            # Check if it fits
            fits = size_x <= volume[0] and size_y <= volume[1] and size_z <= volume[2]
            fit_status = "Fits" if fits else "Too large"

            self.report({'INFO'}, f"Imported: {size_x:.1f}x{size_y:.1f}x{size_z:.1f}mm ({fit_status})")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class BAMBU_OT_import_3mf(bpy.types.Operator):
    """Import 3MF file with correct scale for millimeter workflow"""
    bl_idname = "bambu.import_3mf"
    bl_label = "Import 3MF"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default="*.3mf", options={'HIDDEN'})

    def execute(self, context):
        props = context.scene.bambu_props
        volume = PRINTER_VOLUMES[props.printer_model]

        # Import 3MF using the Import3MF operator with mm native scale
        getattr(bpy.ops.import_mesh, '3mf')(filepath=self.filepath, scale_unit='MM_NATIVE')

        # Get the imported object(s)
        imported = context.selected_objects

        if imported:
            obj = imported[0]
            size_x = obj.dimensions.x
            size_y = obj.dimensions.y
            size_z = obj.dimensions.z

            fits = size_x <= volume[0] and size_y <= volume[1] and size_z <= volume[2]
            fit_status = "Fits" if fits else "Too large"

            self.report({'INFO'}, f"Imported: {size_x:.1f}x{size_y:.1f}x{size_z:.1f}mm ({fit_status})")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class BAMBU_OT_export_stl(bpy.types.Operator):
    """Export selected objects as STL for slicing"""
    bl_idname = "bambu.export_stl"
    bl_label = "Export STL"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default="*.stl", options={'HIDDEN'})

    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "No objects selected for export")
            return {'CANCELLED'}

        # Export at 1:1 scale (mm stays mm)
        bpy.ops.wm.stl_export(
            filepath=self.filepath,
            export_selected_objects=True,
            global_scale=1.0,
            ascii_format=False
        )

        self.report({'INFO'}, f"Exported to {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        if not context.selected_objects:
            self.report({'WARNING'}, "No objects selected for export")
            return {'CANCELLED'}

        # Default filename from first selected object
        self.filepath = context.selected_objects[0].name + ".stl"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class BAMBU_OT_export_3mf(bpy.types.Operator):
    """Export selected objects as 3MF for slicing"""
    bl_idname = "bambu.export_3mf"
    bl_label = "Export 3MF"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default="*.3mf", options={'HIDDEN'})

    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "No objects selected for export")
            return {'CANCELLED'}

        # Export using the Export3MF operator at 1:1 scale
        getattr(bpy.ops.export_mesh, '3mf')(
            filepath=self.filepath,
            use_selection=True,
            global_scale=1.0
        )

        self.report({'INFO'}, f"Exported to {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        if not context.selected_objects:
            self.report({'WARNING'}, "No objects selected for export")
            return {'CANCELLED'}

        # Default filename from first selected object
        self.filepath = context.selected_objects[0].name + ".3mf"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class BAMBU_PT_main_panel(bpy.types.Panel):
    """Main panel for Bambu Lab printer setup"""
    bl_label = "Bambu Lab Setup"
    bl_idname = "BAMBU_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bambu Lab"

    def draw(self, context):
        layout = self.layout
        props = context.scene.bambu_props

        # Printer selection
        layout.label(text="Printer Model:")
        layout.prop(props, "printer_model", text="")

        layout.separator()

        # Setup buttons
        layout.label(text="Scene Setup:")
        layout.operator("bambu.full_setup", icon='MODIFIER')

        layout.separator()

        col = layout.column(align=True)
        col.operator("bambu.setup_scene", icon='SCENE_DATA')
        col.operator("bambu.create_build_volume", icon='MESH_CUBE')
        col.operator("bambu.create_build_plate", icon='MESH_PLANE')

        layout.separator()

        # Model tools
        layout.label(text="Model Tools:")
        col = layout.column(align=True)
        col.operator("bambu.check_model_fit", icon='VIEWZOOM')
        col.operator("bambu.center_on_plate", icon='VIEW_PAN')

        layout.separator()

        # Import/Export
        layout.label(text="Import (mm scale):")
        row = layout.row(align=True)
        row.operator("bambu.import_stl", text="STL", icon='IMPORT')
        row.operator("bambu.import_3mf", text="3MF", icon='IMPORT')

        layout.label(text="Export:")
        row = layout.row(align=True)
        row.operator("bambu.export_stl", text="STL", icon='EXPORT')
        row.operator("bambu.export_3mf", text="3MF", icon='EXPORT')
