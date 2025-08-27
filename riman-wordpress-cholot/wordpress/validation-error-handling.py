#!/usr/bin/env python3
"""
Validation and Error Handling Strategy
=====================================

Comprehensive validation and error handling system for the widget generator
Ensures reliability and provides clear feedback for debugging and user guidance
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class ErrorSeverity(Enum):
    """Error severity levels"""
    INFO = "info"
    WARNING = "warning" 
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Categories of validation errors"""
    CONTENT_MISSING = auto()
    CONTENT_INVALID = auto()
    STRUCTURE_INVALID = auto()
    TYPE_MISMATCH = auto()
    CONSTRAINT_VIOLATION = auto()
    ELEMENTOR_COMPLIANCE = auto()
    THEME_COMPLIANCE = auto()
    PLACEHOLDER_ERROR = auto()


@dataclass
class ValidationError:
    """Represents a validation error with context"""
    code: str
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    field_path: Optional[str] = None
    expected_value: Optional[Any] = None
    actual_value: Optional[Any] = None
    suggestion: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity.value,
            "category": self.category.name,
            "field_path": self.field_path,
            "expected_value": self.expected_value,
            "actual_value": self.actual_value,
            "suggestion": self.suggestion,
            "context": self.context
        }


@dataclass
class ValidationResult:
    """Result of validation with errors and warnings"""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    info: List[ValidationError] = field(default_factory=list)
    
    def add_error(self, error: ValidationError):
        """Add an error to the result"""
        if error.severity == ErrorSeverity.ERROR or error.severity == ErrorSeverity.CRITICAL:
            self.errors.append(error)
            self.is_valid = False
        elif error.severity == ErrorSeverity.WARNING:
            self.warnings.append(error)
        elif error.severity == ErrorSeverity.INFO:
            self.info.append(error)
    
    def get_all_issues(self) -> List[ValidationError]:
        """Get all issues regardless of severity"""
        return self.errors + self.warnings + self.info
    
    def has_critical_errors(self) -> bool:
        """Check if there are critical errors"""
        return any(error.severity == ErrorSeverity.CRITICAL for error in self.errors)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "is_valid": self.is_valid,
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
            "info": [i.to_dict() for i in self.info],
            "summary": {
                "total_issues": len(self.get_all_issues()),
                "error_count": len(self.errors),
                "warning_count": len(self.warnings),
                "info_count": len(self.info)
            }
        }


