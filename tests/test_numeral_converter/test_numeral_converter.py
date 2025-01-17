import pytest

from src.numeral_converter.numeral_data_collector.numeral_data_loader.numeral_entry import NumClass, Gender, Number, Case
from src.numeral_converter import numeral2int, int2numeral, int2numerals, get_available_languages, convert_numerical_in_text

def test_():
    print(get_available_languages())
    print(numeral2int("two thousand and twenty-five", lang='en'))
    print(numeral2int("two thosnd and twnty-fiv", lang='en'))
    print(numeral2int("дві тисяіч двдціять пятий", lang="uk"))
    print(numeral2int("дві тисячі двадцять п'ятий", lang="uk"))
    print(int2numeral(
        2025,
        lang='uk',
        case="nominative",
        gender="neuter",
        num_class="ordinal"))

    print(convert_numerical_in_text("After twenty, numbers such as twenty-five, fifty, seventy-five, "
    "and one hundred follow. So long as one knows the core number, or the number "
    "situated in the tens or hundreds position that determines the general "
    "amount, understanding these more complicated numbers won't be difficult. "
    "For example thirty-three is simply \"thirty\" plus three; sixty-seven "
    "is \"sixty\" plus seven; and sixty-nine is simply \"sixty\" plus nine.",
    lang="en"))

# "After 20, numbers such as 25, 50, 75, and 100 follow. So long as 1 "
# # "knows the core number, or the number situated in the 10 or 100 "
# # "position that determines the general amount, understanding these more "
# # "complicated numbers won't be difficult. For example 33 is simply "
# # "\"30\" plus 3; 67 is \"60\" plus 7; and 69 is simply \"60\" plus 9."

def test_numeral2int_simple():
    assert numeral2int('one', 'en') == 1
    assert numeral2int('одного', 'ru') == 1
    assert numeral2int('twenti', 'en') == 20
    assert numeral2int('thousend', 'en') == 1000
    assert numeral2int('тисячний', 'uk') == 1000


def test_numeral2int():
    assert numeral2int("сто сорок дві тисячи тридцять один", lang="uk") == 142031
    assert numeral2int("сто сорок две тысячи тридцать один", lang="ru") == 142031
    assert numeral2int("one hundred forty-two thousand thirty-one", lang="en") == 142031
    assert (
        numeral2int("one hundred and forty-two thousand and thirty-one", lang="en")
        == 142031
    )
    assert (numeral2int("nine hundred and ninety-nine thousand", lang="en")) == 999000
    assert (numeral2int("two thousand and twenty-third", lang="en")) == 2023

    assert (numeral2int("thirty-three", lang="en")) == 33
    assert (numeral2int("thirty three", lang="en")) == 33


def test_numeral2int_unprocessed():
    assert (
        numeral2int("сто     сорок \t\tдві тисячи\tтридцять    один  ", lang="uk")
        == 142031
    )


def test_numeral2int_scale_of_scales():
    assert numeral2int("сто тисяч мільйонів", lang="uk") == 100000000000
    assert numeral2int("сто тисяч", lang="uk") == 100000


def test_numeral2int_scale_of_scales_en():
    assert numeral2int("one hundred thousand million", lang="en") == 100000000000
    assert numeral2int("one hundred thousand", lang="en") == 100000


def test_numeral2int_scale():
    assert numeral2int("три десятки", lang="uk") == 30
    assert numeral2int("три тисячі три сотні три десятки три", lang="uk") == 3333


def test_numeral2int_diff_morph_forms():
    assert numeral2int("сорок два", lang="uk") == 42
    assert numeral2int("сорока двох", lang="uk") == 42
    assert numeral2int("сорок другий", lang="uk") == 42
    assert numeral2int("сорок другій", lang="uk") == 42


def test_numeral2int_invalid_numeral():
    msg = (
        "position 1: order of 1000000000:9 "
        "is less/equal of summary order in next group: 9"
    )
    with pytest.raises(ValueError, match=msg):
        numeral2int("три мільярди тисяча пятдесят пять мільонів", lang="uk")


