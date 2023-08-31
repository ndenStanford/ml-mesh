"""Entity fishing helpers."""


def _entity_text_match(lhs: str, rhs: str) -> bool:
    """Match entity in the tntities dictionary with one from the entity fishing backend,"""
    if (text_1 in text_2) or (text_2 in text_1):
        return True
    else:
        return False
