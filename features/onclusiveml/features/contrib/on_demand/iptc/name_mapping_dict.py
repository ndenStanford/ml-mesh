"""IPTC name mapping dictionary from legacy to current label."""

NAME_MAPPING_DICT_FIRST = {
    "arts, culture and entertainment": "arts, culture, entertainment and media",
    "conflicts, war and peace": "conflict, war and peace",
}

NAME_MAPPING_DICT_SECOND = {
    # Category: 'crime, law and justice'
    "justice and rights": "justice",  # Renamed
    "religious facilities": "religious facility",
}

NAME_MAPPING_DICT_THIRD = {
    # Category: 'act of terror'
    "terrorist bombings": "terrorist bombings",  # Renamed
    # Category: 'crime'
    "cyber crime": "cyber crime",  # Renamed
    "robbery and theft": "robbery and theft",  # Renamed
    # Category: 'accident and emergency incident'
    "transportation accident and incident": "transportation accident and incident",  # Renamed
    # Category: 'disaster'
    "natural disaster": "natural disaster",  # Renamed
    # Category: 'disease and condition'
    "mental health and disorder": "mental health and disorder",  # Renamed
    # Category: 'health treatment and procedure'
    "medical test": "medical test",  # Renamed
    # Category: 'leisure'
    "outdoor recreational activities": "outdoor recreational activities",  # Renamed
    "travel and tourism": "travel and tourism",  # Renamed
    # Category: 'wellness'
    "exercise and fitness": "exercise and fitness",  # Renamed
    "mental wellbeing": "mental wellbeing",  # Renamed
    # Category: 'fundamental rights'
    "civil rights": "civil rights",  # Renamed
    # Category: 'government'
    "government department": "government department",  # Renamed
    "heads of government": "heads of government",  # Renamed
    "minister and secretary (government)": "minister and secretary (government)",  # Renamed
    "national government": "national government",  # Renamed
    "regional government and authority": "regional government and authority",  # Renamed
    # Category: 'family'
    "Dating and Relationships": "Dating and Relationships",  # Renamed
    "parenting": "parenting",  # Renamed
    "pregnancy and childbirth": "pregnancy and childbirth",  # Renamed
    "bullfighting ": "bullfighting",
}
