"""Entity fishing helpers."""


def entity_text_match(lhs: str, rhs: str) -> bool:
    """Match entity in the tntities dictionary with one from the entity fishing backend."""
    if (lhs in rhs) or (rhs in lhs):
        return True
    else:
        return False
