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
from ui.template_customizer import TemplateCustomizer
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
            QMessageBox.warning(self, "設定エラー", msg)

        # Load templates
        self.load_templates()

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("ATEM メディアファイルジェネレーター")
        self.setGeometry(100, 100, 1600, 900)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left Panel: Template List
        left_panel = self.create_left_panel()

        # Middle Panel: Parameter Editor & Template Customizer
        middle_panel = self.create_middle_panel()

        # Right Panel: Preview
        self.preview_panel = PreviewPanel()

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(middle_panel)
        splitter.addWidget(self.preview_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 1)

        main_layout.addWidget(splitter)

        # Create toolbar
        self.create_toolbar()

        # Create status bar
        self.statusBar().showMessage("準備完了")

    def create_left_panel(self) -> QWidget:
        """Create left panel with template list"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title label
        title = QLabel("テンプレート")
        layout.addWidget(title)

        # Template list
        self.template_list = QListWidget()
        self.template_list.itemClicked.connect(self.on_template_selected)
        layout.addWidget(self.template_list)

        # Refresh button
        refresh_btn = QPushButton("テンプレートを更新")
        refresh_btn.clicked.connect(self.load_templates)
        layout.addWidget(refresh_btn)

        return widget

    def create_middle_panel(self) -> QWidget:
        """Create middle panel with parameter editor and template customizer"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Create splitter for vertical division
        splitter = QSplitter(Qt.Vertical)

        # Parameter Editor
        self.parameter_editor = ParameterEditorPanel()
        self.parameter_editor.parameter_changed.connect(self.on_parameter_changed)

        # Template Customizer
        self.template_customizer = TemplateCustomizer()
        self.template_customizer.template_modified.connect(self.on_template_modified)

        splitter.addWidget(self.parameter_editor)
        splitter.addWidget(self.template_customizer)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)
        return widget

    def create_toolbar(self):
        """Create toolbar with action buttons"""
        toolbar = QToolBar("アクション")
        self.addToolBar(toolbar)

        # Save button
        save_btn = QPushButton("PNGを保存")
        save_btn.clicked.connect(self.on_save_png)
        toolbar.addWidget(save_btn)

        toolbar.addSeparator()

        # Export CSV button
        export_btn = QPushButton("一括エクスポート (CSV)")
        export_btn.clicked.connect(self.on_export_csv)
        toolbar.addWidget(export_btn)

        toolbar.addSeparator()

        # Settings button
        settings_btn = QPushButton("設定")
        settings_btn.clicked.connect(self.on_settings)
        toolbar.addWidget(settings_btn)

        toolbar.addSeparator()

        # Status label
        self.status_label = QLabel("準備完了")
        toolbar.addWidget(self.status_label)

    def load_templates(self):
        """Load templates from template directory"""
        self.statusBar().showMessage("テンプレート読込中...")
        self.template_list.clear()

        success, error_msg, templates = self.template_manager.load_all_templates()

        if success and templates:
            for template in templates:
                item = QListWidgetItem(f"{template.name} ({template.template_type})")
                item.setData(Qt.UserRole, template)
                self.template_list.addItem(item)

            self.statusBar().showMessage(f"{len(templates)}個のテンプレートを読込")
        elif templates:
            # Partial success
            for template in templates:
                item = QListWidgetItem(f"{template.name} ({template.template_type})")
                item.setData(Qt.UserRole, template)
                self.template_list.addItem(item)
            self.statusBar().showMessage(f"{len(templates)}個のテンプレートを読込（警告あり）")
        else:
            # No templates found
            error_msg = error_msg or "テンプレートが見つかりません"
            self.statusBar().showMessage(f"警告: {error_msg}")
            # Don't show dialog - just warn in status bar

    def on_template_selected(self, item: QListWidgetItem):
        """Handle template selection"""
        self.current_template = item.data(Qt.UserRole)
        self.current_parameters = {}

        # Load template into parameter editor
        self.parameter_editor.load_template(self.current_template)

        # Load template into customizer
        self.template_customizer.load_template(self.current_template)

        self.statusBar().showMessage(f"テンプレート: {self.current_template.name}")

        # Generate preview with default parameters
        self.generate_preview()

    def on_parameter_changed(self, parameters: dict):
        """Handle parameter changes - trigger realtime preview"""
        self.current_parameters = parameters

        if Config.PREVIEW_UPDATE_MODE == 'realtime' and self.current_template:
            self.generate_preview()

    def on_template_modified(self, modified_template):
        """Handle template modification from customizer"""
        # Template attributes have changed, regenerate preview
        if self.current_template:
            self.generate_preview()

    def generate_preview(self):
        """Generate image preview in background thread"""
        if not self.current_template:
            return

        # Disable UI during generation
        self.parameter_editor.setEnabled(False)
        self.statusBar().showMessage("プレビュー生成中...")

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

        self.statusBar().showMessage("プレビュー準備完了")
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
            QMessageBox.warning(self, "警告", "保存する画像がありません。まず画像を生成してください。")
            return

        # Open save dialog
        filename = self.image_generator.generate_filename(
            self.current_template.name,
            self.current_template.template_type
        )

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "PNGイメージを保存",
            str(Path(Config.OUTPUT_DIR) / filename),
            "PNGファイル (*.png)"
        )

        if not filepath:
            return  # User cancelled

        # Save image
        success, error_msg = self.image_generator.save_png(
            self.preview_panel.current_image,
            filepath
        )

        if success:
            self.statusBar().showMessage(f"保存されました: {Path(filepath).name}")
            QMessageBox.information(self, "成功", f"画像を保存しました:\n{filepath}")
        else:
            QMessageBox.critical(self, "エラー", f"画像の保存に失敗しました:\n{error_msg}")

    def on_export_csv(self):
        """Open CSV batch export dialog"""
        # Check if a template is selected
        if not self.current_template:
            QMessageBox.warning(
                self,
                "警告",
                "先にテンプレートを選択してください。"
            )
            return

        # Open file dialog to select CSV file
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "一括処理用CSVファイルを開く",
            str(Path.home()),
            "CSVファイル (*.csv)"
        )

        if not filepath:
            return  # User cancelled

        # Confirm batch processing
        reply = QMessageBox.question(
            self,
            "一括処理を確認",
            f"このテンプレートでCSVファイルを処理してもよろしいですか?: {self.current_template.name}\n\n"
            f"ファイル: {Path(filepath).name}\n"
            f"出力: {Config.OUTPUT_DIR}",
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
        self.statusBar().showMessage(f"CSV処理中: {Path(csv_filepath).name}")

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
        message = f"一括処理が完了しました！\n{num_generated}個の画像を生成しました。"
        self.statusBar().showMessage(message)

        QMessageBox.information(
            self,
            "一括処理完了",
            f"{message}\n\n"
            f"出力ディレクトリ: {Config.OUTPUT_DIR}"
        )

        # Cleanup thread
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()

    def on_csv_batch_error(self, error_msg: str):
        """Handle CSV batch processing error"""
        self.statusBar().showMessage(f"一括処理に失敗しました")

        QMessageBox.critical(
            self,
            "一括処理エラー",
            f"一括処理中にエラーが発生しました:\n\n{error_msg}"
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
            "設定",
            "設定ダイアログは今後のバージョンで実装される予定です"
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
