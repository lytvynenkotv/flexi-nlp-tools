import pytest

from src.numeral_converter.numeral_data_collector.numeral_data_loader import NumeralDataLoader
from src.numeral_converter.numeral_data_collector.numeral_data_loader.numeral_entry import (
    Number, NumClass, Gender, Case
)

@pytest.fixture
def numeral_data_loader():
    return NumeralDataLoader()


def test_get_available_languages(numeral_data_loader):
    available_languages = numeral_data_loader.get_available_languages()
    assert len(available_languages) > 0


def test_is_available_language(numeral_data_loader):
    assert numeral_data_loader.is_available_language('uk')
    assert numeral_data_loader.is_available_language('ru')
    assert numeral_data_loader.is_available_language('en')
    assert not numeral_data_loader.is_available_language('unrecognized')


def test_load_language_data(numeral_data_loader):
    assert numeral_data_loader.load_language_data('uk')
    assert numeral_data_loader.load_language_data('ru')
    assert numeral_data_loader.load_language_data('en')
    with pytest.raises(ValueError):
        numeral_data_loader.load_language_data('unrecognized')


def test_load_language_data_correctness(numeral_data_loader):
    numeral_data = numeral_data_loader.load_language_data('uk')
    assert len(numeral_data) > 0
    for idx, numeral_entry in numeral_data.items():
        assert isinstance(numeral_entry.string, str)
        assert len(numeral_entry.string) > 0
        assert isinstance(numeral_entry.value, int)
        assert numeral_entry.value >= 0
        assert isinstance(numeral_entry.order, int)
        assert isinstance(numeral_entry.num_class, NumClass)
        assert isinstance(numeral_entry.scale, bool)
        assert numeral_entry.gender is None or isinstance(numeral_entry.gender, Gender)
        assert numeral_entry.number is None or isinstance(numeral_entry.number, Number)
        assert numeral_entry.case is None or isinstance(numeral_entry.case, Case)


def test_load_language_data_correct_scales(numeral_data_loader):
    numeral_data = numeral_data_loader.load_language_data('uk')
    numeral = 'квадрильйон'
    for idx, numeral_entry in numeral_data.items():
        if numeral_entry.string == numeral:
            assert numeral_entry.value == 10**15
            break

    for idx, numeral_entry in numeral_data.items():
        if numeral_entry.value == 1000:
            assert numeral_entry.scale






