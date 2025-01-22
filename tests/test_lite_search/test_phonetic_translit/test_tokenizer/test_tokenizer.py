from lite_search.phonetic_translit.tokenizer import tokenize, detokenize


def test_tokenize_detokenize():
    tokens, seps = tokenize("iPhone14 proX")
    assert tokens == ['i', 'Phone', 'pro', 'X']
    assert detokenize(tokens, seps) == "iPhone14 proX"

    tokens, seps = tokenize('LG OLED CX 65"')
    print(tokens)
    print(seps)
    assert detokenize(tokens, seps) == 'LG OLED CX 65"'