def test_numeral2int_spelling_invalid_numeral():
    msg = r'ordinal numeral word "[^"]+" inside numeral'
    with pytest.raises(ValueError, match=msg):
        numeral2int("три мільярди тисячний пятдесят пятий мільон", lang="uk")


def test_numeral2int_not_number():
    msg = 'can\'t convert "роки" to integer'
    with pytest.raises(ValueError, match=msg):
        numeral2int("дві тисячі двадцять три роки", lang="uk")


def test_numeral2int_spelly():
    assert numeral2int("дви тисичи двадцить тре", lang="ru") == 2023
    assert numeral2int("дви тисичи двадцить тре", lang="uk") == 2023
    assert numeral2int("two thousend twenti tree", lang="en") == 2023


def test_numeral2int_invalid_order():
    with pytest.raises(ValueError):
        numeral2int("двадцять дванадцять", lang="uk")
    with pytest.raises(ValueError):
        numeral2int("дванадцять два", lang="uk")
        

def test_int2numeral_01():
    R = int2numeral(2023, lang="uk")
    assert R == "дві тисячі двадцять три"


def test_int2numeral_02():
    R = int2numeral(2023, lang="uk", num_class=NumClass.ORDINAL, number=Number.SINGULAR)
    assert R == "дві тисячі двадцять третій"


def test_int2numeral_03():
    R = int2numeral(1000, lang="uk")
    assert R == "одна тисяча"


def test_int2numeral_04():
    R = int2numeral(2023, lang="ru")
    assert R == "две тысячи двадцать три"


def test_int2numeral_05():
    R = int2numeral(2023, lang="en")
    assert R == "two thousand twenty-three"


def test_int2numeral_06():
    R = int2numeral(2023, lang="en", num_class=NumClass.ORDINAL)
    assert R == "two thousand twenty-third"


def test_int2numeral_07():
    R = int2numeral(1000, lang="en")
    assert R == "one thousand"


def test_int2numeral_08():
    R = int2numeral(7325, lang="en")
    print(R)


def test_int2numeral_09():
    R = int2numeral(300, lang="ru")
    assert R == 'триста'


def test_int2numeral_10():
    R = int2numeral(300, lang="en")
    assert R == 'three hundred'


def test_int2numeral_11():
    R = int2numeral(100, lang="en")
    assert R == 'one hundred'


def test_int2numeral_empty_label_value():
    int2numeral(2023, lang="uk", case=None, num_class=None)
    assert True


