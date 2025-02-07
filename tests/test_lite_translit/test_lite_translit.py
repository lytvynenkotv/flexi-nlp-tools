from flexi_nlp_tools.lite_translit import en2uk_translit, en2ru_translit, uk2ru_translit


def test_sample():
    # Легковесная (rule-based) транслитерация с английского на русский/украинский с претензией на фонетическую
    # учитывает case
    # учитывает положение en символа в слове для корректной транлитерации ("с" транслитерируется в "c" в зависимости от положения в слове)

    en2uk_translit("coca-cola")
    # "кока-кола"

    en2uk_translit('science')
    # 'сайенс'

    en2uk_translit('conscience')
    # 'коншєнс'

    print(en2uk_translit("lucene"))
    # лусен

    print(en2uk_translit('Samsung'))
    # 'Самсунг'

    print(en2ru_translit("borjomi"))
    # "боржоми"

    print(uk2ru_translit("подвір’я"))
    # 'подвирья'


def test_en2uk_translit_01() -> None:
    data = [
        ("iaka prikra situatsiia", "яка прікра сітуація"),
        ("ia duzjeh rozcharovanii", "я дуже розчарованій"),
        ("otseh tak neshchastia", "оце так нещастя"),
        ("просто текст українською мовою", "просто текст українською мовою"),
        (
            'Transliteruvati text mozjna po riznomu, aleh ieh intuitivni pravila',
            'Транслітеруваті текст можна по різному, але є інтутівні правіла'

        )
    ]
    errors = 0
    for en, translit in data:
        result = en2uk_translit(en)
        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_en2uk_translit_02() -> None:
    data = [
        ("coca-cola", "кока-кола"),
        ('alpro', 'алпро'),
        ('columbiia', 'колумбія'),
        ('Samsung', 'Самсунг'),
        ('YARO Veggie cheese', 'ЯРО Веггє чіс'),
        ('Coca-Cola', 'Кока-Кола'),
        ('iPhone 14 Pro', 'іФоне 14 Про'),
        ('Samsung Galaxy S23+', 'Самсунг Галаксай С23+'),
        ('HOKKAIDO CLUB', 'ХОККАІДО КЛУБ'),
        ('sonatural', 'сонатурал')
    ]
    errors = 0
    for en, translit in data:
        result = en2uk_translit(en)
        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_en2uk_translit_03() -> None:
    data = [
        ("borjomi", "боржомі"),
        ('Lamborghini', 'Ламборжіні'),
        ('major', 'мажор'),
        ('journey', 'жоурнеі')
    ]
    errors = 0
    for en, translit in data:
        result = en2uk_translit(en)
        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_en2uk_translit_04() -> None:
    data = [
        ("look", "лук"),
        ('cock', 'кок'),
        ('cocktail', 'коктаіл'),
        ('sock', 'сок')
    ]
    errors = 0
    for en, translit in data:
        result = en2uk_translit(en)
        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_en2uk_translit_05() -> None:
    data = [
        ("witch", "вітч"),
        ('beach', 'біач'),
        ('bear', 'біар'),
        ('march', 'марч'),
        ('choose', 'чус')
    ]
    errors = 0
    for en, translit in data:
        result = en2uk_translit(en)
        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_en2uk_translit_06() -> None:
    data = [
        ('invitation', 'інвіташн'),
        ('collaborations', 'коллаборашнс'),
        ('vision', 'віжн'),
        ('musicians', 'мусішнс'),
        ('through', 'тру'),
        ('though', 'су'),
        ('thumb', 'сумб'),
        ('phone', 'фон'),
        ('whisper', 'віспер'),
        ('night', 'найт'),
        ('science', 'сайенс'),
        ('conscience', 'коншєнс'),
        ('conscious', 'консшс'),
        ('delicious', "делішс"),
        ('chat', 'чат'),
        ('chemistry', 'чемістрі'),
        ('machine', 'мачін'),
    ]
    errors = 0
    for en, translit in data:
        result = en2uk_translit(en)
        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_en2uk_translit_07() -> None:
    data = [
        ('the invitation and collaborations', 'сі інвіташн анд коллаборашнс'),
    ]
    errors = 0
    for en, translit in data:
        result = en2uk_translit(en)
        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_uk2ru_translit_01() -> None:
    data = [
        ('мрія', 'мрия'),
        ('подвір’я', 'подвирья'),
        ('пір’їнки', 'пирьйинкы'),
    ]
    errors = 0
    for uk, translit in data:
        result = uk2ru_translit(uk)
        if result != translit:
            print(f'"{uk}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_en2ru_translit_03() -> None:
    data = [
        ("borjomi", "боржоми"),
        ('Lamborghini', 'Ламборжини'),
        ('major', 'мажор'),
        ('journey', 'жоурнэи')
    ]
    errors = 0
    for en, translit in data:
        result = en2ru_translit(en)
        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors

