"""Request model."""

from typing import Optional

from pydantic import BaseModel


class Request(BaseModel):
    """Keybert input request item."""

    content: Optional[str] = ""  # NOTE: an empty string is needed (at least).
    keyphrase_ngram_range: Optional[tuple] = (1, 3)
    use_maxsum: Optional[bool] = False
    use_mmr: Optional[bool] = True
    diversity: Optional[float] = 0.35
    nr_candidates: Optional[int] = 20
    top_n: Optional[int] = 20
