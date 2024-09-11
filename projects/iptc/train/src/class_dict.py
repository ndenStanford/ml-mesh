# flake8: noqa
"""IPTC label to topic dictionary."""
CLASS_DICT_FIRST = {
    "root": {
        0: "arts, culture, entertainment and media",
        1: "conflict, war and peace",  # name update #2 changes #to retrain
        2: "crime, law and justice",  # 1 changes #to retrain
        3: "disaster, accident and emergency incident",  # 2 changes #to retrain
        4: "economy, business and finance",  # 2 changes #to retrain
        5: "education",  # 10 changes #to retrain
        6: "environment",  # 1 changes #to retrain
        7: "health",  # 3 changes #to retrain
        8: "labour",  # 3 changes #to retrain
        9: "lifestyle and leisure",  # 1 changes #to retrain
        10: "politics",  # 3 changes #to retrain
        11: "religion",  # 7 changes #to retrain
        12: "science and technology",  # 3 changes #to retrain
        13: "society",  # 2 changes #to retrain
        14: "sport",  # 10 changes #to retrain
        15: "weather",  # 2 changes #to retrain
    }
}

CLASS_DICT_SECOND = {
    "arts, culture, entertainment and media": {
        0: "arts and entertainment",  # 2 changes #to retrain
        1: "culture",  # 3 changes #to retrain
        2: "mass media",  # 3 changes #to retrain
    },
    "conflict, war and peace": {
        0: "act of terror",  # 1 change #to retrain
        1: "armed conflict",  # 2 changes #to retrain
        2: "civil unrest",
        3: "coup d'etat",
        4: "cyber warfare",  # new Field #to train
        5: "massacre",
        6: "peace process",  # 5 changes #to retrain
        7: "post-war reconstruction",  # 1 change #to retrain
        8: "war victims",  # new Field #to train
    },
    "crime, law and justice": {
        0: "crime",  # 10 changes #to retrain
        1: "judiciary",  # 1 change #to retrain
        2: "justice",  # name update
        3: "law",  # 1 change #to retrain
        4: "law enforcement",  # 1 change #to retrain
    },
    "disaster, accident and emergency incident": {
        0: "accident and emergency incident",  # 3 changes #to retrain
        1: "disaster",  # 1 change #to retrain
        2: "emergency incident",  # name update #3 changes #to retrain
        3: "emergency planning",  # new Field #to train
        4: "emergency response",
    },
    "economy, business and finance": {
        0: "business enterprise",  # name update #3 changes #to retrain
        1: "business information",  # 4 changes #to retrain
        2: "economy",  # 9 changes #to retrain
        3: "market and exchange",  # 2 changes #to retrain
        4: "products and services",  # new Field #to train
    },
    "education": {
        0: "curriculum",  # new Field #to train
        1: "educational grading",  # new Field #to train
        2: "educational testing and examinations",  # new Field #to train
        3: "entrance examination",  # new Field #to train
        4: "online and remote learning",  # new Field #to train
        5: "parents group",  # new Field #to train
        6: "religious education",  # new Field #to train
        7: "school",  # 11 changes #to retrain
        8: "social learning",  # new Field #to train
        9: "students",  # new Field #to train
        10: "teachers",  # new Field #to train
        11: "teaching and learning",
        12: "vocational education",  # new Field #to train
    },
    "environment": {
        0: "climate change",  # 1 change #to retrain
        1: "conservation",  # 2 changes #to retrain
        2: "environmental pollution",  # 3 changes #to retrain
        3: "natural resources",  # 1 change #to retrain
        4: "nature",  # 2 changes #to retrain
        5: "sustainability",  # new Field #to train
    },
    "health": {
        0: "disease and condition",  # 4 changes #to retrain
        1: "government health care",  # 2 changes #to retrain
        2: "health facility",  # 2 changes #to retrain
        3: "health insurance",
        4: "health organisation",  # new Field #to train
        5: "health treatment and procedure",  # 8 changes #to retrain
        6: "medical profession",  # 3 changes #to retrain
        7: "non-human diseases",
        8: "private health care",  # new Field #to train
        9: "public health",  # new Field #to train
    },
    "labour": {
        0: "employment",  # 11 changes #to retrain
        1: "employment legislation",  # new Field #to train
        2: "labour market",  # new Field #to train
        3: "labour relations",  # 2 changes #to retrain
        4: "retirement",  # 1 changes #to retrain
        5: "unemployment",  # 2 changes #to retrain
        6: "unions",  # new Field #to train
    },
    "lifestyle and leisure": {
        0: "leisure",  # 2 changes #to retrain
        1: "lifestyle",  # 1 change #to retrain
        2: "wellness",  # new Field #to train
    },
    "politics": {
        0: "election",  # 8 changes #to retrain
        1: "fundamental rights",  # 4 changes #to retrain
        2: "government",  # 9 changes #to retrain
        3: "government policy",  # 6 changes #to retrain
        4: "international relations",  # 3 changes #to retrain
        5: "non-governmental organisation",  # new Field #to train
        6: "political crisis",  # new Field #to train
        7: "political dissent",  # new Field #to train
        8: "political process",  # 1 change #to retrain
    },
    "religion": {
        0: "belief systems",  # 6 changes #to retrain
        1: "interreligious dialogue",  # new Field #to train
        2: "relations between religion and government",  # new Field #to train
        3: "religious conflict",  # new Field #to train
        4: "religious event",  # new Field #to train
        5: "religious facility",
        6: "religious festival and holiday",  # name update
        7: "religious leader",  # new Field #to train
        8: "religious ritual",  # new Field #to train
        9: "religious text",
    },
    "science and technology": {
        0: "biomedical science",  # 1 change #to retrain
        1: "mathematics",  # new Field #to train
        2: "natural science",
        3: "scientific institution",  # new Field #to train
        4: "scientific research",  # 2 changes #to retrain
        5: "scientific standards",  # new Field #to train
        6: "social sciences",  # 1 change #to retrain
        7: "technology and engineering",  # 3 changes #to retrain
    },
    "society": {
        0: "communities",  # 2 changes #to retrain
        1: "demographics",  # 1 change #to retrain
        2: "discrimination",  # 1 change #to retrain
        3: "diversity, equity and inclusion",  # new Field #to train
        4: "emigration",  # new Field #to train
        5: "family",  # 3 changes #to retrain
        6: "immigration",  # 1 change #to retrain
        7: "mankind",  # 8 changes #to retrain
        8: "social condition",
        9: "social problem",  # 3 changes #to retrain
        10: "values",  # 1 change #to retrain
        11: "welfare",  # 6 changes #to retrain
    },
    "sport": {
        0: "competition discipline",
        1: "disciplinary action in sport",  # new Field #to train
        2: "drug use in sport",  # 3 changes #to retrain
        3: "sport achievement",  # new Field #to train
        4: "sport event",  # new Field #to train
        5: "sport industry",  # new Field #to train
        6: "sport organisation",  # new Field #to train
        7: "sport venue",  # new Field #to train
        8: "sports coaching",  # new Field #to train
        9: "sports management and ownership",  # new Field #to train
        10: "sports officiating",  # new Field #to train
        11: "sports transaction",  # new Field #to train
    },
    "weather": {
        0: "weather forecast",
        1: "weather phenomena",  # new Field #to train
        2: "weather statistic",  # new Field #to train
        3: "weather warning",
    },
}


