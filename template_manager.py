"""
Template Manager for ATEM Media File Generator
Handles JSON template file I/O and management
"""
import json
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from config import Config
from models.template import Template, TextLayer


class TemplateManager:
    """Manage template file loading, saving, and validation"""

    def __init__(self):
        """Initialize template manager"""
        self.template_dir = Path(Config.TEMPLATE_DIR)
        self.template_dir.mkdir(parents=True, exist_ok=True)

    def load_all_templates(self) -> Tuple[bool, Optional[str], List[Template]]:
        """
        Load all templates from template directory

        Returns:
            (success: bool, error_message: str or None, templates: List[Template])
        """
        try:
            templates = []

            # Find all JSON files in template directory
            json_files = list(self.template_dir.glob('*.json'))

            if not json_files:
                return False, f"No templates found in {self.template_dir}", []

            for json_file in json_files:
                success, error_msg, template = self.load_template(json_file.name)
                if success and template:
                    templates.append(template)
                else:
                    # Log error but continue loading other templates
                    print(f"Warning: Failed to load {json_file.name}: {error_msg}")

            if not templates:
                return False, "No valid templates could be loaded", []

            return True, None, templates

        except Exception as e:
            return False, f"Failed to load templates: {str(e)}", []

    def load_template(self, filename: str) -> Tuple[bool, Optional[str], Optional[Template]]:
        """
        Load single template from JSON file

        Args:
            filename: Template filename (e.g., 'title.json')

        Returns:
            (success: bool, error_message: str or None, template: Template or None)
        """
        try:
            filepath = self.template_dir / filename

            if not filepath.exists():
                return False, f"Template file not found: {filepath}", None

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert dict to Template object
            template = Template.from_dict(data)

            return True, None, template

        except json.JSONDecodeError as e:
            return False, f"Invalid JSON in {filename}: {str(e)}", None
        except Exception as e:
            return False, f"Failed to load template {filename}: {str(e)}", None

    def save_template(self, template: Template, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Save template to JSON file

        Args:
            template: Template object to save
            filename: Output filename (e.g., 'custom.json')

        Returns:
            (success: bool, error_message: str or None)
        """
        try:
            filepath = self.template_dir / filename

            # Convert template to dict
            data = template.to_dict()

            # Write to JSON file with pretty printing
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True, None

        except Exception as e:
            return False, f"Failed to save template: {str(e)}"

    def get_templates_by_type(self, template_type: str) -> Tuple[bool, Optional[str], List[Template]]:
        """
        Load templates filtered by type

        Args:
            template_type: Type to filter ('title', 'lower_third', 'other')

        Returns:
            (success: bool, error_message: str or None, templates: List[Template])
        """
        success, error_msg, all_templates = self.load_all_templates()

        if not success:
            return success, error_msg, []

        # Filter by type
        filtered = [t for t in all_templates if t.template_type == template_type]

        if not filtered:
            return False, f"No templates found with type '{template_type}'", []

        return True, None, filtered

    def validate_template_file(self, filepath: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate JSON template file structure

        Args:
            filepath: Path to template JSON file

        Returns:
            (success: bool, error_message: str or None)
        """
        try:
            if not filepath.exists():
                return False, f"File not found: {filepath}"

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check required fields
            required_fields = ['name', 'template_type', 'layers']
            for field in required_fields:
                if field not in data:
                    return False, f"Missing required field: '{field}'"

            # Validate template_type
            if data['template_type'] not in Config.SUPPORTED_TEMPLATE_TYPES:
                return False, f"Invalid template_type: {data['template_type']}"

            # Try to create Template object (validates structure)
            template = Template.from_dict(data)

            return True, None

        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return False, f"Validation failed: {str(e)}"

    def delete_template(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Delete template file

        Args:
            filename: Template filename to delete

        Returns:
            (success: bool, error_message: str or None)
        """
        try:
            filepath = self.template_dir / filename

            if not filepath.exists():
                return False, f"Template file not found: {filepath}"

            filepath.unlink()
            return True, None

        except Exception as e:
            return False, f"Failed to delete template: {str(e)}"

    def list_template_files(self) -> Tuple[bool, Optional[str], List[str]]:
        """
        List all template filenames in template directory

        Returns:
            (success: bool, error_message: str or None, filenames: List[str])
        """
        try:
            if not self.template_dir.exists():
                return False, f"Template directory not found: {self.template_dir}", []

            json_files = [f.name for f in self.template_dir.glob('*.json')]

            if not json_files:
                return False, "No template files found", []

            return True, None, sorted(json_files)

        except Exception as e:
            return False, f"Failed to list templates: {str(e)}", []
