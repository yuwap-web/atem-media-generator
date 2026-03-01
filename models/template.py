"""
Data models for ATEM Media File Generator templates
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple


@dataclass
class TextLayer:
    """Text layer definition for template"""
    name: str
    x: int
    y: int
    width: int
    height: int
    font_name: str
    font_size: int
    color: Tuple[int, int, int, int]  # RGBA
    alignment: str  # 'left', 'center', 'right'
    parameter_key: str  # Maps to CSV column or parameter key

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'TextLayer':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class Template:
    """Template definition for image generation"""
    name: str
    template_type: str  # 'title', 'lower_third', 'other'
    background_color: Optional[Tuple[int, int, int, int]] = None  # RGBA
    layers: List[TextLayer] = field(default_factory=list)
    required_parameters: List[str] = field(default_factory=list)
    optional_parameters: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'template_type': self.template_type,
            'background_color': self.background_color,
            'layers': [layer.to_dict() for layer in self.layers],
            'required_parameters': self.required_parameters,
            'optional_parameters': self.optional_parameters,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Template':
        """Create from dictionary"""
        layers = [TextLayer.from_dict(layer) for layer in data.get('layers', [])]
        return cls(
            name=data['name'],
            template_type=data['template_type'],
            background_color=data.get('background_color'),
            layers=layers,
            required_parameters=data.get('required_parameters', []),
            optional_parameters=data.get('optional_parameters', []),
        )

    def validate_parameters(self, parameters: dict) -> tuple:
        """Validate parameters against template requirements

        Returns:
            (is_valid, error_message or None)
        """
        # Check required parameters
        for param in self.required_parameters:
            if param not in parameters or parameters[param] is None or parameters[param] == '':
                return False, f"Missing required parameter: '{param}'"

        return True, None

    def get_all_parameters(self) -> List[str]:
        """Get list of all parameters (required + optional)"""
        return self.required_parameters + self.optional_parameters