CLASS_DICT_THIRD = {
    "arts and entertainment": {
        0: "animation",
        1: "cartoon",
        2: "cinema",
        3: "dance",
        4: "fashion",
        5: "festival",  # new Field
        6: "literature",
        7: "music",
        8: "series",  # new Field
        9: "theatre",
        10: "visual arts",
    },
    "culture": {
        0: "art exhibition",
        1: "cultural development",  # new Field
        2: "customs and tradition",  # new Field
        3: "festive event (culture)",  # new Field
        4: "language",
        5: "library and museum",
        6: "monument and heritage site",
    },
    "mass media": {
        0: "disinformation and misinformation",  # new Field
        1: "news media",
        2: "newspaper",
        3: "online media outlet",  # new Field
        4: "periodical",
        5: "radio",
        6: "social media",  # new Field
        7: "television",
    },
    "act of terror": {0: "act of bioterrorism", 1: "terrorist bombings"},  # name update
    "armed conflict": {
        0: "guerrilla activity",  # new Field
        1: "international military intervention",  # new Field
        2: "military occupation",
        3: "war",
    },
    "civil unrest": {0: "demonstration", 1: "rebellion", 2: "revolution", 3: "riot"},
    "peace process": {
        0: "disarmament",  # new Field
        1: "peace envoy",  # new Field
        2: "peace plan",  # new Field
        3: "peace talks",  # new Field
        4: "peacekeeping force",  # new Field
    },
    "post-war reconstruction": {0: "ordnance clearance"},  # new Field
    "war victims": {
        0: "missing in action",  # new Field
        1: "prisoners of war",  # new Field
    },
    "crime": {
        0: "animal abuse",  # new Field
        1: "arson",
        2: "assault",
        3: "corporate crime",
        4: "corruption",
        5: "cyber crime",  # name update
        6: "drug related crimes",
        7: "fraud",
        8: "genocide",  # new Field
        9: "hijacking",
        10: "homicide",
        11: "human smuggling and trafficking",  # new Field
        12: "kidnapping",
        13: "organised crime",
        14: "reckless driving",  # new Field
        15: "robbery and theft",  # name update
        16: "shootings",  # new Field
        17: "terrorism",
        18: "torture",  # new Field
        19: "vandalism",  # new Field
        20: "war crime",
    },
    "judiciary": {
        0: "court",
        1: "out of court procedures",
        2: "prosecution and prosecutors",  # name update
    },
    "law": {
        0: "administrative law",  # new Field
        1: "civil law",
        2: "criminal law",
        3: "international law",
    },
    "law enforcement": {
        0: "arrest",
        1: "investigation (criminal)",
        2: "police",
        3: "surveillance",  # new Field
    },
    "accident and emergency incident": {
        0: "drowning",  # new Field
        1: "explosion accident and incident",
        2: "industrial accident and incident",
        3: "structural failure",  # new Field
        4: "transportation accident and incident",  # name update
    },
    "disaster": {0: "famine", 1: "fire", 2: "natural disaster"},  # name update
    "emergency incident": {0: "transport incident"},  # new Field
    "business enterprise": {
        0: "cooperative",  # new Field
        1: "small and medium enterprise",  # new Field
        2: "start-up and entrepreneurial business",  # new Field
    },
    "business information": {
        0: "business finance",
        1: "business financing",  # new Field
        2: "business governance",  # new Field
        3: "business reporting and performance",  # new Field
        4: "business restructuring",  # new Field
        5: "business strategy and marketing",
        6: "human resources",
    },
    "economy": {
        0: "central bank",  # new Field
        1: "currency",
        2: "economic organisation",  # new Field
        3: "economic trends and indicators",  # new Field
        4: "emerging market",  # new Field
        5: "international economic institution",  # new Field
        6: "international trade",  # new Field
        7: "monetary policy",  # new Field
        8: "mutual funds",  # new Field
        9: "sharing economy",  # new Field
    },
    "market and exchange": {
        0: "commodities market",  # name update
        1: "debt market",  # name update
        2: "foreign exchange market",
        3: "loan market",
    },
    "products and services": {
        0: "agriculture",
        1: "business service",  # name update
        2: "chemicals",
        3: "commercial fishing",  # name update
        4: "computing and information technology",
        5: "construction and property",
        6: "consumer goods",
        7: "energy and resource",
        8: "financial and business service",
        9: "financial service",  # name update
        10: "forestry and timber",  # name update
        11: "healthcare industry",  # name update
        12: "manufacturing and engineering",
        13: "media and entertainment industry",  # name update
        14: "metal and mineral mining and refining",  # name update
        15: "plastic",  # new Field
        16: "process industry",
        17: "sales channel",  # new Field
        18: "tourism and leisure industry",  # name update
        19: "transport",
        20: "utilities",  # new Field
    },
    "school": {
        0: "adult and continuing education",  # new Field
        1: "college and university",  # name update
        2: "early childhood education",  # new Field
        3: "further education",  # new Field
        4: "independent school",  # new Field
        5: "lower secondary education",  # new Field
        6: "primary education",  # new Field
        7: "private school",  # new Field
        8: "religious school",  # new Field
        9: "state school",  # new Field
        10: "upper secondary education",  # new Field
    },
    "climate change": {0: "global warming"},  # new Field
    "conservation": {0: "energy saving", 1: "parks"},  # new Field  # new Field
    "environmental pollution": {
        0: "air pollution",
        1: "environmental clean-up",  # new Field
        2: "hazardous materials",  # new Field
        3: "waste materials",  # new Field
        4: "water pollution",
    },
    "natural resources": {
        0: "energy resources",  # name update
        1: "land resources",
        2: "population growth",
        3: "renewable energy",
        4: "water",
    },
    "nature": {
        0: "animal",  # new Field
        1: "ecosystem",
        2: "endangered species",
        3: "flowers and plants",  # new Field
        4: "invasive species",
    },
    "disease and condition": {
        0: "cancer",
        1: "communicable disease",
        2: "developmental disorder",  # new Field
        3: "heart disease",
        4: "illness",
        5: "injury",
        6: "medical condition",  # new Field
        7: "mental health and disorder",  # name update
        8: "poisoning",  # new Field
    },
    "government health care": {0: "Medicaid", 1: "Medicare"},  # new Field  # new Field
    "health facility": {
        0: "healthcare clinic",  # new Field
        1: "hospital",  # new Field
    },
    "health treatment and procedure": {
        0: "diet",
        1: "drug rehabilitation",  # new Field
        2: "emergency care",  # new Field
        3: "health care approach",  # new Field
        4: "medical test",  # name update
        5: "non-prescription drug",  # new Field
        6: "physical fitness",
        7: "prescription drug",  # new Field
        8: "preventative medicine",
        9: "surgery",  # new Field
        10: "therapy",
        11: "vaccine",  # new Field
    },
    "medical profession": {
        0: "medical service",  # new Field
        1: "medical specialisation",  # new Field
        2: "medical staff",  # new Field
    },
    "employment": {
        0: "apprenticeship",  # new Field
        1: "child labour",  # new Field
        2: "commuting",  # new Field
        3: "employee",  # new Field
        4: "employer",  # new Field
        5: "employment training",  # new Field
        6: "occupations",  # new Field
        7: "parental leave",  # new Field
        8: "self-employment",  # new Field
        9: "volunteering",  # new Field
        10: "wages and benefits",  # new Field
    },
    "employment legislation": {0: "workplace health and safety"},  # new Field
    "labour market": {0: "gig economy"},  # new Field
    "labour relations": {
        0: "collective agreements",  # new Field
        1: "labour dispute",  # new Field
    },
    "retirement": {0: "pension"},  # new Field
    "unemployment": {
        0: "job layoffs",  # new Field
        1: "unemployment benefits",  # new Field
    },
    "leisure": {
        0: "club and association",
        1: "game",
        2: "gaming and lottery",
        3: "hobby",
        4: "holiday",
        5: "leisure venue",
        6: "outdoor recreational activities",  # name update
        7: "travel and tourism",  # name update
    },
    "lifestyle": {
        0: "house and home",
        1: "organic food",  # new Field
        2: "party",
        3: "trend",
    },
    "wellness": {
        0: "exercise and fitness",  # name update
        1: "mental wellbeing",  # name update
    },
    "election": {
        0: "church elections",  # new Field
        1: "citizens' initiative and recall",  # new Field
        2: "electoral system",
        3: "intergovernmental elections",  # new Field
        4: "local elections",
        5: "national elections",  # new Field
        6: "political campaigns",
        7: "political candidates",  # new Field
        8: "political debates",  # new Field
        9: "primary elections",  # new Field
        10: "referenda",
        11: "regional elections",  # new Field
        12: "voting",
    },
    "fundamental rights": {
        0: "censorship and freedom of speech",
        1: "civil rights",  # name update
        2: "freedom of religion",  # new Field
        3: "freedom of the press",
        4: "human rights",
        5: "privacy",  # new Field
        6: "women's rights",  # new Field
    },
    "government": {
        0: "civil and public service",
        1: "constitution (law)",
        2: "defence",
        3: "espionage and intelligence",
        4: "executive (government)",
        5: "government budget",
        6: "government department",  # name update
        7: "heads of government",  # name update
        8: "heads of state",
        9: "impeachment",
        10: "legislative body",
        11: "local government and authority",
        12: "minister and secretary (government)",  # name update
        13: "national government",  # name update
        14: "political committees",  # new Field
        15: "political convention",  # new Field
        16: "public inquiry",  # new Field
        17: "regional government and authority",  # name update
        18: "regulatory authority",  # new Field
    },
    "government policy": {
        0: "cultural policies",  # new Field
        1: "economic policy",
        2: "education policy",  # new Field
        3: "environmental policy",  # new Field
        4: "healthcare policy",  # new Field
        5: "interior policy",  # new Field
        6: "local government policy",  # new Field
        7: "migration policy",
        8: "nuclear policy",
        9: "regulation of industry",
        10: "safety of citizens",
        11: "sports policies",
        12: "taxation",
    },
    "international relations": {
        0: "border disputes",  # new Field
        1: "diplomacy",
        2: "economic sanction",  # new Field
        3: "foreign aid",
        4: "international organisation",  # new Field
        5: "refugees and internally displaced people",
    },
    "political process": {
        0: "lobbying",
        1: "political development",  # new Field
        2: "political parties and movements",
        3: "political system",
    },
    "belief systems": {
        0: "Buddhism",
        1: "Christianity",
        2: "Confucianism",
        3: "Freemasonry",  # new Field
        4: "Hinduism",
        5: "Islam",
        6: "Jainism",
        7: "Judaism",
        8: "Scientology",
        9: "Shintoism",
        10: "Sikhism",
        11: "Taoism",
        12: "Unificationism",  # new Field
        13: "Zoroastrianism",  # new Field
        14: "atheism and agnosticism",  # new Field
        15: "cult",  # name update
        16: "nature religion",  # new Field
    },
    "religious facility": {0: "church", 1: "mosque", 2: "synagogue", 3: "temple"},
    "religious festival and holiday": {
        0: "All Saints Day",  # new Field
        1: "Christmas",
        2: "Easter",
        3: "Eid al-Adha",  # new Field
        4: "Hanukkah",  # new Field
        5: "Pentecost",  # new Field
        6: "Ramadan",  # new Field
        7: "Walpurgis night",  # new Field
        8: "Yom Kippur",  # new Field
    },
    "religious leader": {0: "pope"},  # new Field
    "religious ritual": {
        0: "baptism",  # new Field
        1: "bar and bat mitzvah",  # new Field
        2: "canonisation",  # new Field
    },
    "religious text": {0: "Bible", 1: "Qur'an", 2: "Torah"},
    "biomedical science": {0: "biotechnology"},  # new Field
    "natural science": {
        0: "astronomy",
        1: "biology",
        2: "chemistry",
        3: "cosmology",
        4: "geology",
        5: "horticulture",
        6: "marine science",
        7: "meteorology",
        8: "physics",
    },
    "scientific research": {
        0: "medical research",
        1: "scientific exploration",
        2: "scientific innovation",  # new Field
        3: "scientific publication",  # new Field
    },
    "social sciences": {
        0: "anthropology",
        1: "archaeology",
        2: "economics",
        3: "geography",
        4: "history",
        5: "information science",
        6: "linguistics",
        7: "philosophy",
        8: "political science",
        9: "psychology",
        10: "sociology",
        11: "study of law",  # new Field
    },
    "technology and engineering": {
        0: "aerospace engineering",
        1: "agricultural technology",  # new Field
        2: "civil engineering",
        3: "electronic engineering",
        4: "identification technology",  # new Field
        5: "information technology and computer science",
        6: "materials science",  # new Field
        7: "mechanical engineering",
        8: "micro science",
    },
    "communities": {
        0: "fraternal and community group",  # new Field
        1: "social networking",  # new Field
    },
    "demographics": {0: "population and census"},  # new Field
    "discrimination": {
        0: "ageism",
        1: "racism",
        2: "religious discrimination",  # new Field
        3: "sexism",
    },
    "family": {
        0: "Dating and Relationships",  # name update
        1: "adoption",
        2: "divorce",
        3: "family planning",
        4: "marriage",
        5: "parenting",  # name update
        6: "pregnancy and childbirth",  # name update
    },
    "immigration": {0: "illegal immigration"},  # new Field
    "mankind": {
        0: "LGBTQ",  # name update
        1: "adults",  # new Field
        2: "children",
        3: "disabilities",  # new Field
        4: "gender",
        5: "indigenous people",  # new Field
        6: "infants",
        7: "men",  # new Field
        8: "national or ethnic minority",  # name update
        9: "nuclear radiation victims",  # new Field
        10: "senior citizens",
        11: "teenagers",
        12: "women",  # new Field
    },
    "social condition": {0: "homelessness", 1: "poverty"},
    "social problem": {
        0: "abusive behaviour",  # new Field
        1: "addiction",
        2: "bullying",  # new Field
        3: "juvenile delinquency",
        4: "prostitution",
        5: "sexual misconduct",  # new Field
        6: "slavery",
    },
    "values": {
        0: "corrupt practices",
        1: "death and dying",
        2: "ethics",
        3: "pornography",
        4: "sexual behaviour",  # new Field
    },
    "welfare": {
        0: "charity",  # new Field
        1: "child care",  # new Field
        2: "elderly care",  # new Field
        3: "long-term care",  # new Field
        4: "public housing",  # new Field
        5: "social services",  # new Field
    },
    "competition discipline": {
        0: "3x3 basketball",  # new Field
        1: "American football",
        2: "Australian rules football",
        3: "Canadian football",  # new Field
        4: "Gaelic football",  # new Field
        5: "Jai Alai (Pelota)",
        6: "archery",
        7: "arm wrestling",  # new Field
        8: "artistic swimming",  # new Field
        9: "athletics",  # name update
        10: "badminton",
        11: "bandy",
        12: "baseball",
        13: "basketball",
        14: "biathlon",
        15: "billiards",
        16: "bobsleigh",
        17: "bodybuilding",  # new Field
        18: "boules",  # new Field
        19: "boxing",
        20: "bullfighting",
        21: "canoe slalom",  # new Field
        22: "canoe sprint",  # new Field
        23: "canoeing",
        24: "casting (fishing)",  # new Field
        25: "cheerleading",  # new Field
        26: "chess",
        27: "competitive dancing",  # new Field
        28: "cricket",
        29: "croquet",  # new Field
        30: "curling",
        31: "cycling",
        32: "darts",
        33: "diving",
        34: "dog racing",
        35: "duathlon",  # new Field
        36: "eSports",  # new Field
        37: "equestrian",  # name update
        38: "fencing",
        39: "field hockey",
        40: "figure skating",
        41: "fist ball",  # new Field
        42: "floorball",
        43: "flying disc",  # new Field
        44: "football 5-a-side",  # new Field
        45: "goalball",  # new Field
        46: "golf",
        47: "gymnastics",
        48: "handball (team)",
        49: "hornuss",  # new Field
        50: "horse racing",
        51: "hurling",
        52: "ice hockey",
        53: "inline skating",
        54: "kabaddi",
        55: "kayaking",
        56: "kiting",  # new Field
        57: "lacrosse",
        58: "luge",
        59: "marathon",
        60: "martial arts",
        61: "modern pentathlon",
        62: "motor car racing",
        63: "motorboat racing",  # new Field
        64: "motorcycling",
        65: "mountain climbing",
        66: "netball",
        67: "orienteering",
        68: "padel",  # new Field
        69: "parachuting",
        70: "polo",
        71: "pool",
        72: "power boating",  # new Field
        73: "racquetball",  # new Field
        74: "ringette",  # new Field
        75: "road cycling",  # new Field
        76: "rodeo",
        77: "roller sports",
        78: "rowing",
        79: "rugby",  # name update
        80: "sailing",
        81: "sepak takraw",  # new Field
        82: "shinty",
        83: "short track speed skating",  # new Field
        84: "skeleton",
        85: "skiing",
        86: "sky diving",  # new Field
        87: "snooker",
        88: "snowboarding",
        89: "soccer",
        90: "softball",
        91: "speed skating",
        92: "sport climbing",  # new Field
        93: "sport shooting",  # name update
        94: "squash",
        95: "stand up paddleboarding (SUP)",  # new Field
        96: "sumo wrestling",
        97: "surfing",
        98: "swimming",
        99: "table tennis",
        100: "ten pin bowling",  # new Field
        101: "tennis",
        102: "track cycling",  # new Field
        103: "triathlon",
        104: "tug-of-war",  # new Field
        105: "underwater sports",  # new Field
        106: "volleyball",
        107: "water polo",
        108: "water skiing",  # new Field
        109: "weightlifting and powerlifting",  # name update
        110: "windsurfing",  # new Field
        111: "wrestling",
    },
    "drug use in sport": {
        0: "drug abuse in sport",  # new Field
        1: "drug testing in sport",  # new Field
        2: "medical drug use in sport",  # new Field
    },
    "sport achievement": {
        0: "sports honour",  # new Field
        1: "sports medal and trophy",  # new Field
        2: "sports record",  # new Field
    },
    "sport event": {
        0: "Olympic Games",  # new Field
        1: "Paralympic Games",  # new Field
        2: "continental championship",  # new Field
        3: "continental cup",  # new Field
        4: "continental games",  # new Field
        5: "final game",  # new Field
        6: "international championship",  # new Field
        7: "international cup",  # new Field
        8: "international games",  # new Field
        9: "national championship",  # new Field
        10: "national cup",  # new Field
        11: "national games",  # new Field
        12: "playoff championship",  # new Field
        13: "regional championship",  # new Field
        14: "regional cup",  # new Field
        15: "regional games",  # new Field
        16: "regular competition",  # new Field
        17: "world championship",  # new Field
        18: "world cup",  # new Field
        19: "world games",  # new Field
    },
}

