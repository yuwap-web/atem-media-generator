"""
Test script for Phase 3: PyQt5 GUI
Tests application initialization and UI components
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all GUI modules can be imported"""
    print("Testing imports...")

    try:
        from main import ATEMMediaGeneratorApp
        from ui.parameter_editor import ParameterEditorPanel
        from ui.preview_panel import PreviewPanel
        from workers.image_generator_worker import ImageGeneratorWorker
        from template_manager import TemplateManager
        from image_generator import ImageGenerator

        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {str(e)}")
        return False


def test_ui_components():
    """Test UI components without displaying"""
    print("\nTesting UI components...")

    try:
        from PyQt5.QtWidgets import QApplication
        from ui.parameter_editor import ParameterEditorPanel
        from ui.preview_panel import PreviewPanel
        from models.template import Template, TextLayer

        # Create QApplication (required for PyQt5)
        app = QApplication.instance() or QApplication([])

        # Test ParameterEditorPanel
        print("  - Testing ParameterEditorPanel...")
        param_editor = ParameterEditorPanel()

        # Create test template
        test_template = Template(
            name="Test Template",
            template_type="title",
            background_color=(0, 0, 0, 255),
            layers=[
                TextLayer(
                    name="Title",
                    x=100, y=400,
                    width=1720, height=200,
                    font_name="Helvetica",
                    font_size=80,
                    color=(255, 255, 255, 255),
                    alignment="center",
                    parameter_key="title"
                )
            ],
            required_parameters=["title"],
            optional_parameters=[]
        )

        # Load template
        param_editor.load_template(test_template)
        params = param_editor.get_parameters()

        if "title" in params:
            print("    ✓ ParameterEditorPanel works")
        else:
            print("    ✗ ParameterEditorPanel failed")
            return False

        # Test PreviewPanel
        print("  - Testing PreviewPanel...")
        preview_panel = PreviewPanel()

        # Create test image
        from PIL import Image
        test_image = Image.new('RGBA', (1920, 1080), (0, 0, 0, 255))
        preview_panel.display_image(test_image)

        if preview_panel.current_image is not None:
            print("    ✓ PreviewPanel works")
        else:
            print("    ✗ PreviewPanel failed")
            return False

        # Test ImageGeneratorWorker
        print("  - Testing ImageGeneratorWorker...")
        from image_generator import ImageGenerator
        from workers.image_generator_worker import ImageGeneratorWorker

        image_gen = ImageGenerator()
        worker = ImageGeneratorWorker(test_template, {"title": "Test"}, image_gen)

        if worker is not None:
            print("    ✓ ImageGeneratorWorker created")
        else:
            print("    ✗ ImageGeneratorWorker failed")
            return False

        return True

    except Exception as e:
        print(f"✗ UI component test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_template_loading():
    """Test that templates load correctly"""
    print("\nTesting template loading...")

    try:
        from template_manager import TemplateManager

        manager = TemplateManager()
        success, error_msg, templates = manager.load_all_templates()

        if success:
            print(f"✓ Loaded {len(templates)} templates")
            for template in templates:
                print(f"  - {template.name}")
            return True
        else:
            print(f"✗ Failed to load templates: {error_msg}")
            return False

    except Exception as e:
        print(f"✗ Template loading test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  ATEM Media File Generator - Phase 3 GUI Tests  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    all_passed = True

    if not test_imports():
        all_passed = False

    if not test_template_loading():
        all_passed = False

    if not test_ui_components():
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All GUI tests PASSED!")
        print("\nTo run the application:")
        print("  python main.py")
    else:
        print("✗ Some GUI tests FAILED")
    print("=" * 60)

    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
