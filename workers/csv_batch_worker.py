"""
CSV Batch Processor Worker for ATEM Media File Generator
QThread worker for non-blocking CSV batch processing
"""
from PyQt5.QtCore import QObject, pyqtSignal
from pathlib import Path

from csv_processor import CSVProcessor
from models.template import Template
from image_generator import ImageGenerator


class CSVBatchWorker(QObject):
    """Worker thread for CSV batch processing"""

    # Signals
    finished = pyqtSignal(int)  # Emitted with number of images generated
    error = pyqtSignal(str)  # Emitted with error message
    progress = pyqtSignal(int)  # Emitted with progress percentage
    row_complete = pyqtSignal(int, str)  # Emitted with row number and filename

    def __init__(self, csv_filepath: str, template: Template, image_generator: ImageGenerator, output_dir: str):
        """
        Initialize worker

        Args:
            csv_filepath: Path to CSV file
            template: Template to use for generation
            image_generator: ImageGenerator instance
            output_dir: Output directory
        """
        super().__init__()

        self.csv_filepath = csv_filepath
        self.template = template
        self.image_generator = image_generator
        self.output_dir = output_dir

    def run(self):
        """Run CSV batch processing in worker thread"""
        try:
            self.progress.emit(5)

            # Create processor
            processor = CSVProcessor(self.image_generator, output_dir=self.output_dir)

            # Process CSV
            success, message, generated, errors = processor.process_csv(
                self.csv_filepath,
                self.template
            )

            self.progress.emit(95)

            if success or generated > 0:
                self.progress.emit(100)
                self.finished.emit(generated)
            else:
                error_msg = message or "CSV processing failed"
                self.error.emit(error_msg)

        except Exception as e:
            self.error.emit(f"CSV processing error: {str(e)}")
