from flexi_nlp_tools.lite_translit import en2uk_translit


def test_en2uk_translit_01() -> None:
    data = [
        ("iaka prikra situatsiia", "яка прікра сітуація"),
        ("ia duzje rozcharovanii", "я дуже розчарованій"),
        ("otse tak neshchastia", "оце так нещастя"),
        ("просто текст українською мовою", "просто текст українською мовою"),
        (
            'Transliteruvati text mozjna po riznomu, ale ie intuitivni pravila',
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
