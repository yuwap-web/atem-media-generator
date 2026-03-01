"""
Template Customizer - Runtime Template Attribute Editor
Allows users to modify template attributes (font size, color, alignment, font) without editing JSON
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QComboBox,
    QPushButton, QGroupBox, QScrollArea, QColorDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QSlider, QLineEdit, QFormLayout
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QColor, QIcon
from pathlib import Path

from models.template import Template, TextLayer, ImageLayer
from font_manager import get_font_manager


class TextLayerEditor(QGroupBox):
    """Editor for individual text layer attributes"""

    changed = pyqtSignal()

    # Class-level cache for available fonts (shared across all instances)
    _font_list_cache = None
    _priority_fonts = [
        # Japanese fonts (優先順位 - 日本語フォント)
        "Hiragino Sans",
        "ヒラギノ角ゴ Pro",
        "Hiragino Mincho",
        "ヒラギノ明朝 Pro",
        "YuGothic",
        "YuMincho",
        "AppleGothic",
        "Apple SD Gothic Neo",
        # English fonts
        "Helvetica", "Arial", "Menlo", "Monaco",
        "Times New Roman", "Georgia", "Courier New",
        "Arial Unicode"
    ]

    @classmethod
    def _get_cached_font_list(cls):
        """Get cached font list or create it once"""
        if cls._font_list_cache is None:
            font_manager = get_font_manager()
            available_fonts = font_manager.get_available_fonts()

            # Build prioritized font list
            added_fonts = set()
            cached_list = []

            # Add priority fonts first
            for font in cls._priority_fonts:
                for available in available_fonts:
                    if font.lower() in available.lower():
                        if available not in added_fonts:
                            cached_list.append(available)
                            added_fonts.add(available)
                        break

            # Add remaining fonts
            for font in available_fonts:
                if font not in added_fonts:
                    cached_list.append(font)
                    added_fonts.add(font)

            cls._font_list_cache = cached_list

        return cls._font_list_cache

    def __init__(self, layer):
        """Initialize layer editor"""
        super().__init__(f"Layer: {layer.name}")
        self.layer = layer  # Keep reference to actual layer object
        self.original_layer = layer
        self.layer_name = layer.name  # Store name for reference
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()

        # Font name - use cached font list for performance
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("フォント:"))
        self.font_combo = QComboBox()

        # Get cached font list (built once, reused for all instances)
        cached_fonts = self._get_cached_font_list()

        # Add all fonts to combo box at once (faster than individual addItem)
        self.font_combo.addItems(cached_fonts)

        # Set current font or fallback
        try:
            self.font_combo.setCurrentText(self.layer.font_name)
        except:
            # If font not found, set to first available
            if self.font_combo.count() > 0:
                self.font_combo.setCurrentIndex(0)

        self.font_combo.currentTextChanged.connect(self.on_changed)
        font_layout.addWidget(self.font_combo)
        font_layout.addStretch()
        layout.addLayout(font_layout)

        # Font size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("サイズ:"))
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(8)
        self.size_spin.setMaximum(200)
        self.size_spin.setValue(self.layer.font_size)
        self.size_spin.setSuffix(" px")
        self.size_spin.valueChanged.connect(self.on_changed)
        size_layout.addWidget(self.size_spin)
        size_layout.addStretch()
        layout.addLayout(size_layout)

        # Alignment
        align_layout = QHBoxLayout()
        align_layout.addWidget(QLabel("配置:"))
        self.align_combo = QComboBox()
        self.align_combo.addItems(["左", "中央", "右"])
        # Map UI display values back to internal format
        alignment_map = {"左": "left", "中央": "center", "右": "right"}
        reverse_map = {"left": "左", "center": "中央", "right": "右"}
        current_display = reverse_map.get(self.layer.alignment, "左")
        self.align_combo.setCurrentText(current_display)
        self.align_combo.currentTextChanged.connect(self.on_changed)
        align_layout.addWidget(self.align_combo)
        align_layout.addStretch()
        layout.addLayout(align_layout)

        # Color picker
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("色:"))
        self.color_button = QPushButton()
        self.color_button.setMaximumWidth(100)
        self.update_color_button()
        self.color_button.clicked.connect(self.on_color_picked)
        color_layout.addWidget(self.color_button)
        color_layout.addStretch()
        layout.addLayout(color_layout)

        # Position and size controls - grouped for clarity
        position_group = QGroupBox("位置とサイズ")
        position_layout = QFormLayout(position_group)

        # X Position
        self.x_spin = QSpinBox()
        self.x_spin.setMinimum(0)
        self.x_spin.setMaximum(1920)
        self.x_spin.setValue(self.layer.x)
        self.x_spin.setSuffix(" px")
        self.x_spin.valueChanged.connect(self.on_changed)
        position_layout.addRow("X位置:", self.x_spin)

        # Y Position
        self.y_spin = QSpinBox()
        self.y_spin.setMinimum(0)
        self.y_spin.setMaximum(1080)
        self.y_spin.setValue(self.layer.y)
        self.y_spin.setSuffix(" px")
        self.y_spin.valueChanged.connect(self.on_changed)
        position_layout.addRow("Y位置:", self.y_spin)

        # Width
        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(50)
        self.width_spin.setMaximum(1920)
        self.width_spin.setValue(self.layer.width)
        self.width_spin.setSuffix(" px")
        self.width_spin.valueChanged.connect(self.on_changed)
        position_layout.addRow("幅:", self.width_spin)

        # Height
        self.height_spin = QSpinBox()
        self.height_spin.setMinimum(20)
        self.height_spin.setMaximum(500)
        self.height_spin.setValue(self.layer.height)
        self.height_spin.setSuffix(" px")
        self.height_spin.valueChanged.connect(self.on_changed)
        position_layout.addRow("高さ:", self.height_spin)

        layout.addWidget(position_group)

        self.setLayout(layout)

    def update_color_button(self):
        """Update color button appearance"""
        r, g, b, a = self.layer.color
        qcolor = QColor(r, g, b, a)
        self.color_button.setStyleSheet(
            f"background-color: rgb({r},{g},{b}); color: white;"
        )

    def on_color_picked(self):
        """Handle color picker dialog"""
        r, g, b, a = self.layer.color
        initial_color = QColor(r, g, b, a)

        color = QColorDialog.getColor(initial_color, self, "テキストの色を選択")
        if color.isValid():
            self.layer.color = (color.red(), color.green(), color.blue(), 255)
            self.update_color_button()
            self.on_changed()

    def on_changed(self):
        """Handle attribute change - update layer object immediately"""
        # Update layer attributes directly
        self.layer.font_name = self.font_combo.currentText()
        self.layer.font_size = self.size_spin.value()
        # Map Japanese display value back to internal format
        alignment_map = {"左": "left", "中央": "center", "右": "right"}
        display_value = self.align_combo.currentText()
        self.layer.alignment = alignment_map.get(display_value, "left")

        # Update position and size
        self.layer.x = self.x_spin.value()
        self.layer.y = self.y_spin.value()
        self.layer.width = self.width_spin.value()
        self.layer.height = self.height_spin.value()
        # Note: color is updated separately in on_color_picked

        # Debug output for troubleshooting
        print(f"[DEBUG] Layer '{self.layer.name}' updated: font={self.layer.font_name}, size={self.layer.font_size}, x={self.layer.x}, y={self.layer.y}, w={self.layer.width}, h={self.layer.height}")

        # Signal parent that layer changed
        self.changed.emit()

    def get_modified_layer(self):
        """Return modified layer"""
        return self.layer


class ImageLayerEditor(QGroupBox):
    """Editor for individual image layer attributes"""

    changed = pyqtSignal()

    def __init__(self, layer: ImageLayer):
        """Initialize image layer editor"""
        super().__init__(f"レイヤー: {layer.name}")
        self.layer = layer
        self.original_layer = layer
        self.layer_name = layer.name
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()

        # Image file
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("ファイル:"))
        self.file_input = QLineEdit()
        self.file_input.setText(self.layer.image_path)
        self.file_input.textChanged.connect(self.on_changed)
        file_layout.addWidget(self.file_input)

        browse_btn = QPushButton("参照...")
        browse_btn.clicked.connect(self.on_browse_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        # Position and size controls - grouped for clarity
        position_group = QGroupBox("位置とサイズ")
        position_layout = QFormLayout(position_group)

        # X Position
        self.x_spin = QSpinBox()
        self.x_spin.setMinimum(0)
        self.x_spin.setMaximum(1920)
        self.x_spin.setValue(self.layer.x)
        self.x_spin.setSuffix(" px")
        self.x_spin.valueChanged.connect(self.on_changed)
        position_layout.addRow("X位置:", self.x_spin)

        # Y Position
        self.y_spin = QSpinBox()
        self.y_spin.setMinimum(0)
        self.y_spin.setMaximum(1080)
        self.y_spin.setValue(self.layer.y)
        self.y_spin.setSuffix(" px")
        self.y_spin.valueChanged.connect(self.on_changed)
        position_layout.addRow("Y位置:", self.y_spin)

        # Width
        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(50)
        self.width_spin.setMaximum(1920)
        self.width_spin.setValue(self.layer.width)
        self.width_spin.setSuffix(" px")
        self.width_spin.valueChanged.connect(self.on_changed)
        position_layout.addRow("幅:", self.width_spin)

        # Height
        self.height_spin = QSpinBox()
        self.height_spin.setMinimum(20)
        self.height_spin.setMaximum(1080)
        self.height_spin.setValue(self.layer.height)
        self.height_spin.setSuffix(" px")
        self.height_spin.valueChanged.connect(self.on_changed)
        position_layout.addRow("高さ:", self.height_spin)

        layout.addWidget(position_group)

        # Opacity and Z-order controls - grouped for clarity
        appearance_group = QGroupBox("表示設定")
        appearance_layout = QFormLayout(appearance_group)

        # Opacity
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(self.layer.opacity * 100))
        self.opacity_slider.setTickPosition(QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        self.opacity_slider.sliderMoved.connect(self.on_opacity_changed)
        self.opacity_label = QLabel(f"{int(self.layer.opacity * 100)}%")
        opacity_container = QHBoxLayout()
        opacity_container.addWidget(self.opacity_slider)
        opacity_container.addWidget(self.opacity_label)
        appearance_layout.addRow("不透明度:", opacity_container)

        # Z-order (drawing order)
        self.z_spin = QSpinBox()
        self.z_spin.setMinimum(0)
        self.z_spin.setMaximum(100)
        self.z_spin.setValue(self.layer.z_order)
        self.z_spin.valueChanged.connect(self.on_changed)
        appearance_layout.addRow("Z順序:", self.z_spin)

        layout.addWidget(appearance_group)
        layout.addStretch()

        self.setLayout(layout)

    def on_browse_file(self):
        """Handle file browser dialog"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "画像ファイルを選択",
            str(Path.home()),
            "画像ファイル (*.png *.jpg *.jpeg *.gif *.bmp);;すべてのファイル (*)"
        )
        if filepath:
            self.file_input.setText(filepath)

    def on_opacity_changed(self):
        """Handle opacity slider change"""
        value = self.opacity_slider.value()
        self.opacity_label.setText(f"{value}%")
        self.on_changed()

    def on_changed(self):
        """Handle attribute change - update layer object immediately"""
        self.layer.image_path = self.file_input.text()
        self.layer.x = self.x_spin.value()
        self.layer.y = self.y_spin.value()
        self.layer.width = self.width_spin.value()
        self.layer.height = self.height_spin.value()
        self.layer.opacity = self.opacity_slider.value() / 100.0
        self.layer.z_order = self.z_spin.value()

        self.changed.emit()

    def get_modified_layer(self):
        """Return modified layer"""
        return self.layer


