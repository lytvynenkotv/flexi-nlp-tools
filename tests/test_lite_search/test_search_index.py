from flexi_nlp_tools.flexi_dict import FlexiDict

from flexi_nlp_tools.lite_search import SearchIndex


def test_init():
    search_index = SearchIndex()
    assert not len(search_index.items())

    search_index[1] = FlexiDict()
    assert len(search_index.items()) == 1

    search_index[2]['a'] = 1
    assert len(search_index.items()) == 2

    assert search_index[2]['a'] == 1
