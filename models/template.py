"""
Data models for ATEM Media File Generator templates
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple, Union


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
class ImageLayer:
    """Image layer definition for template"""
    name: str
    image_path: str  # Path to image file
    x: int = 0
    y: int = 0
    width: int = 1920
    height: int = 1080
    opacity: float = 1.0  # 0.0 to 1.0
    z_order: int = 1  # Drawing order (lower = drawn first)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ImageLayer':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class Template:
    """Template definition for image generation"""
    name: str
    template_type: str  # 'title', 'lower_third', 'other'
    background_color: Optional[Tuple[int, int, int, int]] = None  # RGBA
    layers: List[Union[TextLayer, ImageLayer]] = field(default_factory=list)
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
        layers = []
        for layer_data in data.get('layers', []):
            # Determine layer type by checking for identifying fields
            if 'image_path' in layer_data:
                # Image layer
                layers.append(ImageLayer.from_dict(layer_data))
            elif 'parameter_key' in layer_data:
                # Text layer
                layers.append(TextLayer.from_dict(layer_data))
            else:
                # Default to text layer for backward compatibility
                layers.append(TextLayer.from_dict(layer_data))

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
