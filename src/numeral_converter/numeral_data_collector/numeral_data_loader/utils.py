from typing import Type
from .numeral_entry import MorphForm


def transform_to_morph_form(input_string: str, morph_class: Type[MorphForm]) -> MorphForm:
    """Converts a string into its corresponding morphological form based on the given enum class.

    Args:
        input_string (str): The string to be converted into the desired morphological form (e.g., "one").
        morph_class (Type[MorphForm]): The enum class (e.g., `NumClass`, `Case`, `Gender`) that defines the target morph form.

    Returns:
        MorphForm: The input string converted to the morphological form defined by the `morph_class` enum.

    """
    if not input_string:
        return None

    # Assuming morph_class defines how the string is transformed into a specific form
    # The actual transformation logic will depend on the specific enum and its use case
    # For now, we assume the class provides a direct mapping or transformation method
    return morph_class(input_string)  # Assuming the enum value transformation
