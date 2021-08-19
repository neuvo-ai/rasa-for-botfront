"""
This module regroups custom validation functions, and it is
loaded as an extension of the pykwalify library:

https://pykwalify.readthedocs.io/en/latest/extensions.html#extensions
"""
from typing import Any, List, Dict, Text, Union

from pykwalify.errors import SchemaError


def require_response_keys(
    responses: List[Dict[Text, Any]], _: Dict, __: Text
) -> Union[SchemaError, bool]:
    """Validates that response dicts have either the "text" key or the "custom" key."""
    for response in responses:
        if not isinstance(response, dict):
            # this is handled by other validation rules
            continue

<<<<<<< HEAD
        # bf =========
        # if response.get("text") is None and not response.get("custom"):
        #     raise SchemaError("Missing 'text' or 'custom' key in response.")
=======
        if response.get("text") is None and not response.get("custom"):
            return SchemaError(
                "Missing 'text' or 'custom' key in response or "
                "null 'text' value in response.",
            )
>>>>>>> 2.8.2

    return True
