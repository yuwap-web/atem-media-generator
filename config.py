"""
ATEM Media File Generator - Configuration Management
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""

    # Output Settings
    OUTPUT_DIR = os.getenv('ATEM_OUTPUT_DIR', './output')
    IMAGE_WIDTH = 1920
    IMAGE_HEIGHT = 1080

    # Template Settings
    TEMPLATE_DIR = os.getenv('ATEM_TEMPLATE_DIR', './templates')
    SUPPORTED_TEMPLATE_TYPES = ['title', 'lower_third', 'other']

    # Font Settings
    DEFAULT_FONT = os.getenv('ATEM_DEFAULT_FONT', 'Helvetica')
    CUSTOM_FONTS_DIR = './fonts'

    # ATEM Device Settings (for future use)
    ATEM_IP = os.getenv('ATEM_IP', '')
    ATEM_PORT = int(os.getenv('ATEM_PORT', '20990'))
    ATEM_MEDIA_POOL_INDEX = 0

    # GUI Settings
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 800
    PREVIEW_UPDATE_MODE = 'realtime'  # リアルタイム更新（パラメータ変更時に自動更新）

    @classmethod
    def validate(cls) -> tuple:
        """Validate configuration

        Returns:
            (validation_success, error_message)
        """
        if not os.path.exists(cls.OUTPUT_DIR):
            try:
                os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
            except Exception as e:
                return False, f"Failed to create output directory: {str(e)}"

        if not os.path.exists(cls.TEMPLATE_DIR):
            return False, f"Template directory not found: {cls.TEMPLATE_DIR}"

        return True, "Configuration OK"
