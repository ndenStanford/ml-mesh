"""IPTC label to topic dictionary."""
CLASS_DICT_FIRST = {
    "root": {
        0: "arts, culture, entertainment and media",
        1: "conflict, war and peace",
        2: "crime, law and justice",
        3: "disaster, accident and emergency incident",
        4: "economy, business and finance",
        5: "education",
        6: "environment",
        7: "health",
        8: "labour",
        9: "lifestyle and leisure",
        10: "politics",
        11: "religion",
        12: "science and technology",
        13: "society",
        14: "sport",
        15: "weather",
    }
}

CLASS_DICT_SECOND = {
    "arts, culture, entertainment and media": {
        0: "arts and entertainment",
        1: "culture",
        2: "mass media",
    },
    "conflict, war and peace": {
        0: "armed conflict",
        1: "civil unrest",
        2: "act of terror",
        3: "massacre",
        4: "peace process",
        5: "post-war reconstruction",
        6: "coup d'etat",
    },
    "crime, law and justice": {
        0: "judiciary",
        1: "law enforcement",
        2: "law",
        3: "crime",
        4: "justice and rights",
    },
    "disaster, accident and emergency incident": {
        0: "disaster",
        1: "accident and emergency incident",
        2: "emergency response",
    },
    "economy, business and finance": {
        0: "economy",
        1: "economic sector",
        2: "business information",
        3: "market and exchange",
    },
    "education": {0: "school", 1: "religious education", 2: "teaching and learning"},
    "environment": {
        0: "natural resources",
        1: "conservation",
        2: "environmental pollution",
        3: "climate change",
        4: "nature",
        5: "environmental politics",
    },
    "health": {
        0: "health treatment and procedure",
        1: "disease and condition",  # 'diseases and conditions',
        2: "government health care",  # now in politics
        3: "health insurance",
        4: "health facility",
        5: "medical profession",
        6: "non-human diseases",
    },
    "labour": {
        0: "employment",
        1: "retirement",
        2: "unemployment",
        3: "employment legislation",
        4: "labour relations",
        5: "unions",
    },
    "lifestyle and leisure": {0: "leisure", 1: "lifestyle"},
    "politics": {
        0: "government",
        1: "election",
        2: "international relations",
        3: "government policy",
        4: "fundamental rights",
        5: "political process",
    },
    "religion": {
        0: "belief systems",  # religious belief
        1: "religious text",
        2: "religious facilities",
        3: "religious festival or holiday",
    },  # religious event
    "science and technology": {
        0: "natural science",
        1: "technology and engineering",
        2: "biomedical science",
        3: "social sciences",
        4: "mathematics",
        5: "scientific research",  # 'research',
        6: "mechanical engineering",
    },
    "society": {
        0: "demographics",
        1: "family",
        2: "values",
        3: "social problem",
        4: "discrimination",
        5: "welfare",
        6: "social condition",
        7: "mankind",
        8: "communities",
    },
    "sport": {0: "competition discipline", 1: "drug use in sport"},
    "weather": {0: "weather forecast", 1: "weather warning"},
}

