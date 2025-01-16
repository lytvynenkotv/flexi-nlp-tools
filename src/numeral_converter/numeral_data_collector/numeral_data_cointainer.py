from typing import Dict, Set
from dataclasses import dataclass

from flexi_dict import FlexiDict

from .numeral_data_loader.numeral_data import NumeralData


@dataclass
class NumeralDataContainer:
    numeral_data: NumeralData
    flexi_index: FlexiDict
    value_index: Dict[int, Set[int]]
