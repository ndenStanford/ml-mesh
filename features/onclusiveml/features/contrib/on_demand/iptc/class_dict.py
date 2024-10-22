# flake8: noqa: E501
"""IPTC label to topic dictionary."""

CANDIDATE_DICT_FIRST = {
    "root": {
        "0": {
            "name": "arts, culture, entertainment and media",
            "description": "All forms of arts, entertainment, cultural heritage and media",
        },
        "1": {
            "name": "conflict, war and peace",
            "description": "Acts of socially or politically motivated protest or violence, military activities, geopolitical conflicts, as well as resolution efforts",
        },
        "2": {
            "name": "crime, law and justice",
            "description": "The establishment and/or statement of the rules of behaviour in society, the enforcement of these rules, breaches of the rules, the punishment of offenders and the organisations and bodies involved in these activities",
        },
        "3": {
            "name": "disaster, accident and emergency incident",
            "description": "Man made or natural event resulting in loss of life or injury to living creatures and/or damage to inanimate objects or property",
        },
        "4": {
            "name": "economy, business and finance",
            "description": "All matters concerning the planning, production and exchange of wealth.",
        },
        "5": {
            "name": "education",
            "description": "All aspects of furthering knowledge, formally or informally",
        },
        "6": {
            "name": "environment",
            "description": "All aspects of protection, damage, and condition of the ecosystem of the planet earth and its surroundings.",
        },
        "7": {
            "name": "health",
            "description": "All aspects of physical and mental well-being",
        },
        "8": {
            "name": "labour",
            "description": "Social aspects, organisations, rules and conditions affecting the employment of human effort for the generation of wealth or provision of services and the economic support of the unemployed.",
        },
        "9": {
            "name": "lifestyle and leisure",
            "description": "Activities undertaken for pleasure, relaxation or recreation outside paid employment, including eating and travel.",
        },
        "10": {
            "name": "politics",
            "description": "Local, regional, national and international exercise of power, or struggle for power, and the relationships between governing bodies and states.",
        },
        "11": {
            "name": "religion",
            "description": "Belief systems, institutions and people who provide moral guidance to followers",
        },
        "12": {
            "name": "science and technology",
            "description": "All aspects pertaining to human understanding of, as well as methodical study and research of natural, formal and social sciences, such as astronomy, linguistics or economics",
        },
        "13": {
            "name": "society",
            "description": "The concerns, issues, affairs and institutions relevant to human social interactions, problems and welfare, such as poverty, human rights and family planning",
        },
        "14": {
            "name": "sport",
            "description": "Competitive activity or skill that involves physical and/or mental effort and organisations and bodies involved in these activities",
        },
        "15": {
            "name": "weather",
            "description": "The study, prediction and reporting of meteorological phenomena",
        },
        "16": {"name": "none", "description": "none"},
    }
}

# Updated class_dic.py
CANDIDATE_DICT_SECOND = {
    "arts, culture, entertainment and media": {
        "0": {
            "name": "arts and entertainment",
            "description": "All forms of arts and entertainment",
        },
        "1": {
            "name": "culture",
            "description": "The ideas, customs, arts, traditions of a particular group of persons",
        },
        "2": {"name": "mass media", "description": "Media addressing a large audience"},
        "3": {"name": "none", "description": "none"},
    },
    "conflict, war and peace": {
        "0": {
            "name": "act of terror",
            "description": "Act of violence, often resulting in casualties, designed to raise fear and anxiety in a population",
        },
        "1": {
            "name": "armed conflict",
            "description": "Disputes between opposing groups involving the use of weapons, but not necessarily formally declared wars",
        },
        "2": {
            "name": "civil unrest",
            "description": "Rallies, strikes, demonstrations, riots or other disturbances by a population, often in protest to a government or other organization's policies or actions",
        },
        "3": {
            "name": "coup d'etat",
            "description": "The overthrow of an established government by an organised military or political group",
        },
        "4": {
            "name": "cyber warfare",
            "description": "Cyber attacks, or suspected attacks, involving a government entity as either the sponsor or the target, or preventive measures against these types of actions",
        },
        "5": {
            "name": "massacre",
            "description": "The mass killing of people, usually civilians, during wartime hostilities",
        },
        "6": {
            "name": "peace process",
            "description": "Organized actions to end a war or conflict, usually involving peace negotiations and agreements",
        },
        "7": {
            "name": "post-war reconstruction",
            "description": "Actions to rebuild a society, economy or political system in an area affected by war",
        },
        "8": {
            "name": "war victims",
            "description": "Individuals who are injured or killed in a war or armed conflict, including civilians",
        },
        "9": {"name": "none", "description": "none"},
    },
    "crime, law and justice": {
        "0": {
            "name": "crime",
            "description": "Violations of laws by individuals, companies or organisations",
        },
        "1": {"name": "judiciary", "description": "The system of courts of law"},
        "2": {"name": "law", "description": "The codification of rules of behaviour"},
        "3": {
            "name": "law enforcement",
            "description": "Agencies that attempt to prevent disobedience to established laws or bring to justice those who disobey those laws",
        },
        "4": {"name": "none", "description": "none"},
    },
    "disaster, accident and emergency incident": {
        "0": {
            "name": "accident and emergency incident",
            "description": "A sudden, unexpected event that causes unwanted consequences or requires immediate action",
        },
        "1": {
            "name": "disaster",
            "description": "A sudden, unplanned event that causes great damage or loss of life, such as an accident or a natural catastrophe",
        },
        "2": {
            "name": "emergency response",
            "description": "The planning and efforts made by people and organizations to help victims of a sudden, unplanned event, natural disaster or crisis",
        },
        "3": {"name": "none", "description": "none"},
    },
    "economy, business and finance": {
        "0": {
            "name": "business enterprise",
            "description": "Organisations set up to create and sell a product or service",
        },
        "1": {
            "name": "business information",
            "description": "Information about individual business entities, including companies, corporations, charities",
        },
        "2": {
            "name": "economy",
            "description": "Production, consumption, distribution and trade activities affecting regions or countries as a whole",
        },
        "3": {
            "name": "market and exchange",
            "description": "Market for buying and selling stocks, currencies, commodities and other goods",
        },
        "4": {
            "name": "products and services",
            "description": "Products and services consumed by companies and individuals and the companies that manufacture or manage them",
        },
        "5": {"name": "none", "description": "none"},
    },
    "education": {
        "0": {
            "name": "curriculum",
            "description": "The courses offered by a learning institution and the regulation of those courses",
        },
        "1": {
            "name": "educational grading",
            "description": "The evaluation of a student's achievement on a test, assignment or course and the policies and methods around assigning those grades",
        },
        "2": {
            "name": "educational testing and examinations",
            "description": "Polices and standards around the testing and assessment of students, including the merits of standardised testing, and testing methods",
        },
        "3": {
            "name": "entrance examination",
            "description": "Exams for entering colleges, universities and all other higher and lower education institutions",
        },
        "4": {
            "name": "online and remote learning",
            "description": "Learning where a student and teacher are not physically present in the same location. Instruction can occur synchronously or asynchronously and utilizes technology such as video conferencing, online assessments and video conferencing.",
        },
        "5": {
            "name": "parents group",
            "description": "Group of parents set up to support educational activities of their children",
        },
        "6": {
            "name": "religious education",
            "description": "Instruction by any faith about that faith's principles and beliefs, including Sunday school or preparation for a religious rite, such as a bar mitzvah",
        },
        "7": {
            "name": "school",
            "description": "A building or institution in which education is provided",
        },
        "8": {
            "name": "social learning",
            "description": "The learning of social skills and behaviours through the imitation and observation of others. This can include formal and informal instruction around empathy, emotions and mental health.",
        },
        "9": {
            "name": "students",
            "description": "Students as a demographic, including student protests and requests for change and trends among students",
        },
        "10": {
            "name": "teachers",
            "description": "Teachers as a demographic, including teacher unions, teacher education and training and the criteria for teachers in various locations",
        },
        "11": {
            "name": "vocational education",
            "description": "Education that provides students with practical experience and training in a particular occupational field. It is sometimes referred to as career education or technical education",
        },
        "12": {"name": "none", "description": "none"},
    },
    "environment": {
        "0": {
            "name": "climate change",
            "description": "Significant change in measures of climate (such as temperature, precipitation, or wind) lasting for an extended period",
        },
        "1": {
            "name": "conservation",
            "description": "Preservation of wilderness areas, flora and fauna, including species extinction",
        },
        "2": {
            "name": "environmental pollution",
            "description": "Corruption of air, water, land etc. by harmful substances",
        },
        "3": {
            "name": "natural resources",
            "description": "Environmental issues related to the exploitation of natural resources",
        },
        "4": {"name": "nature", "description": "The natural world in its entirety"},
        "5": {
            "name": "sustainability",
            "description": "Actions by businesses, governments and individuals to counter major environmental problems, including climate change, loss of biodiversity, loss of ecosystem services, land degradation and air and water pollution",
        },
        "6": {"name": "none", "description": "none"},
    },
    "health": {
        "0": {
            "name": "disease and condition",
            "description": "Any health conditions affecting humans",
        },
        "1": {
            "name": "government health care",
            "description": "Health care provided by governments at any level",
        },
        "2": {
            "name": "health facility",
            "description": "Facilities used for any kind of health care",
        },
        "3": {
            "name": "health insurance",
            "description": "Insurance covering medical costs",
        },
        "4": {
            "name": "health organisation",
            "description": "Specific health organisations, including professional associations, non-profit and international groups",
        },
        "5": {
            "name": "health treatment and procedure",
            "description": "Remedies, therapies, interventions, medications, testing and treatments to prevent, diagnose, manage or improve a health condition",
        },
        "6": {
            "name": "medical profession",
            "description": "Profession requiring formal training in the study, diagnosis, treatment, care and prevention of disease, medical condition or injury",
        },
        "7": {
            "name": "private health care",
            "description": "Health care provided by private organisations",
        },
        "8": {
            "name": "public health",
            "description": "Organised public or private measures designed to prevent disease, promote health and prolong life among the population as a whole",
        },
        "9": {"name": "none", "description": "none"},
    },
    "labour": {
        "0": {
            "name": "employment",
            "description": "The state of having work, usually paid, for a company, organisation, or individual",
        },
        "1": {
            "name": "employment legislation",
            "description": "Laws governing employment",
        },
        "2": {
            "name": "labour market",
            "description": "The supply and demand of labour in an economy",
        },
        "3": {
            "name": "labour relations",
            "description": "The relationship between workers and employers",
        },
        "4": {"name": "retirement", "description": "The years after work"},
        "5": {
            "name": "unemployment",
            "description": "The state of being available to work but not having a job",
        },
        "6": {
            "name": "unions",
            "description": "Groups established to represent bodies of workers in order to obtain better workplace conditions through collective bargaining",
        },
        "7": {"name": "none", "description": "none"},
    },
    "lifestyle and leisure": {
        "0": {
            "name": "leisure",
            "description": "Activities carried out in ones' spare time and not in a competitive way.",
        },
        "1": {
            "name": "lifestyle",
            "description": "The way in which a person lives, including their style and possessions",
        },
        "2": {
            "name": "wellness",
            "description": "The active pursuit of good mental and physical health",
        },
        "3": {"name": "none", "description": "none"},
    },
    "politics": {
        "0": {
            "name": "election",
            "description": "The selection of representatives by the casting of votes",
        },
        "1": {
            "name": "fundamental rights",
            "description": "The political, social and economic rights to which all creatures are entitled, usually upheld by law.",
        },
        "2": {"name": "government", "description": "The system for ruling a country"},
        "3": {
            "name": "government policy",
            "description": "An overall plan or course of action set out by a government intended to influence and guide decisions and actions towards a desired outcome.",
        },
        "4": {
            "name": "international relations",
            "description": "Non-violent relations between nations through negotiation, treaty, or personal meetings",
        },
        "5": {
            "name": "non-governmental organisation",
            "description": "Groups officially outside of government that lobby, demonstrate or campaign on a wide range of issues such as economics, environment healthcare etc.",
        },
        "6": {
            "name": "political crisis",
            "description": "Conflict that rises to a level where, depending on events, governments can fall etc",
        },
        "7": {
            "name": "political dissent",
            "description": "Disagreement between political groups, usually organised and sometimes resulting in imprisonment of the dissenters",
        },
        "8": {
            "name": "political process",
            "description": "The art or science of participating in the affairs of government, a state of political party",
        },
        "9": {"name": "none", "description": "none"},
    },
    "religion": {
        "0": {
            "name": "belief systems",
            "description": "A set of beliefs prescribed by an institution or text often focusing on the worship of a higher power and the outlining of moral guidelines",
        },
        "1": {
            "name": "relations between religion and government",
            "description": "Matters arising from the relationship between religions and a government, including the question of whether churches should pay taxes, the push to keep religion out of publicly funded institutions and the freedom, or lack of to wear religious symbols in a school setting",
        },
        "2": {
            "name": "religious conflict",
            "description": "Conflicts involving religious differences",
        },
        "3": {
            "name": "religious facility",
            "description": "Any facility where a group carries out its religious rites",
        },
        "4": {
            "name": "religious festival and holiday",
            "description": "Holy day or period of observance in a religion which is sometimes a public holiday",
        },
        "5": {
            "name": "religious leader",
            "description": "Person or persons who have a ritual, juridical or otherwise leading role in their respective church or religion",
        },
        "6": {
            "name": "religious ritual",
            "description": "Established religious rituals such as mass, baptism, prayer meetings and bar and bat mitzvah",
        },
        "7": {
            "name": "religious text",
            "description": "Texts regarded as holy or important by a religion",
        },
        "8": {"name": "none", "description": "none"},
    },
    "science and technology": {
        "0": {
            "name": "biomedical science",
            "description": "The application of biology-based science to medical fields such as research, health monitoring or medical treatment",
        },
        "1": {
            "name": "mathematics",
            "description": "The study of structure, space, change and number in abstract, often using symbolic logic and language, and including subjects such as geometry, algebra or trigonometry",
        },
        "2": {
            "name": "natural science",
            "description": "The sciences that deal with matter, energy and the physical world, including physics, biology, chemistry and astronomy",
        },
        "3": {
            "name": "scientific institution",
            "description": "Institution that carries out or governs scientific work, such as the National Academy of Arts and Sciences",
        },
        "4": {
            "name": "scientific research",
            "description": "The scientific and methodical investigation of events, procedures and interactions to explain why they occur, or to find solutions for problems",
        },
        "5": {
            "name": "scientific standards",
            "description": "Nationally or internationally established rules governing scientific and technological study and development, such as calibration standards for scientific tools or equipment",
        },
        "6": {
            "name": "social sciences",
            "description": "The study of human society in such aspects as linguistics, anthropology, economics or sociology",
        },
        "7": {
            "name": "technology and engineering",
            "description": "The study and practice of industrial or applied sciences such as physics, hydrodynamics or thermodynamics",
        },
        "8": {"name": "none", "description": "none"},
    },
    "society": {
        "0": {
            "name": "communities",
            "description": "A group of individuals actively sharing a common value or interest",
        },
        "1": {
            "name": "demographics",
            "description": "The study of human populations and their characteristics, for example statistics or trends around aging populations in a particular geographic region",
        },
        "2": {
            "name": "discrimination",
            "description": "Unfair treatment of, or policies or practices against, individuals or groups of people on the basis of real or perceived membership in a group, such as race, sexual orientation, political or religious beliefs, age or height",
        },
        "3": {
            "name": "diversity, equity and inclusion",
            "description": "Efforts that seeks to promote the fair treatment and full participation of groups of people who have historically been underrepresented or subject to discrimination on the basis of identity or disability",
        },
        "4": {
            "name": "emigration",
            "description": "Leaving one's country of residence to settle permanently elsewhere",
        },
        "5": {
            "name": "family",
            "description": "A group of people related genetically or by a legal bond, or who consider themselves part of a familial unit regardless of genetic or legal status",
        },
        "6": {
            "name": "immigration",
            "description": "The movement of individuals or groups of people from one country to another",
        },
        "7": {
            "name": "mankind",
            "description": "Human beings taken as a whole, or described as members of particular groups such as teenagers, women, or people with disabilities",
        },
        "8": {
            "name": "social condition",
            "description": "The circumstances or state of affairs affecting a person's life, welfare and relations with others in a society",
        },
        "9": {
            "name": "social problem",
            "description": "Issues related to human rights, human welfare and other areas of societal concern",
        },
        "10": {
            "name": "values",
            "description": "A person's or group's principles or standards of behaviour, which guide their way of living and choices made",
        },
        "11": {
            "name": "welfare",
            "description": "Help for those in need of food, housing, health and other services",
        },
        "12": {"name": "none", "description": "none"},
    },
    "sport": {
        "0": {
            "name": "competition discipline",
            "description": "Different types of sport which can be executed in competitions",
        },
        "1": {
            "name": "disciplinary action in sport",
            "description": "Actions, including fines and suspensions levied by sports organisations and teams",
        },
        "2": {
            "name": "drug use in sport",
            "description": "Drug use associated with sport activities, including doping, abuse, testing and permitted medical uses",
        },
        "3": {
            "name": "sport achievement",
            "description": "Records or honours earned by athletes for their performance",
        },
        "4": {
            "name": "sport event",
            "description": "An event featuring one or more sport competitions",
        },
        "5": {
            "name": "sport industry",
            "description": "Commercial issues related to sport",
        },
        "6": {
            "name": "sport organisation",
            "description": "Organisations or associations that govern sports",
        },
        "7": {
            "name": "sport venue",
            "description": "Gymnasiums, stadiums, arenas or facilities where sports events take place",
        },
        "8": {
            "name": "sports coaching",
            "description": "The staff responsible for the training and on-field management of a sports team",
        },
        "9": {
            "name": "sports management and ownership",
            "description": "The executive leadership and owners of a sports team",
        },
        "10": {
            "name": "sports officiating",
            "description": "Referees, umpires and other staff who enforce the rules of a sport from on the field of play",
        },
        "11": {
            "name": "sports transaction",
            "description": "The transfer of an athlete from one team to another, the hiring or drafting of an athlete onto a team or the change in professional status of a player on a team",
        },
        "12": {"name": "none", "description": "none"},
    },
    "weather": {
        "0": {
            "name": "weather forecast",
            "description": "The long- or short-term meteorological prediction and reporting of the upcoming weather for a given region",
        },
        "1": {
            "name": "weather phenomena",
            "description": "Short- or long-term meteorological phenomena worthy of study, reporting or public advisory such as climate change, storms, heat waves or tornadoes",
        },
        "2": {
            "name": "weather statistic",
            "description": "Numerical facts about the weather such as temperature, barometric pressure, river levels, humidity or high and low tides",
        },
        "3": {
            "name": "weather warning",
            "description": "Alerts issued to the public about severe or notable weather in their area",
        },
        "4": {"name": "none", "description": "none"},
    },
}

