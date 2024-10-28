"""Class dict and id to topic."""

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
        16: "none",
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
        0: "business enterprise",
        1: "business information",
        2: "economy",
        3: "market and exchange",
        4: "products and services",
        5: "none",
    },
    "education": {0: "school", 1: "teaching and learning"},
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
        1: "disease and condition",
        2: "government health care",
        3: "health insurance",
        4: "health facility",
        5: "medical profession",
        6: "non-human diseases",
    },
    "labour": {
        0: "employment",
        1: "retirement",
        2: "unemployment",
        3: "labour relations",
    },
    "lifestyle and leisure": {
        0: "leisure",
        1: "lifestyle",
    },
    "politics": {
        0: "government",
        1: "election",
        2: "international relations",
        3: "government policy",
        4: "fundamental rights",
        5: "political process",
    },
    "religion": {
        0: "belief systems",
        1: "religious text",
        2: "religious facility",
        3: "religious festival or holiday",
    },
    "science and technology": {
        0: "natural science",
        1: "technology and engineering",
        2: "biomedical science",
        3: "social sciences",
        4: "mathematics",
        5: "scientific research",
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
    "sport": {
        0: "competition discipline",
        1: "drug use in sport",
    },
    "weather": {
        0: "weather forecast",
        1: "weather warning",
    },
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
        0: "business finance",
        1: "business financing",
        2: "business governance",
        3: "business reporting and performance",
        4: "business restructuring",
        5: "business strategy and marketing",
        6: "human resources",
        7: "none",
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

CLASS_DICT_FOURTH = {
    "information technology and computer science": {
        0: "artificial intelligence",
        1: "none",
    }
}
CLASS_DICT = {
    **CLASS_DICT_FIRST,
    **CLASS_DICT_SECOND,
    **CLASS_DICT_THIRD,
    **CLASS_DICT_FOURTH,
}

ID_TO_TOPIC = {
    "00000000": "root",
    "01000000": "arts, culture, entertainment and media",
    "16000000": "conflict, war and peace",
    "02000000": "crime, law and justice",
    "03000000": "disaster, accident and emergency incident",
    "04000000": "economy, business and finance",
    "05000000": "education",
    "06000000": "environment",
    "07000000": "health",
    "08000000": "human interest",
    "09000000": "labour",
    "10000000": "lifestyle and leisure",
    "11000000": "politics",
    "12000000": "religion",
    "13000000": "science and technology",
    "14000000": "society",
    "15000000": "sport",
    "17000000": "weather",
    "20000002": "arts and entertainment",
    "20000038": "culture",
    "20000045": "mass media",
    "20000053": "act of terror",
    "20000056": "armed conflict",
    "20000065": "civil unrest",
    "20000070": "coup d'etat",
    "20001361": "cyber warfare",
    "20000071": "massacre",
    "20000073": "peace process",
    "20000077": "post-war reconstruction",
    "20000080": "prisoners of war",
    "20000082": "crime",
    "20000106": "judiciary",
    "20000119": "justice",
    "20000121": "law",
    "20000129": "law enforcement",
    "20000139": "accident and emergency incident",
    "20000148": "disaster",
    "20000160": "emergency incident",
    "20000167": "emergency planning",
    "20000168": "emergency response",
    "20000170": "business information",
    "20000209": "economic sector",
    "20000344": "economy",
    "20000385": "market and exchange",
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
    "20000418": "climate change",
    "20000420": "conservation",
    "20000424": "environmental pollution",
    "20000430": "natural resources",
    "20000441": "nature",
    "20000446": "disease and condition",
    "20000480": "government health care",
    "20000460": "obesity",
    "20000461": "health facility",
    "20000483": "health insurance",
    "20000463": "health organisation",
    "20000464": "health treatment and procedure",
    "20000485": "medical profession",
    "20000493": "non-human diseases",
    "20000494": "animal disease",
    "20000495": "plant disease",
    "20000484": "private health care",
    "20001358": "public health",
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
    "20000509": "employment",
    "20000521": "employment legislation",
    "20000523": "labour market",
    "20000524": "labour relations",
    "20000531": "retirement",
    "20000533": "unemployment",
    "20000536": "unions",
    "20000538": "leisure",
    "20000565": "lifestyle",
    "20000568": "food and drink enthusiasm",
    "20001339": "wellness",
    "20000574": "election",
    "20000587": "fundamental rights",
    "20000593": "government",
    "20000621": "government policy",
    "20000638": "international relations",
    "20000646": "non-governmental organisation",
    "20000647": "political crisis",
    "20000648": "political dissent",
    "20000649": "political process",
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
    "20000710": "biomedical science",
    "20000715": "mathematics",
    "20000717": "natural science",
    "20000741": "scientific institution",
    "20000735": "scientific research",
    "20000755": "scientific standards",
    "20000742": "social sciences",
    "20000756": "technology and engineering",
    "20000768": "communities",
    "20000770": "demographics",
    "20000775": "discrimination",
    "20000772": "emigration",
    "20000780": "family",
    "20000771": "immigration",
    "20000788": "mankind",
    "20000799": "social condition",
    "20000802": "social problem",
    "20000808": "values",
    "20000817": "welfare",
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
    "20001128": "weather forecast",
    "20001129": "weather phenomena",
    "20001130": "weather statistic",
    "20001131": "weather warning",
    "20000479": "healthcare policy",
    "20000003": "animation",
    "20000004": "cartoon",
    "20000005": "cinema",
    "20000007": "dance",
    "20000011": "fashion",
    "20000013": "literature",
    "20000018": "music",
    "20000028": "opera",
    "20000029": "theatre",
    "20000031": "visual arts",
    "20000039": "cultural development",
    "20000040": "customs and tradition",
    "20000041": "festive event (culture)",
    "20000042": "language",
    "20000043": "library and museum",
    "20000044": "monument and heritage site",
    "20000046": "news media",
    "20000047": "newspaper",
    "20000048": "online media outlet",
    "20000049": "periodical",
    "20000050": "radio",
    "20000051": "television",
    "20000054": "act of bioterrorism",
    "20000055": "bombings",
    "20000057": "guerrilla activity",
    "20000058": "international military intervention",
    "20000060": "military occupation",
    "20000061": "missing in action",
    "20000062": "war",
    "20000066": "demonstration",
    "20000067": "rebellion",
    "20000068": "revolution",
    "20000069": "riot",
    "20000072": "genocide",
    "20000074": "peace envoy",
    "20000075": "peace plan",
    "20000076": "peace talks",
    "20000078": "disarmament",
    "20000079": "ordnance clearance",
    "20000083": "arson",
    "20000084": "assault",
    "20000086": "cyber crime",
    "20000087": "corporate crime",
    "20000093": "corruption",
    "20000095": "drug related crimes",
    "20000097": "fraud",
    "20000098": "hijacking",
    "20000099": "homicide",
    "20000100": "kidnapping",
    "20000101": "organised crime",
    "20000103": "terrorism",
    "20000104": "robbery and theft",
    "20000105": "war crime",
    "20000107": "court",
    "20000116": "out of court procedures",
    "20000118": "prosecution and prosecutors",
    "20000120": "civil rights",
    "20000122": "civil law",
    "20000125": "criminal law",
    "20000126": "international law",
    "20000130": "arrest",
    "20000131": "investigation (criminal)",
    "20000133": "police",
    "20000140": "explosion accident and incident",
    "20000141": "industrial accident and incident",
    "20000143": "transportation accident and incident",
    "20000149": "famine",
    "20000150": "fire",
    "20000151": "natural disaster",
    "20000161": "structural failure",
    "20000162": "transport incident",
    "20000171": "business finance",
    "20000188": "human resources",
    "20000192": "strategy and marketing",
    "20000210": "agriculture",
    "20000217": "chemicals",
    "20000223": "pharmaceutical",
    "20000225": "computing and information technology",
    "20000235": "construction and property",
    "20000243": "consumer goods",
    "20000252": "retail",
    "20000256": "energy and resource",
    "20000271": "financial and business service",
    "20000294": "manufacturing and engineering",
    "20000304": "media",
    "20000316": "metal and mineral",
    "20000322": "process industry",
    "20000331": "tourism and leisure industry",
    "20000337": "transport",
    "20000339": "commuting",
    "20000345": "economic policy",
    "20000346": "macro economics",
    "20000386": "commodity market",
    "20000390": "debt market",
    "20000391": "foreign exchange market",
    "20000392": "loan market",
    "20000394": "securities",
    "20000396": "stocks",
    "20000401": "primary education",
    "20000402": "further education",
    "20000403": "adult and continuing education",
    "20000404": "upper secondary education",
    "20000405": "college and university",
    "20000408": "lower secondary education",
    "20000409": "early childhood education",
    "20000419": "global warming",
    "20000421": "energy saving",
    "20000422": "parks",
    "20000423": "environmental policy",
    "20000425": "air pollution",
    "20000426": "environmental clean-up",
    "20000427": "hazardous materials",
    "20000428": "waste materials",
    "20000429": "water pollution",
    "20000431": "energy resources",
    "20000432": "land resources",
    "20000435": "population growth",
    "20000436": "renewable energy",
    "20000437": "water",
    "20000442": "ecosystem",
    "20000443": "endangered species",
    "20000444": "invasive species",
    "20000447": "cancer",
    "20000448": "communicable disease",
    "20000454": "heart disease",
    "20000455": "illness",
    "20000456": "injury",
    "20000457": "medical condition",
    "20000458": "mental health and disorder",
    "20000462": "hospital",
    "20000465": "diet",
    "20000467": "non-prescription drug",
    "20000468": "prescription drug",
    "20000469": "medical test",
    "20000470": "health care approach",
    "20000475": "physical fitness",
    "20000476": "preventative medicine",
    "20000477": "vaccine",
    "20000478": "therapy",
    "20000479": "healthcare policy",
    "20000481": "Medicaid",
    "20000482": "Medicare",
    "20000486": "medical service",
    "20000487": "medical specialisation",
    "20000492": "medical staff",
    "20000500": "animal",
    "20000506": "royalty",
    "20000507": "flowers and plants",
    "20000510": "apprenticeship",
    "20000511": "child labour",
    "20000512": "employee",
    "20000513": "employer",
    "20000514": "employment training",
    "20000517": "occupations",
    "20000518": "wages and benefits",
    "20000522": "workplace health and safety",
    "20000525": "collective agreements",
    "20000529": "labour dispute",
    "20000532": "pension",
    "20000534": "job layoffs",
    "20000535": "unemployment benefits",
    "20000539": "club and association",
    "20000540": "game",
    "20000549": "gaming and lottery",
    "20000550": "hobby",
    "20000551": "holiday",
    "20000553": "leisure venue",
    "20000560": "outdoor recreational activities",
    "20000563": "travel and tourism",
    "20000569": "organic food",
    "20000570": "house and home",
    "20000572": "trend",
    "20000575": "citizens' initiative and recall",
    "20000576": "electoral system",
    "20000577": "intergovernmental elections",
    "20000578": "local elections",
    "20000579": "national elections",
    "20000580": "political campaigns",
    "20000582": "political candidates",
    "20000583": "primary elections",
    "20000584": "referenda",
    "20000585": "regional elections",
    "20000586": "voting",
    "20000588": "censorship and freedom of speech",
    "20000590": "freedom of religion",
    "20000591": "freedom of the press",
    "20000592": "human rights",
    "20000594": "civil and public service",
    "20000597": "constitution (law)",
    "20000598": "defence",
    "20000605": "espionage and intelligence",
    "20000606": "executive (government)",
    "20000607": "government budget",
    "20000609": "government department",
    "20000610": "heads of state",
    "20000611": "impeachment",
    "20000612": "local government and authority",
    "20000613": "minister and secretary (government)",
    "20000614": "national government",
    "20000615": "legislative body",
    "20000618": "regional government and authority",
    "20000619": "safety of citizens",
    "20000620": "taxation",
    "20000626": "interior policy",
    "20000634": "migration policy",
    "20000635": "nuclear policy",
    "20000636": "regulation of industry",
    "20000639": "diplomacy",
    "20000642": "economic sanction",
    "20000643": "foreign aid",
    "20000644": "international organisation",
    "20000645": "refugees and internally displaced people",
    "20000650": "lobbying",
    "20000651": "political parties and movements",
    "20000652": "political development",
    "20000653": "political system",
    "20000658": "Buddhism",
    "20000659": "Christianity",
    "20000673": "Confucianism",
    "20000674": "cult",
    "20000675": "Freemasonry",
    "20000676": "Hinduism",
    "20000677": "Islam",
    "20000678": "Jainism",
    "20000679": "Judaism",
    "20000680": "nature religion",
    "20000681": "Zoroastrianism",
    "20000682": "Scientology",
    "20000683": "Shintoism",
    "20000684": "Sikhism",
    "20000685": "Taoism",
    "20000686": "Unificationism",
    "20000691": "Christmas",
    "20000692": "Easter",
    "20000693": "Pentecost",
    "20000694": "Ramadan",
    "20000695": "Yom Kippur",
    "20000698": "church",
    "20000699": "mosque",
    "20000700": "synagogue",
    "20000701": "temple",
    "20000704": "pope",
    "20000706": "Bible",
    "20000707": "Qur'an",
    "20000708": "Torah",
    "20000711": "biotechnology",
    "20000712": "dentistry",
    "20000714": "veterinary medicine",
    "20000716": "mechanical engineering",
    "20000718": "astronomy",
    "20000719": "biology",
    "20000725": "chemistry",
    "20000726": "cosmology",
    "20000727": "geology",
    "20000728": "horticulture",
    "20000729": "marine science",
    "20000730": "meteorology",
    "20000731": "physics",
    "20000736": "scientific innovation",
    "20000737": "medical research",
    "20000738": "scientific exploration",
    "20000740": "scientific publication",
    "20000743": "anthropology",
    "20000744": "archaeology",
    "20000745": "economics",
    "20000746": "geography",
    "20000747": "history",
    "20000748": "information science",
    "20000749": "study of law",
    "20000750": "linguistics",
    "20000751": "philosophy",
    "20000752": "political science",
    "20000753": "psychology",
    "20000754": "sociology",
    "20000757": "aerospace engineering",
    "20000759": "agricultural technology",
    "20000760": "civil engineering",
    "20000761": "electronic engineering",
    "20000762": "identification technology",
    "20000763": "information technology and computer science",
    "20000764": "materials science",
    "20000765": "micro science",
    "20000769": "social networking",
    "20000773": "illegal immigration",
    "20000774": "population and census",
    "20000776": "ageism",
    "20000777": "racism",
    "20000778": "religious discrimination",
    "20000779": "sexism",
    "20000781": "adoption",
    "20000782": "Dating and Relationships",
    "20000783": "divorce",
    "20000784": "family planning",
    "20000786": "marriage",
    "20000787": "parenting",
    "20000789": "adults",
    "20000790": "children",
    "20000791": "disabilities",
    "20000792": "LGBTQ",
    "20000793": "gender",
    "20000794": "infants",
    "20000795": "national or ethnic minority",
    "20000796": "nuclear radiation victims",
    "20000797": "senior citizens",
    "20000798": "teenagers",
    "20000800": "homelessness",
    "20000801": "poverty",
    "20000803": "abusive behaviour",
    "20000804": "addiction",
    "20000805": "juvenile delinquency",
    "20000806": "prostitution",
    "20000807": "slavery",
    "20000809": "corrupt practices",
    "20000810": "death and dying",
    "20000814": "ethics",
    "20000815": "pornography",
    "20000816": "sexual behaviour",
    "20000818": "charity",
    "20000819": "long-term care",
    "20000820": "social services",
    "20000823": "American football",
    "20000824": "archery",
    "20000827": "athletics",
    "20000846": "Australian rules football",
    "20000847": "badminton",
    "20000848": "bandy",
    "20000849": "baseball",
    "20000851": "basketball",
    "20000852": "biathlon",
    "20000853": "billiards",
    "20000854": "bobsleigh",
    "20000855": "boules",
    "20000856": "boxing",
    "20000875": "bullfighting",
    "20000876": "Canadian football",
    "20000877": "canoeing",
    "20000883": "casting (fishing)",
    "20000884": "mountain climbing",
    "20000887": "sport climbing",
    "20000888": "cricket",
    "20000889": "croquet",
    "20000890": "curling",
    "20000892": "cycling",
    "20000911": "competitive dancing",
    "20000912": "darts",
    "20000913": "diving",
    "20000918": "underwater sports",
    "20000919": "dog racing",
    "20000922": "duathlon",
    "20000923": "equestrian",
    "20000929": "fencing",
    "20000933": "field hockey",
    "20000934": "figure skating",
    "20000936": "fist ball",
    "20000937": "floorball",
    "20000938": "flying disc",
    "20000939": "Gaelic football",
    "20000940": "golf",
    "20000942": "gymnastics",
    "20000958": "handball (team)",
    "20000959": "hornuss",
    "20000960": "horse racing",
    "20000964": "hurling",
    "20000965": "ice hockey",
    "20000967": "inline skating",
    "20000968": "Jai Alai (Pelota)",
    "20000978": "kabaddi",
    "20000979": "kayaking",
    "20000986": "lacrosse",
    "20000987": "luge",
    "20000988": "marathon",
    "20000989": "modern pentathlon",
    "20000990": "motorboat racing",
    "20000991": "motor car racing",
    "20000998": "motorcycling",
    "20001010": "netball",
    "20001011": "orienteering",
    "20001013": "parachuting",
    "20001014": "polo",
    "20001015": "pool",
    "20001016": "power boating",
    "20001017": "rodeo",
    "20001026": "rowing",
    "20001035": "rugby league",
    "20001036": "rugby union",
    "20001038": "sailing",
    "20001047": "sepak takraw",
    "20001048": "shinty",
    "20001049": "sport shooting",
    "20001055": "skeleton",
    "20001056": "skiing",
    "20001062": "sky diving",
    "20001063": "snooker",
    "20001064": "snowboarding",
    "20001065": "soccer",
    "20001066": "softball",
    "20001067": "speed skating",
    "20001068": "squash",
    "20001069": "sumo wrestling",
    "20001070": "surfing",
    "20001071": "swimming",
    "20001083": "table tennis",
    "20001085": "tennis",
    "20001086": "ten pin bowling",
    "20001087": "triathlon",
    "20001088": "tug-of-war",
    "20001089": "volleyball",
    "20001091": "water polo",
    "20001092": "water skiing",
    "20001093": "weightlifting and powerlifting",
    "20001097": "windsurfing",
    "20001098": "wrestling",
    "20001105": "drug abuse in sport",
    "20001106": "drug testing in sport",
    "20001107": "medical drug use in sport",
    "20001109": "continental championship",
    "20001110": "continental cup",
    "20001111": "continental games",
    "20001112": "international championship",
    "20001113": "international cup",
    "20001114": "international games",
    "20001115": "national championship",
    "20001116": "national cup",
    "20001117": "national games",
    "20001118": "regional championship",
    "20001119": "regional cup",
    "20001120": "regional games",
    "20001121": "world championship",
    "20001122": "world cup",
    "20001123": "world games",
    "20001132": "cultural policies",
    "20001135": "art exhibition",
    "20001143": "party",
    "20001147": "sports policies",
    "20001151": "short track speed skating",
    "20001154": "chess",
    "20001155": "roller sports",
    "20001157": "martial arts",
    "20001160": "crafts industry",
    "20001170": "logistics",
    "20001171": "sharing economy",
    "20001173": "regulatory authority",
    "20001175": "artistic swimming",
    "20001176": "rugby",
    "20001177": "Olympic Games",
    "20001178": "Paralympic Games",
    "20001179": "series",
    "20001181": "festival",
    "20001182": "social media",
    "20001183": "eSports",
    "20001193": "sexual misconduct",
    "20001196": "reckless driving",
    "20001197": "administrative law",
    "20001206": "self-employment",
    "20001212": "religious school",
    "20001213": "state school",
    "20001214": "private school",
    "20001215": "independent school",
    "20001219": "drug rehabilitation",
    "20001221": "emergency care",
    "20001228": "surgery",
    "20001229": "healthcare clinic",
    "20001230": "environmental, social and governance policy (ESG)",
    "20001232": "elderly care",
    "20001233": "name ceremony",
    "20001234": "graduation",
    "20001235": "funeral and memorial service",
    "20001236": "wedding",
    "20001239": "exercise and fitness",
    "20001240": "bodybuilding",
    "20001244": "utilities",
    "20001259": "political convention",
    "20001260": "political committees",
    "20001261": "heads of government",
    "20001262": "public inquiry",
    "20001263": "church elections",
    "20001265": "local government policy",
    "20001266": "political debates",
    "20001271": "All Saints Day",
    "20001272": "Walpurgis night",
    "20001273": "baptism",
    "20001275": "gig economy",
    "20001276": "parental leave",
    "20001277": "volunteering",
    "20001281": "racquetball",
    "20001282": "ringette",
    "20001283": "human smuggling and trafficking",
    "20001284": "bullying",
    "20001285": "vandalism",
    "20001286": "arm wrestling",
    "20001288": "indigenous people",
    "20001290": "public housing",
    "20001299": "surveillance",
    "20001300": "privacy",
    "20001302": "sports record",
    "20001303": "sports medal and trophy",
    "20001304": "sports honour",
    "20001305": "padel",
    "20001306": "kiting",
    "20001307": "stand up paddleboarding (SUP)",
    "20001309": "cheerleading",
    "20001313": "shootings",
    "20001314": "animal abuse",
    "20001316": "border disputes",
    "20001317": "child care",
    "20001319": "disinformation and misinformation",
    "20001320": "torture",
    "20001321": "drowning",
    "20001322": "poisoning",
    "20001326": "women's rights",
    "20001327": "women",
    "20001328": "men",
    "20001329": "3x3 basketball",
    "20001330": "canoe slalom",
    "20001331": "canoe sprint",
    "20001332": "bmx freesytle",
    "20001333": "road cycling",
    "20001334": "track cycling",
    "20001335": "football 5-a-side",
    "20001336": "goalball",
    "20001338": "education policy",
    "20001340": "mental wellbeing",
    "20001341": "regular competition",
    "20001342": "playoff championship",
    "20001343": "final game",
    "20001345": "bar and bat mitzvah",
    "20001346": "canonisation",
    "20001349": "atheism and agnosticism",
    "20001350": "Eid al-Adha",
    "20001352": "Hanukkah",
    "20001354": "healthcare industry",
    "20001355": "developmental disorder",
    "20001359": "pregnancy and childbirth",
    "20001360": "fraternal and community group",
}

TOPIC_TO_ID = {value: key for key, value in ID_TO_TOPIC.items()}

AVAILABLE_MODELS = {
    TOPIC_TO_ID[topic]: topic for topic in CLASS_DICT if topic in TOPIC_TO_ID
}

DROP_LIST = [
    "government health care",
    "health insurance",
    "economic policy",
    "environmental politics",
    "opera",
    "food and drink",
]

CONVERSION_DICT = {
    "censorship": "censorship and freedom of speech",
    "parliament": "legislative body",
    "regulatory of industry": "regulation of industry",
    "migration of people": "migration policy",
    "IT/computer sciences": "information technology and computer science",
    "electronics": "electronic engineering",
    "pharmacology": "pharmaceutical",
    "veterinarian science": "veterinary medicine",
    "health treatment": "health treatment and procedure",
    "mental and behavioural disorder": "mental health and disorder",
    "travel": "travel and tourism",
    "punishment (criminal)": "investigation (criminal)",
    "religious facilities": "religious facility",
    "theft": "robbery and theft",
    "ministers (government)": "minister and secretary (government)",
    "computer crime": "cyber crime",
    "religious belief": "belief systems",
    "justice and rights": "justice",
    "recreational activities": "outdoor recreational activities",
    "prosecution": "prosecution and prosecutors",
    "tourism and leisure": "tourism and leisure industry",
    "medicine": "preventative medicine",
    "athletics, track and field": "athletics",
    "transport accident and incident": "transportation accident and incident",
    "natural disasters": "natural disaster",
    "medical procedure/test": "medical test",
    "medical drugs": "prescription drug",
    "food and drink": "food and drink enthusiasm",
    "weightlifting": "weightlifting and powerlifting",
    "equestrianism": "equestrian",
    "cult and sect": "cult",
    "parent and child": "parenting",
    "gays and lesbians": "LGBTQ",
}
