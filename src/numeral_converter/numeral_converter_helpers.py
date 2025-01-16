import warnings
from typing import List, Optional, Dict, Set, Any
import math
from dataclasses import dataclass
import logging

from .numeral_data_collector.flexi_index_builder.flexi_index_builder import FlexiDict
from .numeral_data_collector.numeral_data_loader.numeral_entry import NumeralEntry, Case, Gender, Number, NumClass
from .numeral_data_collector.numeral_data_loader.numeral_data import NumeralData
from .numeral_preprocessor import preprocess_numeral


logger = logging.getLogger(__name__)


@dataclass
class NumberItem:
    value: int
    order: int
    scale: bool


@dataclass
class NumeralWord:
    default: str
    alt: List[str]


def _numeral2number_items(
        numeral: str, lang: str, flexi_index: FlexiDict, numeral_data: NumeralData) -> List[NumberItem]:
    numeral = preprocess_numeral(numeral, lang)
    number_items: List[NumberItem] = list()

    for i, number_word in enumerate(numeral.split(" ")[::-1]):
        fuzzy_search_result = flexi_index.get(number_word)

        if not len(fuzzy_search_result):
            raise ValueError(f'can\'t convert "{number_word}" to integer')

        if i > 0:
            fuzzy_search_result = [
                idx
                for idx in fuzzy_search_result
                if not _is_ordinal(numeral_data[idx])
            ]
            if not len(fuzzy_search_result):
                raise ValueError(f'ordinal numeral word "{number_word}" inside numeral')


        numeral_idx = fuzzy_search_result[0]
        numeral_entry = numeral_data[numeral_idx]

        number_items.insert(
            0,
            NumberItem(
                value=numeral_entry.value,
                order=numeral_entry.order,
                scale=numeral_entry.scale,
            ),
        )

    return number_items


def _number_items2int(number_items: List[NumberItem]) -> int:
    int_value = 0
    number_items = number_items[::-1]

    i_number = num_block_start = 0
    num_block_order = 0

    if number_items[0].scale:
        i_number = num_block_start = 1
        num_block_order = number_items[0].order

    while i_number < len(number_items):
        i_number, inner_order = __search_block(number_items, i_number, num_block_order)
        __check_correct_order(number_items, num_block_start, i_number, inner_order)
        __value = (
            _number_items2int(number_items[num_block_start:i_number][::-1])
            if inner_order
            else max(sum([x.value for x in number_items[num_block_start:i_number]]), 1)
        )

        int_value += (10**num_block_order) * __value
        if i_number >= len(number_items):
            return int(int_value)

        __check_number_is_correct_scale(number_items, i_number, int_value)
        num_block_order = number_items[i_number].order
        num_block_start = i_number + 1
        i_number += 1

    if num_block_start is not None:
        int_value += 10**num_block_order

    return int(int_value)


def _int2number_items(number: int, lang: str) -> List[NumberItem]:

    logger.debug(f'In _int2number_items:\n\tnumber: {number}\n\tlang: {lang}')
    if number == 0:
        return [
            NumberItem(0, -1, None),
        ]

    number_items: List[NumberItem] = list()
    current_order, ones = 0, None  # type: int, Optional[int]

    mem = None

    while number:
        logger.debug(f'Step #{number}')
        digit = number % 10
        if current_order % 3 == 2 and digit:

            if mem:
                logger.debug(f'Step #{number}: detected order % 3 == 2, inserted from mem: {mem}')
                number_items.insert(0, mem)
                mem = None
            if lang == 'en':
                number_items.insert(0, NumberItem(100, current_order % 3, None))
                number_items.insert(0, NumberItem(digit, current_order % 3, None))
                logger.debug(f'Step #{number}: detected order == 2, inserted {digit} and {100}')
            else:
                number_items.insert(0, NumberItem(100 * digit, current_order % 3, None))
                logger.debug(f'Step #{number}: detected order == 2, inserted {100 * digit}')

        elif current_order % 3 == 0:
            logger.debug(f'Step #{number}: detected order % 3 == 0')
            ones = digit
            if current_order > 0:
                mem = NumberItem(10**current_order, current_order, True)
        else:
            logger.debug(f'Step #{number}')
            if digit == 1 and ones > 0:
                value = 10 * digit + ones
                if value:
                    if mem:
                        number_items.insert(0, mem)
                        mem = None
                    number_items.insert(0, NumberItem(value, current_order % 3, None))
                    logger.debug(f'Step #{number}: inserted {value}')
            else:
                if ones:
                    if mem:
                        number_items.insert(0, mem)
                        mem = None
                    number_items.insert(0, NumberItem(ones, 0, None))
                    logger.debug(f'Step #{number}: inserted {ones}')

                if digit:
                    if mem:
                        number_items.insert(0, mem)
                        mem = None
                    number_items.insert(
                        0, NumberItem(10 * digit, current_order % 3, None)
                    )
                    logger.debug(f'Step #{number}: inserted {10 * digit}')

            ones = None

        current_order += 1
        number = number // 10

    if ones:
        if mem:
            number_items.insert(0, mem)
        number_items.insert(0, NumberItem(ones, 0, None))

    if number_items[0].scale is not None:
        number_items.insert(0, NumberItem(1, 0, None))

    logger.debug(f'Result: {number_items}')
    return number_items