CANDIDATE_DICT_THIRD = {
    "arts and entertainment": {
        "0": {
            "name": "animation",
            "description": "Stories told through animated drawings in either full-length or short format",
        },
        "1": {
            "name": "cartoon",
            "description": "Drawings, such as editorial cartoons and comic strips, often using humour or satire",
        },
        "2": {
            "name": "cinema",
            "description": "Stories told through motion pictures, such as full-length or short format documentary or fictional features",
        },
        "3": {
            "name": "dance",
            "description": "A form of performing art consisting of purposefully selected sequences of human movement",
        },
        "4": {
            "name": "fashion",
            "description": "Styles and trends in clothing, footwear, accessories, including the design, presentation and wearing of these styles and trends",
        },
        "5": {
            "name": "festival",
            "description": "Events showcasing artistic endeavours, often regularly occurring, such as dance, music, theatre, poetry or comedy festivals",
        },
        "6": {
            "name": "literature",
            "description": "The telling of a story through written language",
        },
        "7": {
            "name": "music",
            "description": "A form of performing art using instruments or voice to create different sounds, tones and harmonies",
        },
        "8": {
            "name": "series",
            "description": "A connected set of fictional or non-fictional program episodes that run under the same title.",
        },
        "9": {
            "name": "theatre",
            "description": "A form of performing art where live performers portray a narrative to an audience through dialogue and action",
        },
        "10": {
            "name": "visual arts",
            "description": "A form of art which appeals primarily to the visual senses, such as ceramics, drawing, painting, sculpture, printmaking, design, crafts, photography, video, filmmaking, and architecture.",
        },
        "11": {"name": "none", "description": "none"},
    },
    "culture": {
        "0": {
            "name": "art exhibition",
            "description": "Temporary presentation of art in museums, art halls or galleries",
        },
        "1": {
            "name": "cultural development",
            "description": "The history of the development of art and culture such as the rise of cave paintings, linguistic variations over time, the evolution of values",
        },
        "2": {
            "name": "customs and tradition",
            "description": "A particular way of behaving, or observances that have developed over time by a group of people",
        },
        "3": {
            "name": "festive event (culture)",
            "description": "An event ordinarily celebrated by a community and centring on some characteristic aspect of that community and its religion or traditions",
        },
        "4": {
            "name": "language",
            "description": "The method of human communication, either spoken or written, consisting of words that are used in a structured and conventional way",
        },
        "5": {
            "name": "library and museum",
            "description": "Institutions that house collections of books, music, art, or objects from the past and present optionally for public use and display",
        },
        "6": {
            "name": "monument and heritage site",
            "description": "Commemorations of historical people, events, or the areas containing them, in the form of structures such as sculptures, statues or buildings",
        },
        "7": {"name": "none", "description": "none"},
    },
    "mass media": {
        "0": {
            "name": "disinformation and misinformation",
            "description": "The spread of false information regardless of intent",
        },
        "1": {
            "name": "news media",
            "description": "The presentation of news to the public through different platforms, such as TV, radio, newspapers, magazines, web pages and blogs",
        },
        "2": {
            "name": "newspaper",
            "description": "Daily or weekly publication that presents the news, locally, regionally or globally, as well as features, opinion columns, comics and other content",
        },
        "3": {
            "name": "online media outlet",
            "description": "Publication distributing content, such as articles, blogs, photos, video and music, only over the internet",
        },
        "4": {
            "name": "periodical",
            "description": "Publication that is usually published weekly, bi-weekly, monthly or annually, such as magazines, journals or newsletters",
        },
        "5": {
            "name": "radio",
            "description": "Audio content, such as news, entertainment or information, distributed via broadcast or internet",
        },
        "6": {
            "name": "social media",
            "description": "Content created to be shared within online social networks",
        },
        "7": {
            "name": "television",
            "description": "Video content, such as news, entertainment or information, distributed via broadcast or internet",
        },
        "8": {"name": "none", "description": "none"},
    },
    "act of terror": {
        "0": {
            "name": "act of bioterrorism",
            "description": "Attacks using biological agents intended to raise the level of fear within a population",
        },
        "1": {
            "name": "terrorist bombings",
            "description": "Intentional use of explosive devices on people, buildings or other structures",
        },
        "2": {"name": "none", "description": "none"},
    },
    "armed conflict": {
        "0": {
            "name": "guerrilla activity",
            "description": "Anti-government or wartime actions by clandestine or non-state combatant groups, often using tactics such as ambush, sabotage, raids and kidnapping",
        },
        "1": {
            "name": "international military intervention",
            "description": "The temporary use of international forces in a country or region that requires outside help with resolving a crisis",
        },
        "2": {
            "name": "military occupation",
            "description": "The temporary forceful taking over of a country or region by invading military forces",
        },
        "3": {
            "name": "war",
            "description": "Armed hostilities by one group or geopolitical entity against another",
        },
        "4": {"name": "none", "description": "none"},
    },
    "civil unrest": {
        "0": {
            "name": "demonstration",
            "description": "A non-violent public show of support for or opposition to a cause, idea or policy, in the form of a mass meeting or march",
        },
        "1": {
            "name": "rebellion",
            "description": "Organized actions of opposition to a government or ruling party by a country's residents, often violent and with the aim of overthrowing the government",
        },
        "2": {
            "name": "revolution",
            "description": "A forcible and often violent change to, or overthrow of, a country's political system or social order by internal forces, in favour of a new system",
        },
        "3": {
            "name": "riot",
            "description": "Violent, destructive events of civil disorder by groups of people, usually in response to a grievance or as acts of opposition, often involving injury to individuals and destruction of property",
        },
        "4": {"name": "none", "description": "none"},
    },
    "peace process": {
        "0": {
            "name": "disarmament",
            "description": "The abolishment or reduction of a country's military weapons cache",
        },
        "1": {
            "name": "peace envoy",
            "description": "Person or organisation initiating and carrying out a peace process",
        },
        "2": {
            "name": "peace plan",
            "description": "A strategy for achieving peace in a warring nation or area of conflict",
        },
        "3": {
            "name": "peace talks",
            "description": "Discussions between countries, world regions or geopolitical entities in conflict or at war, often with a mediator, with the goal of arriving at a solution for peace",
        },
        "4": {
            "name": "peacekeeping force",
            "description": "The military forces of a nation, or of several nations working together, whose mission is to maintain peace in areas of conflict",
        },
        "5": {"name": "none", "description": "none"},
    },
    "post-war reconstruction": {
        "0": {
            "name": "ordnance clearance",
            "description": "The removal or neutralisation of ordnance such as landmines or cluster bombs that may remain after a war or armed conflict on public ground",
        },
        "1": {"name": "none", "description": "none"},
    },
    "war victims": {
        "0": {
            "name": "missing in action",
            "description": "Civilians or military personnel who have gone missing during or after hostilities, conflicts or war",
        },
        "1": {
            "name": "prisoners of war",
            "description": "Individuals captured, imprisoned or detained by enemy factions during military conflicts or war",
        },
        "2": {"name": "none", "description": "none"},
    },
    "crime": {
        "0": {
            "name": "animal abuse",
            "description": "The infliction of cruelty or neglect onto animals by humans",
        },
        "1": {
            "name": "arson",
            "description": "The intentional setting of fires with criminal intent",
        },
        "2": {
            "name": "assault",
            "description": "Physical crime against a person, including battery, brawls and threat of bodily harm",
        },
        "3": {
            "name": "corporate crime",
            "description": "Crimes committed by a corporation or by individuals acting on behalf of a corporation",
        },
        "4": {
            "name": "corruption",
            "description": "Dishonest actions by a person in power in return for pecuniary or personal gain",
        },
        "5": {
            "name": "cyber crime",
            "description": "Criminal activities carried out by means of computers or the internet, such as hacking, phishing scams and identity theft",
        },
        "6": {
            "name": "drug related crimes",
            "description": "Illegal activities involving illicit substances, including buying, distribution, selling and smuggling",
        },
        "7": {
            "name": "fraud",
            "description": "Intentional deception for personal or financial gain",
        },
        "8": {
            "name": "genocide",
            "description": "The systematic killing of one clan, tribe, or religious or ethnic group by another",
        },
        "9": {
            "name": "hijacking",
            "description": "Taking over a transportation vehicle by force",
        },
        "10": {
            "name": "homicide",
            "description": "The killing of one person by another, including murder and manslaughter",
        },
        "11": {
            "name": "human smuggling and trafficking",
            "description": "The illegal transporting of people from one country or area to another. When the result is forced labour or sexual exploitation, the crime is considered trafficking.",
        },
        "12": {
            "name": "kidnapping",
            "description": "To seize and detain a person against that person's will by unlawful threat, force or fraud",
        },
        "13": {
            "name": "organised crime",
            "description": "Crimes committed by gangs or criminal organizations, such as the mafia",
        },
        "14": {
            "name": "reckless driving",
            "description": "Serious traffic violations that are likely to, or have led to, the endangerment, injury or death of a person or persons, or the endangerment of or significant property damage",
        },
        "15": {
            "name": "robbery and theft",
            "description": "The taking of another person's property without their consent, sometimes by force",
        },
        "16": {
            "name": "shootings",
            "description": "An act of violence committed by individuals with the use of armed weapons",
        },
        "17": {
            "name": "terrorism",
            "description": "Violence against people to create fear in order to achieve political or ideological objectives",
        },
        "18": {
            "name": "torture",
            "description": "Intentionally inflicting severe physical or psychological pain in order to punish the victim or get the victim to take an action or give information",
        },
        "19": {
            "name": "vandalism",
            "description": "Deliberately damaging or destroying public or private property",
        },
        "20": {
            "name": "war crime",
            "description": "Crimes committed during a war or armed conflict, usually against civilians or prisoners of war, including the prosecution of such crimes",
        },
        "21": {"name": "none", "description": "none"},
    },
    "judiciary": {
        "0": {
            "name": "court",
            "description": "Place where legal cases are heard and decided",
        },
        "1": {
            "name": "out of court procedures",
            "description": "Legal issues which are settled outside of court",
        },
        "2": {
            "name": "prosecution and prosecutors",
            "description": "The process of holding a trial against a person who is accused of a crime to determine guilt and the lawyers and legal team who argue that the accused is guilty",
        },
        "3": {"name": "none", "description": "none"},
    },
    "law": {
        "0": {
            "name": "administrative law",
            "description": "Body of law that governs the actions of governmental administrative agencies",
        },
        "1": {
            "name": "civil law",
            "description": "The system of law focused on private rights and disputes between individuals in such areas as contracts, torts, property, and family law",
        },
        "2": {
            "name": "criminal law",
            "description": "The system of law concerned with the punishment of those who commit crimes",
        },
        "3": {
            "name": "international law",
            "description": "The system of laws embraced by all nations, such as the Geneva Convention and the International Law of the Seas",
        },
        "4": {"name": "none", "description": "none"},
    },
    "law enforcement": {
        "0": {"name": "arrest", "description": "The detention of a suspect of a crime"},
        "1": {
            "name": "investigation (criminal)",
            "description": "Inquiry into an alleged crime, including searching, interviews, interrogations and evidence collection",
        },
        "2": {
            "name": "police",
            "description": "Civil force of a national, regional or local government that is responsible for the prevention and detection of crime and the maintenance of public order",
        },
        "3": {
            "name": "surveillance",
            "description": "Monitoring the activities of the individual through the use of cameras and data in order to prevent or uncover criminal activities",
        },
        "4": {"name": "none", "description": "none"},
    },
    "accident and emergency incident": {
        "0": {
            "name": "drowning",
            "description": "When a person's airpipe and lungs become filled with water causing death or injury, most often caused by falling into or bathing in rivers, lakes or the ocean",
        },
        "1": {
            "name": "explosion accident and incident",
            "description": "Explosions caused by an accidental, non-combat, or non-terrorism source. Also use when the source of the explosion is non-specified or unknown",
        },
        "2": {
            "name": "industrial accident and incident",
            "description": "Any unplanned event or mishap in an industrial setting that result in injuries to people and damage to property or the environment",
        },
        "3": {
            "name": "structural failure",
            "description": "The unexpected collapse of a building, bridge or other structure",
        },
        "4": {
            "name": "transportation accident and incident",
            "description": "An accident or incident involving one or more vehicles",
        },
        "5": {"name": "none", "description": "none"},
    },
    "disaster": {
        "0": {
            "name": "famine",
            "description": "Severe lack of food for a large population",
        },
        "1": {
            "name": "fire",
            "description": "Fires started by an accidental or unknown source. For wildfires, use wildfire. For fires started with a criminal intent, use arson.",
        },
        "2": {
            "name": "natural disaster",
            "description": "Destructive incidents caused by nature, such as earthquakes and floods",
        },
        "3": {"name": "none", "description": "none"},
    },
    "emergency incident": {"0": {"name": "none", "description": "none"}},
    "business enterprise": {
        "0": {
            "name": "cooperative",
            "description": "An organisation which is owned and run jointly by its members, who share the profits or benefits of their work",
        },
        "1": {
            "name": "small and medium enterprise",
            "description": "A small and medium enterprise (SME) is a company whose number of employees, balance and turnover cannot exceed certain limits set by the country where it is located",
        },
        "2": {
            "name": "start-up and entrepreneurial business",
            "description": "The process of designing, launching and running a new business",
        },
        "3": {"name": "none", "description": "none"},
    },
    "business information": {
        "0": {
            "name": "business financing",
            "description": "The financing, capital structuring, and investment decisions of a business",
        },
        "1": {
            "name": "business governance",
            "description": "The rules, practices, and processes used to oversee and manage a company",
        },
        "2": {
            "name": "business reporting and performance",
            "description": "Measuring and reporting on the performance of a business",
        },
        "3": {
            "name": "business restructuring",
            "description": "Changes to the structure of a business or organisation",
        },
        "4": {
            "name": "business strategy and marketing",
            "description": "Planning the direction of a company and selling its products and services to achieve the strategy",
        },
        "5": {
            "name": "human resources",
            "description": "People working for a business and how they are managed",
        },
        "6": {"name": "none", "description": "none"},
    },
    "economy": {
        "0": {
            "name": "central bank",
            "description": "A country's major bank that sets interest rates and provides transfer of funds between commercial banks",
        },
        "1": {
            "name": "currency",
            "description": "The system of money used by a country, including the value of one currency as measured against another",
        },
        "2": {
            "name": "economic organisation",
            "description": "Business, industrial and trade associations, societies and other private-sector groups",
        },
        "3": {
            "name": "economic trends and indicators",
            "description": "The behaviour and performance of the economy as a whole",
        },
        "4": {
            "name": "emerging market",
            "description": "Economies of developing nations that are growing and becoming more engaged with global markets",
        },
        "5": {
            "name": "international economic institution",
            "description": "Global institutions working in the domain of international economic cooperation and stability, such as the International Monetary Fund, UNIDO, World Bank and World Trade Organization",
        },
        "6": {
            "name": "international trade",
            "description": "Trade of goods and services between nations",
        },
        "7": {
            "name": "monetary policy",
            "description": "Government bank directed policy on the amount of money in circulation and the rate at which it can be loaned",
        },
        "8": {
            "name": "mutual funds",
            "description": "Pools of shares or bonds for sale often grouped by investment intention, such as growth, income or security",
        },
        "9": {
            "name": "sharing economy",
            "description": "Peer-to-peer-based sharing of access to goods and services",
        },
        "10": {"name": "none", "description": "none"},
    },
    "market and exchange": {
        "0": {
            "name": "commodities market",
            "description": "The market for goods such as cotton, oil, coal and metals",
        },
        "1": {
            "name": "debt market",
            "description": "Market for debt instruments such as bonds, certificates of deposit, banker's acceptances and Treasury bills",
        },
        "2": {
            "name": "foreign exchange market",
            "description": "The market for international currency",
        },
        "3": {
            "name": "loan market",
            "description": "The market where financial organisations provide loans to borrowers and sell them on to investors",
        },
        "4": {"name": "none", "description": "none"},
    },
    "products and services": {
        "0": {
            "name": "agriculture",
            "description": "The growing and raising of plants and animals for consumption and the processing, cleaning, packing or storage of these products",
        },
        "1": {
            "name": "business service",
            "description": "Services provided to business operations and for individuals, such as consulting, legal representation and job placement",
        },
        "2": {
            "name": "chemicals",
            "description": "Natural or manmade materials used to produce other materials",
        },
        "3": {
            "name": "commercial fishing",
            "description": "Fish farming and commercial activity around the catching of fish and seafood for consumption",
        },
        "4": {
            "name": "computing and information technology",
            "description": "Computers and the transmission of information",
        },
        "5": {
            "name": "construction and property",
            "description": "All items pertaining to the construction and sale of property",
        },
        "6": {
            "name": "consumer goods",
            "description": "Items produced for and sold to individuals",
        },
        "7": {
            "name": "energy and resource",
            "description": "The use of natural resources to generate energy",
        },
        "8": {
            "name": "financial service",
            "description": "Professional services involving the investment, lending or management of money and other assets",
        },
        "9": {
            "name": "forestry and timber",
            "description": "The production, collection and preparation of wood products",
        },
        "10": {
            "name": "healthcare industry",
            "description": "Goods and services to treat patients through curative, preventive, rehabilitative and palliative care",
        },
        "11": {
            "name": "manufacturing and engineering",
            "description": "Manufacturers of electrical, electronic and mechanical equipment but does not cover civil engineering.",
        },
        "12": {
            "name": "media and entertainment industry",
            "description": "The various means of disseminating news, information and entertainment to the public",
        },
        "13": {
            "name": "metal and mineral mining and refining",
            "description": "The extractive businesses that remove raw materials, including coal, gold iron and copper, from the earth by drilling and pumping, quarrying or mining",
        },
        "14": {
            "name": "plastic",
            "description": "The production of plastics and issues around plastic consumption, including bans, recycling, using less plastics and plastic alternatives",
        },
        "15": {
            "name": "sales channel",
            "description": "Indirect or direct ways of bringing products or services to market so that they can be purchased by consumers",
        },
        "16": {
            "name": "tourism and leisure industry",
            "description": "Commercial organisations and operations dealing with travel and the pursuit of recreational activities",
        },
        "17": {
            "name": "transport",
            "description": "The means of getting people or goods from one place to another",
        },
        "18": {
            "name": "utilities",
            "description": "The providing of basic services to the public, such as supplying water, waste removal, heating and cooling",
        },
        "19": {"name": "none", "description": "none"},
    },
    "school": {
        "0": {
            "name": "adult and continuing education",
            "description": "Education for adults who have left the formal education system that offers new forms of knowledge or skills, including professional certificates and online courses provided by companies such as Codeacademy or Udemy",
        },
        "1": {
            "name": "college and university",
            "description": "Institutions of higher learning that provide degrees in a course of study at the undergraduate, postgraduate or doctorate level",
        },
        "2": {
            "name": "early childhood education",
            "description": "Education for children under the national compulsory education age",
        },
        "3": {
            "name": "independent school",
            "description": "Schools funded by money from taxes via government, but run by companies, organisations or cooperatives",
        },
        "4": {
            "name": "lower secondary education",
            "description": "Education and schools that build on primary education with a more subject-oriented curriculum. Schools may be called middle schools or junior highs in the United States.",
        },
        "5": {
            "name": "primary education",
            "description": "Education and schools designed to provide students with fundamental skills in reading, writing and mathematics and to establish a solid foundation for later learning",
        },
        "6": {
            "name": "private school",
            "description": "Schools maintained by private funds and organisations",
        },
        "7": {
            "name": "religious school",
            "description": "School that has a religious component in its operations or its curriculum",
        },
        "8": {
            "name": "state school",
            "description": "Schools maintained by public funds, usually government-imposed taxes",
        },
        "9": {
            "name": "upper secondary education",
            "description": "Education and schools preparing students for tertiary education or providing skills relevant to employment through a curriculum with an increased range of subject options and streams",
        },
        "10": {"name": "none", "description": "none"},
    },
    "climate change": {
        "0": {
            "name": "global warming",
            "description": "This category includes all issues relating to global warming including temperature research, remote sensing on temperature trends, debate on global warming, ways to reduce emissions and carbon trading.",
        },
        "1": {"name": "none", "description": "none"},
    },
    "conservation": {
        "0": {
            "name": "energy saving",
            "description": "Conservation of electrical, and other power sources",
        },
        "1": {"name": "parks", "description": "Areas set aside for preservation"},
        "2": {"name": "none", "description": "none"},
    },
    "environmental pollution": {
        "0": {
            "name": "air pollution",
            "description": "Solid or gaseous matter affecting the quality of air that we breathe",
        },
        "1": {
            "name": "environmental clean-up",
            "description": "Processes whereby contaminated areas are cleaned of hazardous materials so they can be inhabited again by either people or animals.",
        },
        "2": {
            "name": "hazardous materials",
            "description": "Materials that are harmful to humans or animals if they are exposed to them. Includes radiation, poison gases, chemicals, heavy metals, PCBs, and certain plant products",
        },
        "3": {
            "name": "waste materials",
            "description": "The environmental impact of waste, including recycling efforts",
        },
        "4": {
            "name": "water pollution",
            "description": "Solids or liquids that corrupt the quality of water that could be used for drinking or irrigation",
        },
        "5": {"name": "none", "description": "none"},
    },
    "natural resources": {
        "0": {
            "name": "renewable energy",
            "description": "Energy derived from sustainable sources",
        },
        "1": {
            "name": "energy resources",
            "description": "Such resources as coal, gas, wind, sunlight etc., used to generate heat, electricity and power",
        },
        "2": {
            "name": "land resources",
            "description": "That portion of a nation or state that is above water and available for development either for profit or for the general good of the public",
        },
        "3": {
            "name": "population growth",
            "description": "People and their growth and development within a natural setting",
        },
        "4": {
            "name": "water",
            "description": "Environmental issues about bodies of water, including oceans, lakes, streams and reservoirs, as well as ice, glaciers and forms of precipitation",
        },
        "5": {"name": "none", "description": "none"},
    },
    "nature": {
        "0": {
            "name": "animal",
            "description": "Human interest and cultural stories related to animals, including pets",
        },
        "1": {
            "name": "ecosystem",
            "description": "A system of plants, animals and bacteria interrelated in its physical/chemical environment",
        },
        "2": {
            "name": "endangered species",
            "description": "Those species in danger of disappearing, largely because of changes in environment, hunting, or weather",
        },
        "3": {
            "name": "flowers and plants",
            "description": "Human interest and cultural stories related to plants, flowers and trees",
        },
        "4": {
            "name": "invasive species",
            "description": "Non-native plants, animals and other organisms that tend to take over native species",
        },
        "5": {"name": "none", "description": "none"},
    },
    "disease and condition": {
        "0": {
            "name": "cancer",
            "description": "A serious and often fatal disease caused when normal cells mutate into tumours",
        },
        "1": {
            "name": "communicable disease",
            "description": "Diseases that can be transmitted from one person or animal to another",
        },
        "2": {
            "name": "developmental disorder",
            "description": "Conditions due to an impairment in learning, language or behaviour areas, such as autism, Aspergers and dyslexia",
        },
        "3": {
            "name": "heart disease",
            "description": "Diseases and conditions affecting the heart such as heart attacks, the narrowing of arteries, arrhythmia or cardiomyopathy",
        },
        "4": {
            "name": "injury",
            "description": "Harm caused to the human body by external forces such as falls, weapons or accidents",
        },
        "5": {
            "name": "medical condition",
            "description": "An abnormal condition that affects the structure and functioning of the body, such as chronic pain, high blood pressure or osteoporosis",
        },
        "6": {
            "name": "mental health and disorder",
            "description": "The psychological well-being of an individual and the diseases and disorders that affect mood, thinking and behaviour as well as actions taken to bring improvement and awareness to these conditions",
        },
        "7": {
            "name": "poisoning",
            "description": "When a substance in sufficient quantity adversely affects the body and its functions",
        },
        "8": {"name": "none", "description": "none"},
    },
    "government health care": {"0": {"name": "none", "description": "none"}},
    "health facility": {
        "0": {
            "name": "healthcare clinic",
            "description": "Local medical facility or doctor's office associated with a general medicine practice, staffed by one or many doctors, focusing on outpatient treatment or giving recommendations to visit a specialist or hospital",
        },
        "1": {
            "name": "hospital",
            "description": "Medical facilities for the treatment of illnesses and injury",
        },
        "2": {"name": "none", "description": "none"},
    },
    "health treatment and procedure": {
        "0": {
            "name": "diet",
            "description": "Ways of eating to benefit health or treat a condition, such as plant-based, low-salt, high-fibre or gluten-free",
        },
        "1": {
            "name": "drug rehabilitation",
            "description": "Medical or psychotherapeutic treatment for dependency on substances such as alcohol, prescription and controlled drugs",
        },
        "2": {
            "name": "emergency care",
            "description": "Immediate care of patients with critical medical emergencies, either inside or outside of a hospital",
        },
        "3": {
            "name": "health care approach",
            "description": "Different approaches to medical care that vary in the methods and substances used to treat symptoms",
        },
        "4": {
            "name": "medical test",
            "description": "Diagnostic procedure, such as stress test, blood test, CAT scan or MRI",
        },
        "5": {
            "name": "non-prescription drug",
            "description": "Chemical substances used in the treatment or prevention of physical or mental condition or disease",
        },
        "6": {
            "name": "prescription drug",
            "description": "Drugs that can be obtained only with a doctor's authorisation",
        },
        "7": {
            "name": "surgery",
            "description": "The use of incisions made by medical instruments to investigate or treat a medical condition or injury",
        },
        "8": {
            "name": "therapy",
            "description": "Treatment of physical, mental or medical conditions by non-surgical means",
        },
        "9": {
            "name": "vaccine",
            "description": "Medications designed to create immunity to diseases",
        },
        "10": {"name": "none", "description": "none"},
    },
    "medical profession": {
        "0": {
            "name": "medical service",
            "description": "Medical support for doctors, including blood tests and other medical tests on individuals, X-rays, CAT scans, MRIs, etc",
        },
        "1": {
            "name": "medical specialisation",
            "description": "The different medical specialist areas",
        },
        "2": {
            "name": "medical staff",
            "description": "Doctors, nurses, interns and others in a medical facility",
        },
        "3": {"name": "none", "description": "none"},
    },
    "employment": {
        "0": {
            "name": "apprenticeship",
            "description": "A period of work used to learn a skill or trade",
        },
        "1": {"name": "child labour", "description": "The employment of children"},
        "2": {
            "name": "commuting",
            "description": "The process of getting to and from work, including transport options, travel networks, car pooling.",
        },
        "3": {
            "name": "employee",
            "description": "Those who are paid or otherwise compensated for providing services to employers",
        },
        "4": {
            "name": "employer",
            "description": "People and organisations that pay employees to provide services",
        },
        "5": {
            "name": "employment training",
            "description": "Learning new skills as part of an existing job, such as developing specialisations, learning new techniques or retraining when an employee's skills are no longer relevant",
        },
        "6": {
            "name": "parental leave",
            "description": "Time off work to give birth or care for a child",
        },
        "7": {
            "name": "self-employment",
            "description": "A situation in which an individual works for themselves as a freelancer or business owner instead of working for an employer that pays a salary or a wage",
        },
        "8": {
            "name": "volunteering",
            "description": "Unpaid work undertaken freely by individuals as a service to others",
        },
        "9": {
            "name": "wages and benefits",
            "description": "Money, or other items of value such as pension contributions and health insurance, paid to employees as compensation for their work",
        },
        "10": {"name": "none", "description": "none"},
    },
    "employment legislation": {
        "0": {
            "name": "workplace health and safety",
            "description": "Laws protecting a safe and healthy work environment",
        },
        "1": {"name": "none", "description": "none"},
    },
    "labour market": {
        "0": {
            "name": "gig economy",
            "description": "a labour market consisting of individual suppliers on short-term contracts or freelance work as opposed to permanent jobs, such as drivers or delivery workers",
        },
        "1": {"name": "none", "description": "none"},
    },
    "labour relations": {
        "0": {
            "name": "collective agreements",
            "description": "Negotiated guidelines for relationships between groups of employees and employers, including issues such as working hours, wages, health care, pensions and other benefits",
        },
        "1": {
            "name": "labour dispute",
            "description": "Disagreements between employers and employees regarding work conditions, pay or other issues",
        },
        "2": {"name": "none", "description": "none"},
    },
    "retirement": {
        "0": {
            "name": "pension",
            "description": "Payments, either government or private, to retired people",
        },
        "1": {"name": "none", "description": "none"},
    },
    "unemployment": {
        "0": {
            "name": "unemployment benefits",
            "description": "Monetary compensation paid to the jobless",
        },
        "1": {"name": "none", "description": "none"},
    },
    "leisure": {
        "0": {
            "name": "club and association",
            "description": "Organisations joined by individuals because of similar interests",
        },
        "1": {"name": "game", "description": "Contests generally for one's amusement"},
        "2": {
            "name": "gaming and lottery",
            "description": "Gambling, often involving selection of sets of numbers one expects to come up",
        },
        "3": {"name": "hobby", "description": "Recreational pursuit"},
        "4": {
            "name": "holiday",
            "description": "Time spent not at work for rest and relaxation",
        },
        "5": {
            "name": "leisure venue",
            "description": "A place where people go to be entertained or amused. For sporting events, use sport venue.",
        },
        "6": {
            "name": "outdoor recreational activities",
            "description": "Leisure activities engaged in the outdoors, most commonly in natural settings",
        },
        "7": {
            "name": "travel and tourism",
            "description": "Spending time away from home in pursuit of recreation, relaxation or pleasure",
        },
        "8": {"name": "none", "description": "none"},
    },
    "lifestyle": {
        "0": {
            "name": "house and home",
            "description": "Interest in maintaining and decorating one's home",
        },
        "1": {
            "name": "organic food",
            "description": "Food which is grown using no artificial fertilisers or chemical compounds",
        },
        "2": {
            "name": "party",
            "description": "A social gathering of invited guests, often involving eating, drinking, dancing or the playing of games",
        },
        "3": {
            "name": "trend",
            "description": "Interest in what is considered hip or popular at a certain point in time",
        },
        "4": {"name": "none", "description": "none"},
    },
    "wellness": {
        "0": {
            "name": "exercise and fitness",
            "description": "Physical activity with the purpose to maintain and improve health and wellness, gain stamina or for enjoyment",
        },
        "1": {
            "name": "mental wellbeing",
            "description": "The personal pursuit of mental health through activities such as meditation, stress reduction, technology detoxes and journalling",
        },
        "2": {"name": "none", "description": "none"},
    },
    "election": {
        "0": {
            "name": "church elections",
            "description": "Elections to choose leaders to run church organisations at various levels",
        },
        "1": {
            "name": "citizens' initiative and recall",
            "description": "Political suggestions by non-government officials for corrective action, or for changes in existing rules and regulations",
        },
        "2": {"name": "electoral system", "description": "Voting systems"},
        "3": {
            "name": "intergovernmental elections",
            "description": "Choosing individuals for the government of an international organization, such as the United Nations, European Union, NATO and World Bank",
        },
        "4": {
            "name": "local elections",
            "description": "Choosing individuals for government at the basic level, whether city, village or county",
        },
        "5": {
            "name": "national elections",
            "description": "Choosing individuals for government at a national level",
        },
        "6": {
            "name": "political campaigns",
            "description": "Campaigns for public office",
        },
        "7": {
            "name": "political candidates",
            "description": "Individuals who are chosen to stand for office",
        },
        "8": {
            "name": "political debates",
            "description": "Organised debates between political candidates, live in front of an audience or broadcast in some manner",
        },
        "9": {
            "name": "primary elections",
            "description": "Preliminary elections on a local or regional basis leading up to a regional or national election",
        },
        "10": {
            "name": "referenda",
            "description": "Political proposals, laws and actions suggested by non-government officials to be voted on by the entire voting body",
        },
        "11": {
            "name": "regional elections",
            "description": "Choosing individuals for government at a regional level",
        },
        "12": {
            "name": "voting",
            "description": "The act of selecting an individual you would like to represent your interests in government",
        },
        "13": {"name": "none", "description": "none"},
    },
    "fundamental rights": {
        "0": {
            "name": "censorship and freedom of speech",
            "description": "Attempts by any group to control freedoms of speech, religion, and ideas distributed in print, graphics, cyberspace and other ways. Does not include official standards such as cinema ratings, advertising and broadcast standards.",
        },
        "1": {
            "name": "civil rights",
            "description": "Rights of individuals under civil law",
        },
        "2": {
            "name": "freedom of religion",
            "description": "Religious rights and freedoms, pressure and intimidation of believers, censorship in mass media, activities of government bodies, journalistic associations and/or organisations and other NGOs in regard to freedom of belief and practice",
        },
        "3": {
            "name": "freedom of the press",
            "description": "Mass media rights and freedoms, pressure and intimidation of the journalists, censorship in mass media, activities of government bodies, journalistic associations and/or organisations and other NGOs in regards to press freedom",
        },
        "4": {
            "name": "human rights",
            "description": "Rights entitled to be enjoyed by all citizens universally",
        },
        "5": {
            "name": "privacy",
            "description": "The right of an individual or group to keep information about themselves private",
        },
        "6": {
            "name": "women's rights",
            "description": "Feminism, restrictions on the rights of women and the fight for equality with men",
        },
        "7": {"name": "none", "description": "none"},
    },
    "government": {
        "0": {
            "name": "civil and public service",
            "description": "The paid service by civilians for the government, and the often non-paid service of individuals for the benefit of others (public service)",
        },
        "1": {
            "name": "constitution (law)",
            "description": "Usually a written document setting forth the operations of a government and the rights of the citizens therein",
        },
        "2": {
            "name": "defence",
            "description": "Anything involving the protection of one's own country",
        },
        "3": {
            "name": "espionage and intelligence",
            "description": "Covert collection of information",
        },
        "4": {
            "name": "executive (government)",
            "description": "That portion of a ruling body involving the overall operation of government",
        },
        "5": {
            "name": "government budget",
            "description": "The expenses and revenues approved by the legislature.",
        },
        "6": {
            "name": "government department",
            "description": "Divisions of a government that concentrate on specific areas such as health, welfare, economy or war",
        },
        "7": {
            "name": "heads of government",
            "description": "The highest official in the executive branch of a sovereign state, a federated state, or a self-governing colony",
        },
        "8": {
            "name": "heads of state",
            "description": "Symbolic or actual chief representative of a nation, such as royalty, or president or emir, for example",
        },
        "9": {
            "name": "impeachment",
            "description": "The process of bringing a public official before a tribunal to answer charges of wrongdoing",
        },
        "10": {
            "name": "legislative body",
            "description": "A legislature of elected officials representing the people that has the authority to make laws",
        },
        "11": {
            "name": "local government and authority",
            "description": "Authorities at borough, city or county level",
        },
        "12": {
            "name": "minister and secretary (government)",
            "description": "Senior government official, either elected or appointed, who heads a government department",
        },
        "13": {
            "name": "national government",
            "description": "The ruling body of a nation",
        },
        "14": {
            "name": "political committees",
            "description": "A legislative sub-group that focuses on a specific area or action",
        },
        "15": {
            "name": "political convention",
            "description": "Meeting of political party to nominate a candidate, choose a party leader or set policy",
        },
        "16": {
            "name": "public inquiry",
            "description": "An official review of events or actions ordered by a government body, including royal commissions",
        },
        "17": {
            "name": "regional government and authority",
            "description": "Authorities at a level above the local and below the national one. Could be named a state, province, department etc.",
        },
        "18": {
            "name": "regulatory authority",
            "description": "Authority responsible for the regulation or supervision of a business sector.",
        },
        "19": {"name": "none", "description": "none"},
    },
    "government policy": {
        "0": {
            "name": "cultural policies",
            "description": "Government policies affecting cultural affairs",
        },
        "1": {
            "name": "economic policy",
            "description": "Government directed policy on production, taxes, tariffs and things that affect the direction and health of the economy",
        },
        "2": {
            "name": "education policy",
            "description": "Government programmes and policies related to education and proposals to change or protests against those positions",
        },
        "3": {
            "name": "environmental policy",
            "description": "Government programs and policies related to the environment and proposals to change or protests against those positions",
        },
        "4": {
            "name": "healthcare policy",
            "description": "Health-related policy decisions including what different countries are doing regarding prescription drug policies, psychiatric care, health care funding, pandemic response and related topics",
        },
        "5": {
            "name": "interior policy",
            "description": "Government policies affecting internal affairs",
        },
        "6": {
            "name": "local government policy",
            "description": "Policies for the development and maintenance of a local government area",
        },
        "7": {
            "name": "migration policy",
            "description": "Movement of one body of persons from one place to another",
        },
        "8": {
            "name": "nuclear policy",
            "description": "Government policies as regards to use of nuclear fuels for power production or weapons",
        },
        "9": {
            "name": "regulation of industry",
            "description": "The rules and bodies, both national and international, that govern conflict of interest and good practice regulations.",
        },
        "10": {
            "name": "safety of citizens",
            "description": "Government policies to protect the well-being of its citizens",
        },
        "11": {
            "name": "sports policies",
            "description": "Government policies affecting sports",
        },
        "12": {
            "name": "taxation",
            "description": "A levy to fund government expenditure",
        },
        "13": {"name": "none", "description": "none"},
    },
    "international relations": {
        "0": {
            "name": "border disputes",
            "description": "Diplomatic issues between two countries surrounding the border, sometimes involving military conflict",
        },
        "1": {
            "name": "diplomacy",
            "description": "The use of verbal and written skills for persuading others to your point of view",
        },
        "2": {
            "name": "economic sanction",
            "description": "Punitive actions taken by one country against another including trade restrictions, embargoes etc.",
        },
        "3": {
            "name": "foreign aid",
            "description": "Help provided by one nation to another",
        },
        "4": {
            "name": "international organisation",
            "description": "Includes organisations with members and functions that cross international borders, and may include intergovernmental organisations of sovereign nations.",
        },
        "5": {
            "name": "refugees and internally displaced people",
            "description": "A person seeking shelter in another country because of some fear of persecution in his own country",
        },
        "6": {"name": "none", "description": "none"},
    },
    "political process": {
        "0": {
            "name": "lobbying",
            "description": "The attempt by non-government bodies and individuals to affect the outcome of legislation through verbal, or other, persuasion",
        },
        "1": {
            "name": "political development",
            "description": "The creation and rise of political systems and the history of the people and nations that are associated with those systems.",
        },
        "2": {
            "name": "political parties and movements",
            "description": "Covers both formally recognised and informal political associations",
        },
        "3": {
            "name": "political system",
            "description": "System designed to provide order to government",
        },
        "4": {"name": "none", "description": "none"},
    },
    "belief systems": {
        "0": {
            "name": "Buddhism",
            "description": "An Asian religion founded in the 6th century BC in India based on the teachings of the Buddha with the goal of overcoming suffering and transcending desire and the individual self to achieve nirvana",
        },
        "1": {
            "name": "Christianity",
            "description": "Religions that follow the teachings of Jesus Christ and the Bible",
        },
        "2": {
            "name": "Confucianism",
            "description": "A system of thought and behaviour originating in ancient China and based on the teachings of the philosopher Confucius",
        },
        "3": {
            "name": "Hinduism",
            "description": "A religion and social system originating in India that includes a caste system, a belief in reincarnation and the worship of multiple deities",
        },
        "4": {
            "name": "Islam",
            "description": "Monotheistic religion that considers Muhammad as a prophet and the Qur'an as holy scripture",
        },
        "5": {
            "name": "Jainism",
            "description": "A religion beginning in the 7th-5th century BC in India that teaches a path to spiritual purity and enlightenment through a disciplined mode of life founded upon the tradition of ahimsa, nonviolence to all living creatures",
        },
        "6": {
            "name": "Judaism",
            "description": "A monotheistic religion and culture that follows the teachings of the Torah",
        },
        "7": {
            "name": "Scientology",
            "description": "A set of beliefs and practices invented by American science fiction author L. Ron Hubbard asserting that a human is an immortal, spiritual being (Thetan) that is resident in a physical body",
        },
        "8": {
            "name": "Shintoism",
            "description": "An indigenous Japanese polytheistic religion that revolves around kami, supernatural entities believed to inhabit all things",
        },
        "9": {
            "name": "Sikhism",
            "description": "An Indian Dharmic religion that originated at the end of the 15th century CE in the Punjab region, developed from the spiritual teachings of Guru Nanak",
        },
        "10": {
            "name": "Taoism",
            "description": "A philosophical and spiritual tradition originating in the 4th century BCE in China which emphasizes living in harmony with the Tao, the source, pattern and substance of everything that exists",
        },
        "11": {
            "name": "Unificationism",
            "description": "A religion founded in 1954 in South Korea following the teachings of Rev. Syn Myung Moon and known for its mass wedding ceremonies",
        },
        "12": {
            "name": "Zoroastrianism",
            "description": "A religion originating in ancient Iran following the teachings of the prophet Zoroaster, predicting the triumph of good over evil and exalting the benevolent deity of wisdom, Ahura Mazda (Wise Lord), as its supreme being",
        },
        "13": {
            "name": "atheism and agnosticism",
            "description": "The belief that god does not exist or that it is impossible to know whether a god exists",
        },
        "14": {
            "name": "cult",
            "description": "A group that consists of followers who are fully devoted to a charismatic leader. Members are sometimes exploited financially or subject to emotional or physical harm",
        },
        "15": {
            "name": "nature religion",
            "description": "Religions that believe nature and the natural world is an embodiment of divinity, sacredness or spiritual power, including indigenous religions practiced in various parts of the world, and modern Pagan faiths, such as Wicca",
        },
        "16": {"name": "none", "description": "none"},
    },
    "religious facility": {
        "0": {
            "name": "church",
            "description": "A building used as a place of worship for the Christian religion",
        },
        "1": {
            "name": "mosque",
            "description": "A building used as a place of worship for the Islamic religion",
        },
        "2": {
            "name": "synagogue",
            "description": "A building used as a place of worship for the Jewish religion",
        },
        "3": {"name": "none", "description": "none"},
    },
    "religious festival and holiday": {
        "0": {
            "name": "All Saints Day",
            "description": "Christian festival celebrated in honour of all the saints, known and unknown. Holiday is also known as All Hallows' Day, Hallowmas, Feast of All Saints or Solemnity of All Saints.",
        },
        "1": {
            "name": "Christmas",
            "description": "Christian holiday that celebrates the birth of Jesus Christ. Is also celebrated by many as a secular holiday.",
        },
        "2": {
            "name": "Easter",
            "description": "Christian festival commemorating the resurrection of Jesus Christ. Is also celebrated by many as a secular holiday.",
        },
        "3": {
            "name": "Eid al-Adha",
            "description": "Muslim festival marking the culmination of the annual hajj pilgrimage and commemorating the willingness of the Prophet Ibrahim to sacrifice his son",
        },
        "4": {
            "name": "Hanukkah",
            "description": "Jewish festival, sometimes spelled Chanukah, observed by lighting the candles of a menorah",
        },
        "5": {
            "name": "Pentecost",
            "description": "Christian festival, celebrated on the 50th day after Easter commemorating the descent of the Holy Spirit, also known as Whitsun",
        },
        "6": {
            "name": "Ramadan",
            "description": "Holy month of fasting in Islam concluding in Eid al-Fitr",
        },
        "7": {
            "name": "Walpurgis night",
            "description": "The eve of the Christian feast day of Saint Walpurga, an 8th-century abbess in Francia, celebrated on the night of 30 April and the day of 1 May",
        },
        "8": {
            "name": "Yom Kippur",
            "description": "Most solemn of Jewish religious holidays, observed on the 10th day of the lunar month of tishri by fasting and prayer from sunset to sundown the following day",
        },
        "9": {"name": "none", "description": "none"},
    },
    "religious leader": {
        "0": {
            "name": "pope",
            "description": "Head of the Roman Catholic Church worldwide",
        },
        "1": {"name": "none", "description": "none"},
    },
    "religious ritual": {
        "0": {
            "name": "baptism",
            "description": "A Christian religious rite, sometimes also called a Christening, involving the sprinkling of holy water onto a person's forehead or immersing them in water, symbolising purification and admission to the Church",
        },
        "1": {
            "name": "bar and bat mitzvah",
            "description": "Young person becoming an adult in the Jewish faith",
        },
        "2": {
            "name": "canonisation",
            "description": "The declaration of a deceased person as an officially recognised saint",
        },
        "3": {"name": "none", "description": "none"},
    },
    "religious text": {
        "0": {"name": "Bible", "description": "Holy book of Christianity"},
        "1": {"name": "Qur'an", "description": "Holy book of Islam"},
        "2": {"name": "Torah", "description": "Holy book of Judaism"},
        "3": {"name": "none", "description": "none"},
    },
    "biomedical science": {
        "0": {
            "name": "biotechnology",
            "description": "The scientific manipulation of living organisms and biological processes for scientific, medical or agricultural purposes",
        },
        "1": {"name": "none", "description": "none"},
    },
    "natural science": {
        "0": {
            "name": "astronomy",
            "description": "The study of celestial objects through direct observation and theoretical models",
        },
        "1": {
            "name": "biology",
            "description": "The study of the anatomy, behaviour, origin, physiology and other aspects of living organisms",
        },
        "2": {
            "name": "chemistry",
            "description": "The study of the composition and properties of matter on the scale of atoms and molecules, and of the reactions between compounds",
        },
        "3": {
            "name": "cosmology",
            "description": "The study of the origin, evolution, organisation and structure of the universe",
        },
        "4": {
            "name": "geology",
            "description": "The study of Earth's physical processes, material structures and its properties",
        },
        "5": {
            "name": "horticulture",
            "description": "The study and art of plant cultivation, including landscape and garden design and plant conservation",
        },
        "6": {
            "name": "marine science",
            "description": "The study of living organisms and environments in saltwater ecosystems",
        },
        "7": {
            "name": "meteorology",
            "description": "The study of atmospheric chemistry and physics, with a focus on weather forecasting",
        },
        "8": {
            "name": "physics",
            "description": "The study of the movement and structure of matter, and how it relates to energy",
        },
        "9": {"name": "none", "description": "none"},
    },
    "scientific research": {
        "0": {
            "name": "medical research",
            "description": "Investigation conducted in the fields of health and medicine, such as genetic studies, disease research or pharmaceutical drug trials",
        },
        "1": {
            "name": "scientific exploration",
            "description": "Land, sea or space journeys undertaken to discover new information",
        },
        "2": {
            "name": "scientific innovation",
            "description": "The development or creation of new scientific or technological products or processes, such as biotech or artificial intelligence applications, robotic limbs or nanoscale cameras",
        },
        "3": {
            "name": "scientific publication",
            "description": "Academic research findings published in a journal, book or thesis",
        },
        "4": {"name": "none", "description": "none"},
    },
    "social sciences": {
        "0": {
            "name": "anthropology",
            "description": "The study of human behaviour and social interactions across time",
        },
        "1": {
            "name": "archaeology",
            "description": "The study of human activity throughout time and cultural history, using artefacts left behind by ancient peoples",
        },
        "2": {
            "name": "economics",
            "description": "The study of the laws and principles of economies, such as the production and distribution of goods and services",
        },
        "3": {
            "name": "geography",
            "description": "The study of the physical features of the surface of Earth and its political divisions",
        },
        "4": {
            "name": "history",
            "description": "The study of human events of the past",
        },
        "5": {
            "name": "information science",
            "description": "The study and practice of collecting, classifying, storing, retrieving and disseminating information",
        },
        "6": {
            "name": "linguistics",
            "description": "The study of all aspects of human language such as syntax, phonetics, written and spoken forms and variations over time",
        },
        "7": {
            "name": "philosophy",
            "description": "The study of the principles and fundamental questions about matters such as the mind, reason, morality or values",
        },
        "8": {
            "name": "political science",
            "description": "The study of the principles of political and governmental systems, political thought and practices",
        },
        "9": {
            "name": "psychology",
            "description": "The study of the human mind, mental characteristics and emotional processes",
        },
        "10": {
            "name": "sociology",
            "description": "The study of human social organisation, social relationships and societal changes",
        },
        "11": {
            "name": "study of law",
            "description": "The study of legal systems and the philosophy of law",
        },
        "12": {"name": "none", "description": "none"},
    },
    "technology and engineering": {
        "0": {
            "name": "aerospace engineering",
            "description": "The study, design, development and construction of aircraft, spacecraft and missile systems",
        },
        "1": {
            "name": "agricultural technology",
            "description": "The study and development of techniques and machinery to improve agricultural management and productivity",
        },
        "2": {
            "name": "civil engineering",
            "description": "The study, design, development and construction of structures such as buildings, bridges, tunnels, irrigation and sewage systems, streets or railroads",
        },
        "3": {
            "name": "electronic engineering",
            "description": "The study, design, development and application of systems built on the exchange of electrical charges, such as consumer devices, communications systems or industrial computers",
        },
        "4": {
            "name": "identification technology",
            "description": "The study, development, application and ethical considerations of technological methods for identifying products, animals or people; including radio frequency, biometrics or face recognition",
        },
        "5": {
            "name": "information technology and computer science",
            "description": "The study and design of computer systems, software and networks",
        },
        "6": {
            "name": "materials science",
            "description": "The study of the composition, structure and properties of materials for their use in industry and manufacturing",
        },
        "7": {
            "name": "mechanical engineering",
            "description": "The study and application of the design, construction and operation of mechanical systems",
        },
        "8": {
            "name": "micro science",
            "description": "The study of and technologies built at a microscopic scale, such as microbiology or microcomputing",
        },
        "9": {"name": "none", "description": "none"},
    },
    "communities": {
        "0": {
            "name": "fraternal and community group",
            "description": "Social organisations whose members freely associate for a mutually beneficial purpose such as for social, professional or honorary principles. Groups include Rotary clubs, Lions clubs or Freemasons.",
        },
        "1": {
            "name": "social networking",
            "description": "Social interactions, either in person or online, intended to share information and build relationships around common interests",
        },
        "2": {"name": "none", "description": "none"},
    },
    "demographics": {
        "0": {
            "name": "population and census",
            "description": "The official count of people living in a given geopolitical area, usually carried out by a governmental body",
        },
        "1": {"name": "none", "description": "none"},
    },
    "discrimination": {
        "0": {
            "name": "ageism",
            "description": "Discrimination against individuals or groups of people on the basis of age",
        },
        "1": {
            "name": "racism",
            "description": "Discrimination against individuals or groups of people on the basis of race",
        },
        "2": {
            "name": "religious discrimination",
            "description": "Unfair treatment of individuals or groups of people on the basis of their religious belief",
        },
        "3": {
            "name": "sexism",
            "description": "Discrimination against individuals or groups of people, usually women, on the basis of gender",
        },
        "4": {"name": "none", "description": "none"},
    },
    "family": {
        "0": {
            "name": "Dating and Relationships",
            "description": "The development of an intimate connection between individuals, through various forms of activities enjoyed together, often leading to a legal or permanent union such as marriage",
        },
        "1": {
            "name": "adoption",
            "description": "The legal process of transferring parental rights to someone other than a person's birth parents, that person usually being a child",
        },
        "2": {
            "name": "divorce",
            "description": "The process by which a marriage is legally dissolved",
        },
        "3": {
            "name": "family planning",
            "description": "Services and education aimed at informing individual decisions about reproduction, such as fertility, in vitro fertilisation, contraception or abortion",
        },
        "4": {
            "name": "marriage",
            "description": "The legal or socially recognised union of individuals, which establishes rights and obligations between them",
        },
        "5": {
            "name": "parenting",
            "description": "The caring for and support of a child's physical, emotional, developmental and social needs from birth to adulthood",
        },
        "6": {
            "name": "pregnancy and childbirth",
            "description": "Social and medical issues around pregnancy and giving birth including, doulas and midwives, obstetrics and medical concerns",
        },
        "7": {"name": "none", "description": "none"},
    },
    "immigration": {
        "0": {
            "name": "illegal immigration",
            "description": "The movement of individuals or groups of people from one country to another without legal authorisation from the destination country",
        },
        "1": {"name": "none", "description": "none"},
    },
    "mankind": {
        "0": {
            "name": "LGBTQ",
            "description": "People who identify as lesbian, gay, bisexual, transgender or queer",
        },
        "1": {
            "name": "adults",
            "description": "People above an age set by law that entitles them to full liability and certain privileges such as the legal right to drink alcoholic beverages and to vote",
        },
        "2": {
            "name": "children",
            "description": "Young people, usually pre-pubescent, who are legally considered minors and are in a guardianship relationship with adults",
        },
        "3": {
            "name": "disabilities",
            "description": "Physical or mental conditions that limit a person's movements, senses, or activities",
        },
        "4": {
            "name": "gender",
            "description": "The classification of individuals as male, female, or a non-binary designation",
        },
        "5": {
            "name": "indigenous people",
            "description": "People who are the original owners and caretakers of a given region, also known as native peoples, first peoples or aboriginal peoples, in contrast to groups that have settled, occupied or colonised the area more recently",
        },
        "6": {
            "name": "infants",
            "description": "Very young people, usually defined as being just born up to the age of two",
        },
        "7": {
            "name": "men",
            "description": "People who identify as male, focusing on the group as a demographic, and masculinity",
        },
        "8": {
            "name": "national or ethnic minority",
            "description": "Groups of people that form a minority on an ethnic or national basis, and their status or issues relating to the majority",
        },
        "9": {
            "name": "senior citizens",
            "description": "People having passed the age of retirement",
        },
        "10": {
            "name": "teenagers",
            "description": "Young people between the ages that describe childhood and adulthood",
        },
        "11": {
            "name": "women",
            "description": "People who identify as female, focusing on the group as a demographic, and accomplishments, such as the first woman to achieve a milestone or serve in a role",
        },
        "12": {"name": "none", "description": "none"},
    },
    "social condition": {
        "0": {
            "name": "homelessness",
            "description": "The social condition defined by lack of permanent residence, living in shelters or on streets, and the issues and problems associated with it",
        },
        "1": {
            "name": "poverty",
            "description": "The lack of sufficient resources and means to provide basic needs such as food, clothing or shelter for oneself and one's family",
        },
        "2": {"name": "none", "description": "none"},
    },
    "social problem": {
        "0": {
            "name": "abusive behaviour",
            "description": "Actions that intentionally harm another person or people, often on an ongoing basis, such as psychological or mental abuse, negligence, physical or sexual abuse and torture",
        },
        "1": {
            "name": "addiction",
            "description": "The habitual and compulsive use of substances such as alcohol or drugs, or behaviour such as gambling, gaming or sex, often causing detrimental effects on the body, brain, and relationships with others",
        },
        "2": {
            "name": "bullying",
            "description": "Taking actions meant to harm, coerce and intimidate another person perceived as vulnerable. These actions can be taken in person or online.",
        },
        "3": {
            "name": "juvenile delinquency",
            "description": "Unlawful conduct perpetrated by minors, often on a repeated basis",
        },
        "4": {
            "name": "prostitution",
            "description": "The business of engaging in sexual activity in exchange for payment",
        },
        "5": {
            "name": "sexual misconduct",
            "description": "Unwanted behaviour of a sexual nature that is of lesser offense than felony sexual assault, particularly when behaviour occurs in a normally non-sexual situation, or where there is some aspect of personal power or authority involved",
        },
        "6": {
            "name": "slavery",
            "description": "The ownership of people as property, and the involuntary servitude of those people to their owners, which includes unpaid labour and coerced actions",
        },
        "7": {"name": "none", "description": "none"},
    },
    "values": {
        "0": {
            "name": "death and dying",
            "description": "Social, medical and mental health issues relating to people at the end of their lives",
        },
        "1": {
            "name": "ethics",
            "description": "The moral values and standards that define right and wrong actions or decisions",
        },
        "2": {
            "name": "pornography",
            "description": "The depiction of sexually explicit acts in various media renditions, such as video or photos, often considered obscene or immoral",
        },
        "3": {
            "name": "sexual behaviour",
            "description": "The manner in which people express their sexuality in physical acts",
        },
        "4": {"name": "none", "description": "none"},
    },
    "welfare": {
        "0": {
            "name": "charity",
            "description": "The voluntary giving of money, food or other necessities to those in need",
        },
        "1": {
            "name": "child care",
            "description": "Services and facilities that look after children while their parents are working or away, including daycare centres and programmes",
        },
        "2": {
            "name": "elderly care",
            "description": "The long-term care of the elderly provided by residential institutions or by paid daily help in the home",
        },
        "3": {
            "name": "long-term care",
            "description": "Services provided on an extended and ongoing basis to patients suffering from chronic illness or disability",
        },
        "4": {
            "name": "public housing",
            "description": "Housing that is owned or managed by a government or nonprofit organisation and rented to tenants with the aim of making housing affordable. Eligibility for such housing arrangements varies country to country.",
        },
        "5": {
            "name": "social services",
            "description": "Social programmes, usually publicly sponsored, aimed at promoting people's welfare, such as housing, health care or education services",
        },
        "6": {"name": "none", "description": "none"},
    },
    "competition discipline": {
        "0": {
            "name": "3x3 basketball",
            "description": "A variation of basketball played three a side on one basketball hoop",
        },
        "1": {
            "name": "American football",
            "description": "Team ball game that opposes two teams of 11 that have offence and defence sections. Each offence attempts to move an oval ball down the 120 yards long field. Points are scored by advancing the ball into the opposing team s end zone.",
        },
        "2": {
            "name": "Australian rules football",
            "description": "A form of football played by two teams of 18 competing on a pitch by running with and passing an oval ball. Points are scored by moving the ball between goal posts. Governed by the Australian Football League.",
        },
        "3": {
            "name": "Canadian football",
            "description": "Team ball game that opposes two teams of 12 that have offence and defence sections. Each offence attempts to move an oval ball down the 150 yards long field. Points are scored by advancing the ball into the opposing team s end zone.",
        },
        "4": {
            "name": "Gaelic football",
            "description": "A form of football played by two teams of 15 competing on a pitch by running with, kicking and passing a spherical ball. Points are scored by moving the ball between goal posts. Governed by the Gaelic Athletic Association.",
        },
        "5": {
            "name": "Jai Alai (Pelota)",
            "description": "A fast ball play using either the bare hand or a wicker scoop in an arena of walls of different outlay and size",
        },
        "6": {
            "name": "archery",
            "description": "Archers use bows and arrows to aim at targets 1.22 metres in diameter which are on average 70 metres distant.",
        },
        "7": {
            "name": "arm wrestling",
            "description": "A form of wrestling in which two participants grapple arm-to-arm",
        },
        "8": {
            "name": "artistic swimming",
            "description": "A sport in which swimmers, in solo, duet or team configurations, perform coordinated or identical movements in time to music. They are judged and are awarded points for body position, control, and the degree of difficulty of the moves.",
        },
        "9": {
            "name": "athletics",
            "description": "Competitions involving foot races, jumping and throwing which can be on a track inside a stadium or on outside roads",
        },
        "10": {
            "name": "badminton",
            "description": "Two players or two teams of two compete by hitting a shuttlecock weighing approximately five grams over a high net. The aim for each player/team is to prevent the shuttlecock landing on their side of the court.",
        },
        "11": {
            "name": "bandy",
            "description": "Played outdoors on ice. The size of the ice rink is about the size of a soccer field. Skates like ice hockey. A small hard ball is used for playing. Players play with sticks, much like in ice hockey, but the sticks are shorter and more rounded than in ice",
        },
        "12": {
            "name": "baseball",
            "description": "A game between two teams of nine played on an enclosed ground. The team which scores the most points wins. A point is scored when a player runs around the ground marked out by four bases. To do this he has to hit the ball thrown at him by a rival player.",
        },
        "13": {
            "name": "basketball",
            "description": "Game played between two teams of five - points are scored by placing the large inflated ball into a net fixed on a ring 3.05m above the ground.",
        },
        "14": {
            "name": "biathlon",
            "description": "A combination of cross-country skiing and target shooting on a 12.5 K course in a pursuit format.",
        },
        "15": {
            "name": "billiards",
            "description": "A cue sport with balls on a table without a specific order to play them",
        },
        "16": {
            "name": "bobsleigh",
            "description": "One, two or four people racing down a course in a sled that consists of a main hull, a frame, two axles and sets of runners. The total time of all heats in a competition is added together to determine the winner.",
        },
        "17": {
            "name": "bodybuilding",
            "description": "Competitions where participants perform specific poses to display their muscles that have been strengthened and enlarged through strenuous exercise. Competitors are judged based on criteria such as symmetry, muscularity and conditioning.",
        },
        "18": {
            "name": "boules",
            "description": "Collective name of a number of games where the common goal is to move the competitor's balls as close to a small target ball as possible, played on a grass or sand surface. Balls are thrown (as in petanque and boules) or rolled (as in lawn bowls or bocce).",
        },
        "19": {
            "name": "boxing",
            "description": "Combat sport in which two men/women fight using only their fists covered by padded gloves in a square ring measuring 6m a side. The fight is usually split into 12 rounds of three minutes each.",
        },
        "20": {
            "name": "bullfighting",
            "description": "Classical contest pitting man against the bull",
        },
        "21": {
            "name": "canoe slalom",
            "description": "Competitors navigate a canoe or a kayak on a white-water course, passing through a combination of upstream and downstream gates on river rapids in the fastest time possible",
        },
        "22": {
            "name": "canoe sprint",
            "description": "Taking place on a flatwater course, multiple canoes take off at once and race each other to the finish",
        },
        "23": {
            "name": "canoeing",
            "description": "Competition involving canoes which are generally kneeled and paddled with a single-bladed paddle",
        },
        "24": {
            "name": "casting (fishing)",
            "description": "Using fishing equipment to hit a target and score points",
        },
        "25": {
            "name": "cheerleading",
            "description": "Cheer squads competing against each other to perform a routine that includes stunts, jumps and tumbling set to music. Squads are judged on difficulty and execution.",
        },
        "26": {
            "name": "chess",
            "description": "Competition between two players using a chequered board with 16 pieces to each side, each with specific ranges of movement depending on their identity",
        },
        "27": {
            "name": "competitive dancing",
            "description": "Dancing competition where competitors are judged on technique and interpretation.",
        },
        "28": {
            "name": "cricket",
            "description": "Ball sport involving two teams of 11 players, balls, bats and wickets. The aim is to score as many runs as possible, and to get the opposing team 'out'. A 'run' involves a player running between two wickets. The opposing team try to get their rivals 'out'",
        },
        "29": {
            "name": "croquet",
            "description": "Using mallets to hit a ball through hoops",
        },
        "30": {
            "name": "curling",
            "description": "A game played on ice with large flat round stones. A player throws the stone, aiming at a target. Teammates of the player who has thrown the stone can sweep the ice in front of the stone to help smooth its path towards the target.",
        },
        "31": {
            "name": "cycling",
            "description": "A race over a given distance on bicycles.",
        },
        "32": {
            "name": "darts",
            "description": "The sport in which small darts are thrown at a dartboard, a circular target divided into numbered sections.",
        },
        "33": {
            "name": "diving",
            "description": "Competitors dive off a fixed or spring board and are assessed by seven judges giving marks up to ten for their acrobatic moves.",
        },
        "34": {"name": "dog racing", "description": "Dogs racing around a track"},
        "35": {
            "name": "duathlon",
            "description": "An athletic event involving running and cycling",
        },
        "36": {
            "name": "eSports",
            "description": "Competitions involving video games played by professional gamers",
        },
        "37": {
            "name": "equestrian",
            "description": "Horse-based sport disciplines governed by the International Federation for Equestrian Sports, such as dressage, eventing, show jumping and vaulting",
        },
        "38": {"name": "fencing", "description": "Combat sport using a sword or foil."},
        "39": {
            "name": "field hockey",
            "description": "A ball sport involving two teams of 11 players using curved sticks. The aim is to score as many goals as possible.",
        },
        "40": {
            "name": "figure skating",
            "description": "To obtain the best marks possible from nine judges who award scores after two prepared sections - both skated to music - during which competitors must attempt to achieve the greatest possible harmony between artistic flair and technical precision.",
        },
        "41": {
            "name": "fist ball",
            "description": "Men's team sport similar to volleyball (with a much lower net) executed mainly in gymnastics clubs",
        },
        "42": {
            "name": "floorball",
            "description": "Played indoors in a court the size of a basketball court. 6 players per team, of which one is a goalkeeper. He/she operates kneeling but there is no goal-stick like in ice hockey. The players use plastic clubs and a light plastic ball to pass and shot goal",
        },
        "43": {
            "name": "flying disc",
            "description": "A group of events all played with a flying plastic disc. The exact regulation for the disc is different in different events but it has to be unbroken of solid plastic and a production model with no modification. Flying disc is sometimes called Frisbee.",
        },
        "44": {
            "name": "football 5-a-side",
            "description": "A variation of association football in which each team fields five players and play is on a smaller pitch. An official Summer Paralympics sport.",
        },
        "45": {
            "name": "goalball",
            "description": "A team sport for athletes with a vision impairment, using a ball containing bells",
        },
        "46": {
            "name": "golf",
            "description": "A game to hit a small hard ball with different clubs around a course of typically 18 holes varying in distance and during a round. The object, depending on the scoring formulae, is to make the fewest strokes possible",
        },
        "47": {
            "name": "gymnastics",
            "description": "A sport consisting of a variety of disciplines in which gymnasts perform artistic and acrobatic moves using different apparatus.",
        },
        "48": {
            "name": "handball (team)",
            "description": "A ball game using the hands contested by two teams of seven trying to throw the ball into the opponents goal.",
        },
        "49": {
            "name": "hornuss",
            "description": "Swiss team sport with 16 or 18 men per team. A rubber puck is hit towards the field of the adversary team which tries to hit the puck in the air with a wooden board thrown in the air",
        },
        "50": {"name": "horse racing", "description": "Mounted horse races."},
        "51": {
            "name": "hurling",
            "description": "A game played by two teams of fifteen each with a curved wooden stick called a hurley. The object is to score a goal by hitting the small ball between the opponents' goalposts either over the crossbar or under it into a net guarded by a goalkeeper.",
        },
        "52": {
            "name": "ice hockey",
            "description": "Two teams of six heavily padded skaters try and outscore each other by hitting a puck into the opponents goal.",
        },
        "53": {
            "name": "kabaddi",
            "description": "The attacking side scores by touching, and the side to guard scores by capturing. The attacker continues calling it 'kabaddi'.",
        },
        "54": {
            "name": "kayaking",
            "description": "Competition involving kayaks where the paddler sits with their legs facing forward using a double-bladed paddle",
        },
        "55": {
            "name": "kiting",
            "description": "Action sport where a person harnesses the power of the wind to propel themselves across water, land or snow on a board, snowboard or skis. Variations of the sport are called kiteboarding/kitesurfing, snowkiting or landkiting.",
        },
        "56": {
            "name": "lacrosse",
            "description": "Two teams of helmeted and padded players try and outscore each other using a netted stick and hard ball.",
        },
        "57": {
            "name": "luge",
            "description": "Luge (French word for sled) is competed in singles or doubles. The competitor(s) lay on their back on an open sled and race down a course. The competitor(s) and the sled must be in contact when passing the finishing line. The competitor can steer the sled",
        },
        "58": {
            "name": "marathon",
            "description": "A road race where competitors run 42.195km, generally through city streets",
        },
        "59": {
            "name": "martial arts",
            "description": "Martial arts are codified systems and traditions of combat practices, which are practiced for a variety of reasons: self-defence, competition, physical health and fitness, entertainment, as well as mental, physical, and spiritual development.",
        },
        "60": {
            "name": "modern pentathlon",
            "description": "The Modern Pentathlon comprises five events run over a single day in the following order: shooting, fencing, swimming, horse riding and running.",
        },
        "61": {"name": "motor car racing", "description": "Racing with cars"},
        "62": {
            "name": "motorboat racing",
            "description": "Racing with boats with engines",
        },
        "63": {
            "name": "motorcycling",
            "description": "Races with 2, 3 or 4 wheels vehicles with a saddle and handlebars",
        },
        "64": {
            "name": "mountain climbing",
            "description": "Moving up mountains using hands and feet",
        },
        "65": {
            "name": "netball",
            "description": "A woman's sport similar to basketball though without a board behind the basket",
        },
        "66": {
            "name": "orienteering",
            "description": "An individual time-trial over a route marked out by beacons. The competitor has to search out and find in a specific order. The contestant makes his way with the help of a compass and map",
        },
        "67": {
            "name": "padel",
            "description": "Racquet sport typically played in doubles on an enclosed court",
        },
        "68": {
            "name": "parachuting",
            "description": "Jumping from an aeroplane using a parachute, competitions are precision landings, voltige, individual and team",
        },
        "69": {
            "name": "polo",
            "description": "With the aid of a mallet two teams of four horsemen try and knock a bamboo ball into the opponents goal over a pitch 250m long and 150m wide. The game is divided into 4, 6, or 8 time periods of 7min 30sec called chukkas.",
        },
        "70": {
            "name": "pool",
            "description": "A cue sport on a table with pockets, played with different numbers of balls",
        },
        "71": {
            "name": "power boating",
            "description": "Races between motor boats on rivers or lakes",
        },
        "72": {
            "name": "racquetball",
            "description": "A racquet sport similar to squash in which the ball must bounce once before being struck and with a greater area of in-bound play",
        },
        "73": {
            "name": "ringette",
            "description": "A team sport usually played on ice by skaters using a straight stick. Players pass and shoot a rubber ring in order to place it in the opponent's goal",
        },
        "74": {
            "name": "road cycling",
            "description": "Cycling events held on roads, including road races and time trials",
        },
        "75": {
            "name": "rodeo",
            "description": "A discipline where wild horses or bulls must be mounted and mastered",
        },
        "76": {
            "name": "roller sports",
            "description": "Various competitions using wheeled equipment such as roller skates, inline skates, and skateboards.",
        },
        "77": {
            "name": "rowing",
            "description": "Boat racing usually on flat calm waters with boats for 1, 2, 4 or 8 rowers",
        },
        "78": {
            "name": "rugby",
            "description": "A form of football developed in Rugby (England) played with an oval ball that may be kicked, carried and passed from hand to hand. Points are scored when one team carries the ball over the other team's goal line or kicks the ball between two goal posts.",
        },
        "79": {"name": "sailing", "description": "Sailing boat racing over a route"},
        "80": {
            "name": "sepak takraw",
            "description": "A game like volleyball where hands must not be used, using a ball made of rattan",
        },
        "81": {
            "name": "shinty",
            "description": "A ball game involving 2 teams with curved sticks called camans. The object is to score goals by hitting the small leather ball through the goals.",
        },
        "82": {
            "name": "short track speed skating",
            "description": "Races competed by four or more skaters at a time on a small oval ice track",
        },
        "83": {
            "name": "skeleton",
            "description": "In skeleton the competitor lies on his/her stomach when racing down the course. The competitor must be on the sled when crossing the finishing line.",
        },
        "84": {
            "name": "skiing",
            "description": "A winter sport using different types of skis",
        },
        "85": {
            "name": "sky diving",
            "description": "Parachuting competitions with long distance falls without using a parachute",
        },
        "86": {
            "name": "snooker",
            "description": "A cue sport with balls on a table to be potted in a specific order",
        },
        "87": {
            "name": "snowboarding",
            "description": "Practiced with a single board (rather than two skis)",
        },
        "88": {
            "name": "soccer",
            "description": "A form of football played by two teams competing on a pitch by kicking a spherical ball. Points are scored by kicking or heading the ball into a goal. Governed by the Fédération Internationale de Football Association",
        },
        "89": {
            "name": "softball",
            "description": "Similar to baseball but with a larger and softer ball, a thinner bat, shorter gaps between bases and less innings",
        },
        "90": {
            "name": "speed skating",
            "description": "Timed races competed by two or more skaters at a time on an oval ice track",
        },
        "91": {
            "name": "sport climbing",
            "description": "Sport climbing as a special category: individual competition, on an artificial wall with time measurement",
        },
        "92": {
            "name": "sport shooting",
            "description": "Precision sport using a hand gun, rifle or shotgun",
        },
        "93": {
            "name": "squash",
            "description": "A racquet sport of strategy and endurance played by singles or doubles teams in a walled court with a small rubber ball",
        },
        "94": {
            "name": "stand up paddleboarding (SUP)",
            "description": "Water sport using a board and paddle to propel through the water while standing",
        },
        "95": {
            "name": "sumo wrestling",
            "description": "A combat sport of speed and rapidity with much ceremony where two contestants try to throw or slap a competitor out of a marked area. Generally practiced in Japan by large men.",
        },
        "96": {
            "name": "surfing",
            "description": "Water sport where contestants catch and ride waves upright on a surfboard",
        },
        "97": {
            "name": "swimming",
            "description": "A water sport where contestants swim as fast as possible in a given style and win races by being the first to touch home",
        },
        "98": {
            "name": "table tennis",
            "description": "A racquet sport for two or four (in doubles), who compete at a table divided by a net using a small bat to play a lightweight ball",
        },
        "99": {
            "name": "ten pin bowling",
            "description": "A game in which a player scores points by trying to knock down ten 'pins' using a ball - if unsuccessful the player has a second attempt. A game consists of ten frames.",
        },
        "100": {
            "name": "tennis",
            "description": "A sport where two players, four in doubles, equipped with a racket compete by hitting the ball over a net into the opponent's side of the court with the aim of putting it out of reach within the regulation lines, thus winning points.",
        },
        "101": {
            "name": "track cycling",
            "description": "Cycling competitions held on tracks, including sprint, team sprint, keirin, team pursuit, omnium and madison events",
        },
        "102": {
            "name": "triathlon",
            "description": "An endurance multi-sport where competitors first swim, then cycle and then run a road race. Distances vary according to the competition.",
        },
        "103": {
            "name": "tug-of-war",
            "description": "Two teams pulling against each other on a rope",
        },
        "104": {
            "name": "underwater sports",
            "description": "Competitive sports played under water",
        },
        "105": {
            "name": "volleyball",
            "description": "Two teams of six record points by hitting a ball over a net into the opponent's half of the court, keeping it in the air at all times. Points are won when opponents fail to return the ball.",
        },
        "106": {
            "name": "water polo",
            "description": "Played in a pool between two teams of 7, who must stay afloat and can only use one hand to pass the ball or swim with it before trying to throw it into the opponents net to score goals.",
        },
        "107": {
            "name": "water skiing",
            "description": "On one or two skis contestants are pulled by a power boat along the water's surface",
        },
        "108": {
            "name": "weightlifting and powerlifting",
            "description": "A strength test where competitors lift as heavy a weight as possible",
        },
        "109": {
            "name": "windsurfing",
            "description": "Contestants must complete a marked out course as fast as possible on a windsurf board",
        },
        "110": {
            "name": "wrestling",
            "description": "Combat sport where each wrestler attempts to win over his adversary, by holding both shoulders on the ground (fall) long enough to be in control. Points can also be decisive.",
        },
        "111": {"name": "none", "description": "none"},
    },
    "drug use in sport": {"0": {"name": "none", "description": "none"}},
    "sport achievement": {
        "0": {
            "name": "sports honour",
            "description": "Honour given to a player for achievements over a career, season or single event, unrelated to event outcome, usually awarded by a panel of judges or a popular vote. Examples include player of the game, most valuable player award or hall of fame induction.",
        },
        "1": {
            "name": "sports medal and trophy",
            "description": "Award given to an athlete or team for placing in a sports competition, such as a gold medal at the Olympics or the Stanley Cup in ice hockey",
        },
        "2": {
            "name": "sports record",
            "description": "The best performance to date by an athlete or team in a sport discipline",
        },
        "3": {"name": "none", "description": "none"},
    },
    "sport event": {
        "0": {
            "name": "Olympic Games",
            "description": "Games organised by the International Olympic Committee and held each 4 years in summer or winter.",
        },
        "1": {
            "name": "Paralympic Games",
            "description": "Games for disabled athletes organised by the International Paralympic Committee and held each 4 years in winter or summer",
        },
        "2": {
            "name": "final game",
            "description": "Single game that determines the winner of a championship, such as the Super Bowl or Champions League Final",
        },
        "3": {
            "name": "playoff championship",
            "description": "A competitive tournament, often played after the regular season of a sports league by the top competitors to determine the league champion or a similar accolade. Can also apply to an all-in elimination tournament meant to produce a final champion.",
        },
        "4": {
            "name": "regular competition",
            "description": "A competitive sporting season where teams or individuals contend for a place in the standings or rankings",
        },
        "5": {"name": "none", "description": "none"},
    },
}