class IValidator(ABC):
    """Interface for validators"""
    
    @abstractmethod
    def validate(self, data: Any, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate data and return result"""
        pass


class ContentValidator(IValidator):
    """Validates content data against widget requirements"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Define widget content requirements
        self.widget_requirements = {
            'cholot-texticon': {
                'required': ['title'],
                'optional': ['subtitle', 'text', 'icon', 'icon_align'],
                'types': {
                    'title': str,
                    'subtitle': str,
                    'text': str,
                    'icon': str,
                    'icon_align': str
                },
                'constraints': {
                    'title': {'min_length': 1, 'max_length': 100},
                    'subtitle': {'max_length': 50},
                    'text': {'max_length': 500},
                    'icon': {'pattern': r'^fa[srlb]?\s+fa-[\w-]+$'}
                }
            },
            'cholot-title': {
                'required': ['title'],
                'optional': ['header_size', 'align'],
                'types': {
                    'title': str,
                    'header_size': str,
                    'align': str
                },
                'constraints': {
                    'title': {'min_length': 1, 'max_length': 200},
                    'header_size': {'choices': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']},
                    'align': {'choices': ['left', 'center', 'right', 'justify']}
                }
            },
            'cholot-team': {
                'required': ['name', 'position', 'image_url'],
                'optional': ['social_links', 'height', 'align'],
                'types': {
                    'name': str,
                    'position': str,
                    'image_url': str,
                    'social_links': list,
                    'height': str,
                    'align': str
                },
                'constraints': {
                    'name': {'min_length': 1, 'max_length': 50},
                    'position': {'min_length': 1, 'max_length': 100},
                    'image_url': {'pattern': r'^https?://.*\.(jpg|jpeg|png|gif|webp)$'},
                    'height': {'pattern': r'^\d+(px|em|rem|%)$'}
                }
            }
        }
    
    def validate(self, data: Any, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate content data"""
        result = ValidationResult(is_valid=True)
        context = context or {}
        
        widget_type = context.get('widget_type')
        if not widget_type:
            result.add_error(ValidationError(
                code="MISSING_CONTEXT",
                message="Widget type not specified in context",
                severity=ErrorSeverity.CRITICAL,
                category=ErrorCategory.CONTENT_INVALID
            ))
            return result
        
        if widget_type not in self.widget_requirements:
            result.add_error(ValidationError(
                code="UNKNOWN_WIDGET_TYPE",
                message=f"Unknown widget type: {widget_type}",
                severity=ErrorSeverity.CRITICAL,
                category=ErrorCategory.CONTENT_INVALID,
                actual_value=widget_type,
                suggestion=f"Supported types: {list(self.widget_requirements.keys())}"
            ))
            return result
        
        requirements = self.widget_requirements[widget_type]
        
        # Validate required fields
        self._validate_required_fields(data, requirements, result)
        
        # Validate field types
        self._validate_field_types(data, requirements, result)
        
        # Validate constraints
        self._validate_constraints(data, requirements, result)
        
        return result
    
    def _validate_required_fields(self, data: Dict, requirements: Dict, result: ValidationResult):
        """Validate that all required fields are present"""
        for field in requirements.get('required', []):
            if field not in data or data[field] is None or data[field] == "":
                result.add_error(ValidationError(
                    code="REQUIRED_FIELD_MISSING",
                    message=f"Required field '{field}' is missing or empty",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.CONTENT_MISSING,
                    field_path=field,
                    suggestion=f"Please provide a value for '{field}'"
                ))
    
    def _validate_field_types(self, data: Dict, requirements: Dict, result: ValidationResult):
        """Validate field data types"""
        type_definitions = requirements.get('types', {})
        
        for field, expected_type in type_definitions.items():
            if field in data and data[field] is not None:
                if not isinstance(data[field], expected_type):
                    result.add_error(ValidationError(
                        code="TYPE_MISMATCH",
                        message=f"Field '{field}' should be {expected_type.__name__}",
                        severity=ErrorSeverity.ERROR,
                        category=ErrorCategory.TYPE_MISMATCH,
                        field_path=field,
                        expected_value=expected_type.__name__,
                        actual_value=type(data[field]).__name__,
                        suggestion=f"Convert '{field}' to {expected_type.__name__}"
                    ))
    
    def _validate_constraints(self, data: Dict, requirements: Dict, result: ValidationResult):
        """Validate field constraints"""
        constraints = requirements.get('constraints', {})
        
        for field, field_constraints in constraints.items():
            if field not in data or data[field] is None:
                continue
            
            value = data[field]
            
            # String length constraints
            if 'min_length' in field_constraints and len(str(value)) < field_constraints['min_length']:
                result.add_error(ValidationError(
                    code="MIN_LENGTH_VIOLATION",
                    message=f"Field '{field}' is too short (minimum {field_constraints['min_length']} characters)",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.CONSTRAINT_VIOLATION,
                    field_path=field,
                    expected_value=f"min {field_constraints['min_length']} chars",
                    actual_value=f"{len(str(value))} chars"
                ))
            
            if 'max_length' in field_constraints and len(str(value)) > field_constraints['max_length']:
                result.add_error(ValidationError(
                    code="MAX_LENGTH_VIOLATION", 
                    message=f"Field '{field}' is too long (maximum {field_constraints['max_length']} characters)",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.CONSTRAINT_VIOLATION,
                    field_path=field,
                    expected_value=f"max {field_constraints['max_length']} chars",
                    actual_value=f"{len(str(value))} chars",
                    suggestion=f"Truncate '{field}' to {field_constraints['max_length']} characters"
                ))
            
            # Pattern validation
            if 'pattern' in field_constraints:
                pattern = field_constraints['pattern']
                if not re.match(pattern, str(value)):
                    result.add_error(ValidationError(
                        code="PATTERN_MISMATCH",
                        message=f"Field '{field}' does not match required pattern",
                        severity=ErrorSeverity.ERROR,
                        category=ErrorCategory.CONSTRAINT_VIOLATION,
                        field_path=field,
                        expected_value=pattern,
                        actual_value=str(value),
                        suggestion=f"Ensure '{field}' matches pattern: {pattern}"
                    ))
            
            # Choice validation
            if 'choices' in field_constraints:
                choices = field_constraints['choices']
                if value not in choices:
                    result.add_error(ValidationError(
                        code="INVALID_CHOICE",
                        message=f"Field '{field}' has invalid value",
                        severity=ErrorSeverity.ERROR,
                        category=ErrorCategory.CONSTRAINT_VIOLATION,
                        field_path=field,
                        expected_value=choices,
                        actual_value=value,
                        suggestion=f"Choose one of: {choices}"
                    ))


class StructureValidator(IValidator):
    """Validates Elementor widget/section structure"""
    
    def validate(self, data: Any, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate Elementor structure"""
        result = ValidationResult(is_valid=True)
        
        if not isinstance(data, dict):
            result.add_error(ValidationError(
                code="INVALID_ROOT_TYPE",
                message="Root element must be a dictionary",
                severity=ErrorSeverity.CRITICAL,
                category=ErrorCategory.STRUCTURE_INVALID,
                expected_value="dict",
                actual_value=type(data).__name__
            ))
            return result
        
        # Validate required Elementor fields
        required_fields = ['id', 'elType', 'elements']
        for field in required_fields:
            if field not in data:
                result.add_error(ValidationError(
                    code="MISSING_ELEMENTOR_FIELD",
                    message=f"Required Elementor field '{field}' is missing",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                    field_path=field
                ))
        
        # Validate ID format
        if 'id' in data:
            element_id = data['id']
            if not re.match(r'^[a-z0-9]{7,8}$', str(element_id)):
                result.add_error(ValidationError(
                    code="INVALID_ID_FORMAT",
                    message="Elementor ID must be 7-8 alphanumeric characters",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                    field_path="id",
                    expected_value="7-8 alphanumeric chars",
                    actual_value=str(element_id),
                    suggestion="Generate new ID using ElementorIDGenerator"
                ))
        
        # Validate elType
        if 'elType' in data:
            el_type = data['elType']
            valid_types = ['section', 'column', 'widget']
            if el_type not in valid_types:
                result.add_error(ValidationError(
                    code="INVALID_ELEMENT_TYPE",
                    message=f"Invalid elType: {el_type}",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                    field_path="elType",
                    expected_value=valid_types,
                    actual_value=el_type
                ))
        
        # Validate widget-specific requirements
        if data.get('elType') == 'widget':
            self._validate_widget_structure(data, result)
        elif data.get('elType') == 'section':
            self._validate_section_structure(data, result)
        elif data.get('elType') == 'column':
            self._validate_column_structure(data, result)
        
        return result
    
    def _validate_widget_structure(self, data: Dict, result: ValidationResult):
        """Validate widget-specific structure"""
        if 'widgetType' not in data:
            result.add_error(ValidationError(
                code="MISSING_WIDGET_TYPE",
                message="Widget must have widgetType field",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                field_path="widgetType"
            ))
        
        if 'settings' not in data:
            result.add_error(ValidationError(
                code="MISSING_WIDGET_SETTINGS",
                message="Widget must have settings field",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                field_path="settings"
            ))
    
    def _validate_section_structure(self, data: Dict, result: ValidationResult):
        """Validate section-specific structure"""
        settings = data.get('settings', {})
        
        if 'structure' not in settings:
            result.add_error(ValidationError(
                code="MISSING_SECTION_STRUCTURE",
                message="Section must have structure setting",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                field_path="settings.structure"
            ))
        else:
            structure = settings['structure']
            if not re.match(r'^\d{2,3}$', str(structure)):
                result.add_error(ValidationError(
                    code="INVALID_SECTION_STRUCTURE",
                    message="Section structure must be 2-3 digit number",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                    field_path="settings.structure",
                    expected_value="2-3 digit number (e.g., '33', '25', '100')",
                    actual_value=str(structure)
                ))
    
    def _validate_column_structure(self, data: Dict, result: ValidationResult):
        """Validate column-specific structure"""
        settings = data.get('settings', {})
        
        if '_column_size' not in settings:
            result.add_error(ValidationError(
                code="MISSING_COLUMN_SIZE",
                message="Column must have _column_size setting",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                field_path="settings._column_size"
            ))
        else:
            column_size = settings['_column_size']
            if not isinstance(column_size, (int, float)) or column_size <= 0 or column_size > 100:
                result.add_error(ValidationError(
                    code="INVALID_COLUMN_SIZE",
                    message="Column size must be between 1 and 100",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.ELEMENTOR_COMPLIANCE,
                    field_path="settings._column_size",
                    expected_value="1-100",
                    actual_value=str(column_size)
                ))


class ThemeComplianceValidator(IValidator):
    """Validates compliance with Cholot theme standards"""
    
    def __init__(self, theme_config):
        self.theme_config = theme_config
    
    def validate(self, data: Any, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate theme compliance"""
        result = ValidationResult(is_valid=True)
        
        if not isinstance(data, dict) or 'settings' not in data:
            return result
        
        settings = data['settings']
        
        # Check for proper color usage
        self._validate_colors(settings, result)
        
        # Check for proper spacing objects
        self._validate_spacing_objects(settings, result)
        
        # Check for typography compliance
        self._validate_typography(settings, result)
        
        return result
    
    def _validate_colors(self, settings: Dict, result: ValidationResult):
        """Validate color usage against theme"""
        color_fields = [
            'title_color', 'subtitle_color', 'text_color', 
            'background_color', 'btn_color', 'icon_color'
        ]
        
        for field in color_fields:
            if field in settings:
                color_value = settings[field]
                if isinstance(color_value, str):
                    # Check if it's a valid color format
                    if not self._is_valid_color(color_value):
                        result.add_error(ValidationError(
                            code="INVALID_COLOR_FORMAT",
                            message=f"Invalid color format in {field}",
                            severity=ErrorSeverity.WARNING,
                            category=ErrorCategory.THEME_COMPLIANCE,
                            field_path=f"settings.{field}",
                            actual_value=color_value,
                            suggestion="Use hex (#ffffff), rgb(), rgba(), or theme colors"
                        ))
    
    def _validate_spacing_objects(self, settings: Dict, result: ValidationResult):
        """Validate spacing objects format"""
        spacing_fields = [
            'margin', '_margin', 'padding', '_padding',
            'title_margin', 'text_margin', 'icon_margin'
        ]
        
        for field in spacing_fields:
            if field in settings:
                spacing_obj = settings[field]
                if isinstance(spacing_obj, dict):
                    required_keys = ['unit', 'top', 'right', 'bottom', 'left', 'isLinked']
                    for key in required_keys:
                        if key not in spacing_obj:
                            result.add_error(ValidationError(
                                code="INCOMPLETE_SPACING_OBJECT",
                                message=f"Spacing object {field} missing '{key}' property",
                                severity=ErrorSeverity.WARNING,
                                category=ErrorCategory.THEME_COMPLIANCE,
                                field_path=f"settings.{field}.{key}",
                                suggestion="Use complete spacing object format"
                            ))
    
    def _validate_typography(self, settings: Dict, result: ValidationResult):
        """Validate typography settings"""
        # Find typography settings
        for key, value in settings.items():
            if '_typography_typography' in key and value == 'custom':
                base_key = key.replace('_typography_typography', '')
                
                # Check for required typography properties
                required_props = ['font_size']
                for prop in required_props:
                    prop_key = f"{base_key}_typography_{prop}"
                    if prop_key not in settings:
                        result.add_error(ValidationError(
                            code="INCOMPLETE_TYPOGRAPHY",
                            message=f"Custom typography for {base_key} missing {prop} setting",
                            severity=ErrorSeverity.WARNING,
                            category=ErrorCategory.THEME_COMPLIANCE,
                            field_path=f"settings.{prop_key}",
                            suggestion=f"Add {prop_key} setting for custom typography"
                        ))
    
    def _is_valid_color(self, color: str) -> bool:
        """Check if color value is in valid format"""
        # Hex colors
        if re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color):
            return True
        
        # RGB/RGBA colors
        if re.match(r'^rgba?\([^)]+\)$', color):
            return True
        
        # Named colors (basic check)
        named_colors = ['transparent', 'inherit', 'initial', 'unset']
        if color.lower() in named_colors:
            return True
        
        return False


class CompositeValidator(IValidator):
    """Combines multiple validators for comprehensive validation"""
    
    def __init__(self, theme_config=None):
        self.validators = [
            ContentValidator(),
            StructureValidator(),
            ThemeComplianceValidator(theme_config) if theme_config else None
        ]
        self.validators = [v for v in self.validators if v is not None]
    
    def validate(self, data: Any, context: Dict[str, Any] = None) -> ValidationResult:
        """Run all validators and combine results"""
        combined_result = ValidationResult(is_valid=True)
        
        for validator in self.validators:
            try:
                result = validator.validate(data, context)
                
                # Combine results
                for error in result.errors:
                    combined_result.add_error(error)
                for warning in result.warnings:
                    combined_result.add_error(warning)
                for info in result.info:
                    combined_result.add_error(info)
                    
            except Exception as e:
                # Handle validator errors gracefully
                combined_result.add_error(ValidationError(
                    code="VALIDATOR_ERROR",
                    message=f"Validator {validator.__class__.__name__} failed: {str(e)}",
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.STRUCTURE_INVALID,
                    context={"validator": validator.__class__.__name__, "exception": str(e)}
                ))
        
        return combined_result


class ErrorHandler:
    """Handles and formats validation errors for different audiences"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def handle_validation_result(self, result: ValidationResult, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process validation result and return formatted response"""
        response = {
            "success": result.is_valid,
            "data": None,
            "errors": [],
            "warnings": [],
            "info": [],
            "debug": {}
        }
        
        # Format errors for different audiences
        if context and context.get('audience') == 'developer':
            response["errors"] = [e.to_dict() for e in result.errors]
            response["warnings"] = [w.to_dict() for w in result.warnings]
            response["debug"] = {
                "total_issues": len(result.get_all_issues()),
                "critical_errors": result.has_critical_errors(),
                "validation_summary": result.to_dict()["summary"]
            }
        else:
            # User-friendly messages
            response["errors"] = [self._format_user_message(e) for e in result.errors]
            response["warnings"] = [self._format_user_message(w) for w in result.warnings]
        
        # Log errors for debugging
        for error in result.errors:
            self.logger.error(f"Validation error [{error.code}]: {error.message}")
        
        return response
    
    def _format_user_message(self, error: ValidationError) -> str:
        """Format error message for end users"""
        message = error.message
        
        if error.suggestion:
            message += f" Suggestion: {error.suggestion}"
        
        return message
    
    def create_error_report(self, result: ValidationResult) -> str:
        """Create detailed error report"""
        report_lines = [
            "VALIDATION REPORT",
            "=" * 50,
            f"Overall Status: {'PASSED' if result.is_valid else 'FAILED'}",
            f"Errors: {len(result.errors)}",
            f"Warnings: {len(result.warnings)}",
            f"Info: {len(result.info)}",
            ""
        ]
        
        if result.errors:
            report_lines.extend([
                "ERRORS:",
                "-" * 20
            ])
            for i, error in enumerate(result.errors, 1):
                report_lines.extend([
                    f"{i}. [{error.code}] {error.message}",
                    f"   Category: {error.category.name}",
                    f"   Severity: {error.severity.value}",
                    f"   Field: {error.field_path or 'N/A'}",
                    f"   Suggestion: {error.suggestion or 'N/A'}",
                    ""
                ])
        
        if result.warnings:
            report_lines.extend([
                "WARNINGS:",
                "-" * 20
            ])
            for i, warning in enumerate(result.warnings, 1):
                report_lines.extend([
                    f"{i}. [{warning.code}] {warning.message}",
                    f"   Suggestion: {warning.suggestion or 'N/A'}",
                    ""
                ])
        
        return "\n".join(report_lines)


# Exception Classes for different error scenarios

class WidgetGenerationError(Exception):
    """Base exception for widget generation errors"""
    pass


class ContentValidationError(WidgetGenerationError):
    """Exception for content validation failures"""
    
    def __init__(self, validation_result: ValidationResult):
        self.validation_result = validation_result
        error_messages = [e.message for e in validation_result.errors]
        super().__init__(f"Content validation failed: {'; '.join(error_messages)}")


class StructureValidationError(WidgetGenerationError):
    """Exception for structure validation failures"""
    pass


class PlaceholderResolutionError(WidgetGenerationError):
    """Exception for placeholder resolution failures"""
    pass


# Usage Example and Testing
if __name__ == "__main__":
    # Example usage of the validation system
    
    # Initialize validator
    validator = CompositeValidator()
    error_handler = ErrorHandler()
    
    # Test content validation
    test_content = {
        "title": "Test Title",
        "subtitle": "Test Subtitle",
        "icon": "invalid-icon-format"  # This should fail validation
    }
    
    context = {
        "widget_type": "cholot-texticon",
        "audience": "developer"
    }
    
    # Validate content
    result = validator.validate(test_content, context)
    
    # Handle results
    response = error_handler.handle_validation_result(result, context)
    print(json.dumps(response, indent=2))
    
    # Generate error report
    if not result.is_valid:
        report = error_handler.create_error_report(result)
        print("\n" + report)
    
    # Test structure validation
    test_widget = {
        "id": "abc123x",  # Valid ID
        "elType": "widget",
        "widgetType": "cholot-texticon",
        "settings": {"title": "Test"},
        "elements": []
    }
    
    structure_result = validator.validate(test_widget, {"validation_type": "structure"})
    print(f"\nStructure validation: {'PASSED' if structure_result.is_valid else 'FAILED'}")
    
    if not structure_result.is_valid:
        for error in structure_result.errors:
            print(f"  - {error.message}")