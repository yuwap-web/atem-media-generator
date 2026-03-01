"""
Template Generator - Visual Template Editor
Allows users to create and customize templates visually with drag-and-drop interface
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsPixmapItem,
    QGraphicsRectItem, QListWidget, QListWidgetItem, QInputDialog, QMessageBox,
    QToolBar, QFileDialog
)
from PyQt5.QtCore import Qt, QRectF, QSizeF, QPointF, pyqtSignal
from PyQt5.QtGui import QPixmap, QPen, QColor, QFont, QBrush
from pathlib import Path
import json

from models.template import Template, TextLayer, ImageLayer
from ui.template_customizer import TextLayerEditor, ImageLayerEditor


class TemplateGeneratorWindow(QMainWindow):
    """Visual template editor window"""

    template_created = pyqtSignal(object)  # Emits created template

    def __init__(self, parent=None):
        """Initialize template generator window"""
        super().__init__(parent)
        self.setWindowTitle("テンプレートジェネレーター")
        self.setGeometry(100, 100, 1600, 1000)

        self.current_template = None
        self.layers = []
        self.selected_layer = None
        self.canvas_items = {}  # Maps layer to canvas item

        self.init_ui()

    def init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # Left panel: Layer list
        left_panel = self.create_left_panel()
        layout.addWidget(left_panel)

        # Center: Canvas
        self.canvas = QGraphicsView()
        self.scene = QGraphicsScene(0, 0, 1920, 1080)
        self.scene.setBackgroundBrush(QBrush(QColor(50, 50, 50)))
        self.canvas.setScene(self.scene)
        layout.addWidget(self.canvas, 1)

        # Right panel: Properties
        right_panel = self.create_right_panel()
        layout.addWidget(right_panel)

        # Create toolbar
        self.create_toolbar()

    def create_left_panel(self) -> QWidget:
        """Create left panel with layer list"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("レイヤー")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Layer list
        self.layer_list = QListWidget()
        self.layer_list.itemSelectionChanged.connect(self.on_layer_selected)
        layout.addWidget(self.layer_list)

        # Buttons
        button_layout = QHBoxLayout()

        add_text_btn = QPushButton("テキストを追加")
        add_text_btn.clicked.connect(self.on_add_text_layer)
        button_layout.addWidget(add_text_btn)

        add_image_btn = QPushButton("画像を追加")
        add_image_btn.clicked.connect(self.on_add_image_layer)
        button_layout.addWidget(add_image_btn)

        layout.addLayout(button_layout)

        return widget

    def create_right_panel(self) -> QWidget:
        """Create right panel with properties"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("プロパティ")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Properties container
        self.properties_layout = QVBoxLayout()
        layout.addLayout(self.properties_layout)

        layout.addStretch()

        return widget

    def create_toolbar(self):
        """Create toolbar with action buttons"""
        toolbar = QToolBar("テンプレート操作")
        self.addToolBar(toolbar)

        # New template
        new_btn = QPushButton("新規テンプレート")
        new_btn.clicked.connect(self.on_new_template)
        toolbar.addWidget(new_btn)

        toolbar.addSeparator()

        # Save template
        save_btn = QPushButton("テンプレートを保存")
        save_btn.clicked.connect(self.on_save_template)
        toolbar.addWidget(save_btn)

        toolbar.addSeparator()

        # Delete layer
        delete_btn = QPushButton("レイヤーを削除")
        delete_btn.clicked.connect(self.on_delete_layer)
        toolbar.addWidget(delete_btn)

    def on_new_template(self):
        """Create new template"""
        template_name, ok = QInputDialog.getText(
            self,
            "新規テンプレート",
            "テンプレート名:"
        )
        if ok and template_name:
            self.current_template = Template(
                name=template_name,
                template_type="custom",
                background_color=(0, 0, 0, 0),
                layers=[]
            )
            self.layers = []
            self.refresh_ui()
            self.scene.clear()

    def on_add_text_layer(self):
        """Add new text layer"""
        if self.current_template is None:
            QMessageBox.warning(self, "警告", "先にテンプレートを作成してください")
            return

        layer_name, ok = QInputDialog.getText(
            self,
            "テキストレイヤーを追加",
            "レイヤー名:"
        )
        if ok and layer_name:
            layer = TextLayer(
                name=layer_name,
                x=100,
                y=100,
                width=400,
                height=100,
                font_name="Helvetica",
                font_size=48,
                color=(255, 255, 255, 255),
                alignment="left",
                parameter_key=layer_name.lower().replace(" ", "_")
            )
            self.current_template.layers.append(layer)
            self.layers.append(layer)
            self.refresh_ui()
            self.draw_layers()

    def on_add_image_layer(self):
        """Add new image layer"""
        if self.current_template is None:
            QMessageBox.warning(self, "警告", "先にテンプレートを作成してください")
            return

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "画像ファイルを選択",
            str(Path.home()),
            "画像ファイル (*.png *.jpg *.jpeg *.gif *.bmp)"
        )

        if filepath:
            layer_name, ok = QInputDialog.getText(
                self,
                "画像レイヤーを追加",
                "レイヤー名:",
                text=Path(filepath).stem
            )
            if ok and layer_name:
                layer = ImageLayer(
                    name=layer_name,
                    image_path=filepath,
                    x=100,
                    y=100,
                    width=400,
                    height=300,
                    opacity=1.0,
                    z_order=1
                )
                self.current_template.layers.append(layer)
                self.layers.append(layer)
                self.refresh_ui()
                self.draw_layers()

    def on_layer_selected(self):
        """Handle layer selection"""
        current_item = self.layer_list.currentItem()
        if current_item:
            layer_index = self.layer_list.row(current_item)
            if 0 <= layer_index < len(self.layers):
                self.selected_layer = self.layers[layer_index]
                self.show_layer_properties()

    def on_delete_layer(self):
        """Delete selected layer"""
        if self.selected_layer and self.current_template:
            self.current_template.layers.remove(self.selected_layer)
            self.layers.remove(self.selected_layer)
            self.selected_layer = None
            self.refresh_ui()
            self.draw_layers()

    def on_save_template(self):
        """Save template to JSON file"""
        if self.current_template is None:
            QMessageBox.warning(self, "警告", "先にテンプレートを作成してください")
            return

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "テンプレートを保存",
            str(Path.home() / f"{self.current_template.name}.json"),
            "JSON Files (*.json)"
        )

        if filepath:
            try:
                template_dict = self.current_template.to_dict()
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(template_dict, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "成功", f"テンプレートを保存しました:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"保存に失敗しました:\n{str(e)}")

    def refresh_ui(self):
        """Refresh UI elements"""
        # Update layer list
        self.layer_list.clear()
        for layer in self.layers:
            item = QListWidgetItem(f"{layer.name} ({type(layer).__name__})")
            self.layer_list.addItem(item)

    def show_layer_properties(self):
        """Show properties for selected layer"""
        # Clear existing properties
        while self.properties_layout.count() > 0:
            widget = self.properties_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        if self.selected_layer:
            if isinstance(self.selected_layer, TextLayer):
                editor = TextLayerEditor(self.selected_layer)
                self.properties_layout.addWidget(editor)
            elif isinstance(self.selected_layer, ImageLayer):
                editor = ImageLayerEditor(self.selected_layer)
                self.properties_layout.addWidget(editor)

    def draw_layers(self):
        """Draw layers on canvas"""
        self.scene.clear()

        for layer in self.layers:
            if isinstance(layer, TextLayer):
                # Draw text layer rectangle
                rect = QGraphicsRectItem(layer.x, layer.y, layer.width, layer.height)
                rect.setPen(QPen(QColor(100, 100, 255), 2))
                self.scene.addItem(rect)

                # Add text label
                text_item = QGraphicsTextItem(layer.parameter_key)
                text_item.setPos(layer.x + 5, layer.y + 5)
                self.scene.addItem(text_item)

            elif isinstance(layer, ImageLayer):
                # Draw image if file exists
                if Path(layer.image_path).exists():
                    pixmap = QPixmap(layer.image_path)
                    if not pixmap.isNull():
                        pixmap = pixmap.scaledToWidth(layer.width)
                        img_item = QGraphicsPixmapItem(pixmap)
                        img_item.setPos(layer.x, layer.y)
                        self.scene.addItem(img_item)

            # Highlight selected layer
            if layer == self.selected_layer:
                selection_rect = QGraphicsRectItem(layer.x - 5, layer.y - 5,
                                                    layer.width + 10, layer.height + 10)
                selection_rect.setPen(QPen(QColor(255, 255, 0), 3))
                self.scene.addItem(selection_rect)
