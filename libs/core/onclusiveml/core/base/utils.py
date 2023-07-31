# Standard Library
from enum import Enum
from typing import List


class OnclusiveEnum(Enum):
    @classmethod
    def list(cls) -> List[str]:

        return [field.value for field in cls]