class TemplateCustomizer(QWidget):
    """Template customizer panel for runtime attribute editing"""

    template_modified = pyqtSignal(object)  # Emits modified template

    def __init__(self):
        """Initialize customizer"""
        super().__init__()
        self.current_template = None
        self.layer_editors = []

        # Debounce timer to prevent excessive preview regeneration
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.on_debounce_timeout)
        self.debounce_delay = 500  # milliseconds

        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()

        # Title
        title = QLabel("テンプレートカスタマイザー")
        title_font = title.font()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Info
        info = QLabel("テキストレイヤーの属性をリアルタイムで編集")
        info.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(info)

        # Scrollable layer editors
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self.editors_widget = QWidget()
        self.editors_layout = QVBoxLayout(self.editors_widget)
        self.editors_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.editors_widget)
        layout.addWidget(scroll, 1)

        # Buttons
        button_layout = QHBoxLayout()

        reset_btn = QPushButton("元に戻す")
        reset_btn.clicked.connect(self.reset_template)
        button_layout.addWidget(reset_btn)

        apply_btn = QPushButton("変更を適用")
        apply_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        apply_btn.clicked.connect(self.apply_changes)
        button_layout.addWidget(apply_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_template(self, template: Template):
        """Load template for customization"""
        self.current_template = template
        self.layer_editors = []

        # Clear existing editors
        while self.editors_layout.count() > 0:
            self.editors_layout.removeWidget(self.editors_layout.itemAt(0).widget())

        # Create editors for each layer
        if not template.layers:
            no_layers_label = QLabel("このテンプレートにはレイヤーがありません")
            no_layers_label.setStyleSheet("color: #999; font-style: italic;")
            self.editors_layout.addWidget(no_layers_label)
            return

        print(f"\n[DEBUG] Loading template '{template.name}' with {len(template.layers)} layers")

        for i, layer in enumerate(template.layers):
            print(f"[DEBUG] Layer {i}: {layer.name}")
            if isinstance(layer, TextLayer):
                print(f"  - TextLayer: x={layer.x}, y={layer.y}, w={layer.width}, h={layer.height}")
            elif isinstance(layer, ImageLayer):
                print(f"  - ImageLayer: x={layer.x}, y={layer.y}, w={layer.width}, h={layer.height}")

            if isinstance(layer, ImageLayer):
                # Create ImageLayerEditor for image layers
                editor = ImageLayerEditor(layer)
            else:
                # Create TextLayerEditor for text layers
                editor = TextLayerEditor(layer)

            editor.changed.connect(self.on_layer_changed)
            self.layer_editors.append(editor)
            self.editors_layout.addWidget(editor)

        self.editors_layout.addStretch()

    def on_layer_changed(self):
        """Handle layer attribute change - debounced to prevent excessive updates"""
        # Sync all layers from editors to template (important for multiple layers!)
        # Each TextLayerEditor directly modifies its layer object
        # We need to ensure all modified layers are in the template
        if self.current_template and self.layer_editors:
            updated_layers = []
            for editor in self.layer_editors:
                # Get the modified layer from editor (it's already modified in place)
                modified_layer = editor.get_modified_layer()
                updated_layers.append(modified_layer)

            # Replace all layers in template with updated versions
            self.current_template.layers = updated_layers

        # Debug: Print which layers have been updated
        # if self.current_template:
        #     for i, layer in enumerate(self.current_template.layers):
        #         print(f"Layer {i} ({layer.name}): font={layer.font_name}, size={layer.font_size}")

        # Restart debounce timer - will emit signal after delay if no more changes
        if self.debounce_timer.isActive():
            self.debounce_timer.stop()
        self.debounce_timer.start(self.debounce_delay)

    def on_debounce_timeout(self):
        """Called when debounce timer expires - emit signal to trigger preview update"""
        print(f"[DEBUG] Debounce timeout - emitting template_modified signal")
        if self.current_template:
            self.template_modified.emit(self.current_template)

    def reset_template(self):
        """Reset template to original state"""
        if self.current_template:
            # Reload template to reset values
            self.load_template(self.current_template)
            self.on_layer_changed()

    def apply_changes(self):
        """Apply changes to template"""
        if self.current_template:
            # Update template layers with modified values
            for i, editor in enumerate(self.layer_editors):
                if i < len(self.current_template.layers):
                    modified_layer = editor.get_modified_layer()
                    self.current_template.layers[i] = modified_layer

            self.template_modified.emit(self.current_template)