def __int2numeral_word(
        value: int,
        value_index: Dict[int, Set[int]],
        numeral_data: NumeralData,
        case: Optional[Case] = None,
        num_class: Optional[NumClass] = None,
        gender: Optional[Gender] = None,
        number: Optional[Number] = None) -> NumeralWord:

    case = case or Case.NOMINATIVE
    num_class = num_class or NumClass.CARDINAL
    gender = gender or Gender.MASCULINE
    number = number or (Number.SINGULAR if value in (0, 1) else Number.PLURAL)

    logger.debug(f'In __int2numeral_word(value={value}, case={case}, num_class={num_class}, gender={gender}, number={number})')

    sub_entry_indices = value_index[value]

    if len(sub_entry_indices) == 0:
        raise ValueError(f"no data for number {value}")

    numeral_words = list()

    if num_class and numeral_data.is_available_num_class:
        logger.debug(f'Check num_class, expect {num_class}, got in list: {[(numeral_data[x].string, numeral_data[x].num_class.value if numeral_data[x].num_class else "None") for x in sub_entry_indices]}')
        sub_entry_indices = [idx for idx in sub_entry_indices if numeral_data[idx].num_class is None or numeral_data[idx].num_class == num_class]
        logger.debug(f'Filtered list: {[numeral_data[x].string for x in sub_entry_indices]}')

    if case and numeral_data.is_available_case:
        logger.debug(f'Check case, expect {case}, got in list: {[(numeral_data[x].string, numeral_data[x].case.value if numeral_data[x].case else "None") for x in sub_entry_indices]}')
        sub_entry_indices = [idx for idx in sub_entry_indices if numeral_data[idx].case is None or numeral_data[idx].case == case]
        logger.debug(f'Filtered list: {[numeral_data[x].string for x in sub_entry_indices]}')

    if gender and numeral_data.is_available_gender:
        logger.debug(f'Check gender, expect {gender}, got in list: {[(numeral_data[x].string, numeral_data[x].gender.value if numeral_data[x].gender else "None") for x in sub_entry_indices]}')
        sub_entry_indices = [idx for idx in sub_entry_indices if numeral_data[idx].gender is None or numeral_data[idx].gender == gender]
        logger.debug(f'Filtered list: {[numeral_data[x].string for x in sub_entry_indices]}')

    if number and numeral_data.is_available_number:
        logger.debug(f'Check number, expect {number}, got in list: {[(numeral_data[x].string, numeral_data[x].number.value if numeral_data[x].number else "None") for x in sub_entry_indices]}')
        sub_entry_indices = [idx for idx in sub_entry_indices if numeral_data[idx].number is None or numeral_data[idx].number == number]
        logger.debug(f'Filtered list: {[numeral_data[x].string for x in sub_entry_indices]}')

    for idx in sub_entry_indices:
        numeral_entry = numeral_data[idx]
        if numeral_entry.string not in numeral_words:
            numeral_words.append(numeral_entry.string)
            logger.debug(f'+ added "{numeral_entry.string}" to number list')

    return NumeralWord(numeral_words[0], numeral_words[1:])


