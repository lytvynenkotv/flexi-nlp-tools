import pytest

from src.numeral_converter.numeral_data_collector.numeral_data_loader.numeral_entry import Case, NumClass, Gender, Number
from src.numeral_converter.numeral_converter_loader import _get_language_data
from src.numeral_converter.numeral_converter_helpers import (
    __get_combinations,
    __int2numeral_word,
    _numeral2number_items,
    _number_items2int,
    NumberItem
)


def test_number_items2int():
    # "тисяча сто"
    assert (
        _number_items2int(
            number_items=[
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=100, order=2, scale=None),
            ]
        )
        == 1100
    )

    assert (
        _number_items2int(
            number_items=[
                NumberItem(value=100, order=2, scale=None),
                NumberItem(value=11, order=1, scale=None),
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=100, order=2, scale=None),
                NumberItem(value=11, order=1, scale=None),
            ]
        )
        == 111111
    )

    assert (
        _number_items2int(
            number_items=[
                NumberItem(value=100, order=2, scale=None),
                NumberItem(value=40, order=1, scale=None),
                NumberItem(value=2, order=0, scale=None),
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=30, order=1, scale=None),
                NumberItem(value=1, order=0, scale=None),
            ]
        )
        == 142031
    )

    assert (
        _number_items2int(
            number_items=[
                NumberItem(200, 2, None),
                NumberItem(20, 1, None),
                NumberItem(2, 0, None),
            ]
        )
        == 222
    )


def test_less_eq_summary_order_in_next_group():
    msg = (
        r"position 1: order of 1000000000:9 is less/equal "
        r"of summary order in next group: 9"
    )
    with pytest.raises(ValueError, match=msg):
        _number_items2int(
            [
                NumberItem(value=3, order=0, scale=None),
                NumberItem(value=1000000000, order=9, scale=True),
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=50, order=1, scale=None),
                NumberItem(value=5, order=0, scale=None),
                NumberItem(value=1000000, order=6, scale=True),
            ]
        )

    msg = (
        "position 1: order of 1000000000:9 is less/equal "
        "of summary order in next group: 9"
    )
    with pytest.raises(ValueError, match=msg):
        _number_items2int(
            [
                NumberItem(value=3, order=0, scale=None),
                NumberItem(value=1000000000, order=9, scale=True),
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=1000000, order=6, scale=True),
            ]
        )

    # "тисяча тисяч"
    msg = "position 0: order of 1000:3 is less/equal of summary order in next group: 3"
    with pytest.raises(ValueError, match=msg):
        _number_items2int(
            number_items=[NumberItem(1000, 3, True), NumberItem(1000, 3, True)]
        )

    # тисяча двадцять сотень
    msg = "position 0: order of 1000:3 is less/equal of summary order in next group: 3"
    with pytest.raises(ValueError, match=msg):
        _number_items2int(
            number_items=[
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=20, order=1, scale=None),
                NumberItem(value=100, order=2, scale=True),
            ]
        )


def test_wrong_by_next_value_order_values():
    msg = "position 1: 2 with order 0 stands after 12 with less/equal order 0"
    with pytest.raises(ValueError, match=msg):
        _number_items2int(
            number_items=[
                NumberItem(value=12, order=1, scale=None),
                NumberItem(value=2, order=0, scale=None),
            ]
        )


def test_wrong_by_scale_values():
    # "триста сто три"
    with pytest.raises(ValueError):
        _number_items2int(
            number_items=[
                NumberItem(value=300, order=2, scale=None),
                NumberItem(value=100, order=2, scale=False),
                NumberItem(value=3, order=0, scale=None),
            ]
        )


def test_scale_of_scale():
    # "тисяча мільонів"
    assert (
        _number_items2int(
            number_items=[
                NumberItem(1000, 3, True),
                NumberItem(1000000, 6, True),
            ]
        )
        == 1000000000
    )

    # "триста сотень три"
    assert (
        _number_items2int(
            number_items=[
                NumberItem(value=300, order=2, scale=None),
                NumberItem(value=100, order=2, scale=True),
                NumberItem(value=3, order=0, scale=None),
            ]
        )
        == 30003
    )


def test_int2numeral_word_existing_number_word_with_one_form():
    numeral_data = _get_language_data('uk')
    R = __int2numeral_word(
        12, 
        numeral_data=numeral_data.numeral_data,
        value_index=numeral_data.value_index
    )
    assert R.default == "дванадцять"
    assert len(R.alt) == 0


def test_int2numeral_word_existing_number_word_with_several_forms():
    numeral_data = _get_language_data('uk')
    R = __int2numeral_word(
        7,         
        numeral_data=numeral_data.numeral_data,
        value_index=numeral_data.value_index, 
        case=Case.DATIVE
    )
    assert len(R.alt) == 1
    assert R.alt == [
        "сімом",
    ]


def test_int2numeral_word_converting_in_different_morph_forms():
    numeral_data = _get_language_data('uk')
    R = __int2numeral_word(
        12, 
        numeral_data=numeral_data.numeral_data,
        value_index=numeral_data.value_index, 
        num_class=NumClass.ORDINAL, gender=Gender.FEMININE,
        number=Number.SINGULAR)
    assert R.default == "дванадцята"

    R = __int2numeral_word(
        12,
        numeral_data=numeral_data.numeral_data,
        value_index=numeral_data.value_index,
        num_class=NumClass.ORDINAL,
        gender=Gender.MASCULINE,
        number=Number.SINGULAR
    )
    assert R.default == "дванадцятий"

    R = __int2numeral_word(
        12,
        numeral_data=numeral_data.numeral_data,
        value_index=numeral_data.value_index,
        num_class=NumClass.ORDINAL,
        number=Number.PLURAL,
        gender=Gender.MASCULINE
    )
    assert R.default == "дванадцяті"