CANDIDATE_DICT_FOURTH = {
    "dance": {
        "0": {
            "name": "ballet",
            "description": "A classical dance form based on formal gestures, steps and postures",
        },
        "1": {
            "name": "modern dance",
            "description": "A theatrical dance style based on free-style expression rather than formal gestures",
        },
        "2": {
            "name": "traditional dance",
            "description": "Dance style that reflects the life and culture of a specific group of people or region, such as folk and ceremonial dance",
        },
        "3": {"name": "none", "description": "none"},
    },
    "fashion": {
        "0": {
            "name": "cosmetics",
            "description": "Products applied to the body to enhance appearance, such as lipstick, eyeliner, foundation and nail polish, and the trends surrounding the application of these products",
        },
        "1": {
            "name": "hairstyles",
            "description": "Trends surrounding the cutting and styling of hair",
        },
        "2": {
            "name": "jewellery",
            "description": "Decorative items worn for personal expression and adornment, such as rings, necklaces, earrings",
        },
        "3": {"name": "none", "description": "none"},
    },
    "festival": {
        "0": {
            "name": "film festival",
            "description": "All forms of national and international film festivals",
        },
        "1": {"name": "none", "description": "none"},
    },
    "literature": {
        "0": {
            "name": "drama (literature)",
            "description": "Work written to be performed on the stage",
        },
        "1": {
            "name": "fiction",
            "description": "Written works that are not based on fact, but are the creation of the author's imagination",
        },
        "2": {
            "name": "non-fiction",
            "description": "Written works that are based on fact",
        },
        "3": {
            "name": "poetry",
            "description": "Written works that use the aesthetic and rhythmic qualities of language to express a message or emotion",
        },
        "4": {"name": "none", "description": "none"},
    },
    "music": {
        "0": {
            "name": "musical genre",
            "description": "A distinguishable type of music",
        },
        "1": {
            "name": "musical instrument",
            "description": "Objects used to play music on",
        },
        "2": {
            "name": "musical performance",
            "description": "Musicians performing for an audience for the purpose of entertainment",
        },
        "3": {"name": "none", "description": "none"},
    },
    "theatre": {
        "0": {
            "name": "cabaret",
            "description": "A form of theatrical entertainment featuring music, song, dance, recitation, or drama that is performed in a nightclub or restaurant while the audience eats or drinks at tables",
        },
        "1": {
            "name": "drama (theatre)",
            "description": "A genre of theatre where dramatic or comedic plays are performed on the stage",
        },
        "2": {
            "name": "musical",
            "description": "A genre of music theatre in which singing and dancing play an essential part of the storytelling",
        },
        "3": {
            "name": "opera",
            "description": "A form of performing art where classically trained musicians and singers perform a musical and dramatic work",
        },
        "4": {
            "name": "operetta",
            "description": "A genre of music theatre that usually has a light or humorous theme where some of the libretto is usually spoken rather than sung.",
        },
        "5": {
            "name": "stand-up comedy",
            "description": "A comic style in which a comedian performs a series of jokes or stories in front of a live audience, usually speaking directly to them",
        },
        "6": {"name": "none", "description": "none"},
    },
    "visual arts": {
        "0": {
            "name": "architecture",
            "description": "The design of buildings, monuments and the spaces around them",
        },
        "1": {
            "name": "design (visual arts)",
            "description": "An artistic discipline which focuses on visual communication and presentation, the final product of which can range from jewellery to interior design",
        },
        "2": {
            "name": "drawing",
            "description": "A form of visual arts using mediums such as pencils, markers, pen and ink, charcoal",
        },
        "3": {
            "name": "forging",
            "description": "The shaping of metal using localized compressive forces, such as heating and hammering",
        },
        "4": {
            "name": "painting",
            "description": "A form of visual arts using mediums such as oil paint, watercolour, pastel, crayon",
        },
        "5": {
            "name": "photography",
            "description": "A form of visual arts using photographic images",
        },
        "6": {
            "name": "sculpture",
            "description": "A form of visual arts using mediums such as clay, stone, wood and metal to create three-dimensional works",
        },
        "7": {
            "name": "textile arts",
            "description": "Arts and crafts that use plant, animal, or synthetic fibres to construct practical or decorative object",
        },
        "8": {
            "name": "woodworking",
            "description": "The activity or skill of making items, such as furniture or cabinets, from wood",
        },
        "9": {"name": "none", "description": "none"},
    },
    "monument and heritage site": {
        "0": {
            "name": "restoration",
            "description": "Restoring historic or important properties or structures to a former better state by cleaning, repairing or rebuilding",
        },
        "1": {"name": "none", "description": "none"},
    },
    "social media": {
        "0": {
            "name": "influencers",
            "description": "Persons who distribute content on internet forums and social media and are followed by many people thereby influencing them to buy and use products",
        },
        "1": {"name": "none", "description": "none"},
    },
    "war": {
        "0": {
            "name": "civil war",
            "description": "Armed conflict between members of the same country, in some cases with the goal of dividing the country",
        },
        "1": {"name": "none", "description": "none"},
    },
    "assault": {
        "0": {
            "name": "sex crime",
            "description": "Sexual crimes against a person, such as rape, harassment, molestation or groping",
        },
        "1": {"name": "none", "description": "none"},
    },
    "corporate crime": {
        "0": {
            "name": "accounting crime",
            "description": "The intentional misrepresentation or alteration of accounting records regarding sales, revenues, expenses and other factors",
        },
        "1": {
            "name": "anti-trust crime",
            "description": "Violations of laws aimed at corporations to promote fair competition for the benefit of consumers",
        },
        "2": {
            "name": "breach of contract",
            "description": "The breaking of terms set in a contractual agreement",
        },
        "3": {
            "name": "embezzlement",
            "description": "The intentional theft or misuse of money left in one's care or belonging to one's employer",
        },
        "4": {
            "name": "insider trading",
            "description": "Trading of stocks by persons having access to internal information not made public at the time",
        },
        "5": {
            "name": "restraint of trade",
            "description": "Interference in free competition in business and trade",
        },
        "6": {"name": "none", "description": "none"},
    },
    "corruption": {
        "0": {
            "name": "bribery",
            "description": "The giving of money or favours in order to influence the judgment or conduct of a person in a position of power",
        },
        "1": {"name": "none", "description": "none"},
    },
    "drug related crimes": {
        "0": {
            "name": "drug trafficking",
            "description": "Dealing in illicit often harmful substances",
        },
        "1": {"name": "none", "description": "none"},
    },
    "fraud": {
        "0": {
            "name": "tax evasion",
            "description": "The illegal evasion of taxes by individuals, corporations, and trusts",
        },
        "1": {"name": "none", "description": "none"},
    },
    "organised crime": {
        "0": {
            "name": "gang activity",
            "description": "Criminal activities by groups of individuals, who are allied by common territories, languages or ethnic backgrounds and identify by a common group identity by using a shared name, tattoo, hand sign, clothing style or graffiti symbol",
        },
        "1": {"name": "none", "description": "none"},
    },
    "court": {
        "0": {
            "name": "appeal (court)",
            "description": "Process in which parties request a formal change to an official decision",
        },
        "1": {
            "name": "judge",
            "description": "Official who decides cases in a court of law and passes sentences on those found guilty",
        },
        "2": {
            "name": "supreme and high court",
            "description": "matters related to supreme or high courts, including nominations and rulings",
        },
        "3": {
            "name": "trial (court)",
            "description": "The process by which evidence is presented and guilt, innocence or culpability is determined",
        },
        "4": {"name": "none", "description": "none"},
    },
    "out of court procedures": {
        "0": {
            "name": "arbitration and mediation",
            "description": "Resolution of disputed issues by a neutral panel, including conciliation, negotiation and tribunals",
        },
        "1": {"name": "none", "description": "none"},
    },
    "civil law": {
        "0": {
            "name": "regulations",
            "description": "laws that guide the conduct and organization of business corporations",
        },
        "1": {"name": "none", "description": "none"},
    },
    "international law": {
        "0": {
            "name": "extradition",
            "description": "Legal transfer of criminals or suspects between countries",
        },
        "1": {
            "name": "international court and tribunal",
            "description": "The activities of courts under the authority of international organizations or formed by treaties between nations, such as the European Court for Human Rights and International Court of Justice",
        },
        "2": {"name": "none", "description": "none"},
    },
    "investigation (criminal)": {
        "0": {
            "name": "dropped criminal investigation",
            "description": "When police and/or prosecutors end an investigation without a conclusion",
        },
        "1": {
            "name": "missing person",
            "description": "An adult whose disappearance is possibly not voluntary, or a child whose whereabouts are unknown to the child's legal guardian",
        },
        "2": {"name": "none", "description": "none"},
    },
    "industrial accident and incident": {
        "0": {
            "name": "nuclear accident and incident",
            "description": "Any unplanned event that causes unwanted consequences involving radioactive materials",
        },
        "1": {"name": "none", "description": "none"},
    },
    "transportation accident and incident": {
        "0": {
            "name": "air and space accident and incident",
            "description": "An accident or incident involving aircrafts or spacecrafts",
        },
        "1": {
            "name": "maritime accident and incident",
            "description": "An accident or incident involving marine vessels.",
        },
        "2": {
            "name": "railway accident and incident",
            "description": "An accident or incident involving trains.",
        },
        "3": {
            "name": "road accident and incident",
            "description": "An accident or incident involving road vehicles.",
        },
        "4": {"name": "none", "description": "none"},
    },
    "fire": {
        "0": {
            "name": "wildfire",
            "description": "An uncontrolled fire in an area of combustible vegetation",
        },
        "1": {"name": "none", "description": "none"},
    },
    "natural disaster": {
        "0": {
            "name": "drought",
            "description": "A severe lack of water over a period of time",
        },
        "1": {
            "name": "earthquake",
            "description": "The shifting of the tectonic plates of the Earth, creating in some cases damage to structures",
        },
        "2": {
            "name": "flood",
            "description": "Surfeit of water, caused by heavy rains or melting snow, usually in places where it's not wanted",
        },
        "3": {
            "name": "landslide",
            "description": "Sudden dislodging of massive amounts of snow or soil",
        },
        "4": {
            "name": "meteorological disaster",
            "description": "A weather-related disaster",
        },
        "5": {
            "name": "tsunami",
            "description": "High and powerful ocean waves caused by an underwater land disturbance, such as an earthquake or volcanic eruption, known to cause significant damage and loss when they hit land",
        },
        "6": {
            "name": "volcanic eruption",
            "description": "A rupture in the crust of the Earth allowing molten material to escape to the surface",
        },
        "7": {"name": "none", "description": "none"},
    },
    "transport incident": {"0": {"name": "none", "description": "none"}},
    "business finance": {"0": {"name": "none", "description": "none"}},
    "business financing": {
        "0": {
            "name": "bankruptcy",
            "description": "Organisations that cannot pay their debts and file for special treatment by governments and financial systems",
        },
        "1": {
            "name": "corporate bond",
            "description": "Corporate paper representing the loan of money at a fixed rate and for a fixed time to that company or government",
        },
        "2": {
            "name": "crowdfunding",
            "description": "The funding of a project or venture by raising small amounts of money from a large number of people, typically via the internet",
        },
        "3": {
            "name": "financially distressed company",
            "description": "Indications that a company is financially distressed but not having filed for bankruptcy yet",
        },
        "4": {
            "name": "stocks and securities",
            "description": "Financial instruments such as company shares and bonds",
        },
        "5": {"name": "none", "description": "none"},
    },
    "business governance": {
        "0": {
            "name": "annual and special corporate meeting",
            "description": "News surrounding company reports and annual or special corporate meetings",
        },
        "1": {
            "name": "annual report",
            "description": "Availability or contents of annual company reports.",
        },
        "2": {
            "name": "board of directors",
            "description": "Appointments to or changes in the board of directors for a company.",
        },
        "3": {
            "name": "environmental, social and governance policy (ESG)",
            "description": "A company's business practices reflecting responsible social, ethical and environmental policies, sometimes known as corporate social responsibility",
        },
        "4": {
            "name": "proxy filing",
            "description": "Filings with regulatory agencies of proxy statements for upcoming shareholder votes.",
        },
        "5": {
            "name": "shareholder activity",
            "description": "Actions taken by owners of one or more shares of a company, including shareholder activism",
        },
        "6": {"name": "none", "description": "none"},
    },
    "business reporting and performance": {
        "0": {
            "name": "corporate earnings",
            "description": "Announcements and discussions of corporate earnings",
        },
        "1": {
            "name": "credit rating",
            "description": "Formal statements by certain rating agencies on the investment risk of a company or enterprise",
        },
        "2": {
            "name": "financial statement",
            "description": "Formal statements about the company financials typically delivered annually or quarterly",
        },
        "3": {"name": "none", "description": "none"},
    },
    "business restructuring": {
        "0": {
            "name": "company spin-off",
            "description": "The creation of new companies being spun off from existing companies",
        },
        "1": {
            "name": "joint venture",
            "description": "Two or more companies agreeing on a venture.",
        },
        "2": {
            "name": "leveraged buyout",
            "description": "Acquiring control over a company by buying its shares with borrowed money.",
        },
        "3": {
            "name": "management buyout",
            "description": "Acquiring control over a company by the management buying its shares.",
        },
        "4": {
            "name": "merger or acquisition",
            "description": "Two or more companies forming a new company mergers, takeovers or acquisitions.",
        },
        "5": {"name": "none", "description": "none"},
    },
    "business strategy and marketing": {
        "0": {
            "name": "client relationship management",
            "description": "Creating and maintaining a relationship with the customers to increase sales.",
        },
        "1": {
            "name": "commercial contract",
            "description": "Contracts regarding commercial activities",
        },
        "2": {
            "name": "economic globalisation",
            "description": "Doing business around the world",
        },
        "3": {
            "name": "market research",
            "description": "Gathering information about the needs and wants of consumers",
        },
        "4": {
            "name": "market trend",
            "description": "Statistically significant consumer behaviour.",
        },
        "5": {
            "name": "new product or service",
            "description": "The introduction of products or services to the market",
        },
        "6": {
            "name": "outsourcing",
            "description": "Business practice in which services or job functions are farmed out to a third party",
        },
        "7": {
            "name": "patent, copyright and trademark",
            "description": "Intellectual properties such as patents, copyright and trademarks",
        },
        "8": {
            "name": "product recall",
            "description": "A decision by a company to take back or repair a defective product",
        },
        "9": {
            "name": "public contract",
            "description": "Written contracts between companies and public authorities for the execution of works, the supply of products or the provision of services.",
        },
        "10": {
            "name": "research and development",
            "description": "Research and expenditure on new product or service development",
        },
        "11": {"name": "none", "description": "none"},
    },
    "human resources": {
        "0": {
            "name": "executive officer",
            "description": "Company executive officers including appointments and changes",
        },
        "1": {
            "name": "layoffs and downsizing",
            "description": "Planned or actual reductions in the labour force.",
        },
        "2": {"name": "none", "description": "none"},
    },
    "currency": {
        "0": {
            "name": "cryptocurrency",
            "description": "An internet-based medium of exchange using cryptography to conduct financial transactions",
        },
        "1": {"name": "none", "description": "none"},
    },
    "economic trends and indicators": {
        "0": {
            "name": "consumer confidence",
            "description": "A measure of consumers' feelings about current and future economic conditions, including prices, inflation and the quality of retail goods, used as an indicator of the overall state of the economy",
        },
        "1": {
            "name": "deflation",
            "description": "The decrease in the general price level of goods and services within an economy",
        },
        "2": {
            "name": "economic growth",
            "description": "An increase of the gross domestic product (GDP)",
        },
        "3": {
            "name": "employment statistics",
            "description": "Trends and statistics about areas such as job growth, unemployment and wage growth",
        },
        "4": {
            "name": "exporting",
            "description": "The producing of manufacturing of goods by a country to be sold elsewhere",
        },
        "5": {
            "name": "government debt",
            "description": "Debt incurred when a country borrows funds to pay for public services and projects that it cannot afford based on the amount of taxes it has raised",
        },
        "6": {
            "name": "gross domestic product",
            "description": "A measure of a region's economic performance, commonly abbreviated as GDP",
        },
        "7": {
            "name": "importing",
            "description": "A country bringing in goods that were produced or manufactured elsewhere",
        },
        "8": {
            "name": "industrial production",
            "description": "Manufacture of durable and non-durable goods",
        },
        "9": {
            "name": "inflation",
            "description": "The overall increase in prices and cost of living throughout an economy",
        },
        "10": {
            "name": "inventories",
            "description": "Goods not sold and held by the producer, wholesaler or retailer",
        },
        "11": {
            "name": "mortgages",
            "description": "Trends around loans taken out to buy homes, such as the interest rates of mortgages, the amount of people buying property with a mortgage and the ease of getting approved for a mortgage",
        },
        "12": {
            "name": "productivity",
            "description": "A measure of output from production or service",
        },
        "13": {
            "name": "recession",
            "description": "A decrease in gross domestic product over a period of two quarters in a row",
        },
        "14": {"name": "none", "description": "none"},
    },
    "international trade": {
        "0": {
            "name": "balance of trade",
            "description": "The difference between the financial value of imports and exports",
        },
        "1": {
            "name": "tariff",
            "description": "Fees placed on imported or exported goods",
        },
        "2": {
            "name": "trade agreements",
            "description": "Agreements between countries or trading blocs for the sale and purchase of goods and services",
        },
        "3": {
            "name": "trade dispute",
            "description": "International dispute over issues such as trade barriers, cartels and dumping, resolved by the World Trade Organization",
        },
        "4": {
            "name": "trade policy",
            "description": "Governmental decisions on tariffs, shipping, embargoes, and the types of goods and services to be imported and exported",
        },
        "5": {"name": "none", "description": "none"},
    },
    "monetary policy": {
        "0": {
            "name": "interest rates",
            "description": "The amount a lender charges a borrower as a percentage of the principal. Often set by a central bank or government.",
        },
        "1": {"name": "none", "description": "none"},
    },
    "commodities market": {
        "0": {
            "name": "energy market",
            "description": "The market for commodities such as electricity, heat, and fuel products",
        },
        "1": {
            "name": "metal",
            "description": "Markets for trading base metals such as copper, aluminium, steel, zinc etc",
        },
        "2": {"name": "none", "description": "none"},
    },
    "agriculture": {"0": {"name": "none", "description": "none"}},
    "business service": {
        "0": {
            "name": "consultancy",
            "description": "Providers of expert knowledge in a wide range of fields usually on a temporary, contract basis",
        },
        "1": {
            "name": "employment agency",
            "description": "A service helping people find jobs, and companies to find workers",
        },
        "2": {
            "name": "legal service",
            "description": "Lawyers, notaries and others who help companies and individuals deal with state, federal and local laws",
        },
        "3": {
            "name": "payment service",
            "description": "Services for executing payments including cash, cheque, credit card, debit card, direct debit, electronic funds transfer, internet banking, electronic and mobile payment.",
        },
        "4": {
            "name": "rental service",
            "description": "Companies that provide items on a short-term rental basis, including motor vehicles, clothing, tools, heavy equipment and other supplies",
        },
        "5": {
            "name": "shipping and postal service",
            "description": "Organisations that prepare and transport packages and documents for individuals or companies by any means, including postal services",
        },
        "6": {
            "name": "trade show or expo",
            "description": "Market place to display and trade goods or services",
        },
        "7": {"name": "none", "description": "none"},
    },
    "chemicals": {"0": {"name": "none", "description": "none"}},
    "computing and information technology": {
        "0": {
            "name": "computer and telecommunications hardware",
            "description": "Physical devices used to provide computer and telecommunication service, such as modems, keyboards, hard drives, telephones, routers and monitors",
        },
        "1": {
            "name": "satellite technology",
            "description": "Hardware and software that enables ground-based devices to send signals to each other via an orbiting satellite.",
        },
        "2": {
            "name": "semiconductor and electronic component",
            "description": "The basic components that together create working electronic devices such as computer chips, transistors, diodes and integrated circuits",
        },
        "3": {
            "name": "software and applications",
            "description": "Computer programs including mobile or web apps and operating systems",
        },
        "4": {
            "name": "telecommunication service",
            "description": "Services provided by commercial companies that facilitate connections between telephones and computers",
        },
        "5": {
            "name": "wireless technology",
            "description": "Technology and services that permit the transfer of information between separated points without physical connection, including Bluetooth and Wi-Fi networks",
        },
        "6": {"name": "none", "description": "none"},
    },
    "construction and property": {
        "0": {
            "name": "building material",
            "description": "Manufacturing of the materials used in construction, such as wallboard, lumber and wire",
        },
        "1": {
            "name": "commercial real estate",
            "description": "The building and sale of property used for business purposes rather than as a living space",
        },
        "2": {
            "name": "infrastructure projects",
            "description": "The construction of the fundamental facilities and systems serving a country, city, or other area, including roads, bridges, dams, tunnels, telecommunications and electrical grids",
        },
        "3": {
            "name": "residential real estate",
            "description": "The building and sale of property to be used as living space",
        },
        "4": {"name": "none", "description": "none"},
    },
    "consumer goods": {
        "0": {
            "name": "beverage and grocery",
            "description": "The production and sale of foodstuffs",
        },
        "1": {
            "name": "clothing",
            "description": "The manufacturing and purchasing of apparel",
        },
        "2": {
            "name": "consumer electronics",
            "description": "Electronic devices, such as computers, smart phones or televisions, designed and sold for personal use",
        },
        "3": {
            "name": "furnishings and furniture",
            "description": "Manufacture of furniture, wallpaper, paints and fabrics for interior decoration",
        },
        "4": {
            "name": "handicrafts",
            "description": "The creators and sellers of crafts and the making and selling of the supplies used to make those crafts",
        },
        "5": {
            "name": "luxury good",
            "description": "Non-essential high-end goods, such as leather bags, jewellery or supercars",
        },
        "6": {
            "name": "pet product and service",
            "description": "Hygiene products, care and nutrition for pets",
        },
        "7": {
            "name": "tobacco and nicotine",
            "description": "The sale and manufacturing of tobacco products for consumers, including cigarettes, e-cigarettes and vaping cartridges",
        },
        "8": {
            "name": "toy and game",
            "description": "Children's playthings or collectible items for adults, such as dolls, action figures and miniatures",
        },
        "9": {"name": "none", "description": "none"},
    },
    "energy and resource": {
        "0": {
            "name": "biofuel",
            "description": "Fuel that is derived from biomass, such as ethanol",
        },
        "1": {
            "name": "coal",
            "description": "Production and mining of anthracite and bituminous products for use in power production",
        },
        "2": {
            "name": "nuclear power",
            "description": "Use of radioactive materials for power production",
        },
        "3": {
            "name": "oil and gas",
            "description": "The exploration, extraction, refining, transporting and marketing of petroleum products and natural gas",
        },
        "4": {
            "name": "renewable energy",
            "description": "Energy derived from sustainable sources",
        },
        "5": {"name": "none", "description": "none"},
    },
    "financial and business service": {"0": {"name": "none", "description": "none"}},
    "financial service": {
        "0": {
            "name": "accountancy and auditing",
            "description": "Companies that provide balance sheet preparation and budget reconciliation services and examine accuracy of financial statements",
        },
        "1": {
            "name": "asset management",
            "description": "Managing investments on behalf of others",
        },
        "2": {
            "name": "banking",
            "description": "Financial institutions and services for storing, transmitting, receiving and delivering money",
        },
        "3": {
            "name": "financial advisory service",
            "description": "Financial advisers, as opposed to stock dealers or consultants",
        },
        "4": {
            "name": "insurance",
            "description": "A risk-taking venture that allows individuals to pay small amounts periodically to guard financially against unexpected events",
        },
        "5": {
            "name": "loans and lending",
            "description": "An agreement by an individual or institution to borrow money with an agreed interest rate and time for its return",
        },
        "6": {
            "name": "personal finance and investment",
            "description": "Investing an individual's savings in the hope of future gains",
        },
        "7": {
            "name": "stock broking",
            "description": "The buying and selling of company shares on behalf of individuals or other entities",
        },
        "8": {"name": "none", "description": "none"},
    },
    "healthcare industry": {
        "0": {
            "name": "biotechnology business",
            "description": "The business of using engineering technology to study and solve problems of living organisms",
        },
        "1": {
            "name": "health care provider",
            "description": "Organisations and individuals that provide medical services at all levels",
        },
        "2": {
            "name": "medical equipment",
            "description": "Manufacture of medical and surgical devices for diagnosis and treatment such as optical and imaging equipment",
        },
        "3": {
            "name": "pharmaceutical",
            "description": "The production of medicines from various chemicals and natural substances and the research and discovery around new medications",
        },
        "4": {"name": "none", "description": "none"},
    },
    "manufacturing and engineering": {
        "0": {
            "name": "aerospace",
            "description": "Companies that assemble or manufacture components for airplanes and space ships.",
        },
        "1": {
            "name": "automotive",
            "description": "Companies that manufacture automotive components and assemble automobiles",
        },
        "2": {
            "name": "defence equipment",
            "description": "Manufacturers of guns, tanks, ships or other equipment for military and non-military protection services",
        },
        "3": {
            "name": "electrical appliance",
            "description": "Makers of large and small electrical goods for use in homes or business",
        },
        "4": {
            "name": "heavy engineering",
            "description": "Manufacturers of engineering equipment, such as cranes and bulldozers, for use in major construction projects",
        },
        "5": {
            "name": "machine manufacturing",
            "description": "Manufacturers of turbines, engines, fans, pumps, motors and other components for powered equipment",
        },
        "6": {
            "name": "railway manufacturing",
            "description": "Manufactures of rolling stock and suppliers for the maintenance and repair of railroads",
        },
        "7": {
            "name": "shipbuilding",
            "description": "Manufacturers of ships and submersibles and suppliers for the maintenance and repair of these vessels",
        },
        "8": {"name": "none", "description": "none"},
    },
    "media and entertainment industry": {
        "0": {
            "name": "advertising",
            "description": "Methods of promoting goods and services to consumers",
        },
        "1": {
            "name": "books and publishing",
            "description": "The business of producing and selling books, including e-books and audiobooks",
        },
        "2": {
            "name": "film industry",
            "description": "The business of making, selling and distributing films",
        },
        "3": {
            "name": "music industry",
            "description": "Recording, production and marketing of music",
        },
        "4": {
            "name": "news industry",
            "description": "The production and distribution of content about newsworthy events through print, broadcast, video or electronic media",
        },
        "5": {
            "name": "podcast",
            "description": "Podcast networks and the people who create and distribute audio content, typically in a series format, to audiences",
        },
        "6": {
            "name": "public relations",
            "description": "The business of managing and disseminating information from an individual or an organization to the public in order to influence their perception",
        },
        "7": {
            "name": "radio industry",
            "description": "Companies and organisations involved in the broadcast of radio stations and their content to the public",
        },
        "8": {
            "name": "satellite and cable service",
            "description": "The business of transmitting news, entertainment and information via satellite or cable television services",
        },
        "9": {
            "name": "streaming service",
            "description": "Providers of entertainment (music, movies, series, etc.) that deliver the content via an internet connection to the subscriber's computer, TV or mobile device",
        },
        "10": {
            "name": "television industry",
            "description": "The production and broadcasting of television content",
        },
        "11": {"name": "none", "description": "none"},
    },
    "metal and mineral mining and refining": {
        "0": {
            "name": "precious material",
            "description": "The mining, refining and sale of materials such as gold, silver, precious metals, diamonds and rare earths",
        },
        "1": {"name": "none", "description": "none"},
    },
    "process industry": {"0": {"name": "none", "description": "none"}},
    "sales channel": {
        "0": {
            "name": "auction",
            "description": "Auction houses and all types of auctions, such as police auctions and silent auctions",
        },
        "1": {
            "name": "retail",
            "description": "The selling of goods directly to consumers",
        },
        "2": {
            "name": "wholesale",
            "description": "The first link in the sales chain after production",
        },
        "3": {"name": "none", "description": "none"},
    },
    "tourism and leisure industry": {
        "0": {
            "name": "casinos and gambling",
            "description": "Organisations providing outlets for betting money on games of chance or animal races",
        },
        "1": {
            "name": "hotel and accommodation",
            "description": "The business of providing lodging to travellers",
        },
        "2": {
            "name": "recreational and sporting goods",
            "description": "Manufacture of goods for leisure activities",
        },
        "3": {
            "name": "restaurant and catering",
            "description": "The business of providing prepared food for customers",
        },
        "4": {
            "name": "tour operator",
            "description": "Operators of trips either locally or internationally",
        },
        "5": {"name": "none", "description": "none"},
    },
    "transport": {
        "0": {
            "name": "air transport",
            "description": "The movement of passengers and freight by air",
        },
        "1": {
            "name": "logistics",
            "description": "Supply chain, inventory management and transportation of products.",
        },
        "2": {
            "name": "public transport",
            "description": "Forms of transportation, such as buses and trains, that charge set fares, run on fixed routes and are available to the general public",
        },
        "3": {
            "name": "railway transport",
            "description": "The movement of passengers and freight by rail",
        },
        "4": {
            "name": "road transport",
            "description": "The movement of passengers and freight by road",
        },
        "5": {
            "name": "shared transport",
            "description": "A network of vehicles, such as cars, bikes and scooters, that can be rented by travellers on an as-needed basis for short-term use",
        },
        "6": {
            "name": "taxi and ride-hailing",
            "description": "On-demand ride service, provided by taxi companies or tech companies such as Uber and Lyft, the drivers who transport passengers and the rules and regulations imposed upon these companies within a region",
        },
        "7": {
            "name": "waterway and maritime transport",
            "description": "Commercial movement of people or goods via boats, ships and water",
        },
        "8": {"name": "none", "description": "none"},
    },
    "utilities": {
        "0": {
            "name": "electricity",
            "description": "The power line distribution system and the sale of electrical power at wholesale and retail levels",
        },
        "1": {
            "name": "heating and cooling",
            "description": "The business of supplying heat or cooling to private residences and commercial buildings",
        },
        "2": {
            "name": "waste management",
            "description": "The collecting, disposing or recycling of household and business waste",
        },
        "3": {
            "name": "water supply",
            "description": "The business of providing water for household and commercial use",
        },
        "4": {"name": "none", "description": "none"},
    },
    "college and university": {"0": {"name": "none", "description": "none"}},
    "land resources": {
        "0": {
            "name": "forests",
            "description": "Open areas of trees either available for public enjoyment, or for commercial purposes",
        },
        "1": {
            "name": "mountains",
            "description": "Elevated land masses formed over the ages either by erosion, volcanic eruption, or movement of massive geographical formations called plates",
        },
        "2": {"name": "none", "description": "none"},
    },
    "water": {
        "0": {
            "name": "oceans",
            "description": "Salt water masses separating continents or other major geographical masses. smaller forms are seas or lakes or ponds",
        },
        "1": {
            "name": "rivers",
            "description": "Moving water areas bounded by land that extend from earth sources and meander through land areas to join with other water areas. In smaller forms they are creeks, rivulets, streams etc",
        },
        "2": {
            "name": "wetlands",
            "description": "Areas generally marshy and not either under water or dry land. Often related to aquifers for water quality and/or wildlife",
        },
        "3": {"name": "none", "description": "none"},
    },
    "animal": {
        "0": {"name": "animal disease", "description": "Disease affecting animals"},
        "1": {
            "name": "pests",
            "description": "Animals or insects that invade a human space causing destruction or unsanitary conditions",
        },
        "2": {"name": "none", "description": "none"},
    },
    "flowers and plants": {
        "0": {
            "name": "plant disease",
            "description": "Disorders affecting plants caused either by parasites or environmental factors",
        },
        "1": {"name": "none", "description": "none"},
    },
    "communicable disease": {
        "0": {
            "name": "epidemic and pandemic",
            "description": "A disease that affects a large number of people within a community, population, region or that has spread to multiple countries or continents across the world",
        },
        "1": {
            "name": "viral disease",
            "description": "Diseases caused by an infection by viruses",
        },
        "2": {"name": "none", "description": "none"},
    },
    "medical condition": {
        "0": {
            "name": "obesity",
            "description": "A condition of body weight generally considered 20 percent above the norm for gender, age, height and bone structure",
        },
        "1": {"name": "none", "description": "none"},
    },
    "mental health and disorder": {
        "0": {
            "name": "anxiety and stress",
            "description": "A mental health disorder characterised by feelings of worry, anxiousness or fear that are strong enough to interfere with one's daily activities",
        },
        "1": {
            "name": "depression",
            "description": "A mental health disorder characterised by persistently depressed mood and loss of interest in activities, causing significant impairment in daily life",
        },
        "2": {
            "name": "eating disorder",
            "description": "Anorexia, bulimia, overeating and similar illnesses",
        },
        "3": {"name": "none", "description": "none"},
    },
    "diet": {
        "0": {
            "name": "dietary supplement",
            "description": "Nutrients taken in addition to food to bolster health",
        },
        "1": {"name": "none", "description": "none"},
    },
    "health care approach": {
        "0": {
            "name": "conventional medicine",
            "description": "The practice of diagnosis, treatment and prevention of disease based on modern scientific research",
        },
        "1": {
            "name": "herbal medicine",
            "description": "Treatment based on the use of herbs and other plants to cure or alleviate symptoms",
        },
        "2": {
            "name": "holistic medicine",
            "description": "Treatment of the whole person including mental and environmental factors in addition to treating symptoms",
        },
        "3": {
            "name": "traditional Chinese medicine",
            "description": "The practice of diagnosis, treatment and prevention of disease based on traditional methods developed in Eastern Asia",
        },
        "4": {"name": "none", "description": "none"},
    },
    "medical specialisation": {
        "0": {
            "name": "dentistry",
            "description": "The medical profession and field of study devoted to diagnosing, preventing and treating oral conditions",
        },
        "1": {
            "name": "eye care",
            "description": "The medical profession and field of study devoted to diagnosing, preventing and treating eye conditions",
        },
        "2": {
            "name": "paediatrics",
            "description": "Medical specialisation that focuses on treating the young, including premature babies, infant care, childhood diseases and teenage health and behaviour problems",
        },
        "3": {
            "name": "veterinary medicine",
            "description": "The medical profession and field of study devoted to diagnosis, prevention and treatment of medical conditions in animals",
        },
        "4": {"name": "none", "description": "none"},
    },
    "employment training": {"0": {"name": "none", "description": "none"}},
    "wages and benefits": {
        "0": {
            "name": "profit sharing",
            "description": "A system by which employees are paid a share of the net profits of their employer. These earnings are distinct from and additional to regular wages.",
        },
        "1": {
            "name": "social security",
            "description": "a government system that provides monetary assistance to people with inadequate or no incomes, such as retirees, disabled people or carers",
        },
        "2": {"name": "none", "description": "none"},
    },
    "collective agreements": {"0": {"name": "none", "description": "none"}},
    "labour dispute": {
        "0": {
            "name": "labour strike",
            "description": "Groups of employees agreeing to cease work activities with the aim of achieving better pay or work conditions",
        },
        "1": {"name": "none", "description": "none"},
    },
    "game": {
        "0": {"name": "board game", "description": "A game played on a board"},
        "1": {"name": "card game", "description": "A game played with a pack of cards"},
        "2": {
            "name": "children's game",
            "description": "A game designed for and most often played by children",
        },
        "3": {"name": "dice game", "description": "A game played using dice only"},
        "4": {"name": "outdoor game", "description": "A game played in an open space"},
        "5": {
            "name": "puzzle",
            "description": "A game played solving logic problems for entertainment",
        },
        "6": {"name": "tile game", "description": "A game played using tiles"},
        "7": {
            "name": "video game",
            "description": "A game played using a video display",
        },
        "8": {"name": "none", "description": "none"},
    },
    "hobby": {
        "0": {
            "name": "automobile enthusiasm",
            "description": "Interest in new and classic cars",
        },
        "1": {
            "name": "bicycle enthusiasm",
            "description": "Interest in new and classic manpowered cycles",
        },
        "2": {
            "name": "collecting",
            "description": "The hobby of seeking, locating, acquiring, organising, cataloguing, displaying, storing or maintaining items that are of interest to an individual collector",
        },
        "3": {
            "name": "food and drink enthusiasm",
            "description": "Interest in eating and drinking",
        },
        "4": {
            "name": "motorcycle enthusiasm",
            "description": "Interest in new and classic motor-powered cycles",
        },
        "5": {"name": "none", "description": "none"},
    },
    "holiday": {
        "0": {
            "name": "Halloween",
            "description": "A celebration observed in a number of countries on 31 October with activities including trick-or-treating, wearing costumes, carving pumpkins, visiting haunted attractions, telling scary stories and watching horror films",
        },
        "1": {
            "name": "public holiday",
            "description": "A day of celebration declared by a government",
        },
        "2": {"name": "none", "description": "none"},
    },
    "leisure venue": {
        "0": {
            "name": "amusement park",
            "description": "A park providing various rides and entertainment attractions for both adults and children, including theme parks",
        },
        "1": {
            "name": "bar",
            "description": "A business where drinks are prepared and served to the public for consumption on the premises",
        },
        "2": {
            "name": "cafe",
            "description": "A small business where drinks and snacks are prepared and served - its specifics may depend on the local culture",
        },
        "3": {
            "name": "nightclub",
            "description": "A commercial establishment providing music, or other entertainment along with food and drink to selected clientele",
        },
        "4": {
            "name": "restaurant",
            "description": "A business where meals are prepared and served to the public",
        },
        "5": {
            "name": "zoo",
            "description": "A park where visitors can see both wild and tame animals that are kept in cages or enclosed areas",
        },
        "6": {"name": "none", "description": "none"},
    },
    "outdoor recreational activities": {
        "0": {
            "name": "fishing",
            "description": "A recreational activity involving the use of baits, lures, weapons and traps for the capture of aquatic species.",
        },
        "1": {
            "name": "horseback riding",
            "description": "The riding of horses for leisure or light exercise.",
        },
        "2": {
            "name": "hunting",
            "description": "An activity involving the use of weapons or traps for the capturing of animals",
        },
        "3": {
            "name": "recreational hiking and climbing",
            "description": "Sportive activities in the mountains including climbing and hiking",
        },
        "4": {
            "name": "scuba diving",
            "description": "Underwater diving with the use of a self-contained underwater breathing apparatus",
        },
        "5": {"name": "none", "description": "none"},
    },
    "travel and tourism": {"0": {"name": "none", "description": "none"}},
    "house and home": {
        "0": {
            "name": "gardening",
            "description": "Interest in working in one's garden",
        },
        "1": {
            "name": "home renovation",
            "description": "Interest in renovating one's property",
        },
        "2": {
            "name": "interior decoration",
            "description": "Interest in decorating one's home",
        },
        "3": {"name": "none", "description": "none"},
    },
    "trend": {
        "0": {
            "name": "body modification",
            "description": "Actions taken to permanently or semi-permanently change body appearance, such as piercing and tattooing",
        },
        "1": {"name": "none", "description": "none"},
    },
    "political campaigns": {
        "0": {
            "name": "campaign finance",
            "description": "The money that makes campaigns for public office possible",
        },
        "1": {"name": "none", "description": "none"},
    },
    "civil and public service": {
        "0": {
            "name": "civilian service",
            "description": "Unpaid service for the community as civilian",
        },
        "1": {
            "name": "public employees",
            "description": "People employed by a government at all levels",
        },
        "2": {
            "name": "public officials",
            "description": "Individuals, usually elected, who are in public service or commonly in the public eye.",
        },
        "3": {"name": "none", "description": "none"},
    },
    "defence": {
        "0": {
            "name": "armed forces",
            "description": "Those employed by a government to conduct war, or to enforce the security of a nation",
        },
        "1": {
            "name": "military equipment",
            "description": "Equipment issued to members of the armed forces",
        },
        "2": {
            "name": "security measures (defence)",
            "description": "Means of making a nation, a state, a building or a person secure from harm and outside interference.",
        },
        "3": {"name": "none", "description": "none"},
    },
    "government budget": {
        "0": {
            "name": "public finance",
            "description": "The money of government used for paying for public programmes and services and public debt",
        },
        "1": {"name": "none", "description": "none"},
    },
    "legislative body": {
        "0": {
            "name": "lower house (legislature)",
            "description": "Lower chamber of a legislative body, such as the US House of Representatives or UK House of Commons",
        },
        "1": {
            "name": "upper house (legislature)",
            "description": "Senior chamber of a legislative body, such as the US Senate or UK House of Lords",
        },
        "2": {"name": "none", "description": "none"},
    },
    "economic policy": {
        "0": {
            "name": "economic development incentive",
            "description": "funding, financial incentive programmes and subsidies to stimulate businesses and parts of the economy",
        },
        "1": {
            "name": "nationalisation",
            "description": "State takeover of private companies or properties",
        },
        "2": {
            "name": "privatisation",
            "description": "The transfer of state-owned companies or properties to private owners",
        },
        "3": {
            "name": "state-owned enterprise",
            "description": "The government as owner of companies, either complete or partial",
        },
        "4": {"name": "none", "description": "none"},
    },
    "interior policy": {
        "0": {
            "name": "data protection policy",
            "description": "Efforts to protect personal information in either written, oral or electronic form",
        },
        "1": {
            "name": "housing and urban planning policy",
            "description": "Systematic planning of urban and suburban areas and the housing within those areas",
        },
        "2": {
            "name": "infrastructure policy",
            "description": "Policies regarding the development and maintenance of the fundamental facilities of a country, city or other area that make business activity possible, such as communication, transportation and distribution networks",
        },
        "3": {
            "name": "integration policy",
            "description": "Improving the co-existence of groups of the society",
        },
        "4": {
            "name": "pension and welfare policy",
            "description": "Government policies affecting the well-being of its citizens through unemployment benefits, state pensions and other similar payments",
        },
        "5": {
            "name": "personal data collection policy",
            "description": "The collection, by government or other entities of information on individuals",
        },
        "6": {
            "name": "personal weapon control policy",
            "description": "Government control of personal ownership of firearms and other offensive weapons, including control of weapons used for sports through licenses and other means",
        },
        "7": {
            "name": "planning inquiries",
            "description": "Public hearings or planning inquiries on proposed constructions, e.g. Construction of water driven power station in a National Park.",
        },
        "8": {
            "name": "policy towards indigenous people",
            "description": "Government policies toward indigenous peoples",
        },
        "9": {
            "name": "regional development policy",
            "description": "Public or private actions carried out to develop a region.",
        },
        "10": {"name": "none", "description": "none"},
    },
    "regulation of industry": {
        "0": {
            "name": "food and drink regulations",
            "description": "Government policies relating to food and drink",
        },
        "1": {"name": "none", "description": "none"},
    },
    "diplomacy": {
        "0": {
            "name": "summit meetings",
            "description": "Includes meetings of leaders, foreign and finance ministers from the Group of Eight major nations and Group of Seven industrialized nations.",
        },
        "1": {
            "name": "treaty",
            "description": "A treaty (as defined by the Vienna Convention on the Law of Treaties) is a written agreement between international entities that is binding under international law.",
        },
        "2": {"name": "none", "description": "none"},
    },
    "political parties and movements": {
        "0": {
            "name": "political leadership",
            "description": "The leaders within a political party",
        },
        "1": {"name": "none", "description": "none"},
    },
    "political system": {
        "0": {
            "name": "democracy",
            "description": "Government in which the people hold the power either directly, or through elected officials.",
        },
        "1": {
            "name": "dictatorship",
            "description": "Government in which a single individual or a small group of individuals hold power without consent of the people",
        },
        "2": {"name": "none", "description": "none"},
    },
    "Christianity": {
        "0": {
            "name": "Catholicism",
            "description": "Largest Christian religion in the world encompassing the Roman Catholic Church which is led by the pope, and Old Catholicism, a breakaway movement founded in 1870 that denies the dogma of infallibility of the pope",
        },
        "1": {
            "name": "Christian Orthodoxy",
            "description": "Eastern rite churches which are characterised by their continuity with the apostolic church, their liturgy and their territorial churches, mainly in eastern and south-eastern Europe and the Middle East",
        },
        "2": {
            "name": "Mormonism",
            "description": "Christian religion founded in New York State in the 1820s that follows the teachings of Joseph Smith and the *Book of Mormon*",
        },
        "3": {
            "name": "Protestantism",
            "description": "Christian denominations that were formed through the 16th century Reformation movement",
        },
        "4": {"name": "none", "description": "none"},
    },
    "Islam": {
        "0": {
            "name": "Shia Islam",
            "description": "The second largest branch of Islam believing that the Prophet Muhammad designated Ali ibn Abi Talib as his successor",
        },
        "1": {
            "name": "Sunni Islam",
            "description": "The largest branch of Islam believing that the Prophet Muhammad did not designate a successor",
        },
        "2": {"name": "none", "description": "none"},
    },
    "Judaism": {
        "0": {
            "name": "Hasidism",
            "description": "Jewish religious group that believes that the Torah is the literal word of God and that carrying out this word is what gives meaning and purpose to life",
        },
        "1": {"name": "none", "description": "none"},
    },
    "biology": {
        "0": {
            "name": "botany",
            "description": "The study of the physical and physiological structure, genetics, ecology and other aspects of plants",
        },
        "1": {
            "name": "genetics",
            "description": "The study of genes in living organisms, and of their role in heredity, development or genetic adaptation",
        },
        "2": {
            "name": "palaeontology",
            "description": "The study of prehistoric life forms, geological periods and fossils",
        },
        "3": {
            "name": "physiology",
            "description": "The study of the vital processes, internal organs or functional mechanisms of living organisms",
        },
        "4": {
            "name": "zoology",
            "description": "The study of the biology, physiology, development, behaviour or other aspects of animals",
        },
        "5": {"name": "none", "description": "none"},
    },
    "physics": {
        "0": {
            "name": "electromagnetism",
            "description": "The study of the physical interactions between electrically charged particles and magnetic fields",
        },
        "1": {
            "name": "nuclear physics",
            "description": "The study of the structure and behaviour of atomic nuclei",
        },
        "2": {"name": "none", "description": "none"},
    },
    "scientific exploration": {
        "0": {
            "name": "space exploration",
            "description": "The scientific exploration of outer space through manned and unmanned missions",
        },
        "1": {"name": "none", "description": "none"},
    },
    "aerospace engineering": {
        "0": {
            "name": "rocketry",
            "description": "The study, design, development and construction of rockets",
        },
        "1": {"name": "none", "description": "none"},
    },
    "information technology and computer science": {
        "0": {
            "name": "artificial intelligence",
            "description": "An attempt to let computers simulate how the human brain works by applying statistical, heuristic or machine learning methods and algorithms to large datasets. Enables a long range of automatic functions like image recognition and categorisation.",
        },
        "1": {"name": "none", "description": "none"},
    },
    "micro science": {
        "0": {
            "name": "nanotechnology",
            "description": "Manipulating objects at the molecular scale",
        },
        "1": {"name": "none", "description": "none"},
    },
    "family planning": {
        "0": {
            "name": "abortion",
            "description": "The intentional termination of a pregnancy for elective or medical reasons",
        },
        "1": {
            "name": "contraception",
            "description": "A method or device used to prevent pregnancy",
        },
        "2": {"name": "none", "description": "none"},
    },
    "death and dying": {
        "0": {
            "name": "euthanasia",
            "description": "The practice of humanely ending the life of a person suffering from a terminal illness",
        },
        "1": {
            "name": "suicide",
            "description": "The intentional taking of one's own life",
        },
        "2": {"name": "none", "description": "none"},
    },
    "archery": {
        "0": {
            "name": "crossbow shooting",
            "description": "Shooting with crossbow on targets from different distances",
        },
        "1": {
            "name": "longbow",
            "description": "Shooting with longbow on targets from different distances. The competition is held outdoors on an open (flat) field.",
        },
        "2": {"name": "none", "description": "none"},
    },
    "artistic swimming": {
        "0": {
            "name": "synchronised free routine",
            "description": "In the free programme, music, movements and their order of execution are not restricted.",
        },
        "1": {
            "name": "synchronised technical routine",
            "description": "Contestants obtain points from 10 sitting judges by executing certain synchronised artistic shapes and movements in the water. In the technical programme, competitors must execute a range of specific moves in a given order.",
        },
        "2": {"name": "none", "description": "none"},
    },
    "athletics": {
        "0": {
            "name": "cross-country run",
            "description": "Competitors run over rough ground and not on a track",
        },
        "1": {
            "name": "decathlon",
            "description": "Individual men's competition which involves accumulating points in 10 different disciplines over two days: 1st day - 100m, long-jump, shot-putt, high-jump, 400m. 2nd day - 110m hurdles, discus, pole-vault, javelin and 1,500 metres.",
        },
        "2": {
            "name": "discus throw",
            "description": "Competitors stand in a netted circle with a 2.50 metres diameter and with a turning motion attempt to throw a discus weighing 2kg for men and 1kg for women as far as possible",
        },
        "3": {
            "name": "hammer throw",
            "description": "Competitors throw a hammer consisting of a metal ball, chain and handle as far as they can from a netted circle which is 2.13 metres in diameter. The hammer weighs 7.26kg for men and 4kg for women",
        },
        "4": {
            "name": "heptathlon",
            "description": "Competition involving seven separate disciplines over two days. 1st day - 100m hurdles, high jump, shot put, 200 metres. 2nd day - long-jump, javelin, 800 metres",
        },
        "5": {
            "name": "high jump",
            "description": "Competitors build up speed over a short sprint and then jump as high as possible over a horizontal bar",
        },
        "6": {
            "name": "hurdles",
            "description": "A sprint running race where athletes jump over a series of upright frames",
        },
        "7": {
            "name": "javelin throw",
            "description": "Competitors in a specially-designated throwing area attempt to fling a spear-like javelin as far as possible. The javelin weighs 800 grams for men and 600 grams for women.",
        },
        "8": {
            "name": "long distance run",
            "description": "A running race at distances for more than 1500 metres",
        },
        "9": {
            "name": "long jump",
            "description": "Competitors build up speed over a short sprint and then jump in one leap as far as possible",
        },
        "10": {
            "name": "middle distance run",
            "description": "A running race at distances for more than 400 metres and up to and including 1500 metres",
        },
        "11": {
            "name": "pentathlon",
            "description": "Only indoor, 60m hurdles, high jump, shot put, long jump, 800 m",
        },
        "12": {
            "name": "pole vault",
            "description": "Competitors use a flexible pole to propel themselves feet-first into the air and clear a bar which is raised higher at each round of jumps.",
        },
        "13": {
            "name": "race walking",
            "description": "A race requiring the competitor to have always one foot on the ground",
        },
        "14": {
            "name": "relay run",
            "description": "A team of athletes run a relay over identical distances",
        },
        "15": {
            "name": "shot put",
            "description": "Competitors stand in a circle with a 2.13 metres diameter and attempt to throw a metal ball weighing 7.26 kg for men and 4kg for women as far as possible. The longest throw wins.",
        },
        "16": {
            "name": "sprint run",
            "description": "A running race at distances of up to and including 400 metres",
        },
        "17": {
            "name": "steeplechase (athletics)",
            "description": "Obstacle race in athletics including barriers and water jumps",
        },
        "18": {
            "name": "triple jump",
            "description": "Competitors build up speed over a short sprint and then attempt to jump as far forward as they can using a hop, skip and a jump technique.",
        },
        "19": {"name": "none", "description": "none"},
    },
    "baseball": {
        "0": {
            "name": "rubberball baseball",
            "description": "Sometimes called ''soft baseball,'' the game is played with a rubber baseball of varying degrees of hardness depending upon the age and level of the players.",
        },
        "1": {"name": "none", "description": "none"},
    },
    "boxing": {"0": {"name": "none", "description": "none"}},
    "canoeing": {"0": {"name": "none", "description": "none"}},
    "competitive dancing": {
        "0": {
            "name": "breaking (breakdance)",
            "description": "Dancing competition featuring an urban dance style that originated in the United States in the 1970s with roots in hip-hop culture and characterised by acrobatic movements, stylised footwork, and the key role played by the DJ and the MC during battles",
        },
        "1": {"name": "none", "description": "none"},
    },
    "curling": {
        "0": {
            "name": "icestock sport",
            "description": "Similar to curling, played on targets on ice, different stones with straight handle and different rules, played in alpine countries",
        },
        "1": {"name": "none", "description": "none"},
    },
    "cycling": {
        "0": {
            "name": "artistic cycling",
            "description": "Individual or teams on one or two bicycles in an arena. Points are awarded by a jury.",
        },
        "1": {
            "name": "bmx freestyle",
            "description": "Riders are given a fixed time to perform acrobatics tricks and skills, with tricks scored on multiple aspects including difficulty, originality, execution, height and creativity",
        },
        "2": {
            "name": "bmx racing",
            "description": "Bicycle racing in with inline start and various obstacles over off-road circuits.",
        },
        "3": {
            "name": "cycle ball",
            "description": "Competitive team sport using bicycles. One team against another with two persons per team. The aim is for competitors to move the ball using the front and rear wheels without letting their feet touch the ground.",
        },
        "4": {
            "name": "mountain biking",
            "description": "All-terrain, off-road bicycle riding requiring endurance and specially adapted mountain bikes",
        },
        "5": {
            "name": "road cycling",
            "description": "Cycling events held on roads, including road races and time trials",
        },
        "6": {"name": "none", "description": "none"},
    },
    "diving": {
        "0": {
            "name": "platform diving",
            "description": "Divers take off from a high platform",
        },
        "1": {
            "name": "springboard diving",
            "description": "Divers dive from a high springboard.",
        },
        "2": {
            "name": "synchronised diving",
            "description": "Two competitors from the same team dive off at the same time from separate platforms or springboards. As well as being judged on the standard criteria they are also awarded marks for synchronisation.",
        },
        "3": {"name": "none", "description": "none"},
    },
    "dog racing": {"0": {"name": "none", "description": "none"}},
    "equestrian": {"0": {"name": "none", "description": "none"}},
    "fencing": {"0": {"name": "none", "description": "none"}},
    "figure skating": {"0": {"name": "none", "description": "none"}},
    "golf": {
        "0": {
            "name": "mini golf",
            "description": "A game where small hard balls must be holed on an artificial course in as few strokes from the club as possible",
        },
        "1": {"name": "none", "description": "none"},
    },
    "gymnastics": {
        "0": {
            "name": "artistic gymnastics",
            "description": "Gymnasts perform artistic and acrobatic moves on different apparatus. There are 6 events for men and 4 for women",
        },
        "1": {
            "name": "rhythmic gymnastics",
            "description": "Mixture of dance and gymnastic moves",
        },
        "2": {
            "name": "trampoline",
            "description": "Competitors perform complicated twists and turns whilst bouncing on the trampoline.",
        },
        "3": {"name": "none", "description": "none"},
    },
    "horse racing": {"0": {"name": "none", "description": "none"}},
    "ice hockey": {
        "0": {
            "name": "sledge hockey",
            "description": "Like ice hockey but instead of skates small sledges are used. Competitors move by pushing with the arms",
        },
        "1": {"name": "none", "description": "none"},
    },
    "kayaking": {"0": {"name": "none", "description": "none"}},
    "martial arts": {
        "0": {"name": "Taekwon-Do", "description": "A martial art of Korean origin"},
        "1": {"name": "judo", "description": "A defensive martial art."},
        "2": {
            "name": "jukendo",
            "description": "Japanese traditional martial art using a model rifle made of wood. 'Juken' means a rifle or gun with blade (bayonet)",
        },
        "3": {
            "name": "karate",
            "description": "A martial art where chops, punches, kicks and throws are used to defeat an opponent.",
        },
        "4": {
            "name": "kendo",
            "description": "Japanese traditional martial art using a bamboo sword, sometimes called Japanese fencing",
        },
        "5": {
            "name": "kickboxing",
            "description": "Stand-up combat sport based on kicking and punching an opponent",
        },
        "6": {
            "name": "krav maga",
            "description": "Fighting and self-defence sport that combines elements from aikido, boxing, judo, karate and wrestling",
        },
        "7": {
            "name": "kyudo",
            "description": "Japanese traditional martial art using a bamboo bow and arrows, sometimes called Japanese archery",
        },
        "8": {
            "name": "mixed martial arts",
            "description": "A full-contact combat sport using techniques from various combat sports and martial arts",
        },
        "9": {
            "name": "naginata",
            "description": "Japanese traditional martial art using a pole sword made of wood. 'Naginata' means a spear with a curved blade",
        },
        "10": {
            "name": "sambo (martial art)",
            "description": "Style of martial art originating in the Soviet Union that is recognised as a form of amateur wrestling",
        },
        "11": {"name": "wushu", "description": "Chinese traditional martial art"},
        "12": {"name": "none", "description": "none"},
    },
    "motor car racing": {"0": {"name": "none", "description": "none"}},
    "motorcycling": {"0": {"name": "none", "description": "none"}},
    "mountain climbing": {
        "0": {
            "name": "ice climbing",
            "description": "Climbing of ice features such as icefalls and frozen cliffs",
        },
        "1": {"name": "mountaineering", "description": "Competitive alpine climbing"},
        "2": {"name": "none", "description": "none"},
    },
    "orienteering": {
        "0": {
            "name": "ski orienteering",
            "description": "An individual ski time-trial over a route marked out by beacons, that the competitor has to search out and find in a specific order. The contestant makes his way with the help of a compass and map",
        },
        "1": {"name": "none", "description": "none"},
    },
    "rodeo": {
        "0": {"name": "bareback bronc", "description": "Rodeo discipline"},
        "1": {"name": "barrel racing", "description": "Rodeo discipline"},
        "2": {"name": "bull riding", "description": "Rodeo discipline"},
        "3": {"name": "bulldogging", "description": "Rodeo discipline"},
        "4": {"name": "calf roping", "description": "Rodeo discipline"},
        "5": {"name": "goat roping", "description": "Rodeo discipline"},
        "6": {"name": "saddle bronc", "description": "Rodeo discipline"},
        "7": {"name": "none", "description": "none"},
    },
    "roller sports": {
        "0": {
            "name": "roller hockey",
            "description": "Team sport similar to ice hockey, executed on 4 wheel roller skates with sticks and a ball",
        },
        "1": {
            "name": "skateboarding",
            "description": "Competitions involving stunts and acrobatic feats performed on a skateboard using various ramps and other obstacles",
        },
        "2": {"name": "none", "description": "none"},
    },
    "rowing": {"0": {"name": "none", "description": "none"}},
    "rugby": {
        "0": {
            "name": "rugby league",
            "description": "A type of rugby where two teams of 13 compete on a pitch by running with and passing an oval ball. Points are scored by touching down the ball behind the goal line or kicking it between goal posts. Governed by Rugby League International Federation.",
        },
        "1": {
            "name": "rugby sevens",
            "description": "A type of rugby union where two teams of 7 compete on a pitch by running with and passing an oval ball. Points are scored by touching down the ball behind the goal line or kicking it between goal posts. Governed by the World Rugby organization.",
        },
        "2": {
            "name": "rugby union",
            "description": "A type of rugby where two teams of 15 compete on a pitch by running with and passing an oval ball. Points are scored by touching down the ball behind the goal line or kicking it between goal posts. Governed by the World Rugby organization.",
        },
        "3": {"name": "none", "description": "none"},
    },
    "sailing": {"0": {"name": "none", "description": "none"}},
    "skiing": {
        "0": {
            "name": "Nordic combined",
            "description": "Competition combining cross-country skiing and ski jumping",
        },
        "1": {
            "name": "Telemark skiing",
            "description": "Races combining downhill and cross-country skiing events with unique Telemark techniques and equipment.",
        },
        "2": {
            "name": "alpine skiing",
            "description": "Racing downhill on snow-covered slopes using alpine techniques and equipment. The slopes contain intermediate gates which are spaced according to the discipline involved.",
        },
        "3": {
            "name": "cross-country skiing",
            "description": "Nordic ski race competed in relatively-flat, snowy countryside on narrow skis.",
        },
        "4": {
            "name": "freestyle skiing",
            "description": "Skiing competitions which, in contrast to alpine skiing, incorporate acrobatic moves and jumps. Events include aerials, halfpipe, slopestyle, ski cross, moguls and big air.",
        },
        "5": {
            "name": "grass skiing",
            "description": "Alpine skiing on roller skis and grass",
        },
        "6": {
            "name": "ski jumping",
            "description": "Competitors descend a snow covered elevated ramp on skis and try to fly off it as far as possible, receiving marks for distance, style of flight and landing",
        },
        "7": {"name": "none", "description": "none"},
    },
    "sport shooting": {"0": {"name": "none", "description": "none"}},
    "swimming": {
        "0": {
            "name": "marathon swimming",
            "description": "A long distance open water swimming",
        },
        "1": {"name": "none", "description": "none"},
    },
    "volleyball": {
        "0": {
            "name": "beach volleyball",
            "description": "Two teams of two players compete on a sand court. Unlike indoor volleyball, points are scored only when the serving team wins a rally or forces an error. The sand surface makes it more physically demanding than volleyball",
        },
        "1": {"name": "none", "description": "none"},
    },
    "weightlifting and powerlifting": {"0": {"name": "none", "description": "none"}},
    "wrestling": {
        "0": {
            "name": "Swiss wrestling",
            "description": "Traditional Swiss sport similar to wrestling with specific rules",
        },
        "1": {
            "name": "freestyle wrestling",
            "description": "A style where leg holds are allowed",
        },
        "2": {
            "name": "greco-roman",
            "description": "A style where the only holds allowed are those between the head and the belt",
        },
        "3": {"name": "none", "description": "none"},
    },
}