def test_int2numeral_one_numeral_form_uk():
    R = int2numeral(2023, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
    assert R == "дві тисячі двадцять три"
    
    R = int2numerals(2023, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
    assert len(R) == 1
    assert R == [
        "дві тисячі двадцять три"
    ]

    R = int2numeral(5000, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
    assert R == "п’ять тисяч"
    
    R = int2numerals(5000, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
    assert len(R) == 1
    assert R == [
        "п’ять тисяч"
    ]


def test_int2numeral_one_numeral_form_ru():
    R = int2numeral(2023, lang="ru", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
    assert R == "две тысячи двадцать три"

    R = int2numerals(2023, lang="ru", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
    assert len(R) == 1
    assert R == [
         "две тысячи двадцать три"
    ]

    R = int2numeral(5000, lang="ru", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
    assert R == "пять тысяч"

    R = int2numerals(5000, lang="ru", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
    assert len(R) == 1
    assert R == [
        "пять тысяч"
    ]


def test_int2numeral_several_numeral_forms():
    R = int2numerals(
        2021, lang="uk", case=Case.NOMINATIVE, gender=Gender.NEUTER, num_class=NumClass.CARDINAL
    )
    assert len(R) == 2
    assert R == [
        "дві тисячі двадцять одне",
        "дві тисячі двадцять одно",
    ]

    R = int2numerals(89, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL)
    assert len(R) == 4
    assert R == [
        "вісімдесяти дев’яти",
        "вісімдесяти дев’ятьох",
        "вісімдесятьох дев’яти",
        "вісімдесятьох дев’ятьох",
    ]


def test_int2numeral_unknown_number():
    unknown_value = 10 ** (3 * 20)
    msg = f"no data for number {unknown_value}"
    with pytest.raises(ValueError, match=msg):
        int2numeral(unknown_value, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)


def test_int2numeral_numbers_morph_forms():
    # Auto collected from https://www.kyivdictionary.com/uk/words/number-spelling
    assert (
        int2numeral(666777888999, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL)
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ять"
    )

    assert (
        int2numeral(666777888999, lang="uk", case=Case.GENETIVE, num_class=NumClass.CARDINAL)
        == "шестисот шістдесяти (шістдесятьох) шести (шістьох) мільярдів семисот "
        "сімдесяти (сімдесятьох) семи (сімох) мільйонів восьмисот вісімдесяти "
        "(вісімдесятьох) восьми (вісьмох) тисяч дев’ятисот дев’яноста дев’яти "
        "(дев’ятьох)"
    )

    assert (
        int2numeral(666777888999, lang="uk", case=Case.DATIVE, num_class=NumClass.CARDINAL) ==
        "шестистам шістдесяти (шістдесятьом) шести (шістьом) мільярдам семистам "
        "сімдесяти (сімдесятьом) семи (сімом) мільйонам восьмистам вісімдесяти "
        "(вісімдесятьом) восьми (вісьмом) тисячам дев’ятистам дев’яноста "
        "дев’яти (дев’ятьом)"
    )

    assert (
        int2numeral(666777888999, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL) ==
        "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ять (дев’ятьох)"
    )

    assert (
        int2numeral(666777888999, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL) ==
        "шістьмастами (шістьомастами) шістдесятьма (шістдесятьома) шістьма "
        "(шістьома) мільярдами сьомастами (сімомастами) сімдесятьма (сімдесятьома) "
        "сімома (сьома) мільйонами вісьмастами (вісьмомастами) вісімдесятьма "
        "(вісімдесятьома) вісьма (вісьмома) тисячами дев’ятьмастами "
        "(дев’ятьомастами) дев’яноста дев’ятьма (дев’ятьома)"
    )

    assert (
        int2numeral(
            666777888999, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL
        )
        == "шестистах шістдесяти (шістдесятьох) шести (шістьох) мільярдах семистах "
        "сімдесяти (сімдесятьох) семи (сімох) мільйонах восьмистах вісімдесяти "
        "(вісімдесятьох) восьми (вісьмох) тисячах дев’ятистах дев’яноста дев’яти "
        "(дев’ятьох)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятий"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ята"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яте"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яті"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятого"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятої"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятого"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятих"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятому"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятій"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятому"
    )

    assert (
        int2numeral(
            666777888999, lang="uk", case=Case.DATIVE, num_class=NumClass.ORDINAL, number=Number.PLURAL
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятим"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятий (дев’ятого)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яту"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яте"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яті (дев’ятих)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятим"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятою"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятим"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятими"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятому (дев’ятім)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятій"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятому (дев’ятім)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятих"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста тридцять "
        "три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ять"
    )

    assert (
        int2numeral(221222333444555, lang="uk", case=Case.GENETIVE, num_class=NumClass.CARDINAL) ==
        "двохсот двадцяти (двадцятьох) одного трильйона двохсот двадцяти "
        "(двадцятьох) двох мільярдів трьохсот тридцяти (тридцятьох) трьох мільйонів "
        "чотирьохсот сорока чотирьох тисяч п’ятисот п’ятдесяти (п’ятдесятьох) "
        "п’яти (п’ятьох)"
    )

    assert (
        int2numeral(221222333444555, lang="uk", case=Case.DATIVE, num_class=NumClass.CARDINAL) ==
        "двомстам двадцяти (двадцятьом) одному трильйону (трильйонові) двомстам "
        "двадцяти (двадцятьом) двом мільярдам трьомстам тридцяти (тридцятьом) "
        "трьом мільйонам чотирьомстам сорока чотирьом тисячам п’ятистам п’ятдесяти "
        "(п’ятдесятьом) п’яти (п’ятьом)"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста тридцять "
        "три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "(п’ятдесятьох) п’ять (п’ятьох)"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL
        )
        == "двомастами двадцятьма (двадцятьома) одним трильйоном двомастами "
        "двадцятьма (двадцятьома) двома мільярдами трьомастами тридцятьма "
        "(тридцятьома) трьома мільйонами чотирмастами сорока чотирма тисячами "
        "п’ятьмастами (п’ятьомастами) п’ятдесятьма (п’ятдесятьома) п’ятьма (п’ятьома)"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL
        )
        == "двохстах двадцяти (двадцятьох) одному (однім) трильйоні двохстах двадцяти "
        "(двадцятьох) двох мільярдах трьохстах тридцяти (тридцятьох) трьох "
        "мільйонах чотирьохстах сорока чотирьох тисячах п’ятистах п’ятдесяти "
        "(п’ятдесятьох) п’яти (п’ятьох)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятий"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ята"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’яте"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’яті"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятого"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятої"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятого"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятих"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятому"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятій"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятому"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятим"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "п’ятий (п’ятого)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’яту"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’яте"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "п’яті (п’ятих)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятим"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятою"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятим"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятими"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "п’ятому (п’ятім)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятій"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "п’ятому (п’ятім)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятих"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцять"
    )

    assert (
        int2numeral(111212313415515, lang="uk", case=Case.GENETIVE, num_class=NumClass.CARDINAL) ==
        "ста одинадцяти (одинадцятьох) трильйонів двохсот дванадцяти (дванадцятьох) "
        "мільярдів трьохсот тринадцяти (тринадцятьох) мільйонів чотирьохсот "
        "п’ятнадцяти (п’ятнадцятьох) тисяч п’ятисот п’ятнадцяти (п’ятнадцятьох)"
    )

    assert (
        int2numeral(111212313415515, lang="uk", case=Case.DATIVE, num_class=NumClass.CARDINAL) ==
        "ста одинадцяти (одинадцятьом) трильйонам двомстам дванадцяти "
        "(дванадцятьом) мільярдам трьомстам тринадцяти (тринадцятьом) мільйонам "
        "чотирьомстам п’ятнадцяти (п’ятнадцятьом) тисячам п’ятистам "
        "п’ятнадцяти (п’ятнадцятьом)"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцять (п’ятнадцятьох)"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL
        )
        == "ста одинадцятьма (одинадцятьома) трильйонами двомастами дванадцятьма "
        "(дванадцятьома) мільярдами трьомастами тринадцятьма (тринадцятьома) "
        "мільйонами чотирмастами п’ятнадцятьма (п’ятнадцятьома) тисячами "
        "п’ятьмастами (п’ятьомастами) п’ятнадцятьма (п’ятнадцятьома)"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL
        )
        == "ста одинадцяти (одинадцятьох) трильйонах двохстах дванадцяти "
        "(дванадцятьох) мільярдах трьохстах тринадцяти (тринадцятьох) мільйонах "
        "чотирьохстах п’ятнадцяти (п’ятнадцятьох) тисячах п’ятистах п’ятнадцяти "
        "(п’ятнадцятьох)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятий"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцята"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяте"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяті"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятого"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятої"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятого"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятих"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятому"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятій"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятому"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятим"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятий (п’ятнадцятого)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяту"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяте"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяті (п’ятнадцятих)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятим"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятою"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятим"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятими"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятому (п’ятнадцятім)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятій"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятому (п’ятнадцятім)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятих"
    )

    assert (
        int2numeral(616717818919, lang="uk", case=Case.NOMINATIVE, num_class=NumClass.CARDINAL) ==
        "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцять"
    )

    assert (
        int2numeral(616717818919, lang="uk", case=Case.GENETIVE, num_class=NumClass.CARDINAL) ==
        "шестисот шістнадцяти (шістнадцятьох) мільярдів семисот сімнадцяти "
        "(сімнадцятьох) мільйонів восьмисот вісімнадцяти (вісімнадцятьох) "
        "тисяч дев’ятисот дев’ятнадцяти (дев’ятнадцятьох)"
    )

    assert (
        int2numeral(616717818919, lang="uk", case=Case.DATIVE, num_class=NumClass.CARDINAL) ==
        "шестистам шістнадцяти (шістнадцятьом) мільярдам семистам сімнадцяти "
        "(сімнадцятьом) мільйонам восьмистам вісімнадцятьом (вісімнадцяти) тисячам "
        "дев’ятистам дев’ятнадцяти (дев’ятнадцятьом)"
    )

    assert (
        int2numeral(616717818919, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL) ==
        "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцять (дев’ятнадцятьох)"
    )

    assert (
        int2numeral(616717818919, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL) ==
        "шістьмастами (шістьомастами) шістнадцятьма (шістнадцятьома) мільярдами "
        "сьомастами (сімомастами) сімнадцятьма (сімнадцятьома) мільйонами "
        "вісьмастами (вісьмомастами) вісімнадцятьма (вісімнадцятьома) тисячами "
        "дев’ятьмастами (дев’ятьомастами) дев’ятнадцятьма (дев’ятнадцятьома)"
    )

    assert (
        int2numeral(
            616717818919, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL
        )
        == "шестистах шістнадцяти (шістнадцятьох) мільярдах семистах сімнадцяти "
        "(сімнадцятьох) мільйонах восьмистах вісімнадцяти (вісімнадцятьох) "
        "тисячах дев’ятистах дев’ятнадцяти (дев’ятнадцятьох)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятий"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцята"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяте"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяті"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятого"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятої"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятого"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.GENETIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятих"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятому"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятій"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.DATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятому"
    )

    assert (
        int2numeral(
            616717818919, lang="uk", case=Case.DATIVE, num_class=NumClass.ORDINAL, number=Number.PLURAL
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятим"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятий (дев’ятнадцятого)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяту"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяте"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяті (дев’ятнадцятих)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятим"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятою"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятим"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятими"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятому (дев’ятнадцятім)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятій"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятому (дев’ятнадцятім)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            number=Number.PLURAL,
        )
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятих"
    )

    assert (
        int2numeral(
            1,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "одне (одно)"
    )

    assert (
        int2numeral(
            1,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "однією (одною)"
    )

    assert (
        int2numeral(
            3,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "третій"
    )

    assert (
        int2numeral(
            4,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "четверте"
    )

    assert (
        int2numeral(7, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "сімома (сьома)"
    )

    assert (
        int2numeral(9, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL)
        == "дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            13, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.ORDINAL, number=Number.PLURAL
        )
        == "тринадцяті (тринадцятих)"
    )

    assert (
        int2numeral(
            21,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "двадцять одне (одно)"
    )

    assert (
        int2numeral(
            21,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "двадцятьма (двадцятьома) однією (одною)"
    )

    assert (
        int2numeral(
            23,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "двадцять третій"
    )

    assert (
        int2numeral(
            24,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "двадцять четверте"
    )

    assert (
        int2numeral(27, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "двадцятьма (двадцятьома) сімома (сьома)"
    )

    assert (
        int2numeral(29, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL) ==
        "двадцяти (двадцятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(30, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох)"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "тридцять одне (одно)"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "тридцять (тридцятьох) один (одного)"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "тридцять (тридцятьох) одну"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "тридцять (тридцятьох) одне"
    )

    assert (
        int2numeral(
            31, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL, number=Number.PLURAL
        )
        == "тридцять (тридцятьох) одні (одних)"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "тридцятьма (тридцятьома) однією (одною)"
    )

    assert (
        int2numeral(32, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох) два (двох)"
    )

    assert (
        int2numeral(
            32,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
        )
        == "тридцять (тридцятьох) дві (двох)"
    )

    assert (
        int2numeral(33, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох) три (трьох)"
    )

    assert (
        int2numeral(
            33,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "тридцять третій"
    )

    assert (
        int2numeral(34, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох) чотири (чотирьох)"
    )

    assert (
        int2numeral(
            34,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "тридцять четверте"
    )

    assert (
        int2numeral(35, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох) п’ять (п’ятьох)"
    )

    assert (
        int2numeral(36, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох) шість (шістьох)"
    )

    assert (
        int2numeral(37, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох) сім (сімох)"
    )

    assert (
        int2numeral(37, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "тридцятьма (тридцятьома) сімома (сьома)"
    )

    assert (
        int2numeral(38, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох) вісім (вісьмох)"
    )

    assert (
        int2numeral(39, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "тридцять (тридцятьох) дев’ять (дев’ятьох)"
    )

    assert (
        int2numeral(39, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL) ==
        "тридцяти (тридцятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(40, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сорок одне (одно)"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.MASCULINE,
            number=Number.SINGULAR,
        )
        == "сорок один (одного)"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сорок одну"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сорок одне"
    )

    assert (
        int2numeral(
            41, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL, number=Number.PLURAL
        )
        == "сорок одні (одних)"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сорока однією (одною)"
    )

    assert (
        int2numeral(42, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок два (двох)"
    )

    assert (
        int2numeral(
            42,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
        )
        == "сорок дві (двох)"
    )

    assert (
        int2numeral(43, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок три (трьох)"
    )

    assert (
        int2numeral(
            43,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сорок третій"
    )

    assert (
        int2numeral(44, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок чотири (чотирьох)"
    )

    assert (
        int2numeral(
            44,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сорок четверте"
    )

    assert (
        int2numeral(45, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок п’ять (п’ятьох)"
    )

    assert (
        int2numeral(46, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок шість (шістьох)"
    )

    assert (
        int2numeral(47, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок сім (сімох)"
    )

    assert (
        int2numeral(47, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "сорока сімома (сьома)"
    )

    assert (
        int2numeral(48, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок вісім (вісьмох)"
    )

    assert (
        int2numeral(49, lang="uk", case=Case.ACCUSATIVE, num_class=NumClass.CARDINAL)
        == "сорок дев’ять (дев’ятьох)"
    )

    assert (
        int2numeral(49, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL) ==
        "сорока дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            50, lang="uk", case=Case.GENETIVE, num_class=NumClass.ORDINAL, number=Number.PLURAL
        )
        == "п’ятдесятих"
    )

    assert (
        int2numeral(
            51,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "п’ятдесят одне (одно)"
    )

    assert (
        int2numeral(
            51,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "п’ятдесятьма (п’ятдесятьома) однією (одною)"
    )

    assert (
        int2numeral(
            53,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "п’ятдесят третій"
    )

    assert (
        int2numeral(
            54,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "п’ятдесят четверте"
    )

    assert (
        int2numeral(57, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "п’ятдесятьма (п’ятдесятьома) сімома (сьома)"
    )

    assert (
        int2numeral(59, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL) ==
        "п’ятдесяти (п’ятдесятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            61,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістдесят одне (одно)"
    )

    assert (
        int2numeral(
            61,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістдесятьма (шістдесятьома) однією (одною)"
    )

    assert (
        int2numeral(
            63,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "шістдесят третій"
    )

    assert (
        int2numeral(
            64,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "шістдесят четверте"
    )

    assert (
        int2numeral(67, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "шістдесятьма (шістдесятьома) сімома (сьома)"
    )

    assert (
        int2numeral(69, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL) ==
        "шістдесяти (шістдесятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            71,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сімдесят одне (одно)"
    )

    assert (
        int2numeral(
            71,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сімдесятьма (сімдесятьома) однією (одною)"
    )

    assert (
        int2numeral(
            73,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "сімдесят третій"
    )

    assert (
        int2numeral(
            74,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "сімдесят четверте"
    )

    assert (
        int2numeral(77, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "сімдесятьма (сімдесятьома) сімома (сьома)"
    )

    assert (
        int2numeral(79, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL) ==
        "сімдесяти (сімдесятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            81,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "вісімдесят одне (одно)"
    )

    assert (
        int2numeral(
            81,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "вісімдесятьма (вісімдесятьома) однією (одною)"
    )

    assert (
        int2numeral(
            83,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "вісімдесят третій"
    )

    assert (
        int2numeral(
            84,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "вісімдесят четверте"
    )

    assert (
        int2numeral(87, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "вісімдесятьма (вісімдесятьома) сімома (сьома)"
    )

    assert (
        int2numeral(89, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL) ==
        "вісімдесяти (вісімдесятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            91,
            lang="uk",
            case=Case.NOMINATIVE,
            num_class=NumClass.CARDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "дев’яносто одне (одно)"
    )

    assert (
        int2numeral(
            91,
            lang="uk",
            case=Case.INSTRUMENTAL,
            num_class=NumClass.CARDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "дев’яноста однією (одною)"
    )

    assert (
        int2numeral(
            93,
            lang="uk",
            case=Case.PREPOSITIONAL,
            num_class=NumClass.ORDINAL,
            gender=Gender.FEMININE,
            number=Number.SINGULAR,
        )
        == "дев’яносто третій"
    )

    assert (
        int2numeral(
            94,
            lang="uk",
            case=Case.ACCUSATIVE,
            num_class=NumClass.ORDINAL,
            gender=Gender.NEUTER,
            number=Number.SINGULAR,
        )
        == "дев’яносто четверте"
    )

    assert (
        int2numeral(97, lang="uk", case=Case.INSTRUMENTAL, num_class=NumClass.CARDINAL)
        == "дев’яноста сімома (сьома)"
    )

    assert (
        int2numeral(99, lang="uk", case=Case.PREPOSITIONAL, num_class=NumClass.CARDINAL) ==
        "дев’яноста дев’яти (дев’ятьох)"
    )


def test_zeros():
    assert int2numeral(0, lang="uk") == "нуль"
    assert int2numeral(0, lang="uk", case=Case.DATIVE) == "нулю (нулеві)"
    assert (
        int2numeral(0, lang="uk", num_class=NumClass.ORDINAL, gender=Gender.FEMININE)
        == "нульова"
    )

    assert int2numeral(0, lang="ru") == "ноль"
    assert int2numeral(0, lang="en") == "zero (nought)"


def test_scales():
    assert int2numeral(10000, lang="ru") == "десять тысяч"
    assert int2numeral(100000, lang="ru") == "сто тысяч"
    assert int2numeral(1000000, lang="ru") == "один миллион"
    assert int2numeral(10000000, lang="ru") == "десять миллионов"
    assert int2numeral(100000000, lang="ru") == "сто миллионов"
    assert int2numeral(1000000000, lang="ru") == "один миллиард"
    assert int2numeral(1000000000000, lang="ru") == "один триллион"
    assert (
        int2numeral(100000000000000000000000000, lang="ru")
        == "сто септиллионов"
    )

    assert int2numeral(10000, lang="uk") == "десять тисяч"
    assert int2numeral(100000, lang="uk") == "сто тисяч"
    assert int2numeral(1000000, lang="uk") == "один мільйон"
    assert int2numeral(10000000, lang="uk") == "десять мільйонів"
    assert int2numeral(100000000, lang="uk") == "сто мільйонів"
    assert int2numeral(1000000000, lang="uk") == "один мільярд"
    assert int2numeral(1000000000000, lang="uk") == "один трильйон"
    assert (
        int2numeral(100000000000000000000000000, lang="uk")
        == "сто септильйонів"
    )

    assert int2numeral(10000, lang="en") == "ten thousand"
    assert int2numeral(100000, lang="en") == "one hundred thousand"
    assert int2numeral(1000000, lang="en") == "one million"
    assert int2numeral(10000000, lang="en") == "ten million"
    assert int2numeral(100000000, lang="en") == "one hundred million"
    assert int2numeral(1000000000, lang="en") == "one billion"
    assert int2numeral(1000000000000, lang="en") == "one trillion"
    assert (
        int2numeral(100000000000000000000000000, lang="en")
        == "one hundred septilion"
    )


def test_int2numeral_13():
    assert int2numeral(111000001, 'uk') == 'сто одинадцять мільйонів один'


def test_int2numeral_14():
    assert int2numeral(111000000, 'uk') == 'сто одинадцять мільйонів'