CLASS_DICT_FOURTH = {
    "dance": {0: "ballet", 1: "modern dance", 2: "traditional dance"},
    "fashion": {0: "cosmetics", 1: "hairstyles", 2: "jewellery"},
    "festival": {0: "film festival"},
    "literature": {
        0: "drama (literature)",
        1: "fiction",
        2: "non-fiction",
        3: "poetry",
    },
    "music": {0: "musical genre", 1: "musical instrument", 2: "musical performance"},
    "theatre": {
        0: "cabaret",
        1: "drama (theatre)",
        2: "music theatre",
        3: "musical",
        4: "opera",
        5: "operetta",
        6: "stand-up comedy",
    },
    "visual arts": {
        0: "architecture",
        1: "design (visual arts)",
        2: "drawing",
        3: "forging",
        4: "painting",
        5: "photography",
        6: "sculpture",
        7: "textile arts",
        8: "woodworking",
    },
    "monument and heritage site": {0: "restoration"},
    "social media": {0: "influencers"},
    "war": {0: "civil war", 1: "war crime action"},
    "assault": {0: "sex crime"},
    "corporate crime": {
        0: "accounting crime",
        1: "anti-trust crime",
        2: "breach of contract",
        3: "embezzlement",
        4: "insider trading",
        5: "restraint of trade",
    },
    "corruption": {0: "bribery"},
    "drug related crimes": {0: "drug trafficking"},
    "fraud": {0: "tax evasion"},
    "organised crime": {0: "gang activity"},
    "court": {
        0: "appeal (court)",
        1: "court administration",
        2: "judge",
        3: "supreme and high court",
        4: "trial (court)",
    },
    "out of court procedures": {0: "arbitration and mediation"},
    "civil law": {0: "regulations"},
    "international law": {0: "extradition", 1: "international court and tribunal"},
    "investigation (criminal)": {
        0: "dropped criminal investigation",
        1: "missing person",
    },
    "industrial accident and incident": {0: "nuclear accident and incident"},
    "transportation accident and incident": {
        0: "air and space accident and incident",
        1: "maritime accident and incident",
        2: "railway accident and incident",
        3: "road accident and incident",
    },
    "fire": {0: "wildfire"},
    "natural disaster": {
        0: "drought",
        1: "earthquake",
        2: "flood",
        3: "landslide",
        4: "meteorological disaster",
        5: "tsunami",
        6: "volcanic eruption",
    },
    "transport incident": {
        0: "air and space incident",
        1: "maritime incident",
        2: "railway incident",
        3: "road incident",
    },
    "business finance": {0: "analysts comment"},
    "business financing": {
        0: "bankruptcy",
        1: "corporate bond",
        2: "crowdfunding",
        3: "financially distressed company",
        4: "restructuring and recapitalisation",
        5: "securities",
        6: "stocks and securities",
    },
    "business governance": {
        0: "annual and special corporate meeting",
        1: "annual report",
        2: "board of directors",
        3: "environmental, social and governance policy (ESG)",
        4: "proxy filing",
        5: "shareholder activity",
    },
    "business reporting and performance": {
        0: "accounting and audit",
        1: "corporate earnings",
        2: "credit rating",
        3: "earnings forecast",
        4: "financial statement",
    },
    "business restructuring": {
        0: "company spin-off",
        1: "joint venture",
        2: "leveraged buyout",
        3: "management buyout",
        4: "merger or acquisition",
    },
    "business strategy and marketing": {
        0: "client relationship management",
        1: "commercial contract",
        2: "economic globalisation",
        3: "licensing agreement",
        4: "market research",
        5: "market trend",
        6: "new product or service",
        7: "outsourcing",
        8: "patent, copyright and trademark",
        9: "product recall",
        10: "public contract",
        11: "research and development",
    },
    "human resources": {0: "executive officer", 1: "layoffs and downsizing"},
    "currency": {0: "cryptocurrency"},
    "economic trends and indicators": {
        0: "bonds",
        1: "budgets and budgeting",
        2: "consumer confidence",
        3: "consumers",
        4: "credit and debt",
        5: "deflation",
        6: "economic growth",
        7: "economic indicator",
        8: "employment statistics",
        9: "exporting",
        10: "government aid",
        11: "government debt",
        12: "gross domestic product",
        13: "importing",
        14: "industrial production",
        15: "inflation",
        16: "inventories",
        17: "investments",
        18: "mortgages",
        19: "prices",
        20: "productivity",
        21: "recession",
    },
    "international trade": {
        0: "balance of trade",
        1: "tariff",
        2: "trade agreements",
        3: "trade dispute",
        4: "trade policy",
    },
    "monetary policy": {0: "interest rates"},
    "commodities market": {
        0: "energy market",
        1: "metal",
        2: "soft commodities market",
    },
    "agriculture": {
        0: "aquaculture",
        1: "arable farming",
        2: "livestock farming",
        3: "viniculture",
    },
    "business service": {
        0: "consultancy",
        1: "employment agency",
        2: "janitorial service",
        3: "legal service",
        4: "payment service",
        5: "personal service",
        6: "rental service",
        7: "shipping and postal service",
        8: "trade show or expo",
        9: "wedding service",
    },
    "chemicals": {
        0: "fertiliser",
        1: "health and beauty product",
        2: "inorganic chemical",
        3: "organic chemical",
    },
    "computing and information technology": {
        0: "Internet of Things",
        1: "computer and telecommunications hardware",
        2: "computer networking",
        3: "computer security",
        4: "satellite technology",
        5: "semiconductor and electronic component",
        6: "software and applications",
        7: "telecommunication equipment",
        8: "telecommunication service",
        9: "wireless technology",
    },
    "construction and property": {
        0: "building material",
        1: "commercial building",
        2: "commercial real estate",
        3: "design and engineering",
        4: "farms",
        5: "heavy construction",
        6: "house building",
        7: "infrastructure projects",
        8: "land price",
        9: "real estate",
        10: "residential real estate",
    },
    "consumer goods": {
        0: "beverage",
        1: "beverage and grocery",
        2: "clothing",
        3: "consumer electronics",
        4: "furnishings and furniture",
        5: "grocery",
        6: "handicrafts",
        7: "luxury good",
        8: "non-durable good",
        9: "pet product and service",
        10: "tobacco and nicotine",
        11: "toy and game",
    },
    "energy and resource": {
        0: "biofuel",
        1: "coal",
        2: "energy industry",
        3: "nuclear power",
        4: "oil and gas",
        5: "oil and gas - downstream activities",
        6: "oil and gas - upstream activities",
        7: "renewable energy",
    },
    "financial and business service": {
        0: "funeral parlour and crematorium",
        1: "personal finance",
        2: "personal income",
        3: "printing service",
    },
    "financial service": {
        0: "accountancy and auditing",
        1: "asset management",
        2: "banking",
        3: "financial advisory service",
        4: "insurance",
        5: "loans and lending",
        6: "personal finance and investment",
        7: "stock broking",
    },
    "healthcare industry": {
        0: "biotechnology business",
        1: "health care provider",
        2: "medical equipment",
        3: "pharmaceutical",
    },
    "manufacturing and engineering": {
        0: "aerospace",
        1: "automotive",
        2: "capital goods",
        3: "defence equipment",
        4: "electrical appliance",
        5: "heavy engineering",
        6: "industrial component",
        7: "instrument engineering",
        8: "machine manufacturing",
        9: "railway manufacturing",
        10: "shipbuilding",
    },
    "media and entertainment industry": {
        0: "advertising",
        1: "books and publishing",
        2: "film industry",
        3: "music industry",
        4: "news agency",
        5: "news industry",
        6: "newspaper and magazine",
        7: "online media industry",
        8: "podcast",
        9: "public relations",
        10: "radio industry",
        11: "satellite and cable service",
        12: "streaming service",
        13: "television industry",
    },
    "metal and mineral mining and refining": {
        0: "iron and steel",
        1: "mining",
        2: "non-ferrous metal",
        3: "precious material",
    },
    "process industry": {
        0: "distiller and brewer",
        1: "e-cigarette",
        2: "paper and packaging product",
        3: "rubber product",
        4: "soft drinks",
        5: "textile and clothing",
    },
    "sales channel": {0: "auction", 1: "retail", 2: "wholesale"},
    "tourism and leisure industry": {
        0: "casinos and gambling",
        1: "hotel and accommodation",
        2: "recreational and sporting goods",
        3: "restaurant and catering",
        4: "tour operator",
    },
    "transport": {
        0: "air transport",
        1: "logistics",
        2: "public transport",
        3: "railway transport",
        4: "road transport",
        5: "shared transport",
        6: "taxi and ride-hailing",
        7: "traffic",
        8: "waterway and maritime transport",
    },
    "utilities": {
        0: "electricity",
        1: "heating and cooling",
        2: "waste management",
        3: "water supply",
    },
    "college and university": {0: "college", 1: "university"},
    "land resources": {0: "forests", 1: "mountains"},
    "water": {0: "oceans", 1: "rivers", 2: "wetlands"},
    "animal": {0: "animal disease", 1: "pests"},
    "flowers and plants": {0: "plant disease"},
    "communicable disease": {0: "epidemic and pandemic", 1: "viral disease"},
    "medical condition": {0: "obesity"},
    "mental health and disorder": {
        0: "anxiety and stress",
        1: "depression",
        2: "eating disorder",
    },
    "diet": {0: "dietary supplement"},
    "health care approach": {
        0: "conventional medicine",
        1: "herbal medicine",
        2: "holistic medicine",
        3: "traditional Chinese medicine",
    },
    "medical specialisation": {
        0: "dentistry",
        1: "eye care",
        2: "general practice",
        3: "geriatric medicine",
        4: "obstetrics/gynaecology",
        5: "oncology",
        6: "orthopaedics",
        7: "paediatrics",
        8: "pharmacology",
        9: "psychiatry",
        10: "radiology",
        11: "reproductive medicine",
        12: "surgical medicine",
        13: "veterinary medicine",
    },
    "employment training": {0: "advanced training", 1: "retraining"},
    "wages and benefits": {
        0: "employee benefits",
        1: "profit sharing",
        2: "social security",
    },
    "collective agreements": {
        0: "contract issue-healthcare",
        1: "contract issue-wages",
        2: "contract issue-work rules",
    },
    "labour dispute": {0: "labour strike"},
    "game": {
        0: "board game",
        1: "card game",
        2: "children's game",
        3: "dice game",
        4: "outdoor game",
        5: "puzzle",
        6: "tile game",
        7: "video game",
    },
    "hobby": {
        0: "automobile enthusiasm",
        1: "bicycle enthusiasm",
        2: "collecting",
        3: "food and drink enthusiasm",
        4: "motorcycle enthusiasm",
    },
    "holiday": {0: "Halloween", 1: "public holiday"},
    "leisure venue": {
        0: "amusement park",
        1: "bar",
        2: "cafe",
        3: "nightclub",
        4: "restaurant",
        5: "sports facilities",
        6: "zoo",
    },
    "outdoor recreational activities": {
        0: "fishing",
        1: "horseback riding",
        2: "hunting",
        3: "recreational hiking and climbing",
        4: "scuba diving",
    },
    "travel and tourism": {0: "tourism"},
    "house and home": {0: "gardening", 1: "home renovation", 2: "interior decoration"},
    "trend": {0: "body modification"},
    "political campaigns": {0: "campaign finance"},
    "civil and public service": {
        0: "civilian service",
        1: "public employees",
        2: "public officials",
    },
    "defence": {
        0: "armed forces",
        1: "military equipment",
        2: "security measures (defence)",
    },
    "government budget": {0: "public finance"},
    "legislative body": {
        0: "lower house (legislature)",
        1: "upper house (legislature)",
    },
    "economic policy": {
        0: "economic development incentive",
        1: "nationalisation",
        2: "privatisation",
        3: "state-owned enterprise",
    },
    "interior policy": {
        0: "data protection policy",
        1: "housing and urban planning policy",
        2: "infrastructure policy",
        3: "integration policy",
        4: "pension and welfare policy",
        5: "personal data collection policy",
        6: "personal weapon control policy",
        7: "planning inquiries",
        8: "policy towards indigenous people",
        9: "regional development policy",
    },
    "regulation of industry": {0: "food and drink regulations"},
    "diplomacy": {0: "summit meetings", 1: "treaty"},
    "political parties and movements": {0: "political leadership"},
    "political system": {0: "democracy", 1: "dictatorship"},
    "Christianity": {
        0: "Catholicism",
        1: "Christian Orthodoxy",
        2: "Mormonism",
        3: "Old Catholic",
        4: "Protestantism",
        5: "Roman Catholic",
        6: "ecumenism",
    },
    "Islam": {0: "Shia Islam", 1: "Sunni Islam"},
    "Judaism": {0: "Hasidism"},
    "biology": {
        0: "botany",
        1: "genetics",
        2: "palaeontology",
        3: "physiology",
        4: "zoology",
    },
    "physics": {0: "electromagnetism", 1: "nuclear physics"},
    "scientific exploration": {0: "space exploration"},
    "aerospace engineering": {0: "rocketry"},
    "information technology and computer science": {0: "artificial intelligence"},
    "micro science": {0: "nanotechnology"},
    "family planning": {0: "abortion", 1: "contraception"},
    "death and dying": {0: "euthanasia", 1: "suicide"},
    "archery": {0: "crossbow shooting", 1: "longbow"},
    "artistic swimming": {
        0: "synchronised free routine",
        1: "synchronised technical routine",
    },
    "athletics": {
        0: "cross-country run",
        1: "decathlon",
        2: "discus throw",
        3: "hammer throw",
        4: "heptathlon",
        5: "high jump",
        6: "hurdles",
        7: "javelin throw",
        8: "long distance run",
        9: "long jump",
        10: "middle distance run",
        11: "pentathlon",
        12: "pole vault",
        13: "race walking",
        14: "relay run",
        15: "shot put",
        16: "sprint run",
        17: "steeplechase (athletics)",
        18: "triple jump",
    },
    "baseball": {0: "rubberball baseball"},
    "boxing": {
        0: "bantamweight (boxing)",
        1: "cruiserweight (boxing)",
        2: "featherweight (boxing)",
        3: "flyweight (boxing)",
        4: "heavyweight (boxing)",
        5: "light flyweight (boxing)",
        6: "light-heavyweight (boxing)",
        7: "light-middleweight (boxing)",
        8: "light-welterweight (boxing)",
        9: "lightweight (boxing)",
        10: "middleweight (boxing)",
        11: "straw weight (boxing)",
        12: "super-bantamweight (boxing)",
        13: "super-featherweight (boxing)",
        14: "super-flyweight (boxing)",
        15: "super-heavyweight (boxing)",
        16: "super-middleweight (boxing)",
        17: "welterweight (boxing)",
    },
    "canoeing": {
        0: "C1 (canoeing)",
        1: "C2 (canoeing)",
        2: "C4 (canoeing)",
        3: "canoe sailing",
        4: "pontoniering",
    },
    "competitive dancing": {0: "breaking (breakdance)"},
    "curling": {0: "icestock sport"},
    "cycling": {
        0: "Keirin",
        1: "Madison race",
        2: "artistic cycling",
        3: "bi-crossing",
        4: "bmx freestyle",
        5: "bmx racing",
        6: "cycle ball",
        7: "cycle sprint race",
        8: "cycling staging race",
        9: "cyclo-cross",
        10: "individual pursuit (cycling)",
        11: "individual time trial (cycling)",
        12: "mountain biking",
        13: "points race (cycling)",
        14: "road cycling",
        15: "road cycling team pursuit",
        16: "team cycle sprint",
        17: "team time trial (cycling)",
        18: "track race (cycling)",
    },
    "diving": {0: "platform diving", 1: "springboard diving", 2: "synchronised diving"},
    "dog racing": {0: "dog sled racing", 1: "oval track dog racing"},
    "equestrian": {
        0: "cross-country horse riding",
        1: "dressage",
        2: "horse driving",
        3: "horse jumping",
        4: "three day eventing",
    },
    "fencing": {0: "epee", 1: "foil", 2: "sabre"},
    "figure skating": {0: "ice dance"},
    "golf": {0: "mini golf"},
    "gymnastics": {0: "artistic gymnastics", 1: "rhythmic gymnastics", 2: "trampoline"},
    "horse racing": {0: "flat racing", 1: "harness racing", 2: "steeple chase"},
    "ice hockey": {0: "sledge hockey"},
    "kayaking": {0: "K1 (kayaking)", 1: "K2 (kayaking)", 2: "K4 (kayaking)"},
    "martial arts": {
        0: "Taekwon-Do",
        1: "judo",
        2: "jukendo",
        3: "karate",
        4: "kendo",
        5: "kickboxing",
        6: "krav maga",
        7: "kyudo",
        8: "mixed martial arts",
        9: "naginata",
        10: "sambo (martial art)",
        11: "wushu",
    },
    "motor car racing": {
        0: "F3000",
        1: "Formula One",
        2: "Indy Racing",
        3: "endurance race",
        4: "motor car rallycross",
        5: "motor car rallying",
    },
    "motorcycling": {
        0: "enduro",
        1: "grass-track",
        2: "moto-ball",
        3: "moto-cross",
        4: "motoGP",
        5: "motorcycle endurance",
        6: "motorcycle rallying",
        7: "motorcycling trial",
        8: "side-cars",
        9: "speedway",
    },
    "mountain climbing": {0: "ice climbing", 1: "mountaineering"},
    "orienteering": {0: "ski orienteering"},
    "rodeo": {
        0: "bareback bronc",
        1: "barrel racing",
        2: "bull riding",
        3: "bulldogging",
        4: "calf roping",
        5: "goat roping",
        6: "saddle bronc",
    },
    "roller sports": {0: "roller hockey", 1: "skateboarding"},
    "rowing": {
        0: "coxed eight",
        1: "coxed four",
        2: "coxed pair",
        3: "coxless four",
        4: "coxless pair",
        5: "double sculls",
        6: "quadruple sculls",
        7: "single sculls",
    },
    "rugby": {0: "rugby league", 1: "rugby sevens", 2: "rugby union"},
    "sailing": {
        0: "dinghy",
        1: "keelboat",
        2: "multihull",
        3: "non-stop solo race",
        4: "ocean sailing",
        5: "round the world race",
        6: "sailing regatta",
        7: "solo ocean sailing",
    },
    "skiing": {
        0: "Nordic combined",
        1: "Nordic skiing",
        2: "Telemark skiing",
        3: "alpine skiing",
        4: "cross-country skiing",
        5: "freestyle skiing",
        6: "grass skiing",
        7: "ski jumping",
    },
    "sport shooting": {
        0: "clay pigeon shooting",
        1: "pistol shooting",
        2: "rifle shooting",
        3: "running target shooting",
        4: "shotgun shooting",
    },
    "swimming": {
        0: "backstroke",
        1: "breaststroke",
        2: "butterfly swimming",
        3: "freestyle swimming",
        4: "marathon swimming",
        5: "medley swimming",
        6: "relay freestyle swimming",
        7: "relay medley swimming",
        8: "short course swimming",
    },
    "volleyball": {0: "beach volleyball"},
    "weightlifting and powerlifting": {
        0: "clean and jerk (weightlifting)",
        1: "powerlifting",
        2: "snatch (weightlifting)",
    },
    "wrestling": {0: "Swiss wrestling", 1: "freestyle wrestling", 2: "greco-roman"},
}

