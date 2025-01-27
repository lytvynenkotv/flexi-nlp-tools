from flexi_nlp_tools.lite_search.utils import tokenize, detokenize


def test_tokenize_detokenize_01():
    tokens, seps = tokenize("iPhone14 proX")
    assert tokens == ['iPhone14', 'proX']
    assert detokenize(tokens, seps) == "iPhone14 proX"


def test_tokenize_detokenize_02():
    tokens, seps = tokenize('LG OLED CX 65"')
    assert detokenize(tokens, seps) == 'LG OLED CX 65"'


def test_tokenize_detokenize_03():
    tokens, seps = tokenize("Яблоко Голден в пакете, 3 кг")
    assert tokens == ["Яблоко", "Голден", "в", "пакете", "3", "кг"]
    assert detokenize(tokens, seps) == "Яблоко Голден в пакете, 3 кг"
