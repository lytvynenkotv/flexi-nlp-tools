# nlp-flexi-tools

[![Python Versions](https://img.shields.io/badge/Python%20Versions-%3E%3D3.9-informational)](https://pypi.org/project/nlp-flexi-tools/)
[![Version](https://img.shields.io/badge/Version-0.1.0-informational)](https://pypi.org/project/nlp-flexi-tools/)

A natural language processing toolkit based on the flexi-dict data structure, designed for efficient fuzzy search, with a focus on simplicity, performance, and flexibility.

## Table of Contents

1. [Numeral Converter](#numeral-converter)
4. [Installation](#installation)
6. [License](#license)

---

## Numeral Converter

The Numeral Converter allows you to:

- Convert written numbers (e.g., "forty-two") into integers (42).
- Convert integers back into their textual numeral form, considering morphological parameters.
- Find and replace numerals in a text with their numeric equivalents.

### Available Languages
- Russian (`ru`)
- English (`en`)
- Ukrainian (`uk`)

### Functions

#### `numeral2int(text: str, lang: str) -> int`
Converts a numeral text into its integer representation.

```python
from numeral_converter import numeral2int

numeral2int("two thousand and twenty-five", lang='en')
# Output: 2025
```

#### `int2numeral(number: int, lang: str, case: str, gender: str, num_class: str) -> str`
Converts an integer into a textual numeral based on the specified parameters.

```python
from numeral_converter import int2numeral

int2numeral(
    2025,
    lang='uk',
    case="nominative",
    gender="neuter",
    num_class="ordinal"
)
# Output: дві тисячі двадцять п’яті
```

#### `convert_numerical_in_text(text: str, lang: str) -> str`
Finds and converts numerical words in a given text to their numeric representations.

```python
from numeral_converter import convert_numerical_in_text

convert_numerical_in_text(
    "After twenty, numbers such as twenty-five, fifty, seventy-five, and one hundred follow.",
    lang="en"
)
# Output: After 20, numbers such as 25, 50, 75, and 100 follow.
```

#### `get_available_languages() -> List[str]`
Returns the list of supported languages for numeral conversion.

```python
from numeral_converter import get_available_languages
get_available_languages()
# Output: ['uk', 'en', 'ru']
```

---


## Installation

You can easily install `nlp-flexi-tools` from PyPI using `pip`:

```bash
pip install nlp-flexi-tools
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
