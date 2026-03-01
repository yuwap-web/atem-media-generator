"""
Integration Test for ATEM Media File Generator
Tests complete workflow: template → parameters → preview → save → batch
"""
import sys
import csv
from pathlib import Path
from tempfile import TemporaryDirectory

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from template_manager import TemplateManager
from image_generator import ImageGenerator
from csv_processor import CSVProcessor


def test_complete_workflow():
    """Test complete workflow from template to batch processing"""
    print("=" * 60)
    print("Integration Test: Complete Workflow")
    print("=" * 60)

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # 1. Load template
        print("\n1. Loading template...")
        manager = TemplateManager()
        success, error_msg, template = manager.load_template('title.json')

        if not success:
            print(f"   ✗ Failed to load template: {error_msg}")
            return False

        print(f"   ✓ Loaded: {template.name}")
        print(f"     Type: {template.template_type}")
        print(f"     Required: {template.required_parameters}")
        print(f"     Optional: {template.optional_parameters}")

        # 2. Generate single image with parameters
        print("\n2. Generating single image...")
        image_gen = ImageGenerator()

        parameters = {
            'title': 'Welcome to ATEM Generator',
            'subtitle': 'This is a test subtitle'
        }

        success, error_msg, image = image_gen.generate(template, parameters)

        if not success:
            print(f"   ✗ Image generation failed: {error_msg}")
            return False

        print(f"   ✓ Image generated: {image.size} {image.mode}")

        # 3. Save single image
        print("\n3. Saving single image...")
        output_file = tmpdir / "single_test.png"

        success, error_msg = image_gen.save_png(image, str(output_file))

        if not success:
            print(f"   ✗ Failed to save: {error_msg}")
            return False

        file_size_kb = output_file.stat().st_size / 1024
        print(f"   ✓ Saved: {output_file.name} ({file_size_kb:.1f} KB)")

        # 4. Create test CSV file
        print("\n4. Creating batch CSV file...")
        csv_file = tmpdir / "batch_test.csv"

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'subtitle'])
            writer.writeheader()

            test_rows = [
                {'title': 'Frame 1', 'subtitle': 'Opening'},
                {'title': 'Frame 2', 'subtitle': 'Content'},
                {'title': 'Frame 3', 'subtitle': 'Closing'},
            ]

            writer.writerows(test_rows)

        print(f"   ✓ Created CSV with 3 rows")

        # 5. Batch process CSV
        print("\n5. Batch processing CSV...")
        processor = CSVProcessor(image_gen, output_dir=str(tmpdir))

        success, message, generated, errors = processor.process_csv(
            str(csv_file),
            template
        )

        print(f"   Message: {message}")

        if generated == 0:
            print(f"   ✗ No images generated from CSV")
            return False

        print(f"   ✓ Generated {generated} images from CSV")

        # 6. Verify output files
        print("\n6. Verifying output files...")
        png_files = list(tmpdir.glob("*.png"))

        expected_files = 1 + generated  # 1 single + batch
        if len(png_files) != expected_files:
            print(f"   ✗ Expected {expected_files} PNG files, found {len(png_files)}")
            return False

        print(f"   ✓ Found {len(png_files)} PNG files:")
        for png_file in sorted(png_files):
            file_size_kb = png_file.stat().st_size / 1024
            print(f"     - {png_file.name} ({file_size_kb:.1f} KB)")

        return True


def test_all_template_types():
    """Test workflow with all available templates"""
    print("\n" + "=" * 60)
    print("Testing All Template Types")
    print("=" * 60)

    manager = TemplateManager()
    image_gen = ImageGenerator()

    # Get all templates
    success, error_msg, templates = manager.load_all_templates()
    if not success:
        print(f"✗ Failed to load templates: {error_msg}")
        return False

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        print(f"\nTesting {len(templates)} templates...\n")

        for i, template in enumerate(templates, 1):
            print(f"{i}. {template.name} ({template.template_type})")

            # Create test parameters
            test_params = {}
            for param in template.required_parameters:
                test_params[param] = f"Test {param}"
            for param in template.optional_parameters:
                test_params[param] = f"Optional {param}"

            # Generate image
            success, error_msg, image = image_gen.generate(template, test_params)

            if not success:
                print(f"   ✗ Failed: {error_msg}")
                return False

            # Save image
            filename = f"test_{template.template_type}_{i}.png"
            filepath = tmpdir / filename

            save_success, save_error = image_gen.save_png(image, str(filepath))

            if not save_success:
                print(f"   ✗ Save failed: {save_error}")
                return False

            file_size_kb = filepath.stat().st_size / 1024
            print(f"   ✓ Generated and saved ({file_size_kb:.1f} KB)")

    return True


def test_parameter_variations():
    """Test template with various parameter values"""
    print("\n" + "=" * 60)
    print("Testing Parameter Variations")
    print("=" * 60)

    manager = TemplateManager()
    image_gen = ImageGenerator()

    success, error_msg, template = manager.load_template('title.json')
    if not success:
        print(f"✗ Failed to load template: {error_msg}")
        return False

    print(f"\nTemplate: {template.name}\n")

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        test_cases = [
            {
                'name': 'Simple text',
                'params': {'title': 'Hello World'},
            },
            {
                'name': 'Long title',
                'params': {'title': 'This is a very long title that might wrap across multiple lines in the image'},
            },
            {
                'name': 'Title with special chars',
                'params': {'title': 'Special: @#$% & Chars!'},
            },
            {
                'name': 'With subtitle',
                'params': {'title': 'Main Title', 'subtitle': 'Supporting Subtitle'},
            },
            {
                'name': 'Empty optional',
                'params': {'title': 'Title Only'},
            },
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(f"{i}. {test_case['name']}")

            success, error_msg, image = image_gen.generate(template, test_case['params'])

            if not success:
                print(f"   ✗ Failed: {error_msg}")
                return False

            # Save
            filename = f"variation_{i:02d}.png"
            filepath = tmpdir / filename
            image_gen.save_png(image, str(filepath))

            print(f"   ✓ Generated and saved")

    return True


def main():
    """Run all integration tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  ATEM Media File Generator - Integration Tests  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    all_passed = True

    if not test_complete_workflow():
        all_passed = False

    if not test_all_template_types():
        all_passed = False

    if not test_parameter_variations():
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All integration tests PASSED!")
        print("\nApplication is ready for:")
        print("  - GUI testing (python main.py)")
        print("  - Distribution/Building")
    else:
        print("✗ Some integration tests FAILED")
    print("=" * 60)

    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