ID_TO_TOPIC = {
    "00000000": "root",
    "01000000": "arts, culture, entertainment and media",
    "20000002": "arts and entertainment",
    "20000003": "animation",
    "20000004": "cartoon",
    "20000005": "cinema",
    "20000007": "dance",
    "20000011": "fashion",
    "20001181": "festival",
    "20000013": "literature",
    "20000018": "music",
    "20001179": "series",
    "20000029": "theatre",
    "20000031": "visual arts",
    "20000038": "culture",
    "20001135": "art exhibition",
    "20000039": "cultural development",
    "20000040": "customs and tradition",
    "20000041": "festive event (culture)",
    "20000042": "language",
    "20000043": "library and museum",
    "20000044": "monument and heritage site",
    "20000045": "mass media",
    "20001319": "disinformation and misinformation",
    "20000046": "news media",
    "20000047": "newspaper",
    "20000048": "online media outlet",
    "20000049": "periodical",
    "20000050": "radio",
    "20001182": "social media",
    "20000051": "television",
    "16000000": "conflict, war and peace",
    "20000053": "act of terror",
    "20000054": "act of bioterrorism",
    "20000055": "terrorist bombings",
    "20000056": "armed conflict",
    "20000057": "guerrilla activity",
    "20000058": "international military intervention",
    "20000060": "military occupation",
    "20000062": "war",
    "20000065": "civil unrest",
    "20000066": "demonstration",
    "20000067": "rebellion",
    "20000068": "revolution",
    "20000069": "riot",
    "20000070": "coup d'etat",
    "20001361": "cyber warfare",
    "20000071": "massacre",
    "20000073": "peace process",
    "20000078": "disarmament",
    "20000074": "peace envoy",
    "20000075": "peace plan",
    "20000076": "peace talks",
    "20000059": "peacekeeping force",
    "20000077": "post-war reconstruction",
    "20000079": "ordnance clearance",
    "20001377": "war victims",
    "20000061": "missing in action",
    "20001378": "missing in action",
    "20000080": "prisoners of war",
    "02000000": "crime, law and justice",
    "20000082": "crime",
    "20001314": "animal abuse",
    "20000083": "arson",
    "20000084": "assault",
    "20000087": "corporate crime",
    "20000093": "corruption",
    "20000086": "cyber crime",
    "20000095": "drug related crimes",
    "20000097": "fraud",
    "20000072": "genocide",
    "20000098": "hijacking",
    "20000099": "homicide",
    "20001283": "human smuggling and trafficking",
    "20000100": "kidnapping",
    "20000101": "organised crime",
    "20001196": "reckless driving",
    "20000104": "robbery and theft",
    "20001313": "shootings",
    "20000103": "terrorism",
    "20001320": "torture",
    "20001285": "vandalism",
    "20000105": "war crime",
    "20000106": "judiciary",
    "20000107": "court",
    "20000116": "out of court procedures",
    "20000118": "prosecution and prosecutors",
    "20000119": "justice",
    "20000121": "law",
    "20001197": "administrative law",
    "20000122": "civil law",
    "20000125": "criminal law",
    "20000126": "international law",
    "20000129": "law enforcement",
    "20000130": "arrest",
    "20000131": "investigation (criminal)",
    "20000133": "police",
    "20001299": "surveillance",
    "03000000": "disaster, accident and emergency incident",
    "20000139": "accident and emergency incident",
    "20001321": "drowning",
    "20000140": "explosion accident and incident",
    "20000141": "industrial accident and incident",
    "20000161": "structural failure",
    "20000143": "transportation accident and incident",
    "20000148": "disaster",
    "20000149": "famine",
    "20000150": "fire",
    "20000151": "natural disaster",
    "20000160": "emergency incident",
    "20000162": "transport incident",
    "20000167": "emergency planning",
    "20000168": "emergency response",
    "04000000": "economy, business and finance",
    "20000349": "business enterprise",
    "20001278": "cooperative",
    "20001172": "small and medium enterprise",
    "20001158": "start-up and entrepreneurial business",
    "20000170": "business information",
    "20000171": "business finance",
    "20000183": "business financing",
    "20000199": "business governance",
    "20001365": "business reporting and performance",
    "20001366": "business restructuring",
    "20000192": "business strategy and marketing",
    "20000188": "human resources",
    "20000344": "economy",
    "20000350": "central bank",
    "20000355": "currency",
    "20000363": "economic organisation",
    "20000346": "economic trends and indicators",
    "20000364": "emerging market",
    "20000372": "international economic institution",
    "20000373": "international trade",
    "20000379": "monetary policy",
    "20000381": "mutual funds",
    "20001171": "sharing economy",
    "20000385": "market and exchange",
    "20000386": "commodities market",
    "20000390": "debt market",
    "20000391": "foreign exchange market",
    "20000392": "loan market",
    "20000209": "products and services",
    "20000210": "agriculture",
    "20001371": "business service",
    "20000217": "chemicals",
    "20000213": "commercial fishing",
    "20000225": "computing and information technology",
    "20000235": "construction and property",
    "20000243": "consumer goods",
    "20000256": "energy and resource",
    "20000271": "financial and business service",
    "20001370": "financial service",
    "20000214": "forestry and timber",
    "20001354": "healthcare industry",
    "20000294": "manufacturing and engineering",
    "20000304": "media and entertainment industry",
    "20000316": "metal and mineral mining and refining",
    "20000224": "plastic",
    "20000322": "process industry",
    "20001289": "sales channel",
    "20000331": "tourism and leisure industry",
    "20000337": "transport",
    "20001244": "utilities",
    "05000000": "education",
    "20000412": "curriculum",
    "20001217": "educational grading",
    "20000413": "educational testing and examinations",
    "20000414": "entrance examination",
    "20001337": "online and remote learning",
    "20000398": "parents group",
    "20000399": "religious education",
    "20000400": "school",
    "20000403": "adult and continuing education",
    "20000405": "college and university",
    "20000409": "early childhood education",
    "20000402": "further education",
    "20001215": "independent school",
    "20000408": "lower secondary education",
    "20000401": "primary education",
    "20001214": "private school",
    "20001212": "religious school",
    "20001213": "state school",
    "20000404": "upper secondary education",
    "20000410": "social learning",
    "20000415": "students",
    "20000416": "teachers",
    "20000411": "teaching and learning",
    "20001216": "vocational education",
    "06000000": "environment",
    "20000418": "climate change",
    "20000419": "global warming",
    "20000420": "conservation",
    "20000421": "energy saving",
    "20000422": "parks",
    "20000424": "environmental pollution",
    "20000425": "air pollution",
    "20000426": "environmental clean-up",
    "20000427": "hazardous materials",
    "20000428": "waste materials",
    "20000429": "water pollution",
    "20000430": "natural resources",
    "20000431": "energy resources",
    "20000432": "land resources",
    "20000435": "population growth",
    "20000436": "renewable energy",
    "20000437": "water",
    "20000441": "nature",
    "20000500": "animal",
    "20000442": "ecosystem",
    "20000443": "endangered species",
    "20000507": "flowers and plants",
    "20000444": "invasive species",
    "20001374": "sustainability",
    "07000000": "health",
    "20000446": "disease and condition",
    "20000447": "cancer",
    "20000448": "communicable disease",
    "20001355": "developmental disorder",
    "20000454": "heart disease",
    "20000455": "illness",
    "20000456": "injury",
    "20000457": "medical condition",
    "20000458": "mental health and disorder",
    "20001322": "poisoning",
    "20000480": "government health care",
    "20000481": "Medicaid",
    "20000482": "Medicare",
    "20000461": "health facility",
    "20001229": "healthcare clinic",
    "20000462": "hospital",
    "20000483": "health insurance",
    "20000463": "health organisation",
    "20000464": "health treatment and procedure",
    "20000465": "diet",
    "20001219": "drug rehabilitation",
    "20001221": "emergency care",
    "20000470": "health care approach",
    "20000469": "medical test",
    "20000467": "non-prescription drug",
    "20000475": "physical fitness",
    "20000468": "prescription drug",
    "20000476": "preventative medicine",
    "20001228": "surgery",
    "20000478": "therapy",
    "20000477": "vaccine",
    "20000485": "medical profession",
    "20000486": "medical service",
    "20000487": "medical specialisation",
    "20000492": "medical staff",
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
    "20001235": "funeral and memorial service",
    "20001234": "graduation",
    "20001233": "name ceremony",
    "20001236": "wedding",
    "20000504": "high society",
    "20000506": "royalty",
    "20000503": "human mishap",
    "20000502": "people",
    "20000499": "record and achievement",
    "09000000": "labour",
    "20000509": "employment",
    "20000510": "apprenticeship",
    "20000511": "child labour",
    "20000339": "commuting",
    "20000512": "employee",
    "20000513": "employer",
    "20000514": "employment training",
    "20000517": "occupations",
    "20001276": "parental leave",
    "20001206": "self-employment",
    "20001277": "volunteering",
    "20000518": "wages and benefits",
    "20000521": "employment legislation",
    "20000522": "workplace health and safety",
    "20000523": "labour market",
    "20001275": "gig economy",
    "20000524": "labour relations",
    "20000525": "collective agreements",
    "20000529": "labour dispute",
    "20000531": "retirement",
    "20000532": "pension",
    "20000533": "unemployment",
    "20000534": "job layoffs",
    "20000535": "unemployment benefits",
    "20000536": "unions",
    "10000000": "lifestyle and leisure",
    "20000538": "leisure",
    "20000539": "club and association",
    "20000540": "game",
    "20000549": "gaming and lottery",
    "20000550": "hobby",
    "20000551": "holiday",
    "20000553": "leisure venue",
    "20000560": "outdoor recreational activities",
    "20000563": "travel and tourism",
    "20000565": "lifestyle",
    "20000570": "house and home",
    "20000569": "organic food",
    "20001143": "party",
    "20000572": "trend",
    "20001339": "wellness",
    "20001239": "exercise and fitness",
    "20001340": "mental wellbeing",
    "11000000": "politics",
    "20000574": "election",
    "20001263": "church elections",
    "20000575": "citizens' initiative and recall",
    "20000576": "electoral system",
    "20000577": "intergovernmental elections",
    "20000578": "local elections",
    "20000579": "national elections",
    "20000580": "political campaigns",
    "20000582": "political candidates",
    "20001266": "political debates",
    "20000583": "primary elections",
    "20000584": "referenda",
    "20000585": "regional elections",
    "20000586": "voting",
    "20000587": "fundamental rights",
    "20000588": "censorship and freedom of speech",
    "20000120": "civil rights",
    "20000590": "freedom of religion",
    "20000591": "freedom of the press",
    "20000592": "human rights",
    "20001300": "privacy",
    "20001326": "women's rights",
    "20000593": "government",
    "20000594": "civil and public service",
    "20000597": "constitution (law)",
    "20000598": "defence",
    "20000605": "espionage and intelligence",
    "20000606": "executive (government)",
    "20000607": "government budget",
    "20000609": "government department",
    "20001261": "heads of government",
    "20000610": "heads of state",
    "20000611": "impeachment",
    "20000615": "legislative body",
    "20000612": "local government and authority",
    "20000613": "minister and secretary (government)",
    "20000614": "national government",
    "20001260": "political committees",
    "20001259": "political convention",
    "20001262": "public inquiry",
    "20000618": "regional government and authority",
    "20001173": "regulatory authority",
    "20000621": "government policy",
    "20001132": "cultural policies",
    "20000345": "economic policy",
    "20001338": "education policy",
    "20000423": "environmental policy",
    "20000479": "healthcare policy",
    "20000626": "interior policy",
    "20001265": "local government policy",
    "20000634": "migration policy",
    "20000635": "nuclear policy",
    "20000636": "regulation of industry",
    "20000619": "safety of citizens",
    "20001147": "sports policies",
    "20000620": "taxation",
    "20000638": "international relations",
    "20001316": "border disputes",
    "20000639": "diplomacy",
    "20000642": "economic sanction",
    "20000643": "foreign aid",
    "20000644": "international organisation",
    "20000645": "refugees and internally displaced people",
    "20000646": "non-governmental organisation",
    "20000647": "political crisis",
    "20000648": "political dissent",
    "20000649": "political process",
    "20000650": "lobbying",
    "20000652": "political development",
    "20000651": "political parties and movements",
    "20000653": "political system",
    "12000000": "religion",
    "20000657": "belief systems",
    "20000658": "Buddhism",
    "20000659": "Christianity",
    "20000673": "Confucianism",
    "20000675": "Freemasonry",
    "20000676": "Hinduism",
    "20000677": "Islam",
    "20000678": "Jainism",
    "20000679": "Judaism",
    "20000682": "Scientology",
    "20000683": "Shintoism",
    "20000684": "Sikhism",
    "20000685": "Taoism",
    "20000686": "Unificationism",
    "20000681": "Zoroastrianism",
    "20001349": "atheism and agnosticism",
    "20000674": "cult",
    "20000680": "nature religion",
    "20000687": "interreligious dialogue",
    "20000702": "relations between religion and government",
    "20000688": "religious conflict",
    "20000689": "religious event",
    "20000697": "religious facility",
    "20000698": "church",
    "20000699": "mosque",
    "20000700": "synagogue",
    "20000701": "temple",
    "20000690": "religious festival and holiday",
    "20001271": "All Saints Day",
    "20000691": "Christmas",
    "20000692": "Easter",
    "20001350": "Eid al-Adha",
    "20001352": "Hanukkah",
    "20000693": "Pentecost",
    "20000694": "Ramadan",
    "20001272": "Walpurgis night",
    "20000695": "Yom Kippur",
    "20000703": "religious leader",
    "20000704": "pope",
    "20000696": "religious ritual",
    "20001273": "baptism",
    "20001345": "bar and bat mitzvah",
    "20001346": "canonisation",
    "20000705": "religious text",
    "20000706": "Bible",
    "20000707": "Qur'an",
    "20000708": "Torah",
    "13000000": "science and technology",
    "20000710": "biomedical science",
    "20000711": "biotechnology",
    "20000715": "mathematics",
    "20000717": "natural science",
    "20000718": "astronomy",
    "20000719": "biology",
    "20000725": "chemistry",
    "20000726": "cosmology",
    "20000727": "geology",
    "20000728": "horticulture",
    "20000729": "marine science",
    "20000730": "meteorology",
    "20000731": "physics",
    "20000741": "scientific institution",
    "20000735": "scientific research",
    "20000737": "medical research",
    "20000738": "scientific exploration",
    "20000736": "scientific innovation",
    "20000740": "scientific publication",
    "20000755": "scientific standards",
    "20000742": "social sciences",
    "20000743": "anthropology",
    "20000744": "archaeology",
    "20000745": "economics",
    "20000746": "geography",
    "20000747": "history",
    "20000748": "information science",
    "20000750": "linguistics",
    "20000751": "philosophy",
    "20000752": "political science",
    "20000753": "psychology",
    "20000754": "sociology",
    "20000749": "study of law",
    "20000756": "technology and engineering",
    "20000757": "aerospace engineering",
    "20000759": "agricultural technology",
    "20000760": "civil engineering",
    "20000761": "electronic engineering",
    "20000762": "identification technology",
    "20000763": "information technology and computer science",
    "20000764": "materials science",
    "20000716": "mechanical engineering",
    "20000765": "micro science",
    "14000000": "society",
    "20000768": "communities",
    "20001360": "fraternal and community group",
    "20000769": "social networking",
    "20000770": "demographics",
    "20000774": "population and census",
    "20000775": "discrimination",
    "20000776": "ageism",
    "20000777": "racism",
    "20000778": "religious discrimination",
    "20000779": "sexism",
    "20001373": "diversity, equity and inclusion",
    "20000772": "emigration",
    "20000780": "family",
    "20000782": "Dating and Relationships",
    "20000781": "adoption",
    "20000783": "divorce",
    "20000784": "family planning",
    "20000786": "marriage",
    "20000787": "parenting",
    "20001359": "pregnancy and childbirth",
    "20000771": "immigration",
    "20000773": "illegal immigration",
    "20000788": "mankind",
    "20000792": "LGBTQ",
    "20000789": "adults",
    "20000790": "children",
    "20000791": "disabilities",
    "20000793": "gender",
    "20001288": "indigenous people",
    "20000794": "infants",
    "20001328": "men",
    "20000795": "national or ethnic minority",
    "20000796": "nuclear radiation victims",
    "20000797": "senior citizens",
    "20000798": "teenagers",
    "20001327": "women",
    "20000799": "social condition",
    "20000800": "homelessness",
    "20000801": "poverty",
    "20000802": "social problem",
    "20000803": "abusive behaviour",
    "20000804": "addiction",
    "20001284": "bullying",
    "20000805": "juvenile delinquency",
    "20000806": "prostitution",
    "20001193": "sexual misconduct",
    "20000807": "slavery",
    "20000808": "values",
    "20000809": "corrupt practices",
    "20000810": "death and dying",
    "20000814": "ethics",
    "20000815": "pornography",
    "20000816": "sexual behaviour",
    "20000817": "welfare",
    "20000818": "charity",
    "20001317": "child care",
    "20001232": "elderly care",
    "20000819": "long-term care",
    "20001290": "public housing",
    "20000820": "social services",
    "15000000": "sport",
    "20000822": "competition discipline",
    "20001329": "3x3 basketball",
    "20000823": "American football",
    "20000846": "Australian rules football",
    "20000876": "Canadian football",
    "20000939": "Gaelic football",
    "20000968": "Jai Alai (Pelota)",
    "20000824": "archery",
    "20001286": "arm wrestling",
    "20001175": "artistic swimming",
    "20000827": "athletics",
    "20000847": "badminton",
    "20000848": "bandy",
    "20000849": "baseball",
    "20000851": "basketball",
    "20000852": "biathlon",
    "20000853": "billiards",
    "20000854": "bobsleigh",
    "20001240": "bodybuilding",
    "20000855": "boules",
    "20000856": "boxing",
    "20000875": "bullfighting",
    "20001330": "canoe slalom",
    "20001331": "canoe sprint",
    "20000877": "canoeing",
    "20000883": "casting (fishing)",
    "20001309": "cheerleading",
    "20001154": "chess",
    "20000911": "competitive dancing",
    "20000888": "cricket",
    "20000889": "croquet",
    "20000890": "curling",
    "20000892": "cycling",
    "20000912": "darts",
    "20000913": "diving",
    "20000919": "dog racing",
    "20000922": "duathlon",
    "20001183": "eSports",
    "20000923": "equestrian",
    "20000929": "fencing",
    "20000933": "field hockey",
    "20000934": "figure skating",
    "20000936": "fist ball",
    "20000937": "floorball",
    "20000938": "flying disc",
    "20001335": "football 5-a-side",
    "20001336": "goalball",
    "20000940": "golf",
    "20000942": "gymnastics",
    "20000958": "handball (team)",
    "20000959": "hornuss",
    "20000960": "horse racing",
    "20000964": "hurling",
    "20000965": "ice hockey",
    "20000967": "inline skating",
    "20000978": "kabaddi",
    "20000979": "kayaking",
    "20001306": "kiting",
    "20000986": "lacrosse",
    "20000987": "luge",
    "20000988": "marathon",
    "20001157": "martial arts",
    "20000989": "modern pentathlon",
    "20000991": "motor car racing",
    "20000990": "motorboat racing",
    "20000998": "motorcycling",
    "20000884": "mountain climbing",
    "20001010": "netball",
    "20001011": "orienteering",
    "20001305": "padel",
    "20001013": "parachuting",
    "20001014": "polo",
    "20001015": "pool",
    "20001016": "power boating",
    "20001281": "racquetball",
    "20001282": "ringette",
    "20001333": "road cycling",
    "20001017": "rodeo",
    "20001155": "roller sports",
    "20001026": "rowing",
    "20001176": "rugby",
    "20001038": "sailing",
    "20001047": "sepak takraw",
    "20001048": "shinty",
    "20001151": "short track speed skating",
    "20001055": "skeleton",
    "20001056": "skiing",
    "20001062": "sky diving",
    "20001063": "snooker",
    "20001064": "snowboarding",
    "20001065": "soccer",
    "20001066": "softball",
    "20001067": "speed skating",
    "20000887": "sport climbing",
    "20001049": "sport shooting",
    "20001068": "squash",
    "20001307": "stand up paddleboarding (SUP)",
    "20001069": "sumo wrestling",
    "20001070": "surfing",
    "20001071": "swimming",
    "20001083": "table tennis",
    "20001086": "ten pin bowling",
    "20001085": "tennis",
    "20001334": "track cycling",
    "20001087": "triathlon",
    "20001088": "tug-of-war",
    "20000918": "underwater sports",
    "20001089": "volleyball",
    "20001091": "water polo",
    "20001092": "water skiing",
    "20001093": "weightlifting and powerlifting",
    "20001097": "windsurfing",
    "20001098": "wrestling",
    "20001103": "disciplinary action in sport",
    "20001104": "drug use in sport",
    "20001105": "drug abuse in sport",
    "20001106": "drug testing in sport",
    "20001107": "medical drug use in sport",
    "20001301": "sport achievement",
    "20001304": "sports honour",
    "20001303": "sports medal and trophy",
    "20001302": "sports record",
    "20001108": "sport event",
    "20001177": "Olympic Games",
    "20001178": "Paralympic Games",
    "20001109": "continental championship",
    "20001110": "continental cup",
    "20001111": "continental games",
    "20001343": "final game",
    "20001112": "international championship",
    "20001113": "international cup",
    "20001114": "international games",
    "20001115": "national championship",
    "20001116": "national cup",
    "20001117": "national games",
    "20001342": "playoff championship",
    "20001118": "regional championship",
    "20001119": "regional cup",
    "20001120": "regional games",
    "20001341": "regular competition",
    "20001121": "world championship",
    "20001122": "world cup",
    "20001123": "world games",
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
    "20000003": 4,
    "20000004": 4,
    "20000005": 4,
    "20000007": 4,
    "20000011": 4,
    "20001181": 4,
    "20000013": 4,
    "20000018": 4,
    "20001179": 4,
    "20000029": 4,
    "20000031": 4,
    "20000038": 3,
    "20001135": 4,
    "20000039": 4,
    "20000040": 4,
    "20000041": 4,
    "20000042": 4,
    "20000043": 4,
    "20000044": 4,
    "20000045": 3,
    "20001319": 4,
    "20000046": 4,
    "20000047": 4,
    "20000048": 4,
    "20000049": 4,
    "20000050": 4,
    "20001182": 4,
    "20000051": 4,
    "16000000": 2,
    "20000053": 3,
    "20000054": 4,
    "20000055": 4,
    "20000056": 3,
    "20000057": 4,
    "20000058": 4,
    "20000060": 4,
    "20000062": 4,
    "20000065": 3,
    "20000066": 4,
    "20000067": 4,
    "20000068": 4,
    "20000069": 4,
    "20000070": 3,
    "20001361": 3,
    "20000071": 3,
    "20000073": 3,
    "20000078": 4,
    "20000074": 4,
    "20000075": 4,
    "20000076": 4,
    "20000059": 4,
    "20000077": 3,
    "20000079": 4,
    "20001377": 3,
    "20000061": 4,
    "20001378": 4,
    "20000080": 4,
    "02000000": 2,
    "20000082": 3,
    "20001314": 4,
    "20000083": 4,
    "20000084": 4,
    "20000087": 4,
    "20000093": 4,
    "20000086": 4,
    "20000095": 4,
    "20000097": 4,
    "20000072": 4,
    "20000098": 4,
    "20000099": 4,
    "20001283": 4,
    "20000100": 4,
    "20000101": 4,
    "20001196": 4,
    "20000104": 4,
    "20001313": 4,
    "20000103": 4,
    "20001320": 4,
    "20001285": 4,
    "20000105": 4,
    "20000106": 3,
    "20000107": 4,
    "20000116": 4,
    "20000118": 4,
    "20000119": 3,
    "20000121": 3,
    "20001197": 4,
    "20000122": 4,
    "20000125": 4,
    "20000126": 4,
    "20000129": 3,
    "20000130": 4,
    "20000131": 4,
    "20000133": 4,
    "20001299": 4,
    "03000000": 2,
    "20000139": 3,
    "20001321": 4,
    "20000140": 4,
    "20000141": 4,
    "20000161": 4,
    "20000143": 4,
    "20000148": 3,
    "20000149": 4,
    "20000150": 4,
    "20000151": 4,
    "20000160": 3,
    "20000162": 4,
    "20000167": 3,
    "20000168": 3,
    "04000000": 2,
    "20000349": 3,
    "20001278": 4,
    "20001172": 4,
    "20001158": 4,
    "20000170": 3,
    "20000171": 4,
    "20000183": 4,
    "20000199": 4,
    "20001365": 4,
    "20001366": 4,
    "20000192": 4,
    "20000188": 4,
    "20000344": 3,
    "20000350": 4,
    "20000355": 4,
    "20000363": 4,
    "20000346": 4,
    "20000364": 4,
    "20000372": 4,
    "20000373": 4,
    "20000379": 4,
    "20000381": 4,
    "20001171": 4,
    "20000385": 3,
    "20000386": 4,
    "20000390": 4,
    "20000391": 4,
    "20000392": 4,
    "20000209": 3,
    "20000210": 4,
    "20001371": 4,
    "20000217": 4,
    "20000213": 4,
    "20000225": 4,
    "20000235": 4,
    "20000243": 4,
    "20000256": 4,
    "20000271": 4,
    "20001370": 4,
    "20000214": 4,
    "20001354": 4,
    "20000294": 4,
    "20000304": 4,
    "20000316": 4,
    "20000224": 4,
    "20000322": 4,
    "20001289": 4,
    "20000331": 4,
    "20000337": 4,
    "20001244": 4,
    "05000000": 2,
    "20000412": 3,
    "20001217": 3,
    "20000413": 3,
    "20000414": 3,
    "20001337": 3,
    "20000398": 3,
    "20000399": 3,
    "20000400": 3,
    "20000403": 4,
    "20000405": 4,
    "20000409": 4,
    "20000402": 4,
    "20001215": 4,
    "20000408": 4,
    "20000401": 4,
    "20001214": 4,
    "20001212": 4,
    "20001213": 4,
    "20000404": 4,
    "20000410": 3,
    "20000415": 3,
    "20000416": 3,
    "20000411": 3,
    "20001216": 3,
    "06000000": 2,
    "20000418": 3,
    "20000419": 4,
    "20000420": 3,
    "20000421": 4,
    "20000422": 4,
    "20000424": 3,
    "20000425": 4,
    "20000426": 4,
    "20000427": 4,
    "20000428": 4,
    "20000429": 4,
    "20000430": 3,
    "20000431": 4,
    "20000432": 4,
    "20000435": 4,
    "20000436": 4,
    "20000437": 4,
    "20000441": 3,
    "20000500": 4,
    "20000442": 4,
    "20000443": 4,
    "20000507": 4,
    "20000444": 4,
    "20001374": 3,
    "07000000": 2,
    "20000446": 3,
    "20000447": 4,
    "20000448": 4,
    "20001355": 4,
    "20000454": 4,
    "20000455": 4,
    "20000456": 4,
    "20000457": 4,
    "20000458": 4,
    "20001322": 4,
    "20000480": 3,
    "20000481": 4,
    "20000482": 4,
    "20000461": 3,
    "20001229": 4,
    "20000462": 4,
    "20000483": 3,
    "20000463": 3,
    "20000464": 3,
    "20000465": 4,
    "20001219": 4,
    "20001221": 4,
    "20000470": 4,
    "20000469": 4,
    "20000467": 4,
    "20000475": 4,
    "20000468": 4,
    "20000476": 4,
    "20001228": 4,
    "20000478": 4,
    "20000477": 4,
    "20000485": 3,
    "20000486": 4,
    "20000487": 4,
    "20000492": 4,
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
    "20001235": 4,
    "20001234": 4,
    "20001233": 4,
    "20001236": 4,
    "20000504": 3,
    "20000506": 4,
    "20000503": 3,
    "20000502": 3,
    "20000499": 3,
    "09000000": 2,
    "20000509": 3,
    "20000510": 4,
    "20000511": 4,
    "20000339": 4,
    "20000512": 4,
    "20000513": 4,
    "20000514": 4,
    "20000517": 4,
    "20001276": 4,
    "20001206": 4,
    "20001277": 4,
    "20000518": 4,
    "20000521": 3,
    "20000522": 4,
    "20000523": 3,
    "20001275": 4,
    "20000524": 3,
    "20000525": 4,
    "20000529": 4,
    "20000531": 3,
    "20000532": 4,
    "20000533": 3,
    "20000534": 4,
    "20000535": 4,
    "20000536": 3,
    "10000000": 2,
    "20000538": 3,
    "20000539": 4,
    "20000540": 4,
    "20000549": 4,
    "20000550": 4,
    "20000551": 4,
    "20000553": 4,
    "20000560": 4,
    "20000563": 4,
    "20000565": 3,
    "20000570": 4,
    "20000569": 4,
    "20001143": 4,
    "20000572": 4,
    "20001339": 3,
    "20001239": 4,
    "20001340": 4,
    "11000000": 2,
    "20000574": 3,
    "20001263": 4,
    "20000575": 4,
    "20000576": 4,
    "20000577": 4,
    "20000578": 4,
    "20000579": 4,
    "20000580": 4,
    "20000582": 4,
    "20001266": 4,
    "20000583": 4,
    "20000584": 4,
    "20000585": 4,
    "20000586": 4,
    "20000587": 3,
    "20000588": 4,
    "20000120": 4,
    "20000590": 4,
    "20000591": 4,
    "20000592": 4,
    "20001300": 4,
    "20001326": 4,
    "20000593": 3,
    "20000594": 4,
    "20000597": 4,
    "20000598": 4,
    "20000605": 4,
    "20000606": 4,
    "20000607": 4,
    "20000609": 4,
    "20001261": 4,
    "20000610": 4,
    "20000611": 4,
    "20000615": 4,
    "20000612": 4,
    "20000613": 4,
    "20000614": 4,
    "20001260": 4,
    "20001259": 4,
    "20001262": 4,
    "20000618": 4,
    "20001173": 4,
    "20000621": 3,
    "20001132": 4,
    "20000345": 4,
    "20001338": 4,
    "20000423": 4,
    "20000479": 4,
    "20000626": 4,
    "20001265": 4,
    "20000634": 4,
    "20000635": 4,
    "20000636": 4,
    "20000619": 4,
    "20001147": 4,
    "20000620": 4,
    "20000638": 3,
    "20001316": 4,
    "20000639": 4,
    "20000642": 4,
    "20000643": 4,
    "20000644": 4,
    "20000645": 4,
    "20000646": 3,
    "20000647": 3,
    "20000648": 3,
    "20000649": 3,
    "20000650": 4,
    "20000652": 4,
    "20000651": 4,
    "20000653": 4,
    "12000000": 2,
    "20000657": 3,
    "20000658": 4,
    "20000659": 4,
    "20000673": 4,
    "20000675": 4,
    "20000676": 4,
    "20000677": 4,
    "20000678": 4,
    "20000679": 4,
    "20000682": 4,
    "20000683": 4,
    "20000684": 4,
    "20000685": 4,
    "20000686": 4,
    "20000681": 4,
    "20001349": 4,
    "20000674": 4,
    "20000680": 4,
    "20000687": 3,
    "20000702": 3,
    "20000688": 3,
    "20000689": 3,
    "20000697": 3,
    "20000698": 4,
    "20000699": 4,
    "20000700": 4,
    "20000701": 4,
    "20000690": 3,
    "20001271": 4,
    "20000691": 4,
    "20000692": 4,
    "20001350": 4,
    "20001352": 4,
    "20000693": 4,
    "20000694": 4,
    "20001272": 4,
    "20000695": 4,
    "20000703": 3,
    "20000704": 4,
    "20000696": 3,
    "20001273": 4,
    "20001345": 4,
    "20001346": 4,
    "20000705": 3,
    "20000706": 4,
    "20000707": 4,
    "20000708": 4,
    "13000000": 2,
    "20000710": 3,
    "20000711": 4,
    "20000715": 3,
    "20000717": 3,
    "20000718": 4,
    "20000719": 4,
    "20000725": 4,
    "20000726": 4,
    "20000727": 4,
    "20000728": 4,
    "20000729": 4,
    "20000730": 4,
    "20000731": 4,
    "20000741": 3,
    "20000735": 3,
    "20000737": 4,
    "20000738": 4,
    "20000736": 4,
    "20000740": 4,
    "20000755": 3,
    "20000742": 3,
    "20000743": 4,
    "20000744": 4,
    "20000745": 4,
    "20000746": 4,
    "20000747": 4,
    "20000748": 4,
    "20000750": 4,
    "20000751": 4,
    "20000752": 4,
    "20000753": 4,
    "20000754": 4,
    "20000749": 4,
    "20000756": 3,
    "20000757": 4,
    "20000759": 4,
    "20000760": 4,
    "20000761": 4,
    "20000762": 4,
    "20000763": 4,
    "20000764": 4,
    "20000716": 4,
    "20000765": 4,
    "14000000": 2,
    "20000768": 3,
    "20001360": 4,
    "20000769": 4,
    "20000770": 3,
    "20000774": 4,
    "20000775": 3,
    "20000776": 4,
    "20000777": 4,
    "20000778": 4,
    "20000779": 4,
    "20001373": 3,
    "20000772": 3,
    "20000780": 3,
    "20000782": 4,
    "20000781": 4,
    "20000783": 4,
    "20000784": 4,
    "20000786": 4,
    "20000787": 4,
    "20001359": 4,
    "20000771": 3,
    "20000773": 4,
    "20000788": 3,
    "20000792": 4,
    "20000789": 4,
    "20000790": 4,
    "20000791": 4,
    "20000793": 4,
    "20001288": 4,
    "20000794": 4,
    "20001328": 4,
    "20000795": 4,
    "20000796": 4,
    "20000797": 4,
    "20000798": 4,
    "20001327": 4,
    "20000799": 3,
    "20000800": 4,
    "20000801": 4,
    "20000802": 3,
    "20000803": 4,
    "20000804": 4,
    "20001284": 4,
    "20000805": 4,
    "20000806": 4,
    "20001193": 4,
    "20000807": 4,
    "20000808": 3,
    "20000809": 4,
    "20000810": 4,
    "20000814": 4,
    "20000815": 4,
    "20000816": 4,
    "20000817": 3,
    "20000818": 4,
    "20001317": 4,
    "20001232": 4,
    "20000819": 4,
    "20001290": 4,
    "20000820": 4,
    "15000000": 2,
    "20000822": 3,
    "20001329": 4,
    "20000823": 4,
    "20000846": 4,
    "20000876": 4,
    "20000939": 4,
    "20000968": 4,
    "20000824": 4,
    "20001286": 4,
    "20001175": 4,
    "20000827": 4,
    "20000847": 4,
    "20000848": 4,
    "20000849": 4,
    "20000851": 4,
    "20000852": 4,
    "20000853": 4,
    "20000854": 4,
    "20001240": 4,
    "20000855": 4,
    "20000856": 4,
    "20000875": 4,
    "20001330": 4,
    "20001331": 4,
    "20000877": 4,
    "20000883": 4,
    "20001309": 4,
    "20001154": 4,
    "20000911": 4,
    "20000888": 4,
    "20000889": 4,
    "20000890": 4,
    "20000892": 4,
    "20000912": 4,
    "20000913": 4,
    "20000919": 4,
    "20000922": 4,
    "20001183": 4,
    "20000923": 4,
    "20000929": 4,
    "20000933": 4,
    "20000934": 4,
    "20000936": 4,
    "20000937": 4,
    "20000938": 4,
    "20001335": 4,
    "20001336": 4,
    "20000940": 4,
    "20000942": 4,
    "20000958": 4,
    "20000959": 4,
    "20000960": 4,
    "20000964": 4,
    "20000965": 4,
    "20000967": 4,
    "20000978": 4,
    "20000979": 4,
    "20001306": 4,
    "20000986": 4,
    "20000987": 4,
    "20000988": 4,
    "20001157": 4,
    "20000989": 4,
    "20000991": 4,
    "20000990": 4,
    "20000998": 4,
    "20000884": 4,
    "20001010": 4,
    "20001011": 4,
    "20001305": 4,
    "20001013": 4,
    "20001014": 4,
    "20001015": 4,
    "20001016": 4,
    "20001281": 4,
    "20001282": 4,
    "20001333": 4,
    "20001017": 4,
    "20001155": 4,
    "20001026": 4,
    "20001176": 4,
    "20001038": 4,
    "20001047": 4,
    "20001048": 4,
    "20001151": 4,
    "20001055": 4,
    "20001056": 4,
    "20001062": 4,
    "20001063": 4,
    "20001064": 4,
    "20001065": 4,
    "20001066": 4,
    "20001067": 4,
    "20000887": 4,
    "20001049": 4,
    "20001068": 4,
    "20001307": 4,
    "20001069": 4,
    "20001070": 4,
    "20001071": 4,
    "20001083": 4,
    "20001086": 4,
    "20001085": 4,
    "20001334": 4,
    "20001087": 4,
    "20001088": 4,
    "20000918": 4,
    "20001089": 4,
    "20001091": 4,
    "20001092": 4,
    "20001093": 4,
    "20001097": 4,
    "20001098": 4,
    "20001103": 3,
    "20001104": 3,
    "20001105": 4,
    "20001106": 4,
    "20001107": 4,
    "20001301": 3,
    "20001304": 4,
    "20001303": 4,
    "20001302": 4,
    "20001108": 3,
    "20001177": 4,
    "20001178": 4,
    "20001109": 4,
    "20001110": 4,
    "20001111": 4,
    "20001343": 4,
    "20001112": 4,
    "20001113": 4,
    "20001114": 4,
    "20001115": 4,
    "20001116": 4,
    "20001117": 4,
    "20001342": 4,
    "20001118": 4,
    "20001119": 4,
    "20001120": 4,
    "20001341": 4,
    "20001121": 4,
    "20001122": 4,
    "20001123": 4,
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
