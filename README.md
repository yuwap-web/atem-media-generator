# ATEM Media File Generator

A cross-platform desktop application for generating broadcast-quality PNG images for Blackmagic ATEM media pools. Create title slides, lower-third graphics, and custom overlays with real-time preview and batch processing capabilities.

**Version**: 1.0.0
**Platform**: macOS, Windows
**License**: MIT

## Features

- 🖼️ **Template-Based Image Generation**: Define reusable templates with text layers, fonts, and colors
- 🎛️ **Template Customizer**: Modify text attributes (font, size, color, alignment) in real-time without editing JSON
- 🌍 **Japanese Font Support**: Built-in support for Hiragino Sans, Hiragino Sans Serif, and other system fonts
- 🔄 **Real-Time Preview**: See changes instantly as you edit parameters
- 📝 **Batch Processing**: Generate multiple images from CSV files
- 🎨 **Professional Output**: 1920×1080 PNG images with transparent backgrounds (RGBA)
- 💾 **Template Management**: Create, save, and organize custom templates
- 🚀 **Multi-Platform**: Works on macOS and Windows
- ⚡ **Fast & Lightweight**: Efficient image processing with Pillow

## Installation

### 📥 Download Pre-Built Application

Visit the [Releases](https://github.com/kusurix-ux/Atem-picture-tool/releases) page and download:

**macOS** (v1.0.0 and later):
- `ATEM-Media-Generator-mac.zip` - Native .app bundle with all dependencies
- Extract: `unzip ATEM-Media-Generator-mac.zip`
- Run: `open ATEM\ Media\ Generator.app` or double-click the app

**Windows** (v1.0.0 and later):
- `ATEM-Media-Generator-windows.zip` - Portable executable
- Extract the zip file
- Run: Double-click `ATEM-Media-Generator.exe`
- No installation required - portable application

### macOS Quick Start

```bash
# 1. Download ATEM-Media-Generator-mac.zip from Releases
# 2. Extract
unzip ATEM-Media-Generator-mac.zip

# 3. Run the application
open "ATEM Media Generator.app"

# Alternative: Run from terminal
"ATEM Media Generator.app/Contents/MacOS/ATEM Media Generator"
```

### Windows Quick Start

```batch
# 1. Download ATEM-Media-Generator-windows.zip from Releases
# 2. Extract the folder
# 3. Double-click ATEM-Media-Generator.exe to run

# Or from PowerShell:
.\ATEM-Media-Generator\ATEM-Media-Generator.exe
```

## Building from Source

### Prerequisites

- Python 3.9+
- pip package manager

### Setup

```bash
# Clone repository
git clone https://github.com/kusurix-ux/Atem-picture-tool.git
cd Atem-picture-tool/mediafile

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Application

```bash
python main.py
```

### Run Tests

```bash
# Phase 2: Image generation tests
python test_phase2.py

# Phase 3: GUI component tests
python test_gui.py

# Phase 4: CSV batch processing tests
python test_csv.py

# Full integration tests
python test_integration.py
```

## Usage Guide

### 1. Select a Template

1. Launch the application
2. The template list appears on the left panel
3. Click on a template to select it (e.g., "Simple Title")
4. The template's parameters appear in the middle panel

### 2. Edit Parameters

1. In the **Parameters** section (middle panel), enter values for:
   - **Required parameters** (marked with *)
   - **Optional parameters** (can be left empty)
2. Changes appear in real-time in the **Preview** panel (right)

### 2.5. Customize Template (Optional)

Use the **Template Customizer** panel to modify text attributes without editing JSON:

1. In the **Template Customizer** section (middle panel, below parameters):
   - **Font**: Select from system fonts including Japanese fonts (ヒラギノ角ゴシック, etc.)
   - **Size**: Adjust font size from 8px to 200px
   - **Alignment**: Choose left/center/right alignment
   - **Color**: Pick text color with the color picker

2. Changes preview in real-time
3. Click **Apply Changes** to confirm or **Reset to Original** to discard

*See [Template Customizer Guide](TEMPLATE_CUSTOMIZER_GUIDE.md) for detailed instructions*

### 3. Save Single Image

1. Once satisfied with the preview, click **Save PNG** in the toolbar
2. Select output directory and filename
3. Click **Save** to generate the PNG file

### 4. Batch Processing from CSV

1. Prepare a CSV file with columns matching template parameters
2. Click **Batch Export (CSV)** in toolbar
3. Select your CSV file
4. Confirm the batch operation
5. The application generates images for each valid row

**Example CSV** (for "Simple Title" template):
```csv
title,subtitle
Welcome to ATEM,Professional Graphics
Session Start,Live Event
Scene Transition,Smooth Change
```

## Template System

### Template Structure

Templates are JSON files defining image layout and parameters:

```json
{
  "name": "Simple Title",
  "template_type": "title",
  "background_color": [0, 0, 0, 255],
  "layers": [
    {
      "name": "Main Title",
      "x": 100,
      "y": 400,
      "width": 1720,
      "height": 200,
      "font_name": "Helvetica",
      "font_size": 80,
      "color": [255, 255, 255, 255],
      "alignment": "center",
      "parameter_key": "title"
    }
  ],
  "required_parameters": ["title"],
  "optional_parameters": ["subtitle"]
}
```

### Template Types

- **title**: Full-screen title slides
- **lower_third**: Lower-third graphics with name/title
- **other**: Custom layouts

### Available Fonts

The application uses system fonts and supports Japanese fonts:

**Standard Fonts**:
- **macOS**: Helvetica, Arial, Menlo, Courier, Times New Roman, Georgia, Monaco
- **Windows**: Segoe UI, Calibri, Courier New, etc.
- **Custom**: Place TTF files in `fonts/` directory

**Japanese Fonts** (built-in support):
- **ヒラギノ角ゴシック** (Hiragino Sans) - Modern sans-serif
- **ヒラギノゴシック** (Hiragino Sans Serif) - Standard sans-serif
- **Arial Unicode** - Unicode support
- **Meiryo** (Windows) - Standard Japanese font
- **MS 明朝** (Windows) - Japanese serif font

*For detailed Japanese font support and sample templates, see [Template Customizer Guide](TEMPLATE_CUSTOMIZER_GUIDE.md)*

### Adding Custom Templates

1. Create a JSON template file in the `templates/` directory
2. Reload templates in the application
3. Use your custom template for generating images

## CSV Batch Processing

### CSV Format

- **First row**: Column headers (must match template parameter_key values)
- **Data rows**: Parameter values (one row = one image)
- **Encoding**: UTF-8 recommended

### Example Workflow

```bash
# 1. Create CSV file (batch_titles.csv)
# Columns: title, subtitle
# Row 1: Opening, Start of Show
# Row 2: Break, Commercial Break
# ...

# 2. In application:
#    - Select "Simple Title" template
#    - Click "Batch Export (CSV)"
#    - Select batch_titles.csv
#    - Confirm operation
#    - Result: title_0002_Opening.png, title_0003_Break.png, ...
```

### Output Files

Batch processing generates files in the output directory:
- **Naming**: `{template_type}_{row_number}_{first_param_value}.png`
- **Format**: 1920×1080 RGBA PNG
- **Log**: `batch_{template_type}_{timestamp}.log` for debugging

## Output Settings

Edit `.env` to customize:

```env
# Output directory for generated images
ATEM_OUTPUT_DIR=./output

# Template directory
ATEM_TEMPLATE_DIR=./templates

# Image dimensions (recommended: 1920x1080 for ATEM)
# (Configure in config.py)
```

## Configuration

### `.env` File

```env
ATEM_OUTPUT_DIR=./output
ATEM_TEMPLATE_DIR=./templates
ATEM_IP=
ATEM_PORT=20990
ATEM_DEFAULT_FONT=Helvetica
```

### `config.py`

Edit `config.py` to modify:
- Output image size (default: 1920×1080)
- Preview update mode (realtime or manual)
- Font settings

## Troubleshooting

### Common Issues

**"No templates found"**
- Ensure `templates/` directory exists
- Check that template JSON files are valid
- Verify file encoding is UTF-8

**"Failed to load font"**
- Verify font name matches system font
- Check custom fonts are in `fonts/` directory
- Fall back to default font (Helvetica)

**"Image generation failed"**
- Check template parameter values are not empty for required fields
- Verify image dimensions are reasonable (max 4096×4096)
- Check available system memory

**"CSV batch processing failed"**
- Ensure CSV encoding is UTF-8
- Verify column headers match template parameter_key values
- Check for required parameters in each row
- Review batch log file for detailed errors

## System Requirements

### macOS
- macOS 10.13+
- 2GB RAM
- 100MB free disk space

### Windows
- Windows 7+
- 2GB RAM
- 100MB free disk space

## Development

### Project Structure

```
mediafile/
├── main.py                      # PyQt5 main application
├── image_generator.py           # Pillow-based image rendering
├── template_manager.py          # JSON template I/O
├── csv_processor.py             # Batch CSV processing
├── config.py                    # Configuration management
├── models/
│   └── template.py              # Data models
├── ui/
│   ├── parameter_editor.py      # Parameter editing panel
│   └── preview_panel.py         # Image preview panel
├── workers/
│   ├── image_generator_worker.py # Background generation
│   └── csv_batch_worker.py      # Background CSV processing
├── templates/                   # Sample templates
└── output/                      # Generated images
```

### 🏗️ Building for Distribution

#### macOS - Build .app Bundle

```bash
# 1. Setup (first time only)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Build .app bundle
bash build-mac.sh

# Output: dist/ATEM Media Generator.app (2.0MB binary)
# The .app bundle includes all dependencies and libraries

# 3. Create distributable .zip for GitHub Releases
ditto -c -k --sequesterRsrc dist/ATEM\ Media\ Generator.app ATEM-Media-Generator-mac.zip
# Output: ATEM-Media-Generator-mac.zip (28MB)
```

**macOS Build Notes:**
- Creates native .app bundle with proper structure
- Includes all PyQt5 and Pillow dependencies
- Signed for macOS 10.13+
- Binary: 2.0MB, Full bundle with dependencies: 28MB when zipped
- Can be run directly: `open dist/ATEM\ Media\ Generator.app`

#### Windows - Build EXE

```powershell
# 1. Setup (first time only)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Build executable
.\build-windows.ps1

# Output: dist\ATEM-Media-Generator\ATEM-Media-Generator.exe (~50MB)
# Run: .\dist\ATEM-Media-Generator\ATEM-Media-Generator.exe

# 3. Create distributable .zip for GitHub Releases
powershell Compress-Archive -Path 'dist\ATEM-Media-Generator' -DestinationPath 'ATEM-Media-Generator-windows.zip'
# Output: ATEM-Media-Generator-windows.zip (50-60MB)
```

**Windows Build Notes:**
- Creates portable executable with all dependencies included
- No separate installation needed
- Single executable folder can be run from anywhere
- Binary: 50MB (onedir format for portability)

## Future Features

- 🎥 Direct ATEM device upload via REST API
- 🎨 Advanced template editor UI
- 📊 Motion graphics and animations
- 🌐 Web-based interface option
- 🔗 Template sharing and marketplace

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## Support

For issues, questions, or suggestions:
- 📝 [GitHub Issues](https://github.com/kusurix-ux/Atem-picture-tool/issues)
- 💬 [GitHub Discussions](https://github.com/kusurix-ux/Atem-picture-tool/discussions)

## License

MIT License - See LICENSE file for details

## 🚀 Release to GitHub

### Creating a New Release

```bash
# 1. Update version in code if needed
# 2. Ensure builds are tested and in git

# 3. Create git tag
git tag v1.0.0
git push origin v1.0.0

# 4. GitHub Actions automatically builds and creates release with:
#    - ATEM-Media-Generator-mac.zip
#    - ATEM-Media-Generator-windows.zip

# Alternatively, manual release upload:
# - Go to: https://github.com/kusurix-ux/Atem-picture-tool/releases
# - Click "Create a new release"
# - Upload ATEM-Media-Generator-mac.zip and ATEM-Media-Generator-windows.zip
```

### CI/CD Automation

The project uses GitHub Actions for automated builds:

**macOS** (`.github/workflows/build-mac.yml`)
- Triggered on: push to main/master, version tags, manual trigger
- Creates: ATEM-Media-Generator-mac.zip
- Artifacts: Uploaded to release on tag

**Windows** (`.github/workflows/build-windows.yml`)
- Triggered on: push to main/master, version tags, manual trigger
- Creates: ATEM-Media-Generator-windows.zip
- Artifacts: Uploaded to release on tag

### Manual Release Steps

If not using GitHub Actions:

```bash
# 1. Build both platforms
bash build-mac.sh                    # macOS
# On Windows machine: .\build-windows.ps1

# 2. Create archives
ditto -c -k --sequesterRsrc dist/ATEM\ Media\ Generator.app ATEM-Media-Generator-mac.zip

# 3. Upload to GitHub Releases
# Use GitHub web UI or gh CLI:
gh release create v1.0.0 ATEM-Media-Generator-mac.zip --notes "Release notes here"
```

---

## Changelog

### v1.0.0 (2026-03-01)
- ✨ Initial release
- 🖼️ Template system with JSON support
- 🔄 Real-time preview
- 📝 CSV batch processing
- 🏗️ macOS .app bundle and Windows EXE builds
- ✅ Comprehensive test suite (57 tests)
- 📖 Complete documentation
- 🤖 GitHub Actions CI/CD automation

---

**Made with ❤️ for Blackmagic ATEM users**

Repository: https://github.com/kusurix-ux/Atem-picture-tool
