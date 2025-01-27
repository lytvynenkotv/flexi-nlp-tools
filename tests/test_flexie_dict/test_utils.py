from flexi_nlp_tools.flexi_dict import calculate_symbols_distances, calculate_symbols_weights


def test_calculate_symbols_weights():
    corpus = [
        "apple golden delicious", "apple red delicious", "apple granny smith",
        "apple honeycrisp", "apple pink lady", "apple fuji"]
    symbol_weights = calculate_symbols_weights(corpus)
    assert symbol_weights['p'] > symbol_weights['a'] > symbol_weights['j']


def test_calculate_symbols_distances_01():
    keyboards = [
        """'`1234567890-=
  qwertyuiop[]
  asdfghjkl;'
   zxcvbnm,./""",
        """ґ1234567890-=
  йцукенгшщзхїʼ
  фівапролджє
   ячсмитьбю.""",
    ]

    symbols_distances = calculate_symbols_distances(symbol_keyboards=keyboards)
    assert symbols_distances[('1', '2')] < symbols_distances[('1', '0')]
    assert symbols_distances[('q', 'w')] < symbols_distances[('q', 'm')]
    assert symbols_distances[('q', 'й')] < symbols_distances[('q', 'e')]
    assert symbols_distances[('q', 'й')] >= symbols_distances[('q', 'w')]


def test_calculate_symbols_distances_02():
    keyboards = [
        """'`1234567890-=
  qwertyuiop[]
  asdfghjkl;'
   zxcvbnm,./""",
    ]

    symbols_distances = calculate_symbols_distances(symbol_keyboards=keyboards)
    assert symbols_distances[('1', '2')] < symbols_distances[('1', '0')]
    assert symbols_distances[('q', 'w')] < symbols_distances[('q', 'm')]
