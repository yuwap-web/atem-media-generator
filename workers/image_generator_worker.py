"""
Image Generator Worker for ATEM Media File Generator
QThread worker for non-blocking image generation
"""
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PIL import Image
from typing import Dict

from models.template import Template
from image_generator import ImageGenerator


class ImageGeneratorWorker(QObject):
    """Worker thread for image generation"""

    # Signals
    finished = pyqtSignal(Image.Image)  # Emitted with generated image
    error = pyqtSignal(str)  # Emitted with error message
    progress = pyqtSignal(int)  # Emitted with progress percentage

    def __init__(self, template: Template, parameters: Dict[str, str], image_generator: ImageGenerator):
        """
        Initialize worker

        Args:
            template: Template to generate from
            parameters: Parameter values
            image_generator: ImageGenerator instance
        """
        super().__init__()

        self.template = template
        self.parameters = parameters
        self.image_generator = image_generator

    def run(self):
        """Run image generation in worker thread"""
        try:
            self.progress.emit(10)

            # Generate image
            success, error_msg, image = self.image_generator.generate(
                self.template,
                self.parameters
            )

            self.progress.emit(90)

            if success and image:
                self.progress.emit(100)
                self.finished.emit(image)
            else:
                error = error_msg or "Unknown error during image generation"
                self.error.emit(error)

        except Exception as e:
            self.error.emit(f"Worker error: {str(e)}")