ID_TO_TOPIC = {
    "00000000": "root",
    "01000000": "arts, culture, entertainment and media",
    "20000002": "arts and entertainment",
    "20000038": "culture",
    "20000045": "mass media",
    "16000000": "conflict, war and peace",
    "20000053": "act of terror",
    "20000056": "armed conflict",
    "20000065": "civil unrest",
    "20000070": "coup d'etat",
    "20001361": "cyber warfare",
    "20000071": "massacre",
    "20000073": "peace process",
    "20000077": "post-war reconstruction",
    "20001377": "war victims",
    "02000000": "crime, law and justice",
    "20000082": "crime",
    "20000106": "judiciary",
    "20000119": "justice",
    "20000121": "law",
    "20000129": "law enforcement",
    "03000000": "disaster, accident and emergency incident",
    "20000139": "accident and emergency incident",
    "20000148": "disaster",
    "20000160": "emergency incident",
    "20000167": "emergency planning",
    "20000168": "emergency response",
    "04000000": "economy, business and finance",
    "20000349": "business enterprise",
    "20000170": "business information",
    "20000344": "economy",
    "20000385": "market and exchange",
    "20000209": "products and services",
    "05000000": "education",
    "20000412": "curriculum",
    "20001217": "educational grading",
    "20000413": "educational testing and examinations",
    "20000414": "entrance examination",
    "20001337": "online and remote learning",
    "20000398": "parents group",
    "20000399": "religious education",
    "20000400": "school",
    "20000410": "social learning",
    "20000415": "students",
    "20000416": "teachers",
    "20000411": "teaching and learning",
    "20001216": "vocational education",
    "06000000": "environment",
    "20000418": "climate change",
    "20000420": "conservation",
    "20000424": "environmental pollution",
    "20000430": "natural resources",
    "20000441": "nature",
    "20001374": "sustainability",
    "07000000": "health",
    "20000446": "disease and condition",
    "20000480": "government health care",
    "20000461": "health facility",
    "20000483": "health insurance",
    "20000463": "health organisation",
    "20000464": "health treatment and procedure",
    "20000485": "medical profession",
    "20000493": "non-human diseases",
    "20000484": "private health care",
    "20001358": "public health",
    "08000000": "human interest",
    "20000497": "accomplishment",
    "20001237": "anniversary",
    "20000498": "award and prize",
    "20001238": "birthday",
    "20000505": "celebrity",
    "20000501": "ceremony",
    "20000504": "high society",
    "20000503": "human mishap",
    "20000502": "people",
    "20000499": "record and achievement",
    "09000000": "labour",
    "20000509": "employment",
    "20000521": "employment legislation",
    "20000523": "labour market",
    "20000524": "labour relations",
    "20000531": "retirement",
    "20000533": "unemployment",
    "20000536": "unions",
    "10000000": "lifestyle and leisure",
    "20000538": "leisure",
    "20000565": "lifestyle",
    "20001339": "wellness",
    "11000000": "politics",
    "20000574": "election",
    "20000587": "fundamental rights",
    "20000593": "government",
    "20000621": "government policy",
    "20000638": "international relations",
    "20000646": "non-governmental organisation",
    "20000647": "political crisis",
    "20000648": "political dissent",
    "20000649": "political process",
    "12000000": "religion",
    "20000657": "belief systems",
    "20000687": "interreligious dialogue",
    "20000702": "relations between religion and government",
    "20000688": "religious conflict",
    "20000689": "religious event",
    "20000697": "religious facility",
    "20000690": "religious festival and holiday",
    "20000703": "religious leader",
    "20000696": "religious ritual",
    "20000705": "religious text",
    "13000000": "science and technology",
    "20000710": "biomedical science",
    "20000715": "mathematics",
    "20000717": "natural science",
    "20000741": "scientific institution",
    "20000735": "scientific research",
    "20000755": "scientific standards",
    "20000742": "social sciences",
    "20000756": "technology and engineering",
    "14000000": "society",
    "20000763": "information technology and computer science",
    "20000768": "communities",
    "20000770": "demographics",
    "20000775": "discrimination",
    "20001373": "diversity, equity and inclusion",
    "20000772": "emigration",
    "20000780": "family",
    "20000771": "immigration",
    "20000788": "mankind",
    "20000799": "social condition",
    "20000802": "social problem",
    "20000808": "values",
    "20000817": "welfare",
    "15000000": "sport",
    "20000822": "competition discipline",
    "20001103": "disciplinary action in sport",
    "20001104": "drug use in sport",
    "20001301": "sport achievement",
    "20001108": "sport event",
    "20001124": "sport industry",
    "20001125": "sport organisation",
    "20001126": "sport venue",
    "20001323": "sports coaching",
    "20001324": "sports management and ownership",
    "20001325": "sports officiating",
    "20001148": "sports transaction",
    "17000000": "weather",
    "20001128": "weather forecast",
    "20001129": "weather phenomena",
    "20001130": "weather statistic",
    "20001131": "weather warning",
}


