"""
Preview Panel for ATEM Media File Generator
Displays generated image preview
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QImage
from PIL import Image
import io


class PreviewPanel(QWidget):
    """Panel for displaying image preview"""

    def __init__(self):
        """Initialize preview panel"""
        super().__init__()

        self.current_image = None
        self.preview_label = None

        self.init_ui()

    def init_ui(self):
        """Initialize user interface"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Preview")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Image preview area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background-color: #2a2a2a; }")

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("QLabel { background-color: #2a2a2a; color: #888; }")

        scroll.setWidget(self.preview_label)
        layout.addWidget(scroll)

        # Update placeholder
        self.show_placeholder()

    def show_placeholder(self):
        """Show placeholder image"""
        self.preview_label.setText("No preview available\n\nSelect a template and enter parameters to generate preview")
        self.preview_label.setMinimumHeight(400)

    def display_image(self, image: Image.Image):
        """
        Display PIL image in preview area

        Args:
            image: PIL Image object to display
        """
        self.current_image = image

        try:
            # Scale image to fit in preview area while maintaining aspect ratio
            max_width = 600
            max_height = 400

            # Calculate scale factor
            scale_factor = min(max_width / image.width, max_height / image.height, 1.0)
            new_size = (int(image.width * scale_factor), int(image.height * scale_factor))

            # Resize image for preview
            preview_image = image.resize(new_size, Image.Resampling.LANCZOS)

            # Convert PIL Image to QPixmap
            # Convert to RGB if necessary (QPixmap doesn't handle RGBA directly in all cases)
            if preview_image.mode == 'RGBA':
                # Create a white background
                background = Image.new('RGB', preview_image.size, (255, 255, 255))
                background.paste(preview_image, mask=preview_image.split()[3])  # Use alpha as mask
                preview_image = background

            # Convert to bytes and then to QPixmap
            image_data = io.BytesIO()
            preview_image.save(image_data, format='PPM')
            image_data.seek(0)

            # Create QPixmap from bytes
            pixmap = QPixmap()
            pixmap.loadFromData(image_data.read(), 'PPM')

            # Display
            self.preview_label.setPixmap(pixmap)

        except Exception as e:
            self.preview_label.setText(f"Error displaying image: {str(e)}")

    def clear_preview(self):
        """Clear preview"""
        self.current_image = None
        self.show_placeholder()
