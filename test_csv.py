"""
Test script for Phase 4: CSV Batch Processing
Tests CSVProcessor and batch image generation
"""
import sys
import csv
from pathlib import Path
from tempfile import TemporaryDirectory

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from csv_processor import CSVProcessor, CSVRow, BatchResult
from template_manager import TemplateManager
from image_generator import ImageGenerator


def create_test_csv(filepath: Path, num_rows: int = 5) -> Path:
    """Create test CSV file"""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'subtitle'])
        writer.writeheader()

        for i in range(1, num_rows + 1):
            writer.writerow({
                'title': f'Test Title {i}',
                'subtitle': f'Test Subtitle {i}'
            })

    return filepath


def test_csv_row_validation():
    """Test CSV row validation"""
    print("=" * 60)
    print("Testing CSV Row Validation")
    print("=" * 60)

    # Load template
    manager = TemplateManager()
    success, error_msg, template = manager.load_template('title.json')
    if not success:
        print(f"✗ Failed to load template: {error_msg}")
        return False

    # Test 1: Valid row
    print("\n1. Testing valid row...")
    row_data = {'title': 'Test Title', 'subtitle': 'Test Subtitle'}
    csv_row = CSVRow(2, row_data, template)
    is_valid, errors = csv_row.validate()

    if is_valid:
        print(f"   ✓ Row validation passed")
    else:
        print(f"   ✗ Row validation failed: {errors}")
        return False

    # Test 2: Missing required parameter
    print("\n2. Testing missing required parameter...")
    row_data = {'subtitle': 'Test Subtitle'}  # Missing 'title'
    csv_row = CSVRow(3, row_data, template)
    is_valid, errors = csv_row.validate()

    if not is_valid:
        print(f"   ✓ Correctly detected missing parameter")
    else:
        print(f"   ✗ Should have detected missing parameter")
        return False

    # Test 3: Get parameters from row
    print("\n3. Testing parameter extraction...")
    row_data = {'title': 'Test Title', 'subtitle': 'Test Subtitle', 'extra': 'Extra'}
    csv_row = CSVRow(4, row_data, template)
    params = csv_row.get_parameters()

    if 'title' in params and 'subtitle' in params:
        print(f"   ✓ Parameters extracted correctly")
    else:
        print(f"   ✗ Parameter extraction failed")
        return False

    return True


def test_csv_processor():
    """Test CSV processor batch generation"""
    print("\n" + "=" * 60)
    print("Testing CSV Processor - Batch Generation")
    print("=" * 60)

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create test CSV file
        csv_file = tmpdir / "test_batch.csv"
        create_test_csv(csv_file, num_rows=5)

        print(f"\n1. Created test CSV file: {csv_file}")
        print(f"   Rows: 5 test entries")

        # Load template
        manager = TemplateManager()
        success, error_msg, template = manager.load_template('title.json')
        if not success:
            print(f"   ✗ Failed to load template: {error_msg}")
            return False

        # Create processor
        image_gen = ImageGenerator()
        processor = CSVProcessor(image_gen, output_dir=str(tmpdir))

        # Process CSV
        print("\n2. Processing CSV file...")
        success, message, generated, errors = processor.process_csv(str(csv_file), template)

        print(f"   Generated: {generated} images")
        print(f"   Errors: {len(errors)}")
        print(f"   Message: {message}")

        if generated > 0:
            print(f"   ✓ Batch processing succeeded")
        else:
            print(f"   ✗ No images were generated")
            return False

        # Verify output files
        print("\n3. Verifying output files...")
        output_files = list(tmpdir.glob("title_*.png"))
        print(f"   Generated {len(output_files)} PNG files")

        for png_file in output_files:
            file_size_kb = png_file.stat().st_size / 1024
            print(f"   - {png_file.name} ({file_size_kb:.1f} KB)")

        if len(output_files) == generated:
            print(f"   ✓ All output files verified")
            return True
        else:
            print(f"   ✗ Output file count mismatch")
            return False


def test_batch_result():
    """Test BatchResult class"""
    print("\n" + "=" * 60)
    print("Testing BatchResult")
    print("=" * 60)

    # Test success case
    result = BatchResult(
        success=True,
        message="Successfully generated 5 images",
        generated=5,
        errors=[]
    )

    print(f"\n1. Success result:")
    print(f"   {result}")
    print(f"   Summary:\n{result.get_summary()}")

    # Test partial success case
    result = BatchResult(
        success=True,
        message="Generated 4/5 images",
        generated=4,
        errors=["Row 3: Missing required parameter 'title'"]
    )

    print(f"\n2. Partial success result:")
    print(f"   {result}")
    print(f"   Summary:\n{result.get_summary()}")

    return True


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  ATEM Media File Generator - Phase 4 CSV Tests  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    all_passed = True

    if not test_csv_row_validation():
        all_passed = False

    if not test_csv_processor():
        all_passed = False

    if not test_batch_result():
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All CSV tests PASSED!")
    else:
        print("✗ Some CSV tests FAILED")
    print("=" * 60)

    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