ID_TO_LEVEL = {
    "00000000": 1,
    "01000000": 2,
    "20000002": 3,
    "20000038": 3,
    "20000045": 3,
    "16000000": 2,
    "20000053": 3,
    "20000056": 3,
    "20000065": 3,
    "20000070": 3,
    "20001361": 3,
    "20000071": 3,
    "20000073": 3,
    "20000077": 3,
    "20001377": 3,
    "02000000": 2,
    "20000082": 3,
    "20000106": 3,
    "20000119": 3,
    "20000121": 3,
    "20000129": 3,
    "03000000": 2,
    "20000139": 3,
    "20000148": 3,
    "20000160": 3,
    "20000167": 3,
    "20000168": 3,
    "04000000": 2,
    "20000349": 3,
    "20000170": 3,
    "20000344": 3,
    "20000385": 3,
    "20000209": 3,
    "05000000": 2,
    "20000412": 3,
    "20001217": 3,
    "20000413": 3,
    "20000414": 3,
    "20001337": 3,
    "20000398": 3,
    "20000399": 3,
    "20000400": 3,
    "20000410": 3,
    "20000415": 3,
    "20000416": 3,
    "20000411": 3,
    "20001216": 3,
    "06000000": 2,
    "20000418": 3,
    "20000420": 3,
    "20000424": 3,
    "20000430": 3,
    "20000441": 3,
    "20001374": 3,
    "07000000": 2,
    "20000446": 3,
    "20000480": 3,
    "20000461": 3,
    "20000483": 3,
    "20000463": 3,
    "20000464": 3,
    "20000485": 3,
    "20000493": 3,
    "20000484": 3,
    "20001358": 3,
    "08000000": 2,
    "20000497": 3,
    "20001237": 3,
    "20000498": 3,
    "20001238": 3,
    "20000505": 3,
    "20000501": 3,
    "20000504": 3,
    "20000503": 3,
    "20000502": 3,
    "20000499": 3,
    "09000000": 2,
    "20000509": 3,
    "20000521": 3,
    "20000523": 3,
    "20000524": 3,
    "20000531": 3,
    "20000533": 3,
    "20000536": 3,
    "10000000": 2,
    "20000538": 3,
    "20000565": 3,
    "20001339": 3,
    "11000000": 2,
    "20000574": 3,
    "20000587": 3,
    "20000593": 3,
    "20000621": 3,
    "20000638": 3,
    "20000646": 3,
    "20000647": 3,
    "20000648": 3,
    "20000649": 3,
    "12000000": 2,
    "20000657": 3,
    "20000687": 3,
    "20000702": 3,
    "20000688": 3,
    "20000689": 3,
    "20000697": 3,
    "20000690": 3,
    "20000703": 3,
    "20000696": 3,
    "20000705": 3,
    "13000000": 2,
    "20000710": 3,
    "20000715": 3,
    "20000717": 3,
    "20000741": 3,
    "20000735": 3,
    "20000755": 3,
    "20000742": 3,
    "20000756": 3,
    "14000000": 2,
    "20000763": 3,
    "20000768": 3,
    "20000770": 3,
    "20000775": 3,
    "20001373": 3,
    "20000772": 3,
    "20000780": 3,
    "20000771": 3,
    "20000788": 3,
    "20000799": 3,
    "20000802": 3,
    "20000808": 3,
    "20000817": 3,
    "15000000": 2,
    "20000822": 3,
    "20001103": 3,
    "20001104": 3,
    "20001301": 3,
    "20001108": 3,
    "20001124": 3,
    "20001125": 3,
    "20001126": 3,
    "20001323": 3,
    "20001324": 3,
    "20001325": 3,
    "20001148": 3,
    "17000000": 2,
    "20001128": 3,
    "20001129": 3,
    "20001130": 3,
    "20001131": 3,
}

CLASS_DICT = {
    **CLASS_DICT_FIRST,
    **CLASS_DICT_SECOND,
    **CLASS_DICT_THIRD,
    **CLASS_DICT_FOURTH,
}

NAME_MAPPING_DICT_FIRST = {
    "arts, culture, entertainment and media": "arts, culture and entertainment",
    "conflict, war and peace": "conflicts, war and peace",
}

NAME_MAPPING_DICT_SECOND = {
    # Category: 'crime, law and justice'
    "justice": "justice and rights",  # Renamed
    "religious facility": "religious facilities",
}

NAME_MAPPING_DICT_THIRD = {
    # Category: 'crime, law and justice'
    "justice": "justice and rights",  # Renamed
    "religious facility": "religious facilities",
}
