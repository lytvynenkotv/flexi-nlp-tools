from numeral_converter import numeral2int

import cProfile

import logging
logging.basicConfig(level=logging.ERROR)

numeral2int('сто', 'uk')
cProfile.run("numeral2int('сто', 'uk')")
