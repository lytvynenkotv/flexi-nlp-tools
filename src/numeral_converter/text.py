from typing import List, Optional
from .numeral_converter_helpers import NumberItem, preprocess_numeral, _number_items2int
from .numeral_converter_loader import _load_language_data_if_needed, _NUMERAL_LANGUAGE_DATA
from .patterns import WORD_PATTERN


def convert_numerical_in_text(
    text: str,
    lang: str,
    max_correction_rate: Optional[int] = .2,
) -> str:
    """
    Converts numerical string in text into integer values

    :param str text: input text
    :param str lang: input text language
    :param Optional[float] max_correction_rate: default value to calculate
           maximum number of corrections in the query key when searching
           for a matching dictionary key; default = None
           calculated as round(max_corrections_relative * token_length)
    :return str: updated text with converted numerical into integer

    :Example:

    >>> s = "У цій школі працює шість психологів, "
    ...     "і кожен із нас має навантаження понад сто учнів"
    >>> convert_numerical_in_text(s, lang='uk')
    "У цій школі працює 6 психологів, і кожен із нас має навантаження понад 100 учнів"

    >>> s = "У моєму портфелі лежало чотири книги."
    >>> convert_numerical_in_text(s, lang='uk')
    "У моєму портфелі лежало 4 книги."

    """
    _load_language_data_if_needed(lang)

    updated_text = str()
    i = 0

    number_items: List[NumberItem] = list()
    prev_number_end = None

    for match in WORD_PATTERN.finditer(text):
        number_idxs = _NUMERAL_LANGUAGE_DATA[lang].flexi_index.get(
            preprocess_numeral(match.group(), lang=lang),
            max_correction_rate=max_correction_rate
        )

        if number_idxs:
            idx = number_idxs[0]
            number_item = NumberItem(
                _NUMERAL_LANGUAGE_DATA[lang].numeral_data[idx].value,
                _NUMERAL_LANGUAGE_DATA[lang].numeral_data[idx].order,
                _NUMERAL_LANGUAGE_DATA[lang].numeral_data[idx].scale,
            )

            # number starts
            if not len(number_items):
                updated_text += text[i : match.span()[0]]
                number_items.append(number_item)
                prev_number_end = match.span()[1]
                i = match.span()[1]

            # number continues
            elif match.span()[0] - prev_number_end < 2:
                number_items.append(number_item)
                prev_number_end = match.span()[1]
                i = match.span()[1]

            # prev number ends, new number starts
            else:
                updated_text += str(_number_items2int(number_items))
                updated_text += text[i : match.span()[0]]
                number_items = [
                    number_item,
                ]
                prev_number_end = match.span()[1]
                i = match.span()[1]

    if number_items:
        updated_text += str(_number_items2int(number_items))

    updated_text += text[i:]
    return updated_text
