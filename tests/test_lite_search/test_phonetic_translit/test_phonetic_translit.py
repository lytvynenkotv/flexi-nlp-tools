import re


from lite_search.phonetic_translit import latin_to_cyrillic_phonetic
from lite_search.phonetic_translit.constants import PHONEME2UK
from lite_search.phonetic_translit.preprocessor import _preprocess_phoneme


def test_preprocess_phoneme():
    assert _preprocess_phoneme('AH0') == 'AH'


def test_phoneme2uk():
    assert PHONEME2UK.get('AH') == ['а', ]
    for phoneme, cyr_strings in PHONEME2UK.items():
        for cyr_string in cyr_strings:
            assert re.match('[а-яґі\s]+', cyr_string) is not None, f"there are non cyrillic symbols in phoneme {phoneme}: {cyr_string}"


def test_latin_to_cyrillic_phonetic_01():
    test_data = [
        {'latin': 'alpro', 'expect': ['елпро', ]},
        {'latin': 'coca', 'expect': ['кока', ]},
        {'latin': 'cola', 'expect': ['кола',]},
        {'latin': 'columbia', 'expect': ['каламбіа', ]},
        {'latin': 'Samsung', 'expect': ['самсунг', ]},
    ]
    for test_row in test_data:
        latin = test_row['latin']
        expect = test_row['expect']
        translit = latin_to_cyrillic_phonetic(latin)
        for cyr in expect:
            assert cyr in translit, f'"{cyr}" not in latin_to_cyrillic_phonetic("{latin}")? expect one of {translit}'


def test_latin_to_cyrillic_phonetic_02():
    test_data = [
        {
            'latin': 'YARO Veggie cheese',
            'expect': ['яро веджі чіз', 'яро ваджі чіз', 'єро веджі чіз', 'єро ваджі чіз']
        },
        {
            'latin': 'coca cola',
            'expect': ['кока кола', ]
        }
    ]
    for test_row in test_data:
        latin = test_row['latin']
        expect = test_row['expect']
        translit = latin_to_cyrillic_phonetic(latin)
        for cyr in expect:
            assert cyr in translit, f'"{cyr}" not in latin_to_cyrillic_phonetic("{latin}")? expect one of {translit}'


def test_latin_to_cyrillic_phonetic_04():
    test_data = [
        {'latin': 'Coca-Cola', 'expect': ['кока-кола', ]},
        {'latin': 'iPhone 14 Pro', 'expect': ['айфон 14 про', ]},
        {'latin': 'Samsung Galaxy S23+', 'expect': ['самсунг галаксі с23+', ]},
        {'latin': 'NVIDIA RTX 4080', 'expect': ['нвідіа ртx 4080', ]},
        {'latin': 'HOKKAIDO CLUB', 'expect': ['хокаідо клаб', 'хокайдо клаб']},
        {'latin': 'sonatural', 'expect': ['санечеал']}]
    for test_row in test_data:
        latin = test_row['latin']
        expect = test_row['expect']
        translit = latin_to_cyrillic_phonetic(latin)
        for cyr in expect:
            assert cyr in translit, f'"{cyr}" not in latin_to_cyrillic_phonetic("{latin}")? expect one of {translit}'
