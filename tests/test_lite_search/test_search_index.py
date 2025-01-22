from flexi_dict import FlexiDict

from lite_search import SearchIndex, save_search_index, load_search_index
from lite_search.index_builder import build_search_index


def test_init():
    search_index = SearchIndex()
    assert not len(search_index.items())

    search_index[1] = FlexiDict()
    assert len(search_index.items()) == 1

    search_index[2]['a'] = 1
    assert len(search_index.items()) == 2

    assert search_index[2]['a'] == 1


def test_save_load(tmp_path):
    data = [(1, 'молоко Alpro'), ]
    search_index = build_search_index(data, transliterate_latin=True)

    save_search_index(search_index, tmp_path)

    search_index_loaded = load_search_index(dirname=tmp_path)

    assert search_index_loaded[0]['молоко alpro'] == 1
    assert search_index_loaded[1]['молоко елпро'] == 1
    assert search_index_loaded[2]['еlpro молоко'] == 1
