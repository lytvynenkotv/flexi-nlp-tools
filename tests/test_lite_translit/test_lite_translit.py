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


def test_en2uk_translit_08() -> None:
    data = [
        ('Neh vseh teh zoloto, shcho blishchit`!', 'Не все те золото, що бліщіть!'),
        ('Memento mori — remember, you will die!', 'Мементо морі — ремембер, йоу вілл дай!'),
        ('Tempus fugit... carpe diem!', 'Темпус фугіт... карп дєм!'),
        ('Veni, vidi, vici!', 'Вені, віді, вічі!'),
        ('Carpe diem — quam minimum credula postero!', "Карп дєм — кьюуам мінімум кредула постеро!"),
        ('Cogito, ergo sum!', 'Когіто, ерго сум!'),
        ("His conscience was clear, even as he tried to maintain the consistency of his work "
         "on the Lucene project for Samsung, while sipping a cold cola.",
         "Хіс коншєнс вас кліар, евен ас хі трєд то маінтаін сі консістенкі оф хіс ворк "
         "он сі Лусен прожечт фор Самсунг, віл сіппінг а колд кола."),
    ]
    errors = 0
    for en, translit in data:

        result = en2uk_translit(en)

        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
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


def test_en2ru_translit_04() -> None:
    data = [
        ('Neh vseh to zoloto, chto blistit!', 'Не все то золото, что блистит!'),
        ('Memento mori — remember, you will die!', 'Мементо мори — ремембер, йоу вилл дай!'),
        ('Tempus fugit... carpe diem!', 'Темпус фугит... карп дем!'),
        ('Veni, vidi, vici!', 'Вени, види, вичи!'),
        ('Carpe diem — quam minimum credula postero!', "Карп дем — кьюуам минимум кредула постеро!"),
        ('Cogito, ergo sum!', 'Когито, ерго сум!'),
        ("His conscience was clear, even as he tried to maintain the consistency of his work "
         "on the Lucene project for Samsung, while sipping a cold cola.",
         "Хис коншенс вас клиар, евен ас хи тред то маинтаин си консистенки оф хис ворк "
         "он си Лусен прожечт фор Самсунг, вил сиппинг а колд кола."),
        ("After a long day, he enjoyed a refreshing Borjomi and Coca-Cola, feeling victorious like Vici in battle, "
         "while watching the lively citrus circus under the bright lights.",
         "Афтер а лонг дай, хи енжоед а рефрешинг Боржоми анд Кока-Кола, филинг вичторйоус лик Вичи ин баттл, "
         "вил ватчинг си ливели китрус киркус андер си брижт лайтс.")
    ]
    errors = 0
    for en, translit in data:

        result = en2ru_translit(en)

        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1
    assert not errors


def test_uk2ru_translit_01() -> None:
    data = [
        (
            "У мрії вона вирушила на подвір’я, де вітер розносив пір’їнки, і все навколо стало казкою.",
            "У мрийи вона вырушыла на подвирья, де витер розносыв пирьйинкы, и все навколо стало казкою.")
    ]
    errors = 0
    for en, translit in data:

        result = uk2ru_translit(en)

        if result != translit:
            print(f'"{en}": expect "{translit}", got "{result}"')
            errors += 1

    assert not errors
