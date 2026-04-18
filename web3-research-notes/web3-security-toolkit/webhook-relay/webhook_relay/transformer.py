"""Payload transformation utilities."""

from typing import Dict, Any

class PayloadTransformer:
    """Transform webhook payloads."""
    
    @staticmethod
    def add_field(payload: Dict, field: str, value: Any) -> Dict:
        """Add a field to payload."""
        result = dict(payload)
        result[field] = value
        return result
    
    @staticmethod
    def remove_field(payload: Dict, field: str) -> Dict:
        """Remove a field from payload."""
        result = dict(payload)
        result.pop(field, None)
        return result
    
    @staticmethod
    def rename_field(payload: Dict, old_name: str, new_name: str) -> Dict:
        """Rename a field."""
        result = dict(payload)
        if old_name in result:
            result[new_name] = result.pop(old_name)
        return result
