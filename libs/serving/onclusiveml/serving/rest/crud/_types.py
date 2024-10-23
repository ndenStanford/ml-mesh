"""Types."""

# Standard Library
from typing import Optional, Sequence

# 3rd party libraries
from fastapi.params import Depends


depends = Optional[Sequence[Depends]]