CLASS_DICT_THIRD = {
    # removed economy
    "economic sector": {
        0: "energy and resource",  # changed order
        1: "computing and information technology",
        2: "transport",
        3: "media",
        4: "consumer goods",
        5: "agriculture",
        6: "construction and property",
        7: "financial and business service",
        8: "chemicals",
        9: "tourism and leisure",
        10: "metal and mineral",
        11: "manufacturing and engineering",
        12: "process industry",
    },
    "business information": {
        0: "human resources",  # changed order
        1: "strategy and marketing",
        2: "business finance",
    },
    "market and exchange": {
        0: "securities",  # changed order
        1: "stocks",
        2: "commodity market",
        3: "foreign exchange market",
        4: "loan market",
    },
    "disaster": {0: "natural disasters", 1: "fire", 2: "famine"},  # manually added
    "accident and emergency incident": {
        0: "transport accident and incident",  # manually added
        1: "industrial accident and incident",
        2: "explosion accident and incident",
    },
    "natural science": {
        0: "meteorology",  # changed order
        1: "biology",
        2: "physics",
        3: "astronomy",
        4: "geology",
        5: "horticulture",
        6: "chemistry",
        7: "cosmology",
        8: "marine science",
    },
    "technology and engineering": {
        0: "aerospace engineering",  # changed order
        1: "electronic engineering",
        2: "micro science",
        3: "information technology and computer science",  # IT/computer sciences
        4: "civil engineering",
    },
    # removed biomedical science
    "social sciences": {
        0: "economics",  # changed order
        1: "philosophy",
        2: "psychology",
        3: "archaeology",
        4: "geography",
        5: "information science",
        6: "linguistics",
        7: "history",
        8: "political science",
        9: "sociology",
        10: "anthropology",
    },
    "scientific research": {
        0: "scientific exploration",  # changed order
        1: "medical research",
    },
    "judiciary": {0: "prosecution", 1: "court", 2: "out of court procedures"},
    "law enforcement": {
        0: "police",
        1: "punishment (criminal)",
        2: "arrest",
        3: "investigation (criminal)",
    },
    "law": {0: "civil law", 1: "criminal law", 2: "international law"},  # changed order
    "crime": {
        0: "drug related crimes",  # changed order
        1: "fraud",
        2: "terrorism",
        3: "homicide",
        4: "kidnapping",
        5: "corruption",
        6: "assault",
        7: "theft",
        8: "arson",
        9: "hijacking",
        10: "corporate crime",
        11: "computer crime",
        12: "organised crime",
        13: "war crime",
    },
    "health treatment and procedure": {
        0: "medicine",
        1: "medical procedure/test",
        2: "preventative medicine",
        3: "diet",
        4: "physical fitness",
        5: "therapy",
        6: "medical drugs",
    },  # manually added
    "disease and condition": {
        0: "illness",  # changed order
        1: "communicable disease",
        2: "injury",
        3: "heart disease",
        4: "cancer",
        5: "obesity",
        6: "mental and behavioural disorder",
    },
    # removed healthcare policy
    "non-human diseases": {0: "animal disease", 1: "plant disease"},  # manually added
    "leisure": {
        0: "game",  # changed order
        1: "travel",
        2: "holiday",
        3: "recreational activities",
        4: "club and association",
        5: "leisure venue",
        6: "gaming and lottery",
        7: "hobby",
    },
    "lifestyle": {0: "food and drink", 1: "trend", 2: "house and home", 3: "party"},
    "armed conflict": {0: "war", 1: "military occupation"},  # added armed conflict
    "civil unrest": {
        0: "riot",  # changed order
        1: "demonstration",
        2: "revolution",
        3: "rebellion",
    },
    "act of terror": {0: "bombings", 1: "act of bioterrorism"},
    "competition discipline": {
        0: "soccer",  # manually added
        1: "baseball",
        2: "motor car racing",
        3: "cycling",
        4: "motorcycling",
        5: "swimming",
        6: "golf",
        7: "sailing",
        8: "canoeing",
        9: "wrestling",
        10: "boxing",
        11: "tennis",
        12: "rugby union",
        13: "basketball",
        14: "volleyball",
        15: "athletics, track and field",
        16: "speed skating",
        17: "snooker",
        18: "polo",
        19: "triathlon",
        20: "American football",
        21: "gymnastics",
        22: "mountain climbing",
        23: "cricket",
        24: "martial arts",
        25: "ice hockey",
        26: "horse racing",
        27: "rodeo",
        28: "weightlifting",
        29: "bullfighting",
        30: "diving",
        31: "skiing",
        32: "equestrianism",
        33: "rowing",
        34: "luge",
        35: "fencing",
        36: "handball (team)",
        37: "marathon",
        38: "figure skating",
        39: "rugby league",
        40: "chess",
        41: "water polo",
        42: "roller sports",
        43: "squash",
        44: "parachuting",
        45: "badminton",
        46: "hurling",
        47: "surfing",
        48: "field hockey",
        49: "archery",
        50: "netball",
        51: "kabaddi",
        52: "softball",
        53: "shinty",
        54: "lacrosse",
        55: "bobsleigh",
        56: "bandy",
        57: "curling",
        58: "skeleton",
        59: "sport shooting",
        60: "table tennis",
        61: "modern pentathlon",
        62: "sumo wrestling",
        63: "darts",
        64: "pool",
        65: "orienteering",
        66: "billiards",
        67: "snowboarding",
        68: "biathlon",
        69: "kayaking",
        70: "Jai Alai (Pelota)",
        71: "dog racing",
        72: "Australian rules football",
        73: "inline skating",
        74: "floorball",
    },
    "arts and entertainment": {
        0: "music",  # changed order
        1: "fashion",
        2: "theatre",
        3: "literature",
        4: "opera",
        5: "cinema",
        6: "dance",
        7: "visual arts",
        8: "cartoon",
        9: "art exhibition",
        10: "animation",
    },
    "culture": {
        0: "language",  # changed order
        1: "library and museum",
        2: "monument and heritage site",
    },
    "mass media": {
        0: "television",  # changed order
        1: "newspaper",
        2: "radio",
        3: "news media",
        4: "periodical",
    },
    "natural resources": {
        0: "water",
        1: "land resources",
        2: "population growth",
        3: "renewable energy",
    },  # manually added
    "environmental pollution": {
        0: "water pollution",
        1: "air pollution",
    },  # manually added
    "nature": {
        0: "ecosystem",
        1: "endangered species",
        2: "invasive species",
    },  # manually added
    "belief systems": {
        0: "Islam",
        1: "Christianity",
        2: "Shintoism",
        3: "Scientology",
        4: "Buddhism",
        5: "Judaism",
        6: "Hinduism",
        7: "Sikhism",
        8: "Confucianism",
        9: "Taoism",
        10: "cult and sect",
        11: "Jainism",
    },  # manually added
    "religious text": {0: "Torah", 1: "Bible", 2: "Qur'an"},  # manually added
    "religious facility": {
        0: "church",
        1: "temple",
        2: "mosque",
        3: "synagogue",
    },  # manually added
    "government": {
        0: "legislative body",  # changed order
        1: "defence",
        2: "heads of state",
        3: "impeachment",
        4: "espionage and intelligence",
        5: "government budget",
        6: "constitution (law)",
        7: "ministers (government)",
        8: "executive (government)",
        9: "local government and authority",
        10: "civil and public service",
    },
    "election": {
        0: "electoral system",
        1: "voting",
        2: "local elections",
        3: "referenda",
        4: "political campaigns",
    },  # removed regional elections
    "international relations": {
        0: "diplomacy",
        1: "refugees and internally displaced people",
        2: "foreign aid",
    },
    "government policy": {
        0: "sports policies",  # changed order
        1: "nuclear policy",
        2: "regulation of industry",
        3: "safety of citizens",
        4: "taxation",
        5: "migration policy",  # migration of people
        6: "economic policy",
    },  # manually added
    "fundamental rights": {
        0: "human rights",
        1: "censorship and freedom of speech",  # censorship
        2: "freedom of the press",
    },
    "political process": {
        0: "political parties and movements",
        1: "political system",
        2: "lobbying",
    },
    "family": {
        0: "family planning",
        1: "divorce",
        2: "marriage",
        3: "parent and child",
        4: "adoption",
    },
    "values": {
        0: "ethics",
        1: "death and dying",
        2: "pornography",
        3: "corrupt practices",
    },  # manually added
    "social problem": {
        0: "addiction",
        1: "slavery",
        2: "prostitution",
        3: "juvenile delinquency",
    },  # manually added
    "discrimination": {0: "racism", 1: "sexism", 2: "ageism"},  # manually added
    "social condition": {0: "homelessness", 1: "poverty"},  # manually added
    "mankind": {
        0: "teenagers",
        1: "gender",
        2: "gays and lesbians",
        3: "senior citizens",
        4: "infants",
        5: "children",
    },  # manually added
}

CLASS_DICT = {**CLASS_DICT_FIRST, **CLASS_DICT_SECOND, **CLASS_DICT_THIRD}
