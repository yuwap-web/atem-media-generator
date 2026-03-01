"""
Test script for Phase 2: Image Generation Engine
Tests ImageGenerator and TemplateManager modules
"""
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from image_generator import ImageGenerator
from template_manager import TemplateManager
from config import Config


def test_template_manager():
    """Test template loading and validation"""
    print("=" * 60)
    print("Testing TemplateManager")
    print("=" * 60)

    manager = TemplateManager()

    # Test listing template files
    print("\n1. Listing template files...")
    success, error_msg, filenames = manager.list_template_files()
    if success:
        print(f"   ✓ Found {len(filenames)} templates:")
        for filename in filenames:
            print(f"     - {filename}")
    else:
        print(f"   ✗ Error: {error_msg}")
        return False

    # Test loading all templates
    print("\n2. Loading all templates...")
    success, error_msg, templates = manager.load_all_templates()
    if success:
        print(f"   ✓ Loaded {len(templates)} templates:")
        for template in templates:
            print(f"     - {template.name} ({template.template_type})")
            print(f"       Required parameters: {template.required_parameters}")
            print(f"       Optional parameters: {template.optional_parameters}")
    else:
        print(f"   ✗ Error: {error_msg}")
        return False

    # Test filtering by type
    print("\n3. Filtering templates by type...")
    for template_type in ['title', 'lower_third', 'other']:
        success, error_msg, filtered = manager.get_templates_by_type(template_type)
        if success:
            print(f"   ✓ {template_type}: {len(filtered)} template(s)")
        else:
            print(f"   ℹ {template_type}: No templates found")

    return True


def test_image_generator():
    """Test image generation with sample templates"""
    print("\n" + "=" * 60)
    print("Testing ImageGenerator")
    print("=" * 60)

    generator = ImageGenerator()
    manager = TemplateManager()

    # Load all templates
    success, error_msg, templates = manager.load_all_templates()
    if not success:
        print(f"✗ Failed to load templates: {error_msg}")
        return False

    # Test generating images for each template
    print("\n1. Testing image generation...")

    output_dir = Path(Config.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    for template in templates:
        print(f"\n   Testing: {template.name} ({template.template_type})")

        # Create test parameters
        test_params = {}
        for param in template.required_parameters:
            test_params[param] = f"Test {param}"
        for param in template.optional_parameters:
            test_params[param] = f"Test {param}"

        # Generate image
        success, error_msg, image = generator.generate(template, test_params)
        if success and image:
            print(f"   ✓ Image generated: {image.size} {image.mode}")

            # Save image
            filename = generator.generate_filename(template.name, template.template_type)
            filepath = output_dir / filename

            save_success, save_error = generator.save_png(image, str(filepath))
            if save_success:
                file_size_kb = filepath.stat().st_size / 1024
                print(f"   ✓ Saved to: {filepath} ({file_size_kb:.1f} KB)")
            else:
                print(f"   ✗ Save failed: {save_error}")
                return False
        else:
            print(f"   ✗ Generation failed: {error_msg}")
            return False

    return True


def test_parameter_validation():
    """Test parameter validation"""
    print("\n" + "=" * 60)
    print("Testing Parameter Validation")
    print("=" * 60)

    manager = TemplateManager()

    # Load title template
    success, error_msg, template = manager.load_template('title.json')
    if not success:
        print(f"✗ Failed to load title template: {error_msg}")
        return False

    print(f"\nTemplate: {template.name}")
    print(f"Required parameters: {template.required_parameters}")
    print(f"Optional parameters: {template.optional_parameters}")

    # Test 1: Missing required parameter
    print("\n1. Testing missing required parameter...")
    params = {}
    success, error_msg = template.validate_parameters(params)
    if not success:
        print(f"   ✓ Validation correctly failed: {error_msg}")
    else:
        print(f"   ✗ Validation should have failed")
        return False

    # Test 2: Valid required parameter
    print("\n2. Testing valid required parameter...")
    params = {'title': 'Hello World'}
    success, error_msg = template.validate_parameters(params)
    if success:
        print(f"   ✓ Validation passed")
    else:
        print(f"   ✗ Validation failed: {error_msg}")
        return False

    # Test 3: Valid with optional parameter
    print("\n3. Testing with optional parameter...")
    params = {'title': 'Hello World', 'subtitle': 'This is a subtitle'}
    success, error_msg = template.validate_parameters(params)
    if success:
        print(f"   ✓ Validation passed with optional parameter")
    else:
        print(f"   ✗ Validation failed: {error_msg}")
        return False

    return True


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  ATEM Media File Generator - Phase 2 Tests  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    all_passed = True

    # Run tests
    if not test_template_manager():
        all_passed = False

    if not test_parameter_validation():
        all_passed = False

    if not test_image_generator():
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests PASSED!")
    else:
        print("✗ Some tests FAILED")
    print("=" * 60)

    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
