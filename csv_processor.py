"""
CSV Batch Processor for ATEM Media File Generator
Handles batch image generation from CSV files
"""
import csv
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime
import logging

from config import Config
from models.template import Template
from image_generator import ImageGenerator


class CSVRow:
    """Represents a single CSV row with validation"""

    def __init__(self, row_num: int, data: Dict[str, str], template: Template):
        """
        Initialize CSV row

        Args:
            row_num: Row number (1-indexed)
            data: Dictionary of column -> value
            template: Template for validation
        """
        self.row_num = row_num
        self.data = data
        self.template = template
        self.errors = []

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate row against template requirements

        Returns:
            (is_valid: bool, errors: List[str])
        """
        self.errors = []

        # Check required parameters
        for param in self.template.required_parameters:
            if param not in self.data:
                self.errors.append(f"Missing required column: '{param}'")
            elif not self.data[param] or self.data[param].strip() == '':
                self.errors.append(f"Required parameter '{param}' is empty")

        return len(self.errors) == 0, self.errors

    def get_parameters(self) -> Dict[str, str]:
        """
        Get parameters from row, validated

        Returns:
            Dictionary of parameter -> value
        """
        params = {}

        # Include all required parameters
        for param in self.template.required_parameters:
            params[param] = self.data.get(param, '').strip()

        # Include optional parameters if present
        for param in self.template.optional_parameters:
            if param in self.data:
                params[param] = self.data[param].strip()

        return params


class CSVProcessor:
    """Process CSV files for batch image generation"""

    def __init__(self, image_generator: ImageGenerator, output_dir: Optional[str] = None):
        """
        Initialize CSV processor

        Args:
            image_generator: ImageGenerator instance
            output_dir: Output directory (defaults to Config.OUTPUT_DIR)
        """
        self.image_generator = image_generator
        self.output_dir = Path(output_dir or Config.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.log_file = None

    def process_csv(self, csv_filepath: str, template: Template) -> Tuple[bool, str, int, List[str]]:
        """
        Process CSV file and generate images

        Args:
            csv_filepath: Path to CSV file
            template: Template to use for generation

        Returns:
            (success: bool, message: str, images_generated: int, errors: List[str])
        """
        try:
            csv_path = Path(csv_filepath)

            if not csv_path.exists():
                return False, f"CSV file not found: {csv_filepath}", 0, []

            # Create log file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_filename = f"batch_{template.template_type}_{timestamp}.log"
            self.log_file = self.output_dir / log_filename

            # Read CSV file
            rows = self._read_csv(csv_path)
            if not rows:
                return False, "CSV file is empty", 0, []

            # Process rows
            generated_count = 0
            failed_rows = []

            self._log(f"Processing {len(rows)} rows with template: {template.name}")

            for i, row_data in enumerate(rows, start=2):  # Start at 2 (skip header)
                csv_row = CSVRow(i, row_data, template)

                # Validate row
                is_valid, errors = csv_row.validate()
                if not is_valid:
                    failed_rows.extend([f"Row {i}: {error}" for error in errors])
                    self._log(f"Row {i} validation failed: {errors}")
                    continue

                # Generate image
                parameters = csv_row.get_parameters()
                success, error_msg, image = self.image_generator.generate(template, parameters)

                if not success:
                    failed_rows.append(f"Row {i}: Image generation failed - {error_msg}")
                    self._log(f"Row {i} generation failed: {error_msg}")
                    continue

                # Save image
                filename = self._generate_row_filename(template, i, parameters)
                filepath = self.output_dir / filename

                save_success, save_error = self.image_generator.save_png(image, str(filepath))

                if not save_success:
                    failed_rows.append(f"Row {i}: Save failed - {save_error}")
                    self._log(f"Row {i} save failed: {save_error}")
                    continue

                generated_count += 1
                self._log(f"Row {i} → {filename}")

            # Summary
            self._log(f"\nSummary:")
            self._log(f"  Total rows: {len(rows)}")
            self._log(f"  Generated: {generated_count}")
            self._log(f"  Failed: {len(failed_rows)}")

            if failed_rows:
                message = f"Generated {generated_count}/{len(rows)} images. {len(failed_rows)} rows failed."
                return generated_count > 0, message, generated_count, failed_rows
            else:
                message = f"Successfully generated {generated_count} images"
                return True, message, generated_count, []

        except Exception as e:
            error_msg = f"CSV processing failed: {str(e)}"
            self._log(f"Error: {error_msg}")
            return False, error_msg, 0, [error_msg]

    def _read_csv(self, csv_path: Path) -> List[Dict[str, str]]:
        """
        Read CSV file and return list of rows as dictionaries

        Args:
            csv_path: Path to CSV file

        Returns:
            List of dictionaries (column -> value)
        """
        rows = []

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                if not reader.fieldnames:
                    return []

                for row in reader:
                    if row:  # Skip empty rows
                        rows.append(dict(row))

            return rows

        except Exception as e:
            self._log(f"Error reading CSV: {str(e)}")
            return []

    def _generate_row_filename(self, template: Template, row_num: int, parameters: Dict[str, str]) -> str:
        """
        Generate unique filename for row

        Args:
            template: Template object
            row_num: Row number
            parameters: Row parameters

        Returns:
            Filename string
        """
        # Use first parameter value if available
        first_param = next(iter(parameters.values()), '')
        first_param = first_param.replace(' ', '_').replace('/', '_')[:30]  # Limit length

        filename = f"{template.template_type}_{row_num:04d}_{first_param}.png"
        filename = filename.replace('__', '_')

        return filename

    def _log(self, message: str):
        """
        Log message to log file and console

        Args:
            message: Message to log
        """
        # Log to file if available
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')

        # Also log to console
        self.logger.info(message)


class BatchResult:
    """Result of batch processing operation"""

    def __init__(self, success: bool, message: str, generated: int, errors: List[str]):
        """
        Initialize batch result

        Args:
            success: Whether batch processing succeeded
            message: Summary message
            generated: Number of images generated
            errors: List of error messages
        """
        self.success = success
        self.message = message
        self.generated = generated
        self.errors = errors

    def __str__(self) -> str:
        """String representation"""
        return f"BatchResult(success={self.success}, generated={self.generated}, errors={len(self.errors)})"

    def get_summary(self) -> str:
        """Get human-readable summary"""
        summary = f"{self.message}\n\n"

        if self.errors:
            summary += f"Errors ({len(self.errors)}):\n"
            for error in self.errors[:10]:  # Show first 10 errors
                summary += f"  - {error}\n"

            if len(self.errors) > 10:
                summary += f"  ... and {len(self.errors) - 10} more errors\n"

        return summary
