import pytest

from flexi_nlp_tools.numeral_converter.numeral_data_collector import NumeralDataCollector
from flexi_nlp_tools.numeral_converter.numeral_data_collector.numeral_data_loader.numeral_entry import NumeralEntry


@pytest.fixture
def numeral_data_collector():
    numeral_data_collector = NumeralDataCollector()
    return numeral_data_collector


def test_collect(numeral_data_collector):
    numeral_data_collector.collect(lang='uk')
    numeral_data_collector.collect(lang='ru')
    numeral_data_collector.collect(lang='en')


def test_collect_correctness_en(numeral_data_collector):
    numeral_data_container = numeral_data_collector.collect(lang='en')
    assert isinstance(numeral_data_container.numeral_data[1], NumeralEntry)

    idx = numeral_data_container.flexi_index['one']
    numeral_entry = numeral_data_container.numeral_data[idx]
    assert numeral_entry.value == 1

    idx = numeral_data_container.flexi_index['first']
    numeral_entry = numeral_data_container.numeral_data[idx]
    assert numeral_entry.value == 1

    idx = numeral_data_container.flexi_index['hundred']
    numeral_entry = numeral_data_container.numeral_data[idx]
    assert numeral_entry.value == 100


def test_collect_correctness_ru(numeral_data_collector):

    numeral_data_container = numeral_data_collector.collect(lang='ru')
    idx = numeral_data_container.flexi_index['двести']
    numeral_entry = numeral_data_container.numeral_data[idx]
    assert numeral_entry.value == 200


def test_value_index(numeral_data_collector):
    numeral_data_container = numeral_data_collector.collect(lang='ru')
    assert 1000000000000000000000000000000000 in numeral_data_container.value_index
    assert 10**33 in numeral_data_container.value_index

