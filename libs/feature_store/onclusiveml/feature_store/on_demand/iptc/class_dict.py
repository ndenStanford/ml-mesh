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
    }
}

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
    },
    "post-war reconstruction": {
        "0": {
            "name": "ordnance clearance",
            "description": "The removal or neutralisation of ordnance such as landmines or cluster bombs that may remain after a war or armed conflict on public ground",
        }
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
    },
    "emergency incident": {},
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
    },
    "climate change": {
        "0": {
            "name": "global warming",
            "description": "This category includes all issues relating to global warming including temperature research, remote sensing on temperature trends, debate on global warming, ways to reduce emissions and carbon trading.",
        }
    },
    "conservation": {
        "0": {
            "name": "energy saving",
            "description": "Conservation of electrical, and other power sources",
        },
        "1": {"name": "parks", "description": "Areas set aside for preservation"},
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
    },
    "government health care": {},
    "health facility": {
        "0": {
            "name": "healthcare clinic",
            "description": "Local medical facility or doctor's office associated with a general medicine practice, staffed by one or many doctors, focusing on outpatient treatment or giving recommendations to visit a specialist or hospital",
        },
        "1": {
            "name": "hospital",
            "description": "Medical facilities for the treatment of illnesses and injury",
        },
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
    },
    "employment legislation": {
        "0": {
            "name": "workplace health and safety",
            "description": "Laws protecting a safe and healthy work environment",
        }
    },
    "labour market": {
        "0": {
            "name": "gig economy",
            "description": "a labour market consisting of individual suppliers on short-term contracts or freelance work as opposed to permanent jobs, such as drivers or delivery workers",
        }
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
    },
    "retirement": {
        "0": {
            "name": "pension",
            "description": "Payments, either government or private, to retired people",
        }
    },
    "unemployment": {
        "0": {
            "name": "unemployment benefits",
            "description": "Monetary compensation paid to the jobless",
        }
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
    },
    "religious leader": {
        "0": {
            "name": "pope",
            "description": "Head of the Roman Catholic Church worldwide",
        }
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
    },
    "religious text": {
        "0": {"name": "Bible", "description": "Holy book of Christianity"},
        "1": {"name": "Qur'an", "description": "Holy book of Islam"},
        "2": {"name": "Torah", "description": "Holy book of Judaism"},
    },
    "biomedical science": {
        "0": {
            "name": "biotechnology",
            "description": "The scientific manipulation of living organisms and biological processes for scientific, medical or agricultural purposes",
        }
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
    },
    "demographics": {
        "0": {
            "name": "population and census",
            "description": "The official count of people living in a given geopolitical area, usually carried out by a governmental body",
        }
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
    },
    "immigration": {
        "0": {
            "name": "illegal immigration",
            "description": "The movement of individuals or groups of people from one country to another without legal authorisation from the destination country",
        }
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
    },
    "drug use in sport": {},
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
    },
}
