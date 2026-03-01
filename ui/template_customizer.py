"""
Template Customizer - Runtime Template Attribute Editor
Allows users to modify template attributes (font size, color, alignment, font) without editing JSON
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QComboBox,
    QPushButton, QGroupBox, QScrollArea, QColorDialog, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QIcon
from pathlib import Path

from models.template import Template


class TextLayerEditor(QGroupBox):
    """Editor for individual text layer attributes"""

    changed = pyqtSignal()

    def __init__(self, layer):
        """Initialize layer editor"""
        super().__init__(f"Layer: {layer.name}")
        self.layer = layer
        self.original_layer = layer
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()

        # Font name
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Helvetica", "Arial", "Menlo", "Courier New",
            "Times New Roman", "Georgia", "Monaco",
            "ヒラギノ角ゴシック", "ヒラギノゴシック",
            "Arial Unicode"
        ])
        self.font_combo.setCurrentText(self.layer.font_name)
        self.font_combo.currentTextChanged.connect(self.on_changed)
        font_layout.addWidget(self.font_combo)
        font_layout.addStretch()
        layout.addLayout(font_layout)

        # Font size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
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
        align_layout.addWidget(QLabel("Alignment:"))
        self.align_combo = QComboBox()
        self.align_combo.addItems(["left", "center", "right"])
        self.align_combo.setCurrentText(self.layer.alignment)
        self.align_combo.currentTextChanged.connect(self.on_changed)
        align_layout.addWidget(self.align_combo)
        align_layout.addStretch()
        layout.addLayout(align_layout)

        # Color picker
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_button = QPushButton()
        self.color_button.setMaximumWidth(100)
        self.update_color_button()
        self.color_button.clicked.connect(self.on_color_picked)
        color_layout.addWidget(self.color_button)
        color_layout.addStretch()
        layout.addLayout(color_layout)

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

        color = QColorDialog.getColor(initial_color, self, "Select Text Color")
        if color.isValid():
            self.layer.color = (color.red(), color.green(), color.blue(), 255)
            self.update_color_button()
            self.on_changed()

    def on_changed(self):
        """Handle attribute change"""
        self.layer.font_name = self.font_combo.currentText()
        self.layer.font_size = self.size_spin.value()
        self.layer.alignment = self.align_combo.currentText()
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
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Template Customizer")
        title_font = title.font()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Info
        info = QLabel("Modify text layer attributes in real-time")
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

        reset_btn = QPushButton("Reset to Original")
        reset_btn.clicked.connect(self.reset_template)
        button_layout.addWidget(reset_btn)

        apply_btn = QPushButton("Apply Changes")
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
            no_layers_label = QLabel("No text layers in this template")
            no_layers_label.setStyleSheet("color: #999; font-style: italic;")
            self.editors_layout.addWidget(no_layers_label)
            return

        for layer in template.layers:
            editor = TextLayerEditor(layer)
            editor.changed.connect(self.on_layer_changed)
            self.layer_editors.append(editor)
            self.editors_layout.addWidget(editor)

        self.editors_layout.addStretch()

    def on_layer_changed(self):
        """Handle layer attribute change"""
        # Emit signal with modified template
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