def _number_items2numeral(
        number_items: List[NumberItem],
        lang: str,
        numeral_data: NumeralData,
        value_index: Dict[int, Set[int]],
        case: Optional[Case] = None,
        num_class: Optional[NumClass] = None,
        gender: Optional[Gender] = None,
        number: Optional[Number] = None) -> Dict[str, Any]:

    logger.debug(
        f'In _number_items2numeral:\n'
        f'\t number_items: {[i.value for i in number_items]}\n'
        f'\t         case: {case}\n'
        f'\t    num_class: {num_class}\n'
        f'\t       gender: {gender}\n'
        f'\t       number: {number}')

    if num_class is not None and num_class == NumClass.COLLECTIVE and len(number_items) > 1:
        warnings.warn("Can't convert to collective numeral number; cardinal used")
        num_class = NumClass.CARDINAL

    numbers = list()
    for i, number_item in enumerate(number_items):
        logger.debug(f'\nNumber item #{i}/{len(number_items)} {number_item}')

        if i == len(number_items) - 1:

            d_case = __define_morph_case(case, number_items, i, num_class)
            d_number = __define_morph_number(number, number_items, i)
            logger.debug(
                f'\nNumber item #{i}/{len(number_items)}: detected last number; '
                f'next morph changes will be applied:\n\tcase: {case}->{d_case}\n\tnumber: {number}->{d_number}')
            numbers.append(
                __int2numeral_word(
                    number_item.value,
                    numeral_data=numeral_data,
                    value_index=value_index,
                    case=d_case,
                    number=d_number,
                    num_class=num_class,
                    gender=gender,
                )
            )
            continue

        if (
            (0 < number_item.value < 10)
            and (i + 1 < len(number_items))
            and number_items[i + 1].scale
        ):

            d_gender = __define_morph_gender(number_items, i)
            d_case = __define_morph_case(case, number_items, i, num_class)
            d_number = __define_morph_number(number, number_items, i)
            logger.debug(
                f'Number item #{i}/{len(number_items)}: detected inner number before scaled; '
                f'next morph changes will be applied:\n'
                f'\tgender: {gender}->{d_gender}\n\tcase: {case}->{d_case}\n\tnumber: {number}->{d_number}')
            numbers.append(
                __int2numeral_word(
                    number_item.value, case=d_case, gender=d_gender, numeral_data=numeral_data, number=d_number, value_index=value_index)
            )
            continue

        if number_item.scale:
            d_case = __define_morph_case(case, number_items, i, num_class)
            d_number = __define_morph_number(number, number_items, i)
            logger.debug(
                f'Number item #{i}/{len(number_items)}: Detected scaled; '
                f'next morph changes will be applied:\n\tnumber: {number}->{d_number}\n\tcase: {case}->{d_case}')
            numbers.append(
                __int2numeral_word(
                    number_item.value, numeral_data=numeral_data, value_index=value_index, case=d_case, number=d_number)
            )
            continue

        d_case = __define_morph_case(case, number_items, i, num_class)
        numbers.append(
            __int2numeral_word(number_item.value, numeral_data=numeral_data, value_index=value_index, case=d_case))

    return __process_numbers(numbers, number_items, lang=lang)


def __check_correct_order(
    number_items: List[NumberItem], start: int, end: int, inner_order: Optional[int]
):
    for k in range(start + 1, end):
        __order = (
            0
            if number_items[k].value % 10 ** number_items[k].order
            else number_items[k].order
        )

        if not inner_order and number_items[k - 1].order >= __order:
            raise ValueError(
                f"position {len(number_items) - k}: {number_items[k - 1].value}"
                f" with order {number_items[k - 1].order} stands after "
                f"{number_items[k].value} with less/equal order {__order}"
            )

        if inner_order and number_items[k - 1].order == __order:
            raise ValueError(
                f"position {len(number_items) - k}: {number_items[k - 1].value}"
                f" with order {number_items[k - 1].order} stands after "
                f"{number_items[k].value} with equal order {__order}"
            )


