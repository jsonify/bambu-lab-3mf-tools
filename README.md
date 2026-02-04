# Bambu Lab 3MF Tools

A Blender add-on for Bambu Lab 3D printer workflows, featuring 3MF import/export and printer setup tools.

## Features

### 3MF Import/Export
- Import and export 3MF files (3D Manufacturing Format)
- Multiple scale options: native millimeters, mm-to-meters conversion, or custom scale
- Preserves materials and metadata

### Bambu Lab Printer Integration
- **Printer Selection**: Support for A1 Mini, A1, P1S, P1P, X1 Carbon, and X1E
- **Scene Setup**: One-click configuration for millimeter workflow
- **Build Volume Visualization**: Wireframe display of printer dimensions
- **Build Plate**: Visual reference for the print bed
- **Model Fit Check**: Verify your model fits within the build volume
- **Center on Plate**: Automatically position models on the build plate

### Supported Printers

| Printer | Build Volume (mm) |
|---------|-------------------|
| A1 Mini | 180 x 180 x 180 |
| A1 | 256 x 256 x 256 |
| P1S | 256 x 256 x 256 |
| P1P | 256 x 256 x 256 |
| X1 Carbon | 256 x 256 x 256 |
| X1E | 256 x 256 x 256 |

## Requirements

- Blender 5.0 or later

## Installation

### From Blender Extensions
1. Open Blender
2. Go to Edit > Preferences > Get Extensions
3. Search for "Bambu Lab 3MF Tools"
4. Click Install

### Manual Installation
1. Download the latest release
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install from Disk" and select the downloaded `.zip` file
4. Enable "Bambu Lab 3MF Tools"

## Usage

### Sidebar Panel
Access the Bambu Lab panel in the 3D Viewport sidebar (press `N` to toggle):
- **View3D > Sidebar > Bambu Lab**

### Quick Start
1. Select your printer model from the dropdown
2. Click "Full Setup" to configure the scene with build volume and plate
3. Import your model (STL or 3MF)
4. Use "Check Fit" to verify dimensions
5. Use "Center on Plate" to position your model
6. Export as 3MF for Bambu Studio

### Import/Export
- **File > Import > 3D Manufacturing Format (.3mf)**
- **File > Export > 3D Manufacturing Format (.3mf)**

## Credits

3MF import/export functionality based on original work by [Ghostkeeper](https://github.com/Ghostkeeper/Blender3mfFormat) (2020).

Extended and maintained by jsonify (2025).

## License

This add-on is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) (GPL-3.0).
