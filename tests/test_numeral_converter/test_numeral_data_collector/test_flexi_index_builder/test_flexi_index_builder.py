from unittest.mock import Mock

from src.numeral_converter.numeral_data_collector.flexi_index_builder import FlexiIndexBuilder
from src.numeral_converter.numeral_data_collector.numeral_data_loader import NumeralDataLoader

import pytest




@pytest.fixture
def numeral_data_loader() -> NumeralDataLoader:
    return NumeralDataLoader()


@pytest.fixture
def flexi_index_builder() -> FlexiIndexBuilder:
    flexi_index_builder = FlexiIndexBuilder()
    return flexi_index_builder


@pytest.fixture
def numeral_data_mock():
    numeral_data_mock = {
        1: Mock(string='first', value=1),
        2: Mock(string='one', value=1),
        3: Mock(string='second', value=2),
        4: Mock(string='third', value=3),
        5: Mock(string='three', value=3)
    }
    return numeral_data_mock


def test_build(flexi_index_builder, numeral_data_mock):
    flexi_index = flexi_index_builder.build(numeral_data_mock)
    assert flexi_index.get('first', max_correction_rate=.6) == [1, ]
    assert flexi_index.get('frst', max_correction_rate=.6) == [1, ]
    assert flexi_index.search('t', max_correction_rate=.6) == [4, 5]


def test_build_for_language(flexi_index_builder, numeral_data_loader):
    numeral_data = numeral_data_loader.load_language_data('ru')
    flexi_index = flexi_index_builder.build(numeral_data)

    idxs = flexi_index.get('двести')
    assert len(idxs) > 0

    idx= idxs[0]
    assert numeral_data[idx].value == 200