def __search_block(number_items, start, num_block_order):
    inner_order = None
    while start < len(number_items) and (
        not number_items[start].scale or number_items[start].order < num_block_order
    ):
        if number_items[start].scale and (
            inner_order is None or inner_order < number_items[start].order
        ):
            inner_order = number_items[start].order
        start += 1
    return start, inner_order


def __check_number_is_correct_scale(number_items, i_number, int_value):
    if not number_items[i_number].scale:
        raise ValueError(
            f"position {len(number_items) - 1 - i_number}: expects 10^(3n) or 100; "
            f"found {number_items[i_number].value}"
        )

    value_order = int(math.log10(int_value))
    if number_items[i_number].order <= value_order:
        raise ValueError(
            f"position {len(number_items) - 1 - i_number}: order of "
            f"{number_items[i_number].value}:{number_items[i_number].order} "
            f"is less/equal of summary order in next group: {value_order}"
        )


def __define_morph_number(global_number: str, number_items: List[NumberItem], i: int) -> Number:

    number = global_number

    prev_value = number_items[i - 1].value if i > 0 else 1

    if number_items[i].scale:
        number = Number.SINGULAR if prev_value == 1 else Number.PLURAL

    if i + 1 < len(number_items):
        if number_items[i + 1].scale and not number_items[i].scale:
            number = Number.PLURAL if number_items[i].value != 1 else Number.SINGULAR

    return number


def __define_morph_case(global_case, number_items, i, global_num_class) -> Case:
    case = global_case
    prev_value = number_items[i - 1].value if i > 0 else 1

    if i == len(number_items) - 1:
        if number_items[i].scale:
            case = (
                Case.NOMINATIVE
                if prev_value == 1
                else Case.NOMINATIVE
                if prev_value in (2, 3, 4)
                else Case.GENETIVE
            )

        return case

    if global_num_class == NumClass.ORDINAL:
        case = Case.NOMINATIVE

    if (
        (0 < number_items[i].value < 10)
        and (i + 1 < len(number_items))
        and number_items[i + 1].scale
    ):
        if case == Case.ACCUSATIVE:
            case = Case.NOMINATIVE
        return case

    if number_items[i].scale:
        if case in (Case.NOMINATIVE, Case.ACCUSATIVE):
            case = Case.NOMINATIVE if prev_value in (1, 2, 3, 4) else Case.GENETIVE
            return case

    if case == Case.ACCUSATIVE and i != len(number_items) - 2:
        case = Case.NOMINATIVE

    return case


def __define_morph_gender(number_items, i):
    return Gender.FEMININE if number_items[i + 1].value == 1000 else Gender.MASCULINE


def __process_numbers(numbers: List[NumeralWord], number_items, lang: str) -> Dict[str, Any]:
    if lang == "en":
        numbers__ = numbers.copy()
        numbers = list()
        i = 0
        while i < len(number_items):
            if (
                i + 1 < len(number_items)
                and number_items[i].order == 1
                and number_items[i + 1].order == 0
            ):
                numbers.append(
                    NumeralWord(
                        numbers__[i].default + "-" + numbers__[i + 1].default, []
                    )
                )
                i += 2
            else:
                numbers.append(numbers__[i])
                i += 1

    numeral = " ".join(
        [
            f"{number.default}" + (f" ({', '.join(number.alt)})" if number.alt else "")
            for number in numbers
        ]
    )

    numeral_forms = [
        " ".join(
            [
                (
                    [
                        numbers[i].default,
                    ]
                    + numbers[i].alt
                )[j]
                for i, j in enumerate(__combinations)
            ]
        )
        for __combinations in __get_combinations(
            *[range(1 + len(number.alt)) for number in numbers]
        )
    ]

    return {'numeral': numeral, 'numeral_forms': numeral_forms}


def _is_ordinal(numeral_entry: NumeralEntry):
    if numeral_entry.num_class is not None and numeral_entry.num_class == NumClass.ORDINAL:
        return True
    return False


def __get_combinations(*args):
    def __combinations(res, a):
        for r in res:
            for x in a:
                yield r + [
                    x,
                ]

    result = None
    for arr in args:
        if result is None:
            result = (
                [
                    _,
                ]
                for _ in arr
            )
        else:
            result = __combinations(result, arr)

    return result
