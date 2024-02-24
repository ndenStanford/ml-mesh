"""class_dict for iptc."""

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
    "education": {
        0: "school",
        1: "religious education",
        2: "teaching and learning",
    },
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
        3: "employment legislation",
        4: "labour relations",
        5: "unions",
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

CLASS_DICT = {**CLASS_DICT_FIRST, **CLASS_DICT_SECOND}


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
    "20000461": "health facility",
    "20000483": "health insurance",
    "20000463": "health organisation",
    "20000464": "health treatment and procedure",
    "20000485": "medical profession",
    "20000493": "non-human diseases",
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
}
