"""
Font Manager for ATEM Media File Generator
Handles font detection, caching, and fallback
"""
import os
from pathlib import Path
from PIL import ImageFont
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class FontManager:
    """Manages font detection and loading with intelligent fallback"""

    def __init__(self):
        """Initialize font manager"""
        self.font_cache = {}
        self.available_fonts = {}  # Cache of available system fonts
        self._scan_system_fonts()

    def _scan_system_fonts(self):
        """Scan and cache available system fonts"""
        font_dirs = [
            "/Library/Fonts",
            "/System/Library/Fonts",
            "/System/Library/Fonts/Supplemental",
            "/usr/share/fonts/truetype",
            "/usr/share/fonts/opentype",
            "C:\\Windows\\Fonts",  # Windows
        ]

        for font_dir in font_dirs:
            if not os.path.exists(font_dir):
                continue

            try:
                for filename in os.listdir(font_dir):
                    if filename.endswith(('.ttf', '.otf', '.ttc', '.dfont')):
                        # Store full path for quick access
                        font_path = os.path.join(font_dir, filename)
                        # Use filename without extension as key
                        font_name = Path(filename).stem
                        if font_name not in self.available_fonts:
                            self.available_fonts[font_name] = font_path
            except (PermissionError, OSError):
                continue

    def get_available_fonts(self) -> List[str]:
        """Get list of available system fonts"""
        return sorted(list(self.available_fonts.keys()))

    def find_font(self, font_name: str) -> Optional[str]:
        """
        Find font path by name with intelligent matching

        Args:
            font_name: Font name to search for

        Returns:
            Font path if found, None otherwise
        """
        # Exact match
        if font_name in self.available_fonts:
            return self.available_fonts[font_name]

        # Fuzzy match (case-insensitive, partial)
        font_name_lower = font_name.lower()
        for available_name, path in self.available_fonts.items():
            if available_name.lower() == font_name_lower:
                return path
            # Partial match (e.g., "Arial" matches "Arial Black")
            if font_name_lower in available_name.lower():
                return path

        return None

    def load_font(self, font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
        """
        Load font with intelligent fallback

        Args:
            font_name: Font name to load
            font_size: Font size in pixels

        Returns:
            PIL ImageFont object
        """
        cache_key = f"{font_name}_{font_size}"

        # Check cache first
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]

        try:
            # Find font path
            font_path = self.find_font(font_name)

            if font_path and os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    self.font_cache[cache_key] = font
                    return font
                except Exception as e:
                    logger.warning(f"Failed to load font {font_name} from {font_path}: {e}")

        except Exception as e:
            logger.warning(f"Error loading font {font_name}: {e}")

        # Fallback to default font
        logger.warning(f"Font {font_name} not found, using default font")
        default_font = ImageFont.load_default()
        self.font_cache[cache_key] = default_font
        return default_font

    def print_font_report(self):
        """Print available fonts report"""
        print(f"\n{'=' * 60}")
        print(f"Available System Fonts: {len(self.available_fonts)}")
        print(f"{'=' * 60}\n")

        # Group by category
        categories = {
            'Helvetica': [],
            'Arial': [],
            'Times': [],
            'Courier': [],
            'Menlo': [],
            'Monaco': [],
            'Georgia': [],
            'Comic': [],
            'Hiragino': [],
            'Other': []
        }

        for font_name in sorted(self.available_fonts.keys()):
            categorized = False
            for category in categories:
                if category.lower() in font_name.lower():
                    categories[category].append(font_name)
                    categorized = True
                    break
            if not categorized:
                categories['Other'].append(font_name)

        # Print by category
        for category, fonts in categories.items():
            if fonts:
                print(f"{category}:")
                for font in fonts[:5]:  # Show first 5
                    print(f"  ✓ {font}")
                if len(fonts) > 5:
                    print(f"  ... +{len(fonts) - 5} more")
                print()


# Global instance
_font_manager = None


def get_font_manager() -> FontManager:
    """Get global font manager instance"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager
