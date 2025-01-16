import logging
from typing import Optional

from .numeral_data_collector.numeral_data_loader.numeral_entry import Case, Gender, Number, NumClass
from .numeral_converter_helpers import (
    _numeral2number_items,
    _int2number_items,
    _number_items2int,
    _number_items2numeral
)
from .numeral_converter_loader import _load_language_data_if_needed, _NUMERAL_LANGUAGE_DATA


logger = logging.getLogger(__name__)


def numeral2int(numeral: str, lang: str) -> Optional[int]:
    """
    Converts the input numeral (in the form of a string) into an integer value for the given language.

    Args:
        numeral (str): The input numeral string (e.g., "forty two").
        lang (str): The language code (e.g., 'en', 'uk').

    Returns:
        Optional[int]: The corresponding integer value, or None if conversion fails.

    Example:
        >>> numeral2int("сорок два", lang="uk")
        42
    """
    _load_language_data_if_needed(lang)

    logger.info(f"Converting numeral '{numeral}' to integer in language '{lang}'")

    number_items = _numeral2number_items(
        numeral=numeral, lang=lang,
        numeral_data=_NUMERAL_LANGUAGE_DATA[lang].numeral_data,
        flexi_index=_NUMERAL_LANGUAGE_DATA[lang].flexi_index
    )
    value = _number_items2int(number_items=number_items)
    if value is not None:
        logger.debug(f"Conversion successful: {numeral} -> {value}")
    else:
        logger.error(f"Failed to convert numeral: {numeral}")
    return value


def int2numeral(
        value: int,
        lang: str,
        case: Optional[Case] = None,
        num_class: Optional[NumClass] = None,
        gender: Optional[Gender] = None,
        number: Optional[Number] = None) -> str:
    """
    Converts an integer to its corresponding numeral string in the given language and morphological form.

    Args:
        value (int): The input integer value (e.g., 42).
        lang (str): The language code (e.g., 'en', 'uk').
        case (Optional[Case]): The grammatical case to apply.
        num_class (Optional[NumClass]): The numerical class (e.g., ordinal, cardinal).
        gender (Optional[Gender]): The grammatical gender (e.g., masculine, feminine).
        number (Optional[Number]): The number form (singular or plural).

    Returns:
        str: The corresponding numeral string in the given morphological form.

    Example:
        >>> int2numeral(42, lang='uk', case="nominative", num_class="cardinal")
        'сорок два'
    """
    logger.info(f"Converting integer '{value}' to numeral in language '{lang}'")
    _load_language_data_if_needed(lang)
    number_items = _int2number_items(value, lang)

    numeral = _number_items2numeral(
        number_items,
        lang=lang,
        numeral_data=_NUMERAL_LANGUAGE_DATA[lang].numeral_data,
        value_index=_NUMERAL_LANGUAGE_DATA[lang].value_index,
        case=Case(case) if case else None,
        num_class=NumClass(num_class) if num_class else None,
        gender=Gender(gender) if gender else None,
        number=Number(number) if number else None
    )

    logger.debug(f"Converted integer {value} to numeral: {numeral}")
    return numeral['numeral']


def int2numerals(
        value: int,
        lang: str,
        case: Optional[Case] = None,
        num_class: Optional[NumClass] = None,
        gender: Optional[Gender] = None,
        number: Optional[Number] = None) -> str:
    """
    Converts an integer to its corresponding numeral string in the given language and morphological form.

    Args:
        value (int): The input integer value (e.g., 42).
        lang (str): The language code (e.g., 'en', 'uk').
        case (Optional[Case]): The grammatical case to apply.
        num_class (Optional[NumClass]): The numerical class (e.g., ordinal, cardinal).
        gender (Optional[Gender]): The grammatical gender (e.g., masculine, feminine).
        number (Optional[Number]): The number form (singular or plural).

    Returns:
        str: The corresponding numeral string in the given morphological form.

    Example:
        >>> int2numeral(42, lang='uk', case="nominative", num_class="cardinal")
        'сорок два'
    """
    logger.info(f"Converting integer '{value}' to numeral in language '{lang}'")
    _load_language_data_if_needed(lang)
    numeral_items = _int2number_items(value, lang)

    numeral = _number_items2numeral(
        numeral_items,
        lang=lang,
        numeral_data=_NUMERAL_LANGUAGE_DATA[lang].numeral_data,
        value_index=_NUMERAL_LANGUAGE_DATA[lang].value_index,
        case=Case(case) if case else None,
        num_class=NumClass(num_class) if num_class else None,
        gender=Gender(gender) if gender else None,
        number=Number(number) if number else None
    )

    logger.debug(f"Converted integer {value} to numeral: {numeral}")
    return numeral['numeral_forms']
