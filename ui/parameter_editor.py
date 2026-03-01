"""
Parameter Editor Panel for ATEM Media File Generator
Displays and edits template parameters
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QScrollArea, QFormLayout, QPushButton, QMessageBox,
    QTabWidget, QTextEdit
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont

from models.template import Template
from config import Config


class ParameterEditorPanel(QWidget):
    """Panel for editing template parameters"""

    # Signal emitted when parameters change
    parameter_changed = pyqtSignal(dict)

    def __init__(self):
        """Initialize parameter editor panel"""
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
        """Initialize user interface"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("パラメータ")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Scrollable form area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.form_widget = QWidget()
        self.form_layout = QFormLayout(self.form_widget)

        scroll.setWidget(self.form_widget)
        layout.addWidget(scroll)

        # Button layout
        button_layout = QHBoxLayout()

        # Clear button
        clear_btn = QPushButton("すべてクリア")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)

        # Reset button
        reset_btn = QPushButton("リセット")
        reset_btn.clicked.connect(self.reset_values)
        button_layout.addWidget(reset_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)

    def load_template(self, template: Template):
        """
        Load template and create parameter input fields

        Args:
            template: Template object to load
        """
        self.current_template = template
        self.parameter_inputs.clear()

        # Clear existing form
        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)

        # Get all parameters
        all_params = template.get_all_parameters()

        if not all_params:
            label = QLabel("No parameters")
            self.form_layout.addRow(label)
            return

        # Add section for required parameters
        if template.required_parameters:
            section_label = QLabel("Required Parameters")
            section_label.setStyleSheet("font-weight: bold; color: #FF6B6B;")
            self.form_layout.addRow(section_label)

            for param in template.required_parameters:
                self.add_parameter_field(param, is_required=True)

        # Add section for optional parameters
        if template.optional_parameters:
            section_label = QLabel("Optional Parameters")
            section_label.setStyleSheet("font-weight: bold; color: #4ECDC4;")
            self.form_layout.addRow(section_label)

            for param in template.optional_parameters:
                self.add_parameter_field(param, is_required=False)

    def add_parameter_field(self, param_name: str, is_required: bool = False):
        """
        Add single parameter input field

        Args:
            param_name: Name of parameter
            is_required: Whether parameter is required
        """
        # Create input field with better Japanese IME support
        input_field = QLineEdit()
        input_field.setPlaceholderText(f"Enter {param_name}")
        # Enable input method hints for better Japanese IME support
        input_field.setAttribute(Qt.WA_InputMethodEnabled, True)
        # Connect with debounce to avoid rapid updates during text input
        input_field.textChanged.connect(self.on_parameter_text_changed_debounce)

        # Create label
        label_text = param_name
        if is_required:
            label_text += " *"

        label = QLabel(label_text)

        # Add to form
        self.form_layout.addRow(label, input_field)

        # Store reference
        self.parameter_inputs[param_name] = input_field

    def on_parameter_text_changed_debounce(self):
        """Handle parameter text change with debounce"""
        # Restart debounce timer
        self.debounce_timer.stop()
        self.debounce_timer.start(self.debounce_delay)

    def on_text_change_debounced(self):
        """Called after debounce timer expires"""
        parameters = self.get_parameters()
        self.parameter_changed.emit(parameters)

    def get_parameters(self) -> dict:
        """
        Get all current parameter values

        Returns:
            Dictionary of parameter name -> value
        """
        params = {}

        for param_name, input_field in self.parameter_inputs.items():
            text = input_field.text().strip()
            params[param_name] = text if text else ''

        return params

    def set_parameters(self, parameters: dict):
        """
        Set parameter values

        Args:
            parameters: Dictionary of parameter name -> value
        """
        for param_name, value in parameters.items():
            if param_name in self.parameter_inputs:
                self.parameter_inputs[param_name].setText(str(value))

    def clear_all(self):
        """Clear all parameter values"""
        for input_field in self.parameter_inputs.values():
            input_field.clear()

    def reset_values(self):
        """Reset parameters to default (empty) values"""
        self.clear_all()

    def validate_parameters(self) -> tuple:
        """
        Validate parameters against template requirements

        Returns:
            (is_valid: bool, error_message: str or None)
        """
        if not self.current_template:
            return False, "No template loaded"

        parameters = self.get_parameters()
        return self.current_template.validate_parameters(parameters)
