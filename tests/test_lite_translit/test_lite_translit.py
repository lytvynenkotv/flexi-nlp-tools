from flexi_nlp_tools.lite_translit import en2uk_translit, en2ru_translit, uk2ru_translit

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
        ('YARO Veggie cheese', 'ЯРО Веггі чіс'),
        ('Coca-Cola', 'Кока-Кола'),
        ('iPhone 14 Pro', 'іФон 14 Про'),
        ('Samsung Galaxy S23+', 'Самсунг Галаксі С23+'),
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

