from lite_search.index_builder import build_search_index, update_search_index


def test_build_index():
    data = [(1, 'молоко Alpro'), ]
    search_index = build_search_index(data, transliterate_latin=True)
    assert search_index[0]['молоко alpro'] == 1
    assert search_index[1]['молоко елпро'] == 1
    assert search_index[2]['еlpro молоко'] == 1
