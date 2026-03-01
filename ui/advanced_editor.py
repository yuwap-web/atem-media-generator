"""
Advanced Parameter Editor for ATEM Media File Generator
Provides richer editing capabilities with preview
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QScrollArea, QFormLayout,
    QSpinBox, QColorDialog, QComboBox, QGroupBox
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPixmap

from models.template import Template
from config import Config


class AdvancedParameterEditor(QWidget):
    """Advanced parameter editor with rich editing capabilities"""

    parameter_changed = pyqtSignal(dict)

    def __init__(self):
        """Initialize advanced editor"""
        super().__init__()
        self.current_template = None
        self.parameter_inputs = {}

        # Debounce timer for text changes (avoid rapid updates during input)
        # This is especially important for Japanese IME compatibility
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.on_text_change_debounced)
        self.debounce_delay = Config.PARAMETER_INPUT_DEBOUNCE_MS

        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Parameter Editor")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Info text
        info = QLabel("テンプレートのパラメータを入力してください")
        info.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(info)

        # Scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.form_widget = QWidget()
        self.form_layout = QFormLayout(self.form_widget)

        scroll.setWidget(self.form_widget)
        layout.addWidget(scroll, 1)

        # Buttons
        button_layout = QHBoxLayout()

        clear_btn = QPushButton("すべてクリア")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)

        reset_btn = QPushButton("リセット")
        reset_btn.clicked.connect(self.reset_values)
        button_layout.addWidget(reset_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)

    def load_template(self, template: Template):
        """Load template and create editor fields"""
        self.current_template = template
        self.parameter_inputs.clear()

        # Clear form
        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)

        all_params = template.get_all_parameters()

        if not all_params:
            label = QLabel("パラメータなし")
            self.form_layout.addRow(label)
            return

        # Required parameters
        if template.required_parameters:
            section = QLabel("必須パラメータ ※")
            section.setStyleSheet("font-weight: bold; color: #FF6B6B;")
            self.form_layout.addRow(section)

            for param in template.required_parameters:
                self._add_parameter_field(param, required=True)

        # Optional parameters
        if template.optional_parameters:
            section = QLabel("オプション")
            section.setStyleSheet("font-weight: bold; color: #4ECDC4;")
            self.form_layout.addRow(section)

            for param in template.optional_parameters:
                self._add_parameter_field(param, required=False)

    def _add_parameter_field(self, param_name: str, required: bool = False):
        """Add parameter input field"""
        # Input field with larger size for better usability
        input_field = QLineEdit()
        input_field.setPlaceholderText(f"{param_name} を入力...")
        input_field.setMinimumHeight(32)
        # Enable input method hints for better Japanese IME support
        input_field.setAttribute(Qt.WA_InputMethodEnabled, True)
        # Connect with debounce to avoid rapid updates during text input
        input_field.textChanged.connect(self.on_parameter_changed_debounce)

        # Label with required indicator
        label_text = param_name
        if required:
            label_text += " *"

        label = QLabel(label_text)

        self.form_layout.addRow(label, input_field)
        self.parameter_inputs[param_name] = input_field

    def on_parameter_changed_debounce(self):
        """Handle parameter change with debounce"""
        # Restart debounce timer
        self.debounce_timer.stop()
        self.debounce_timer.start(self.debounce_delay)

    def on_text_change_debounced(self):
        """Called after debounce timer expires"""
        parameters = self.get_parameters()
        self.parameter_changed.emit(parameters)

    def get_parameters(self) -> dict:
        """Get all parameter values"""
        params = {}
        for param_name, input_field in self.parameter_inputs.items():
            text = input_field.text().strip()
            params[param_name] = text if text else ''
        return params

    def set_parameters(self, parameters: dict):
        """Set parameter values"""
        for param_name, value in parameters.items():
            if param_name in self.parameter_inputs:
                self.parameter_inputs[param_name].setText(str(value))

    def clear_all(self):
        """Clear all parameters"""
        for input_field in self.parameter_inputs.values():
            input_field.clear()

    def reset_values(self):
        """Reset to empty"""
        self.clear_all()