def test_int2numeral_word_converting_in_not_full_morph_form():
    numeral_data = _get_language_data('uk')
    assert __int2numeral_word(
        1000,
        numeral_data=numeral_data.numeral_data,
        value_index=numeral_data.value_index,
        number=Number.SINGULAR).default == "тисяча"


def test_int2numeral_word_number_without_data():
    numeral_data = _get_language_data('uk')
    msg = "no data for number 42"
    with pytest.raises(ValueError, match=msg):
        __int2numeral_word(
            42,
            numeral_data=numeral_data.numeral_data,
            value_index=numeral_data.value_index,
        )


def test_numeral2number_items_uk():
    numeral_data = _get_language_data('uk')
    
    R = _numeral2number_items(
        "двісти тридцать чотири тисячі шістот п’ятнадцять", 
        lang="uk",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 6
    assert R[0].value == 200
    assert R[1].value == 30
    assert R[2].value == 4
    assert R[3].value == 1000
    assert R[4].value == 600
    assert R[5].value == 15

    R = _numeral2number_items(
        "три мільони шість тисяч шістдесят сім мільон двісті двадцясь "
        "сім тисяч сто тридцять чотири",
        lang="uk",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 14

    R = _numeral2number_items(
        "сто сорок дві тисячі тридцять один", 
        lang="uk",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 6
    assert R[0].value == 100
    assert R[1].value == 40
    assert R[2].value == 2
    assert R[3].value == 1000
    assert R[4].value == 30
    assert R[5].value == 1

    R = _numeral2number_items(
        "тисяча сорок дві тисячі", 
        lang="uk",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 4
    assert R[0].value == 1000
    assert R[1].value == 40
    assert R[2].value == 2
    assert R[3].value == 1000

    R = _numeral2number_items(
        "дванадцять сотня", 
        lang="uk",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index)
    assert len(R) == 2
    assert R[0].value == 12
    assert R[1].value == 100

    numeral_data = _get_language_data('en')
    R = _numeral2number_items(
        "one hundred forty-two thousand thirty-one", 
        lang="en",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index)
    assert R[0].value == 1
    assert R[1].value == 100
    assert R[1].scale
    assert R[2].value == 40
    assert R[3].value == 2
    assert R[4].value == 1000
    assert R[4].scale
    assert R[5].value == 30
    assert R[6].value == 1


def test_numeral2number_items_ru():
    numeral_data = _get_language_data('ru')
    R = _numeral2number_items(
        "двести тридцать четыре тысячи шестьсот пятнадцать", 
        lang="ru",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 6
    assert R[0].value == 200
    assert R[1].value == 30
    assert R[2].value == 4
    assert R[3].value == 1000
    assert R[4].value == 600
    assert R[5].value == 15

    R = _numeral2number_items(
        "три миллиона шесть тысяч шестдесят семь миллионов двести двадцать семь тысяч "
        "сто тридцать четыре",
        lang="ru",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 14

    R = _numeral2number_items(
        "сто сорок две тисячи тридцать один",
        lang="ru",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 6
    assert R[0].value == 100
    assert R[1].value == 40
    assert R[2].value == 2
    assert R[3].value == 1000
    assert R[4].value == 30
    assert R[5].value == 1

    R =_numeral2number_items("тысяча сорок две тысячи",
        lang="ru",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 4
    assert R[0].value == 1000
    assert R[1].value == 40
    assert R[2].value == 2
    assert R[3].value == 1000

    R =_numeral2number_items("двенадцать сто",
        lang="ru",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 2
    assert R[0].value == 12
    assert R[1].value == 100
    
    numeral_data = _get_language_data('en')

    R =_numeral2number_items("nine hundred and ninety-nine thousand",
        lang="en",
        numeral_data=numeral_data.numeral_data,
        flexi_index=numeral_data.flexi_index
    )
    assert len(R) == 5
    assert R[0].value == 9
    assert R[1].value == 100
    assert R[2].value == 90
    assert R[3].value == 9
    assert R[4].value == 1000


def test_numeral2number_items_with_not_number():
    numeral_data = _get_language_data('uk')
    msg = 'Cannot convert "варіант" to integer'
    with pytest.raises(ValueError, match=msg):
       _numeral2number_items(
           "перший варіант",
            lang="uk",
            numeral_data=numeral_data.numeral_data,
            flexi_index=numeral_data.flexi_index
    )


def test_one_item_array():
    assert list(
        __get_combinations(
            [1, 2],
        )
    ) == [[1], [2]]


def test_one_item_arrays():
    assert list(
        __get_combinations(
            [
                1,
            ],
            [
                1,
            ],
        )
    ) == [[1, 1]]


def test_combinations():
    assert list(
        __get_combinations(
            [
                1,
            ],
            [
                1,
                2,
            ],
            [1, 2, 3],
        )
    ) == [[1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 2, 1], [1, 2, 2], [1, 2, 3]]


def test_combinations_ranges():
    assert list(
        __get_combinations(
            range(1),
            range(2),
            range(3),
        )
    ) == [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1], [0, 1, 2]]


def test_combinations_empty_ranges():
    assert list(__get_combinations(range(1), range(1), range(1),)) == [
        [0, 0, 0],
    ]


def test_combinations_ranges_list():
    r = [
        range(1),
        range(1),
        range(1),
    ]
    assert list(__get_combinations(*r)) == [
        [0, 0, 0],
    ]
