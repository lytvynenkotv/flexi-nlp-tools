import re
from typing import Optional


def preprocess_numeral(numeral: str, lang: str) -> str:
    """Preprocess the numeral string based on language and general cleaning rules.

    This function processes the numeral string by:
    - Replacing hyphens with spaces for the English language.
    - Removing the word "and" between numerals for English.
    - Normalizing multiple spaces into a single space.
    - Converting the string to lowercase.

    Args:
        numeral (str): The numeral string to preprocess.
        lang (str): The language code (e.g., 'en' for English).

    Returns:
        str: The preprocessed numeral string.

    Example:
        >>> preprocess_numeral("three-and-four", "en")
        "three four"
    """
    # Handle specific language rules
    if lang == "en":
        numeral = re.sub(r"-", " ", numeral)  # Replace hyphens with spaces
        numeral = re.sub(r"\sand\s", " ", numeral)  # Remove "and" from the string

    # General preprocessing (spaces and case normalization)
    numeral = re.sub(r"\s+", " ", numeral).strip()  # Collapse multiple spaces into one
    numeral = numeral.lower()  # Convert to lowercase

    return numeral


def preprocess_number_string(number_string: str) -> str:
    """Preprocess the number string by stripping spaces and converting to lowercase.

    This function is used for basic number string preprocessing without language-specific logic.

    Args:
        number_string (str): The number string to preprocess.

    Returns:
        str: The preprocessed number string.

    Example:
        >>> preprocess_number_string("   FIVE   ")
        "five"
    """
    # Strips leading and trailing spaces and converts to lowercase
    return number_string.strip().lower()
