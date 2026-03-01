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
from models.template import Template, TextLayer, ImageLayer
from font_manager import get_font_manager


class ImageGenerator:
    """Core image generation engine using Pillow"""

    def __init__(self):
        """Initialize image generator"""
        self.width = Config.IMAGE_WIDTH
        self.height = Config.IMAGE_HEIGHT
        self.default_font = Config.DEFAULT_FONT
        self.fonts_dir = Path(Config.CUSTOM_FONTS_DIR)

        # Use centralized font manager
        self.font_manager = get_font_manager()

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

            # Sort layers by z_order (draw in order: background to foreground)
            sorted_layers = sorted(template.layers, key=lambda l: getattr(l, 'z_order', 0))

            # Draw each layer
            for layer in sorted_layers:
                if isinstance(layer, ImageLayer):
                    # Draw image layer
                    self._draw_image_layer(image, layer)
                elif isinstance(layer, TextLayer):
                    # Draw text layer
                    text = parameters.get(layer.parameter_key, '')
                    if not text:
                        continue  # Skip empty text

                    # Load font
                    font = self._get_font(layer.font_name, layer.font_size)

                    # Ensure color is a tuple (JSON deserializes as list)
                    color = tuple(layer.color) if isinstance(layer.color, list) else layer.color

                    # Calculate text position based on alignment
                    # Note: Pillow's align parameter only works for multi-line text
                    # For single-line text, we use anchor parameter with calculated positions
                    x, y = layer.x, layer.y
                    anchor = 'lm'  # Default: left-middle

                    # Map alignment to anchor parameter
                    if layer.alignment == 'center':
                        anchor = 'mm'  # middle-middle
                    elif layer.alignment == 'right':
                        anchor = 'rm'  # right-middle
                    else:  # 'left' or default
                        anchor = 'lm'  # left-middle

                    # For center alignment, adjust x to middle of layer width
                    if layer.alignment == 'center':
                        x = layer.x + layer.width // 2
                    elif layer.alignment == 'right':
                        x = layer.x + layer.width

                    # Draw text with alignment support
                    draw.text(
                        xy=(x, y),
                        text=text,
                        font=font,
                        fill=color,  # RGBA tuple
                        anchor=anchor  # Use anchor for proper alignment
                    )

            return True, None, image

        except Exception as e:
            return False, f"Image generation failed: {str(e)}", None

    def _draw_image_layer(self, canvas: Image.Image, layer: ImageLayer):
        """
        Draw image layer on canvas

        Args:
            canvas: PIL Image canvas to draw on (modified in-place)
            layer: ImageLayer to draw
        """
        try:
            # Load image from file
            if not os.path.exists(layer.image_path):
                # Try relative path from project root
                relative_path = Path(Config.BASE_DIR) / layer.image_path
                if relative_path.exists():
                    image_path = relative_path
                else:
                    # Image file not found, skip layer
                    return

            # Open image
            img = Image.open(layer.image_path).convert('RGBA')

            # Resize image to layer dimensions if needed
            if img.size != (layer.width, layer.height):
                img = img.resize((layer.width, layer.height), Image.Resampling.LANCZOS)

            # Apply opacity if not fully opaque
            if layer.opacity < 1.0:
                # Adjust alpha channel by opacity
                alpha = img.split()[3]  # Get alpha channel
                alpha = alpha.point(lambda p: int(p * layer.opacity))  # Scale alpha
                img.putalpha(alpha)

            # Paste image onto canvas at specified position
            canvas.paste(img, (layer.x, layer.y), img)

        except Exception as e:
            # Log error but continue rendering
            print(f"Warning: Failed to draw image layer '{layer.name}': {str(e)}")

    def _get_font(self, font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
        """
        Get font object with intelligent fallback

        Args:
            font_name: Font name to load
            font_size: Font size in pixels

        Returns:
            PIL ImageFont object (with intelligent fallback)
        """
        try:
            # Try custom fonts directory first
            custom_font_path = self.fonts_dir / f"{font_name}.ttf"
            if custom_font_path.exists():
                try:
                    font = ImageFont.truetype(str(custom_font_path), font_size)
                    return font
                except Exception:
                    pass  # Fall through to font manager

            # Use font manager for system fonts (with intelligent matching)
            font = self.font_manager.load_font(font_name, font_size)
            return font

        except Exception as e:
            # Final fallback: use default font
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
