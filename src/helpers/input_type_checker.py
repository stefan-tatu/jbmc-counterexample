def is_array_type(type_text: str) -> bool:
    """
    Check if the given type is an array type.

    Args:
        type_text (str): The type to check.

    Returns:
        bool: True if the type is an array type, False otherwise.
    """
    return type_text.startswith('struct java::array')

def is_class_type(type_text: str) -> bool:
    """
    Check if the given type is a class type (non-array).

    Args:
        type_text (str): The type to check.

    Returns:
        bool: True if the type is a class type, False otherwise.
    """
    return type_text.startswith('struct') and not is_array_type(type_text)

def is_primitive_type(type_text: str) -> bool:
    """
    Check if the given type is a primitive type.

    Args:
        type_text (str): The type to check.

    Returns:
        bool: True if the type is a primitive type, False otherwise.
    """
    PRIMITIVE_TYPES = set(['int', 'char', 'short', 'byte', 'double', 'float'])
    return type_text in PRIMITIVE_TYPES

def is_string_type(type_text: str) -> bool:
    """
    Check if the given type is a string type.

    Args:
        type_text (str): The type to check.

    Returns:
        bool: True if the type is a string type, False otherwise.
    """
    return type_text.startswith("struct java.lang.String")

