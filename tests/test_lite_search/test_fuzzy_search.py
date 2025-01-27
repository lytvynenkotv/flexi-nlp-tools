from flexi_nlp_tools.lite_search import fuzzy_search, fuzzy_search_internal, build_search_index


def test_fuzzy_search_01():
    data = [(1, 'one'), (2, 'two'), (3, 'three')]
    search_index = build_search_index(data)
    assert fuzzy_search(query='one', search_index=search_index) == [1, ]


def test_fuzzy_search_02():

    data = [
        (1, 'Бургер Веган'),
        (2, 'Бургер зі Свининою'),
        (3, 'Бургер з м\'ясом і часником'),
        (4, 'Біг Бургер'),
        (5, 'Чіз бургер Веган'),
        (6, 'Салат з буряком'),
        (7, 'Чіз бургер з курятиною'),
        (8, 'Салат з буряком та картоплею'),
        (9, 'Булгур'),
        (10, 'Салат з топінамбуром'),
    ]

    search_index = build_search_index(data)

    query = 'бур'
    search_result = fuzzy_search(query=query, search_index=search_index)

    assert set(search_result) == {1, 2, 3, 4, 5, 6, 7, 8, 9}
    assert search_result[0] in (1, 2, 3)
    assert 10 not in search_result

    query = 'бургер'
    result = fuzzy_search(query=query, search_index=search_index)

    assert result.index(1) < result.index(2)
    assert result.index(1) < result.index(3)
    assert result.index(2) < result.index(4)
    assert result.index(3) < result.index(4)
    assert result.index(1) < result.index(2)

    assert 10 not in result


def test_index_search_03() -> None:

    data = [
        (1, 'Риба варена'),
        (2, 'Риба жарена'),
        (3, 'Суп з Рибою'),
        (4, 'Суп Рибний'),
        (5, 'Котлета Рибна'),
        (6, 'Бургер Рибний'),
        (7, 'Руколла'),
        (8, 'Пиво'),
        (9, 'Сир Брі'),
        (10, 'Фрі'),
    ]

    search_index = build_search_index(data)

    query = 'ри'
    result = fuzzy_search(query=query, search_index=search_index)

    assert set(result[:2]) == {1, 2}
    assert 10 not in result
    assert 8 not in result
    assert 3 in result
    assert 4 in result
    assert 6 in result
    assert 7 in result


def test_index_search_04() -> None:
    data = [
        (1, 'Солод'),
        (2, 'Солодка'),
        (3, 'Яблуко Солодке'),
        (4, 'Яблуко напів-солодке'),
        (5, 'Яблуко Володимир'),
        (6, 'Огірок Солоний'),
        (7, 'Глід'),
        (8, 'Слива'),
        (9, 'Сіль'),
        (10, 'Олива'),
    ]
    search_index = build_search_index(data)

    query = 'солод'
    result = fuzzy_search(query=query, search_index=search_index)
    assert result[0] == 1
    assert 2 in result
    assert 3 in result
    assert 4 in result
    assert 7 not in result
    assert 8 not in result
    assert 9 not in result
    assert 10 not in result


def test_index_search_05() -> None:
    data = [
        (1, "Лимон"),
        (2, "Лимонад"),
        (3, "Лимонка"),
        (4, "Лимонний Фреш"),
        (5, "Лимонно-полуничний фреш"),
        (6, "Фреш лимонний"),
        (7, "Лиман"),
        (8, "Симон"),
        (9, "Лайм"),
        (10, "Паста"),
    ]
    search_index = build_search_index(data)

    query = 'лимон'
    result = fuzzy_search(query=query, search_index=search_index)

    assert result[0] == 1
    assert {1, 2, 3, 4, 5, 6}.issubset(set(result))
    assert 7 not in result
    assert 8 not in result
    assert 9 not in result
    assert 10 not in result

    query = 'лим'
    result = fuzzy_search(query=query, search_index=search_index)
    assert result[0] == 1
    assert {1, 2, 3, 4, 5, 6, 7}.issubset(set(result))
    assert 10 not in result


def test_index_search_06() -> None:
    data = [
        (1, "Цибуля"),
        (1, "Лук"),
        (2, "Тюльпан Цибулина"),
        (2, "Тюльпан Луковица"),
        (3, "Суп Цибулинний"),
        (3, "Суп Луковый"),
        (4, "Шовковиця"),
        (4, "Шелковица"),
        (5, "Лукум"),
        (5, "Лукум"),
        (6, "Картопля із Цибулею"),
        (6, "Картошка с Луком"),
    ]
    search_index = build_search_index(data)

    query = 'луковица'
    result = fuzzy_search(query=query, search_index=search_index)
    assert result[0] == 2

    query = 'лук'
    result = fuzzy_search(query=query, search_index=search_index)
    assert result[0] == 1
    assert 5 in result


def test_index_search_07() -> None:
    data = [
        (1, "Jerry Fox"),
        (2, "Kerry Fox"),
        (3, "Perri Fox"),
        (4, "Stieve Perry"),
        (5, "Stieve Perri"),
        (6, "Jerry Smith"),
        (7, "Larry Smith"),
    ]
    search_index = build_search_index(data)

    query = 'perry'
    result = fuzzy_search_internal(query=query, search_index=search_index, topn=12)
    assert result[0].value == 4

    query = 'perri'
    result = fuzzy_search_internal(query=query, search_index=search_index, topn=12)
    assert result[0].value == 3


def test_index_search_08() -> None:
    data = [
        (1, "Молоко 15%"),
        (1, "Молоко 20%"),
        (2, "Масло 15%"),
        (3, "Сир 20%"),
    ]
    search_index = build_search_index(data)

    query = '20%'
    result = fuzzy_search(query, search_index)
    assert set(result[:2]) == {1, 3}
