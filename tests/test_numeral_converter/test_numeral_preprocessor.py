from src.numeral_converter.numeral_preprocessor import preprocess_numeral, preprocess_number_string  # Импортируйте функции


def test_preprocess_numeral_en():
    assert preprocess_numeral("three-and-four", "en") == "three four"
    assert preprocess_numeral("one and two", "en") == "one two"
    assert preprocess_numeral("   five   ", "en") == "five"
    assert preprocess_numeral("seven   eight   nine", "en") == "seven eight nine"


def test_preprocess_numeral_other_languages():
    assert preprocess_numeral("два и три", "ru") == "два и три"


def test_preprocess_number_string():
    assert preprocess_number_string("   FIVE   ") == "five"
    assert preprocess_number_string("ONE") == "one"
    assert preprocess_number_string("   tHRee   ") == "three"
    assert preprocess_number_string("foUr") == "four"
    assert preprocess_number_string("") == ""  # Проверка на пустую строку
