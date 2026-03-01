"""
Image Generation Engine for ATEM Media File Generator
Uses Pillow (PIL) to generate PNG images with text layers
"""
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional, Dict
from pathlib import Path
import os
from datetime import datetime
from config import Config
from models.template import Template


class ImageGenerator:
    """Core image generation engine using Pillow"""

    def __init__(self):
        """Initialize image generator"""
        self.width = Config.IMAGE_WIDTH
        self.height = Config.IMAGE_HEIGHT
        self.default_font = Config.DEFAULT_FONT
        self.fonts_dir = Path(Config.CUSTOM_FONTS_DIR)

        # Font cache to avoid repeated loading
        self.font_cache = {}

    def generate(self, template: Template, parameters: Dict[str, str]) -> Tuple[bool, Optional[str], Optional[Image.Image]]:
        """
        Generate image from template and parameters

        Args:
            template: Template object defining layout
            parameters: Dict of parameter values (from CSV or user input)

        Returns:
            (success: bool, error_message: str or None, image: PIL.Image or None)
        """
        try:
            # Validate parameters against template requirements
            is_valid, error_msg = template.validate_parameters(parameters)
            if not is_valid:
                return False, error_msg, None

            # Create new image with transparent background (RGBA)
            if template.background_color:
                # Use specified background color - ensure it's a tuple
                bg_color = tuple(template.background_color) if isinstance(template.background_color, list) else template.background_color
            else:
                # Transparent background (0, 0, 0, 0)
                bg_color = (0, 0, 0, 0)

            image = Image.new('RGBA', (self.width, self.height), bg_color)
            draw = ImageDraw.Draw(image)

            # Draw each text layer
            for layer in template.layers:
                # Get text value from parameters
                text = parameters.get(layer.parameter_key, '')

                if not text:
                    continue  # Skip empty text

                # Load font
                font = self._get_font(layer.font_name, layer.font_size)

                # Calculate text position based on alignment
                x, y = layer.x, layer.y

                # Ensure color is a tuple (JSON deserializes as list)
                color = tuple(layer.color) if isinstance(layer.color, list) else layer.color

                # Draw text with specified color
                draw.text(
                    xy=(x, y),
                    text=text,
                    font=font,
                    fill=color,  # RGBA tuple
                    align=layer.alignment
                )

            return True, None, image

        except Exception as e:
            return False, f"Image generation failed: {str(e)}", None

    def _get_font(self, font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
        """
        Get font object with caching

        Args:
            font_name: Font name or path
            font_size: Font size in pixels

        Returns:
            PIL ImageFont object
        """
        cache_key = f"{font_name}_{font_size}"

        if cache_key in self.font_cache:
            return self.font_cache[cache_key]

        try:
            # Try loading from custom fonts directory first
            font_path = self.fonts_dir / f"{font_name}.ttf"
            if font_path.exists():
                font = ImageFont.truetype(str(font_path), font_size)
                self.font_cache[cache_key] = font
                return font

            # Try system fonts (common paths with multiple extensions)
            system_font_paths = [
                # macOS - multiple formats
                f"/Library/Fonts/{font_name}.ttf",
                f"/Library/Fonts/{font_name}.otf",
                f"/System/Library/Fonts/{font_name}.ttf",
                f"/System/Library/Fonts/{font_name}.otf",
                f"/System/Library/Fonts/{font_name}.dfont",
                # macOS Helvetica aliases
                f"/Library/Fonts/Helvetica.ttc",
                f"/System/Library/Fonts/Helvetica.ttc",
                # Linux
                f"/usr/share/fonts/truetype/{font_name.lower()}/{font_name}.ttf",
                f"/usr/share/fonts/opentype/{font_name.lower()}/{font_name}.otf",
                # Windows
                f"C:\\Windows\\Fonts\\{font_name}.ttf",
                f"C:\\Windows\\Fonts\\{font_name}.otf",
            ]

            for path in system_font_paths:
                if os.path.exists(path):
                    try:
                        font = ImageFont.truetype(path, font_size)
                        self.font_cache[cache_key] = font
                        return font
                    except Exception:
                        continue  # Try next path

            # Fallback: use default font
            font = ImageFont.load_default()
            self.font_cache[cache_key] = font
            return font

        except Exception as e:
            # Return default font on error
            return ImageFont.load_default()

    def save_png(self, image: Image.Image, filepath: str) -> Tuple[bool, Optional[str]]:
        """
        Save PIL Image as PNG with RGBA transparency

        Args:
            image: PIL Image object
            filepath: Output file path

        Returns:
            (success: bool, error_message: str or None)
        """
        try:
            # Ensure parent directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            # Save with PNG format preserving RGBA
            image.save(filepath, 'PNG', quality=95)
            return True, None

        except Exception as e:
            return False, f"Failed to save PNG: {str(e)}"

    def generate_filename(self, template_name: str, template_type: str) -> str:
        """
        Generate unique filename for output image

        Args:
            template_name: Name of template
            template_type: Type of template ('title', 'lower_third', 'other')

        Returns:
            Filename string (without path)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{template_type}_{template_name}_{timestamp}.png"

        # Replace spaces and special characters
        filename = filename.replace(' ', '_').replace('/', '_')

        return filename
