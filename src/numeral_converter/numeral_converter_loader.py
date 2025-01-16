from typing import Dict
import logging

from .numeral_data_collector import NumeralDataContainer, NumeralDataCollector
from .numeral_data_collector.numeral_data_collector import NumeralDataLoader
logger = logging.getLogger(__name__)

_NUMERAL_LANGUAGE_DATA: Dict[str, NumeralDataContainer] = {}


def _load_language_data_if_needed(lang: str):
    """
    Check if the language is already loaded, and if not, load the necessary language data.

    Args:
        lang (str): The language code (e.g., 'en', 'uk', 'ru').
    """
    if lang not in _NUMERAL_LANGUAGE_DATA:
        logger.debug(f"Loading language data for: {lang}")
        numeral_data_collector = NumeralDataCollector()
        _NUMERAL_LANGUAGE_DATA[lang] = numeral_data_collector.collect(lang)
    else:
        logger.debug(f"Language data for '{lang}' is already loaded.")


def get_available_languages():
    numeral_data_loader = NumeralDataLoader()
    available_languages = numeral_data_loader.get_available_languages()
    return available_languages
