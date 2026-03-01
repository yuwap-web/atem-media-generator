"""
ATEM Media File Generator - PyQt5 Desktop Application
Main window and application entry point
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLabel, QPushButton, QToolBar,
    QStatusBar, QMessageBox, QFileDialog, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from config import Config
from template_manager import TemplateManager
from image_generator import ImageGenerator
from csv_processor import CSVProcessor
from ui.parameter_editor import ParameterEditorPanel
from ui.preview_panel import PreviewPanel
from workers.image_generator_worker import ImageGeneratorWorker
from workers.csv_batch_worker import CSVBatchWorker


class ATEMMediaGeneratorApp(QMainWindow):
    """Main application window for ATEM Media File Generator"""

    def __init__(self):
        """Initialize main application window"""
        super().__init__()

        # Initialize managers
        self.template_manager = TemplateManager()
        self.image_generator = ImageGenerator()

        # Worker thread
        self.generator_worker = None
        self.worker_thread = None

        # Current state
        self.current_template = None
        self.current_parameters = {}

        # Setup UI
        self.init_ui()

        # Validate configuration
        valid, msg = Config.validate()
        if not valid:
            QMessageBox.warning(self, "Configuration Error", msg)

        # Load templates
        self.load_templates()

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("ATEM Media File Generator")
        self.setGeometry(100, 100, 1400, 800)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left Panel: Template List
        left_panel = self.create_left_panel()

        # Middle Panel: Parameter Editor
        self.parameter_editor = ParameterEditorPanel()
        self.parameter_editor.parameter_changed.connect(self.on_parameter_changed)

        # Right Panel: Preview
        self.preview_panel = PreviewPanel()

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.parameter_editor)
        splitter.addWidget(self.preview_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 1)

        main_layout.addWidget(splitter)

        # Create toolbar
        self.create_toolbar()

        # Create status bar
        self.statusBar().showMessage("Ready")

    def create_left_panel(self) -> QWidget:
        """Create left panel with template list"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title label
        title = QLabel("Templates")
        layout.addWidget(title)

        # Template list
        self.template_list = QListWidget()
        self.template_list.itemClicked.connect(self.on_template_selected)
        layout.addWidget(self.template_list)

        # Refresh button
        refresh_btn = QPushButton("Refresh Templates")
        refresh_btn.clicked.connect(self.load_templates)
        layout.addWidget(refresh_btn)

        return widget

    def create_toolbar(self):
        """Create toolbar with action buttons"""
        toolbar = QToolBar("Actions")
        self.addToolBar(toolbar)

        # Save button
        save_btn = QPushButton("Save PNG")
        save_btn.clicked.connect(self.on_save_png)
        toolbar.addWidget(save_btn)

        toolbar.addSeparator()

        # Export CSV button
        export_btn = QPushButton("Batch Export (CSV)")
        export_btn.clicked.connect(self.on_export_csv)
        toolbar.addWidget(export_btn)

        toolbar.addSeparator()

        # Settings button
        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.on_settings)
        toolbar.addWidget(settings_btn)

        toolbar.addSeparator()

        # Status label
        self.status_label = QLabel("Ready")
        toolbar.addWidget(self.status_label)

    def load_templates(self):
        """Load templates from template directory"""
        self.statusBar().showMessage("Loading templates...")
        self.template_list.clear()

        success, error_msg, templates = self.template_manager.load_all_templates()

        if success:
            for template in templates:
                item = QListWidgetItem(f"{template.name} ({template.template_type})")
                item.setData(Qt.UserRole, template)
                self.template_list.addItem(item)

            self.statusBar().showMessage(f"Loaded {len(templates)} templates")
        else:
            QMessageBox.critical(self, "Error", f"Failed to load templates: {error_msg}")
            self.statusBar().showMessage("Error loading templates")

    def on_template_selected(self, item: QListWidgetItem):
        """Handle template selection"""
        self.current_template = item.data(Qt.UserRole)
        self.current_parameters = {}

        # Load template into parameter editor
        self.parameter_editor.load_template(self.current_template)

        self.statusBar().showMessage(f"Template: {self.current_template.name}")

        # Generate preview with default parameters
        self.generate_preview()

    def on_parameter_changed(self, parameters: dict):
        """Handle parameter changes - trigger realtime preview"""
        self.current_parameters = parameters

        if Config.PREVIEW_UPDATE_MODE == 'realtime' and self.current_template:
            self.generate_preview()

    def generate_preview(self):
        """Generate image preview in background thread"""
        if not self.current_template:
            return

        # Disable UI during generation
        self.parameter_editor.setEnabled(False)
        self.statusBar().showMessage("Generating preview...")

        # Create worker thread
        self.worker_thread = QThread()
        self.generator_worker = ImageGeneratorWorker(
            self.current_template,
            self.current_parameters,
            self.image_generator
        )

        self.generator_worker.moveToThread(self.worker_thread)
        self.generator_worker.finished.connect(self.on_preview_generated)
        self.generator_worker.error.connect(self.on_preview_error)
        self.worker_thread.started.connect(self.generator_worker.run)

        self.worker_thread.start()

    def on_preview_generated(self, image):
        """Handle preview image generation complete"""
        # Display preview
        self.preview_panel.display_image(image)

        self.statusBar().showMessage("Preview ready")
        self.parameter_editor.setEnabled(True)

        # Cleanup thread
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()

    def on_preview_error(self, error_msg: str):
        """Handle preview generation error"""
        self.statusBar().showMessage(f"Error: {error_msg}")
        self.parameter_editor.setEnabled(True)

        # Cleanup thread
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()

    def on_save_png(self):
        """Save current preview as PNG"""
        if not self.current_template or self.preview_panel.current_image is None:
            QMessageBox.warning(self, "Warning", "No image to save. Please generate an image first.")
            return

        # Open save dialog
        filename = self.image_generator.generate_filename(
            self.current_template.name,
            self.current_template.template_type
        )

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save PNG Image",
            str(Path(Config.OUTPUT_DIR) / filename),
            "PNG Images (*.png)"
        )

        if not filepath:
            return  # User cancelled

        # Save image
        success, error_msg = self.image_generator.save_png(
            self.preview_panel.current_image,
            filepath
        )

        if success:
            self.statusBar().showMessage(f"Saved: {Path(filepath).name}")
            QMessageBox.information(self, "Success", f"Image saved to:\n{filepath}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to save image:\n{error_msg}")

    def on_export_csv(self):
        """Open CSV batch export dialog"""
        # Check if a template is selected
        if not self.current_template:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select a template first before batch processing."
            )
            return

        # Open file dialog to select CSV file
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV File for Batch Processing",
            str(Path.home()),
            "CSV Files (*.csv)"
        )

        if not filepath:
            return  # User cancelled

        # Confirm batch processing
        reply = QMessageBox.question(
            self,
            "Confirm Batch Processing",
            f"Process CSV file with template: {self.current_template.name}?\n\n"
            f"File: {Path(filepath).name}\n"
            f"Output: {Config.OUTPUT_DIR}",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # Start batch processing
        self.start_csv_batch_processing(filepath)

    def start_csv_batch_processing(self, csv_filepath: str):
        """
        Start CSV batch processing in background thread

        Args:
            csv_filepath: Path to CSV file
        """
        self.statusBar().showMessage(f"Processing CSV: {Path(csv_filepath).name}")

        # Create worker thread
        self.worker_thread = QThread()
        self.generator_worker = CSVBatchWorker(
            csv_filepath,
            self.current_template,
            self.image_generator,
            Config.OUTPUT_DIR
        )

        self.generator_worker.moveToThread(self.worker_thread)
        self.generator_worker.finished.connect(self.on_csv_batch_finished)
        self.generator_worker.error.connect(self.on_csv_batch_error)
        self.worker_thread.started.connect(self.generator_worker.run)

        self.worker_thread.start()

    def on_csv_batch_finished(self, num_generated: int):
        """Handle CSV batch processing complete"""
        message = f"Batch processing complete!\nGenerated {num_generated} images."
        self.statusBar().showMessage(message)

        QMessageBox.information(
            self,
            "Batch Processing Complete",
            f"{message}\n\n"
            f"Output directory: {Config.OUTPUT_DIR}"
        )

        # Cleanup thread
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()

    def on_csv_batch_error(self, error_msg: str):
        """Handle CSV batch processing error"""
        self.statusBar().showMessage(f"Batch processing failed")

        QMessageBox.critical(
            self,
            "Batch Processing Error",
            f"An error occurred during batch processing:\n\n{error_msg}"
        )

        # Cleanup thread
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()

    def on_settings(self):
        """Open settings dialog"""
        # TODO: Implement settings dialog
        QMessageBox.information(
            self,
            "Settings",
            "Settings dialog will be implemented in future version"
        )

    def closeEvent(self, event):
        """Handle application close"""
        # Stop worker thread if running
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()

        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Apply stylesheet (optional)
    # app.setStyle('Fusion')

    # Create and show main window
    window = ATEMMediaGeneratorApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
