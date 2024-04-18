"""Conftest."""
# isort: skip_file

# Standard Library
from unittest.mock import MagicMock

# 3rd party libraries
import pytest
import json

# Source
from src.serve.category_storage import Category_list


@pytest.fixture
def mock_responses():
    """Mock response for request.post."""
    mock_response = MagicMock()

    # build mock sample
    keys = Category_list
    # The value for each key in the inner JSON object
    value_dict = {
        "Overall summary": "Not mentioned",
        "Theme": "Not mentioned",
        "Impact level": "Not mentioned",
    }
    # Manually construct the inner JSON string
    value_str = json.dumps(value_dict).replace('"', '\\"')
    inner_json_parts = [f'\\"{key}\\": {value_str}' for key in keys] + [
        f'\\"{key}\\": \\"Not mentioned\\"' for key in ["Summary", "Theme"]
    ]
    inner_json_str = "{" + ", ".join(inner_json_parts) + "}"

    # Create the final string
    mock_response.content = f'{{"generated": "{inner_json_str}"}}'
    return mock_response


@pytest.fixture
def mock_responses_aggregate():
    """Mock response for request.post."""
    mock_response = MagicMock()

    # build mock sample
    keys = ["Overall summary", "Theme", "Impact level", "Summary"]
    # Manually construct the inner JSON string
    inner_json_parts = [f'\\"{key}\\": \\"Not mentioned\\"' for key in keys]
    inner_json_str = "{" + ", ".join(inner_json_parts) + "}"

    # Create the final string
    mock_response.content = f'{{"generated": "{inner_json_str}"}}'
    return mock_response


@pytest.fixture
def mock_reponses_production_tool():
    """Mock response for production tool query profile."""
    mock_response = MagicMock()
    string_query = """("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print"""  # noqa: E501
    mock_response_data = {"booleanQuery\\": string_query}
    mock_response.json.return_value = mock_response_data
    return mock_response


@pytest.fixture
def article_input():
    """Input article."""
    return [
        """
            India's semiconductor component market will see its cumulative revenues climb to $300 billion during 2021-2026,
            a report said Tuesday. The ‘India Semiconductor Market Report, 2019-2026',
            a joint research by the India Electronics & Semiconductor Association (IESA) and Counterpoint Research,
            observed that India is poised to be the second largest market in the world in terms of scale and growing demand for
            semiconductor components across several industries and applications.
            It added that this was being bolstered by the increasing pace of digital transformation and the adoption of
            new technologies and covers smartphones, PCs, wearables, cloud data centers,
            Industry 4.0 applications, IoT, smart mobility, and advanced telecom and public utility infrastructure.
            “While the country is becoming one of the largest consumers of electronic and semiconductor components,
            most components are imported, offering limited economic opportunities for the country.
            Currently, only 9% of this semiconductor requirement is met locally,” the report said.
            it noted that India's end equipment market in 2021 stood at $119 billion in terms of revenue and
            is expected to grow at a CAGR of 19% from 2021 to 2026.
            It said that the Electronic System Design and Manufacturing (ESDM) sector in India will play a major role in the
            country's overall growth, from sourcing components to design manufacturing.
            “Before the end of this decade, there will be nothing that will not be touched by electronics and the ubiquitous ‘chip,
            '” IESA CEO Krishna Moorthy said. “Be it fighting carbon emissions, renewable energy, food safety, or healthcare,
            the semiconductor chip will be all-pervasive.""",  # noqa: E501
        """
            Counterpoint Research vice president Neil Shah added that consumption will not only come from the advanced
            semiconductor-heavy 5G and fiber-to-the-home (FTTH) network infrastructure equipment,
            which will contribute to more than 14% of the total semiconductor consumption in 2026,
            but also from the highly capable AI-driven 5G endpoints,
            from smartphones, tablets, PCs, connected cars, industrial robotics to private networks.
            “The telecom sector with the advent of 5G and fiber network rollout will be a key catalyst in boosting
            the semiconductor components consumption,” Shah said.
            “Also, ongoing efforts to embrace cleaner and greener vehicles (electric vehicles) will provide an impetus for
            the automobile industry to adopt advanced technologies,
            which in turn will boost the demand for semiconductor components in India.”
            He also believed that consumer electronics, industrial, and mobile and wearables will be the other key industries
            for the growth of the semiconductor market in India.
            Further, this semiconductor demand will not only be driven by domestic consumption but also by the growing share of exports.
            Mobile and wearables,
            IT and industrial sectors alone contributed to almost 80% of the semiconductor revenues in India in 2021, the research found.
            Tarun Pathak, research director at Counterpoint Research, said the gradual shift from feature phones to smartphones
            has been generating increased proportions of advanced logic processors, memory, integrated controllers, sensors and
            other components. “This will continue to drive the value of the semiconductor content in smartphones, which is still an
            under-penetrated segment in India, aided by the rise of wearables such as smartwatch and TWS,” he said.""",  # noqa: E501
        """
            Over the past decades, my research team has summarized its scientific insights in nearly a thousand publications. But despite
            the large volume of documented thoughts, I hereby confess that I remain puzzled about the three astronomical aspects of our lives.
            First, consider the composition of the material. Our bodies are made of heavy elements grouped together in the cores of large
            stars, which explode to enrich the interstellar medium, where the Solar system is formed, where the Earth thickens and nourishes
            our temporary existence. Viewed this way, we were just passengers in a spaceborn cabin called Earth with borrowed luggage,
            heading to an unknown destination. Despite our basic ignorance, we pride ourselves on peripheral knowledge.
            For example, we recognize that most objects in the universe have a different nature than the object we see in our cosmic
            neighborhood. We label it “dark matter” or “dark energy” and count how much it is up to the second decimal place.
            But a century of famous cosmology without understanding the nature of most of the things that make up the universe, is a sad
            record of scientific knowledge.  Second, consider the time. Our individual lifespan is limited to a period of time at least one
            hundred million times shorter than the age of the Universe. This allows us to experience only a brief snapshot of cosmic history
            and limits our perspective on the big picture. Astronomy benefits greatly from billions of years of documented data. """,  # noqa: E501
        """
            When compared with other fluorophores, chemical fluorophores reserves key advantages in terms of small size and ease of synthesis.
            In addition, they also have the ability to construct compounds when fluorescence is activated by chemical or biochemical processes.
            Currently, various types of fluorophores and their derivatives are widely studied and constantly modified to achieve better
            application value. “Chemical fluorophores prove to be substantially brighter and more photostable than fluorescent proteins.
            Thus, they are extensively employed in the biologic field to detect and visualize different phenomena,” says a representative
            from Alfa Chemistry. “Moreover, chemists and biochemists have developed techniques to couple chemical fluorophores with
            fluorescent proteins, allowing labeling chemistry to be carried out in more complex biological environments such as live cells and
            tissues.” Below are the chemical fluorophores provided by Alfa Chemistry: As novel materials, BODIPY fluorophores and their
            derivatives have been widely used in environmental monitoring, biological sciences, and other fields. Some specifically
            functionalized BODIPY fluorophores are suitable for the selective analysis and detection of extremely small amounts of organic or
            inorganic ions and molecules.""",  # noqa: E501
        """
            The BODIPY fluorophores offered by Alfa Chemistry covered: BDOIPY-Osu (CAS 1025119-04-3), Azido-Bodipy-FL-510 (CAS 1048369-35-2),
            Bodipy Isothiocyate (CAS 1349031-04-4), BDP FL azide (CAS 1379771-95-5), BDP FL maleimide (CAS 773859-49-7),
            BDOIPY (CAS 878888-13-2), Allyl-Bodipy-FL-510 (CAS 926012-31-9), etc. Cyanine fluorophores and their derivatives are helpful in
            exploring dye-sensitized solar cells, textiles, probes, and other applications. Some of the cyanine fluorophores are listed here:
            Sulfo-Cy3-YNE (CAS 1010386-62-5), Cyanine3 NHS ester (CAS 1032678-38-8), Sulfo-Cy5 carboxylic acid (CAS 1121756-16-8),
            Cy3.5 carboxylic acid (CAS 1144107-79-8), Cy5 alkyne (CAS 1223357-57-0), Sulfo Cy5.5 Carboxylic acids(ethyl) (CAS 210892-23-2),
            N-(hydroxy-PEG2)-N’-(azide-PEG3)-Cy5 (CAS 2226235-96-5), and Cy2 Carboxylic acids (CAS 260430-02-2). Rhodamine fluorophores and
            their derivatives have been used in metal ion detection, analytical chemistry, PH spectral probe, and other fields.""",  # noqa: E501
        """
            Alfa Chemistry provides varieties of rhodamine fluorophores, including Azido-ROX (CAS 1048022-18-9), Azido-R6G (CAS 1144503-47-8),
            TAMRA-PEG4-Alkyne (CAS 1225057-68-0), TAMRA-PEG3-Azide (CAS 1228100-59-1), Dy-560 NHS ester (CAS 178623-13-7),
            TAMRA-Azide-PEG-Biotin (CAS 1797415-74-7), 6-Carboxyrhodamine 6G hydrochloride (CAS 180144-68-7), Rhodamine 101 inner salt
            (CAS 41175-43-3), Sulforhodamine 101 (CAS 60311-02-6), Rhodamine 123 (CAS 62669-70-9), etc. Fluorescein Fluorophores Fluorescein
            is one of the most widely used fluorescent dyes in modern biology, biochemistry, and medical research. Due to special
            photochemical properties, fluorescein fluorophores are commonly used in ion recognition probes, biomarkers, and other research
            fields. At Alfa Chemistry, customers can easily access 5-DTAF (CAS 102417-95-8), 5-Dodecanoylaminofluorescein (CAS 107827-77-0),
            Fluorescein-PEG2-azide (CAS 1146195-72-3), 6-HEX dipivaloate (CAS 1166837-63-3), Carboxy-DCFDA N-succinimidyl ester
            (CAS 147265-60-9), and many other fluorescein fluorophores.""",  # noqa: E501
        """
            Scientists had previously seen stars orbiting around something invisible, compact, and very massive at the centre of the Milky Way.
            But the image of Sagittarius A (Sgr A) which is about 27,000 light-years away from Earth, produced by a global research team
            called the Event Horizon Telescope (EHT) Collaboration, provides the first direct visual evidence of it.  "We finally have the
            first look at our Milky Way black hole, Sagittarius A. It\'s the dawn of a new era of black hole physics," the EHT said on Twitter.
            While the black hole is not visible, because it is completely dark, glowing gas around it reveals a telltale signature: a dark
            central region (called a "shadow") surrounded by a bright ring-like structure.  The new view captures light bent by the powerful
            gravity of the black hole, which is four million times more massive than our Sun.  "We were stunned by how well the size of the
            ring agreed with predictions from Einstein\'s Theory of General Relativity," said EHT Project Scientist Geoffrey Bower from the
            Institute of Astronomy and Astrophysics, Academia Sinica, Taipei, in a statement.""",  # noqa: E501
        """
            "These unprecedented observations have greatly improved our understanding of what happens at the very centre of our galaxy,
            and offer new insights on how these giant black holes interact with their surroundings," he added.  The results are being
            published in a special issue of The Astrophysical Journal Letters.  To image Sgr A, the team created the powerful EHT, which
            linked together eight existing radio observatories across the planet to form a single "Earth-sized" virtual telescope.
            The EHT observed Sgr A on multiple nights, collecting data for many hours in a row, similar to using a long exposure time on a
            camera.  The team had in 2019 released the first image of a black hole, called M87, at the centre of the more distant Messier
            87 galaxy.  They noted that the two black holes look remarkably similar, even though our galaxy\'s black hole is more than a
            thousand times smaller and less massive than M87.""",  # noqa: E501
        """
            Scientists are particularly excited to finally have images of two black holes of very different sizes, which offers the
            opportunity to understand how they compare and contrast.  They have also begun to use the new data to test theories and models
            of how gas behaves around supermassive black holes. This process is not yet fully understood but is thought to play a key role
            in shaping the formation and evolution of galaxies.'
        """,  # noqa: E501
    ]


@pytest.fixture
def mock_boolean_query_translated():
    """Mock response for request.post."""
    mock_response = MagicMock()
    query = {
        "query": {
            "es_query": {
                "must": [
                    {
                        "function_score": {
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "bool": {
                                                "should": [
                                                    {
                                                        "multi_match": {
                                                            "query": "Apple Music",
                                                            "fields": [
                                                                "content.split_word",
                                                                "title.split_word",
                                                            ],
                                                            "type": "phrase",
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "AppleMusic",
                                                            "fields": [
                                                                "content.split_word",
                                                                "title.split_word",
                                                            ],
                                                            "type": "best_fields",
                                                        }
                                                    },
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            "functions": [
                                {
                                    "script_score": {
                                        "script": {
                                            "source": "if (doc.containsKey('pagerank') && doc['pagerank'].size() > 0){ def pagerank = doc['pagerank'].value;  if (pagerank > 7)    { return params.pgrb_7_plus; }  else if (pagerank >= 4)    {  return params.pgrb_4_to_7; }  else if (pagerank >= 2)     { return params.pgrb_2_to_4; }  else     { return params.pgrb_less_than_2; }  } else  {return params.pgrb_none;}",  # noqa: E501
                                            "params": {
                                                "pgrb_7_plus": 13.0,
                                                "pgrb_4_to_7": 8.5,
                                                "pgrb_2_to_4": 3.5,
                                                "pgrb_less_than_2": 2.0,
                                                "pgrb_none": 1.0,
                                            },
                                        }
                                    },
                                    "weight": 100.0,
                                },
                                {
                                    "script_score": {
                                        "script": {
                                            "source": "if (doc.containsKey('publication_details.publication_tier') && doc['publication_details.publication_tier'].size() > 0){ def publication_tier = doc['publication_details.publication_tier'].value; if (publication_tier.contains('1'))   { return params.pbb_1; }  else if (publication_tier.contains('2'))   { return params.pbb_2; }  else   { return params.pbb_1; }  }else { return params.pbb_none;} ",  # noqa: E501
                                            "params": {
                                                "pbb_1": 3.0,
                                                "pbb_2": 2.0,
                                                "pbb_3": 1.0,
                                                "pbb_none": 2.0,
                                            },
                                        }
                                    },
                                    "weight": 50.0,
                                },
                                {
                                    "script_score": {
                                        "script": {
                                            "source": " def size = doc['content_size'].value; if (size < params.threshold)  { return params.factor; } else  { return 1;}",  # noqa: E501
                                            "params": {"threshold": 1000, "factor": 0},
                                        }
                                    }
                                },
                            ],
                            "boost_mode": "multiply",
                        }
                    }
                ]
            }
        },
        "filters": {
            "restrict_licenses": False,
            "country": ["ESP", "AND"],
            "date": {
                "start": "2023-12-27 17:04:00",
                "end": "2024-09-27 17:04:00",
                "time_zone": "+00:00",
            },
            "es_filter": {
                "must_not": [
                    {
                        "bool": {
                            "must": [
                                {
                                    "multi_match": {
                                        "query": "moreover",
                                        "fields": ["source"],
                                        "type": "best_fields",
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "print",
                                        "fields": ["media_type"],
                                        "type": "best_fields",
                                    }
                                },
                            ]
                        }
                    },
                    {"prefix": {"licenses": {"value": "AGR"}}},
                ]
            },
        },
        "media_types": ["print"],
        "sort": [{"published_on": {"order": "desc"}}],
        "return_fields": [
            "id",
            "domain",
            "title",
            "author",
            "publication",
            "publication_info",
            "metadata",
            "licenses",
            "is_copyrighted",
            "copyright",
            "published_on",
            "crawled_on",
            "amplification",
            "pagerank",
            "url",
            "country",
            "reach",
            "lang",
            "sentiment",
            "tags",
            "content",
            "highlight",
            "media_type",
            "thumbnail_url",
            "author_id",
            "score",
            "formatted_full_text",
            "iptc_topic",
            "presenter",
            "cluster_id",
            "publication_id",
            "wordplay_media_url",
            "publication_details",
            "ave",
            "ave_legacy",
            "domain_details",
            "source_article_id",
            "source",
        ],
    }
    # Create the final string
    mock_response.content = query
    return mock_response


@pytest.fixture
def mock_topic_profile_es_result_not_trending():
    """Mock response for topic profile elastic search query that isn't trending."""
    return {
        "took": 143,
        "timed_out": False,
        "num_reduce_phases": 2,
        "_shards": {"total": 720, "successful": 720, "skipped": 186, "failed": 0},
        "hits": {
            "total": {"value": 110, "relation": "eq"},
            "max_score": None,
            "hits": [],
        },
        "aggregations": {
            "daily_doc_count": {
                "buckets": [
                    {
                        "key_as_string": "2024-03-14T00:00:00.000Z",
                        "key": 1710374400000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-14T12:00:00.000Z",
                        "key": 1710417600000,
                        "doc_count": 6,
                    },
                    {
                        "key_as_string": "2024-03-15T00:00:00.000Z",
                        "key": 1710460800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-15T12:00:00.000Z",
                        "key": 1710504000000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-03-16T00:00:00.000Z",
                        "key": 1710547200000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-03-16T12:00:00.000Z",
                        "key": 1710590400000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-17T00:00:00.000Z",
                        "key": 1710633600000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-17T12:00:00.000Z",
                        "key": 1710676800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-18T00:00:00.000Z",
                        "key": 1710720000000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-18T12:00:00.000Z",
                        "key": 1710763200000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-03-19T00:00:00.000Z",
                        "key": 1710806400000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-19T12:00:00.000Z",
                        "key": 1710849600000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-03-20T00:00:00.000Z",
                        "key": 1710892800000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-20T12:00:00.000Z",
                        "key": 1710936000000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-21T00:00:00.000Z",
                        "key": 1710979200000,
                        "doc_count": 6,
                    },
                    {
                        "key_as_string": "2024-03-21T12:00:00.000Z",
                        "key": 1711022400000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-22T00:00:00.000Z",
                        "key": 1711065600000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-03-22T12:00:00.000Z",
                        "key": 1711108800000,
                        "doc_count": 6,
                    },
                    {
                        "key_as_string": "2024-03-23T00:00:00.000Z",
                        "key": 1711152000000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-23T12:00:00.000Z",
                        "key": 1711195200000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-24T00:00:00.000Z",
                        "key": 1711238400000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-24T12:00:00.000Z",
                        "key": 1711281600000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-03-25T00:00:00.000Z",
                        "key": 1711324800000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-25T12:00:00.000Z",
                        "key": 1711368000000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-03-26T00:00:00.000Z",
                        "key": 1711411200000,
                        "doc_count": 10,
                    },
                    {
                        "key_as_string": "2024-03-26T12:00:00.000Z",
                        "key": 1711454400000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-03-27T00:00:00.000Z",
                        "key": 1711497600000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-03-27T12:00:00.000Z",
                        "key": 1711540800000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-28T00:00:00.000Z",
                        "key": 1711584000000,
                        "doc_count": 6,
                    },
                ]
            }
        },
    }


@pytest.fixture
def mock_profile_es_result():
    """Mock response for profile elastic search query."""
    return {
        "took": 181,
        "timed_out": False,
        "num_reduce_phases": 2,
        "_shards": {"total": 720, "successful": 720, "skipped": 186, "failed": 0},
        "hits": {
            "total": {"value": 2557, "relation": "eq"},
            "max_score": None,
            "hits": [],
        },
        "aggregations": {
            "daily_doc_count": {
                "buckets": [
                    {
                        "key_as_string": "2024-03-14T00:00:00.000Z",
                        "key": 1710374400000,
                        "doc_count": 22,
                    },
                    {
                        "key_as_string": "2024-03-14T12:00:00.000Z",
                        "key": 1710417600000,
                        "doc_count": 161,
                    },
                    {
                        "key_as_string": "2024-03-15T00:00:00.000Z",
                        "key": 1710460800000,
                        "doc_count": 129,
                    },
                    {
                        "key_as_string": "2024-03-15T12:00:00.000Z",
                        "key": 1710504000000,
                        "doc_count": 114,
                    },
                    {
                        "key_as_string": "2024-03-16T00:00:00.000Z",
                        "key": 1710547200000,
                        "doc_count": 77,
                    },
                    {
                        "key_as_string": "2024-03-16T12:00:00.000Z",
                        "key": 1710590400000,
                        "doc_count": 61,
                    },
                    {
                        "key_as_string": "2024-03-17T00:00:00.000Z",
                        "key": 1710633600000,
                        "doc_count": 48,
                    },
                    {
                        "key_as_string": "2024-03-17T12:00:00.000Z",
                        "key": 1710676800000,
                        "doc_count": 69,
                    },
                    {
                        "key_as_string": "2024-03-18T00:00:00.000Z",
                        "key": 1710720000000,
                        "doc_count": 64,
                    },
                    {
                        "key_as_string": "2024-03-18T12:00:00.000Z",
                        "key": 1710763200000,
                        "doc_count": 81,
                    },
                    {
                        "key_as_string": "2024-03-19T00:00:00.000Z",
                        "key": 1710806400000,
                        "doc_count": 65,
                    },
                    {
                        "key_as_string": "2024-03-19T12:00:00.000Z",
                        "key": 1710849600000,
                        "doc_count": 105,
                    },
                    {
                        "key_as_string": "2024-03-20T00:00:00.000Z",
                        "key": 1710892800000,
                        "doc_count": 85,
                    },
                    {
                        "key_as_string": "2024-03-20T12:00:00.000Z",
                        "key": 1710936000000,
                        "doc_count": 84,
                    },
                    {
                        "key_as_string": "2024-03-21T00:00:00.000Z",
                        "key": 1710979200000,
                        "doc_count": 115,
                    },
                    {
                        "key_as_string": "2024-03-21T12:00:00.000Z",
                        "key": 1711022400000,
                        "doc_count": 168,
                    },
                    {
                        "key_as_string": "2024-03-22T00:00:00.000Z",
                        "key": 1711065600000,
                        "doc_count": 137,
                    },
                    {
                        "key_as_string": "2024-03-22T12:00:00.000Z",
                        "key": 1711108800000,
                        "doc_count": 119,
                    },
                    {
                        "key_as_string": "2024-03-23T00:00:00.000Z",
                        "key": 1711152000000,
                        "doc_count": 61,
                    },
                    {
                        "key_as_string": "2024-03-23T12:00:00.000Z",
                        "key": 1711195200000,
                        "doc_count": 70,
                    },
                    {
                        "key_as_string": "2024-03-24T00:00:00.000Z",
                        "key": 1711238400000,
                        "doc_count": 44,
                    },
                    {
                        "key_as_string": "2024-03-24T12:00:00.000Z",
                        "key": 1711281600000,
                        "doc_count": 55,
                    },
                    {
                        "key_as_string": "2024-03-25T00:00:00.000Z",
                        "key": 1711324800000,
                        "doc_count": 81,
                    },
                    {
                        "key_as_string": "2024-03-25T12:00:00.000Z",
                        "key": 1711368000000,
                        "doc_count": 90,
                    },
                    {
                        "key_as_string": "2024-03-26T00:00:00.000Z",
                        "key": 1711411200000,
                        "doc_count": 79,
                    },
                    {
                        "key_as_string": "2024-03-26T12:00:00.000Z",
                        "key": 1711454400000,
                        "doc_count": 129,
                    },
                    {
                        "key_as_string": "2024-03-27T00:00:00.000Z",
                        "key": 1711497600000,
                        "doc_count": 97,
                    },
                    {
                        "key_as_string": "2024-03-27T12:00:00.000Z",
                        "key": 1711540800000,
                        "doc_count": 97,
                    },
                    {
                        "key_as_string": "2024-03-28T00:00:00.000Z",
                        "key": 1711584000000,
                        "doc_count": 50,
                    },
                ]
            }
        },
    }


@pytest.fixture
def mock_topic_profile_es_result_trending():
    """Mock response for topic profile elastic search query that is trending."""
    return {
        "took": 143,
        "timed_out": False,
        "num_reduce_phases": 2,
        "_shards": {"total": 720, "successful": 720, "skipped": 186, "failed": 0},
        "hits": {
            "total": {"value": 110, "relation": "eq"},
            "max_score": None,
            "hits": [],
        },
        "aggregations": {
            "daily_doc_count": {
                "buckets": [
                    {
                        "key_as_string": "2024-03-14T00:00:00.000Z",
                        "key": 1710374400000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-14T12:00:00.000Z",
                        "key": 1710417600000,
                        "doc_count": 6,
                    },
                    {
                        "key_as_string": "2024-03-15T00:00:00.000Z",
                        "key": 1710460800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-15T12:00:00.000Z",
                        "key": 1710504000000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-03-16T00:00:00.000Z",
                        "key": 1710547200000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-03-16T12:00:00.000Z",
                        "key": 1710590400000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-17T00:00:00.000Z",
                        "key": 1710633600000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-17T12:00:00.000Z",
                        "key": 1710676800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-18T00:00:00.000Z",
                        "key": 1710720000000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-18T12:00:00.000Z",
                        "key": 1710763200000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-03-19T00:00:00.000Z",
                        "key": 1710806400000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-19T12:00:00.000Z",
                        "key": 1710849600000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-03-20T00:00:00.000Z",
                        "key": 1710892800000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-20T12:00:00.000Z",
                        "key": 1710936000000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-21T00:00:00.000Z",
                        "key": 1710979200000,
                        "doc_count": 6,
                    },
                    {
                        "key_as_string": "2024-03-21T12:00:00.000Z",
                        "key": 1711022400000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-22T00:00:00.000Z",
                        "key": 1711065600000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-03-22T12:00:00.000Z",
                        "key": 1711108800000,
                        "doc_count": 6,
                    },
                    {
                        "key_as_string": "2024-03-23T00:00:00.000Z",
                        "key": 1711152000000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-23T12:00:00.000Z",
                        "key": 1711195200000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-24T00:00:00.000Z",
                        "key": 1711238400000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-24T12:00:00.000Z",
                        "key": 1711281600000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-03-25T00:00:00.000Z",
                        "key": 1711324800000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-25T12:00:00.000Z",
                        "key": 1711368000000,
                        "doc_count": 10,
                    },
                    {
                        "key_as_string": "2024-03-26T00:00:00.000Z",
                        "key": 1711411200000,
                        "doc_count": 20,
                    },
                    {
                        "key_as_string": "2024-03-26T12:00:00.000Z",
                        "key": 1711454400000,
                        "doc_count": 32,
                    },
                    {
                        "key_as_string": "2024-03-27T00:00:00.000Z",
                        "key": 1711497600000,
                        "doc_count": 36,
                    },
                    {
                        "key_as_string": "2024-03-27T12:00:00.000Z",
                        "key": 1711540800000,
                        "doc_count": 41,
                    },
                    {
                        "key_as_string": "2024-03-28T00:00:00.000Z",
                        "key": 1711584000000,
                        "doc_count": 39,
                    },
                ]
            }
        },
    }


@pytest.fixture
def mock_all_global_query():
    """Mock response for number of total docs elastic search query (global trend)."""
    return {
        "took": 342,
        "timed_out": False,
        "num_reduce_phases": 2,
        "_shards": {"total": 720, "successful": 720, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 10000, "relation": "gte"},
            "max_score": None,
            "hits": [],
        },
        "aggregations": {
            "daily_doc_count": {
                "buckets": [
                    {
                        "key_as_string": "2024-01-01T00:00:00.000Z",
                        "key": 1704067200000,
                        "doc_count": 67748,
                    },
                    {
                        "key_as_string": "2024-01-02T00:00:00.000Z",
                        "key": 1704153600000,
                        "doc_count": 13651,
                    },
                    {
                        "key_as_string": "2024-01-03T00:00:00.000Z",
                        "key": 1704240000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-04T00:00:00.000Z",
                        "key": 1704326400000,
                        "doc_count": 16778,
                    },
                    {
                        "key_as_string": "2024-01-05T00:00:00.000Z",
                        "key": 1704412800000,
                        "doc_count": 59936,
                    },
                    {
                        "key_as_string": "2024-01-06T00:00:00.000Z",
                        "key": 1704499200000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-07T00:00:00.000Z",
                        "key": 1704585600000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-08T00:00:00.000Z",
                        "key": 1704672000000,
                        "doc_count": 197,
                    },
                    {
                        "key_as_string": "2024-01-09T00:00:00.000Z",
                        "key": 1704758400000,
                        "doc_count": 250101,
                    },
                    {
                        "key_as_string": "2024-01-10T00:00:00.000Z",
                        "key": 1704844800000,
                        "doc_count": 1324637,
                    },
                    {
                        "key_as_string": "2024-01-11T00:00:00.000Z",
                        "key": 1704931200000,
                        "doc_count": 1187612,
                    },
                    {
                        "key_as_string": "2024-01-12T00:00:00.000Z",
                        "key": 1705017600000,
                        "doc_count": 1088847,
                    },
                    {
                        "key_as_string": "2024-01-13T00:00:00.000Z",
                        "key": 1705104000000,
                        "doc_count": 802959,
                    },
                    {
                        "key_as_string": "2024-01-14T00:00:00.000Z",
                        "key": 1705190400000,
                        "doc_count": 830463,
                    },
                    {
                        "key_as_string": "2024-01-15T00:00:00.000Z",
                        "key": 1705276800000,
                        "doc_count": 1288578,
                    },
                    {
                        "key_as_string": "2024-01-16T00:00:00.000Z",
                        "key": 1705363200000,
                        "doc_count": 898290,
                    },
                    {
                        "key_as_string": "2024-01-17T00:00:00.000Z",
                        "key": 1705449600000,
                        "doc_count": 978659,
                    },
                    {
                        "key_as_string": "2024-01-18T00:00:00.000Z",
                        "key": 1705536000000,
                        "doc_count": 984179,
                    },
                    {
                        "key_as_string": "2024-01-19T00:00:00.000Z",
                        "key": 1705622400000,
                        "doc_count": 1035853,
                    },
                    {
                        "key_as_string": "2024-01-20T00:00:00.000Z",
                        "key": 1705708800000,
                        "doc_count": 782609,
                    },
                    {
                        "key_as_string": "2024-01-21T00:00:00.000Z",
                        "key": 1705795200000,
                        "doc_count": 718324,
                    },
                    {
                        "key_as_string": "2024-01-22T00:00:00.000Z",
                        "key": 1705881600000,
                        "doc_count": 957692,
                    },
                    {
                        "key_as_string": "2024-01-23T00:00:00.000Z",
                        "key": 1705968000000,
                        "doc_count": 1077973,
                    },
                    {
                        "key_as_string": "2024-01-24T00:00:00.000Z",
                        "key": 1706054400000,
                        "doc_count": 1187993,
                    },
                    {
                        "key_as_string": "2024-01-25T00:00:00.000Z",
                        "key": 1706140800000,
                        "doc_count": 1136871,
                    },
                    {
                        "key_as_string": "2024-01-26T00:00:00.000Z",
                        "key": 1706227200000,
                        "doc_count": 1078510,
                    },
                    {
                        "key_as_string": "2024-01-27T00:00:00.000Z",
                        "key": 1706313600000,
                        "doc_count": 823214,
                    },
                    {
                        "key_as_string": "2024-01-28T00:00:00.000Z",
                        "key": 1706400000000,
                        "doc_count": 730891,
                    },
                    {
                        "key_as_string": "2024-01-29T00:00:00.000Z",
                        "key": 1706486400000,
                        "doc_count": 999755,
                    },
                    {
                        "key_as_string": "2024-01-30T00:00:00.000Z",
                        "key": 1706572800000,
                        "doc_count": 1076116,
                    },
                    {
                        "key_as_string": "2024-01-31T00:00:00.000Z",
                        "key": 1706659200000,
                        "doc_count": 815610,
                    },
                    {
                        "key_as_string": "2024-02-01T00:00:00.000Z",
                        "key": 1706745600000,
                        "doc_count": 1257888,
                    },
                    {
                        "key_as_string": "2024-02-02T00:00:00.000Z",
                        "key": 1706832000000,
                        "doc_count": 1108245,
                    },
                    {
                        "key_as_string": "2024-02-03T00:00:00.000Z",
                        "key": 1706918400000,
                        "doc_count": 785380,
                    },
                    {
                        "key_as_string": "2024-02-04T00:00:00.000Z",
                        "key": 1707004800000,
                        "doc_count": 672303,
                    },
                    {
                        "key_as_string": "2024-02-05T00:00:00.000Z",
                        "key": 1707091200000,
                        "doc_count": 981176,
                    },
                    {
                        "key_as_string": "2024-02-06T00:00:00.000Z",
                        "key": 1707177600000,
                        "doc_count": 1078084,
                    },
                    {
                        "key_as_string": "2024-02-07T00:00:00.000Z",
                        "key": 1707264000000,
                        "doc_count": 897338,
                    },
                    {
                        "key_as_string": "2024-02-08T00:00:00.000Z",
                        "key": 1707350400000,
                        "doc_count": 1084344,
                    },
                    {
                        "key_as_string": "2024-02-09T00:00:00.000Z",
                        "key": 1707436800000,
                        "doc_count": 1028585,
                    },
                    {
                        "key_as_string": "2024-02-10T00:00:00.000Z",
                        "key": 1707523200000,
                        "doc_count": 737240,
                    },
                    {
                        "key_as_string": "2024-02-11T00:00:00.000Z",
                        "key": 1707609600000,
                        "doc_count": 627138,
                    },
                    {
                        "key_as_string": "2024-02-12T00:00:00.000Z",
                        "key": 1707696000000,
                        "doc_count": 874716,
                    },
                    {
                        "key_as_string": "2024-02-13T00:00:00.000Z",
                        "key": 1707782400000,
                        "doc_count": 641576,
                    },
                    {
                        "key_as_string": "2024-02-14T00:00:00.000Z",
                        "key": 1707868800000,
                        "doc_count": 1142908,
                    },
                    {
                        "key_as_string": "2024-02-15T00:00:00.000Z",
                        "key": 1707955200000,
                        "doc_count": 1046566,
                    },
                    {
                        "key_as_string": "2024-02-16T00:00:00.000Z",
                        "key": 1708041600000,
                        "doc_count": 1070050,
                    },
                    {
                        "key_as_string": "2024-02-17T00:00:00.000Z",
                        "key": 1708128000000,
                        "doc_count": 800130,
                    },
                    {
                        "key_as_string": "2024-02-18T00:00:00.000Z",
                        "key": 1708214400000,
                        "doc_count": 690197,
                    },
                    {
                        "key_as_string": "2024-02-19T00:00:00.000Z",
                        "key": 1708300800000,
                        "doc_count": 996675,
                    },
                    {
                        "key_as_string": "2024-02-20T00:00:00.000Z",
                        "key": 1708387200000,
                        "doc_count": 1057652,
                    },
                    {
                        "key_as_string": "2024-02-21T00:00:00.000Z",
                        "key": 1708473600000,
                        "doc_count": 1154834,
                    },
                    {
                        "key_as_string": "2024-02-22T00:00:00.000Z",
                        "key": 1708560000000,
                        "doc_count": 1144289,
                    },
                    {
                        "key_as_string": "2024-02-23T00:00:00.000Z",
                        "key": 1708646400000,
                        "doc_count": 1052024,
                    },
                    {
                        "key_as_string": "2024-02-24T00:00:00.000Z",
                        "key": 1708732800000,
                        "doc_count": 716493,
                    },
                    {
                        "key_as_string": "2024-02-25T00:00:00.000Z",
                        "key": 1708819200000,
                        "doc_count": 467355,
                    },
                    {
                        "key_as_string": "2024-02-26T00:00:00.000Z",
                        "key": 1708905600000,
                        "doc_count": 544582,
                    },
                    {
                        "key_as_string": "2024-02-27T00:00:00.000Z",
                        "key": 1708992000000,
                        "doc_count": 1317404,
                    },
                    {
                        "key_as_string": "2024-02-28T00:00:00.000Z",
                        "key": 1709078400000,
                        "doc_count": 1250025,
                    },
                    {
                        "key_as_string": "2024-02-29T00:00:00.000Z",
                        "key": 1709164800000,
                        "doc_count": 1131167,
                    },
                    {
                        "key_as_string": "2024-03-01T00:00:00.000Z",
                        "key": 1709251200000,
                        "doc_count": 1171953,
                    },
                    {
                        "key_as_string": "2024-03-02T00:00:00.000Z",
                        "key": 1709337600000,
                        "doc_count": 798017,
                    },
                    {
                        "key_as_string": "2024-03-03T00:00:00.000Z",
                        "key": 1709424000000,
                        "doc_count": 717094,
                    },
                    {
                        "key_as_string": "2024-03-04T00:00:00.000Z",
                        "key": 1709510400000,
                        "doc_count": 1016624,
                    },
                    {
                        "key_as_string": "2024-03-05T00:00:00.000Z",
                        "key": 1709596800000,
                        "doc_count": 1098522,
                    },
                    {
                        "key_as_string": "2024-03-06T00:00:00.000Z",
                        "key": 1709683200000,
                        "doc_count": 1122929,
                    },
                    {
                        "key_as_string": "2024-03-07T00:00:00.000Z",
                        "key": 1709769600000,
                        "doc_count": 1125973,
                    },
                    {
                        "key_as_string": "2024-03-08T00:00:00.000Z",
                        "key": 1709856000000,
                        "doc_count": 1057297,
                    },
                    {
                        "key_as_string": "2024-03-09T00:00:00.000Z",
                        "key": 1709942400000,
                        "doc_count": 799282,
                    },
                    {
                        "key_as_string": "2024-03-10T00:00:00.000Z",
                        "key": 1710028800000,
                        "doc_count": 730031,
                    },
                    {
                        "key_as_string": "2024-03-11T00:00:00.000Z",
                        "key": 1710115200000,
                        "doc_count": 1036136,
                    },
                    {
                        "key_as_string": "2024-03-12T00:00:00.000Z",
                        "key": 1710201600000,
                        "doc_count": 1088144,
                    },
                    {
                        "key_as_string": "2024-03-13T00:00:00.000Z",
                        "key": 1710288000000,
                        "doc_count": 1125828,
                    },
                    {
                        "key_as_string": "2024-03-14T00:00:00.000Z",
                        "key": 1710374400000,
                        "doc_count": 1036442,
                    },
                    {
                        "key_as_string": "2024-03-15T00:00:00.000Z",
                        "key": 1710460800000,
                        "doc_count": 1033589,
                    },
                    {
                        "key_as_string": "2024-03-16T00:00:00.000Z",
                        "key": 1710547200000,
                        "doc_count": 785763,
                    },
                    {
                        "key_as_string": "2024-03-17T00:00:00.000Z",
                        "key": 1710633600000,
                        "doc_count": 670738,
                    },
                    {
                        "key_as_string": "2024-03-18T00:00:00.000Z",
                        "key": 1710720000000,
                        "doc_count": 886529,
                    },
                    {
                        "key_as_string": "2024-03-19T00:00:00.000Z",
                        "key": 1710806400000,
                        "doc_count": 1045892,
                    },
                    {
                        "key_as_string": "2024-03-20T00:00:00.000Z",
                        "key": 1710892800000,
                        "doc_count": 1094908,
                    },
                    {
                        "key_as_string": "2024-03-21T00:00:00.000Z",
                        "key": 1710979200000,
                        "doc_count": 1101727,
                    },
                    {
                        "key_as_string": "2024-03-22T00:00:00.000Z",
                        "key": 1711065600000,
                        "doc_count": 1083266,
                    },
                    {
                        "key_as_string": "2024-03-23T00:00:00.000Z",
                        "key": 1711152000000,
                        "doc_count": 778646,
                    },
                    {
                        "key_as_string": "2024-03-24T00:00:00.000Z",
                        "key": 1711238400000,
                        "doc_count": 687946,
                    },
                    {
                        "key_as_string": "2024-03-25T00:00:00.000Z",
                        "key": 1711324800000,
                        "doc_count": 954033,
                    },
                    {
                        "key_as_string": "2024-03-26T00:00:00.000Z",
                        "key": 1711411200000,
                        "doc_count": 1077655,
                    },
                    {
                        "key_as_string": "2024-03-27T00:00:00.000Z",
                        "key": 1711497600000,
                        "doc_count": 1045056,
                    },
                    {
                        "key_as_string": "2024-03-28T00:00:00.000Z",
                        "key": 1711584000000,
                        "doc_count": 1085074,
                    },
                    {
                        "key_as_string": "2024-03-29T00:00:00.000Z",
                        "key": 1711670400000,
                        "doc_count": 980246,
                    },
                    {
                        "key_as_string": "2024-03-30T00:00:00.000Z",
                        "key": 1711756800000,
                        "doc_count": 731970,
                    },
                    {
                        "key_as_string": "2024-03-31T00:00:00.000Z",
                        "key": 1711843200000,
                        "doc_count": 661183,
                    },
                    {
                        "key_as_string": "2024-04-01T00:00:00.000Z",
                        "key": 1711929600000,
                        "doc_count": 887012,
                    },
                    {
                        "key_as_string": "2024-04-02T00:00:00.000Z",
                        "key": 1712016000000,
                        "doc_count": 1084044,
                    },
                    {
                        "key_as_string": "2024-04-03T00:00:00.000Z",
                        "key": 1712102400000,
                        "doc_count": 1083013,
                    },
                    {
                        "key_as_string": "2024-04-04T00:00:00.000Z",
                        "key": 1712188800000,
                        "doc_count": 1100062,
                    },
                    {
                        "key_as_string": "2024-04-05T00:00:00.000Z",
                        "key": 1712275200000,
                        "doc_count": 1040972,
                    },
                    {
                        "key_as_string": "2024-04-06T00:00:00.000Z",
                        "key": 1712361600000,
                        "doc_count": 756844,
                    },
                    {
                        "key_as_string": "2024-04-07T00:00:00.000Z",
                        "key": 1712448000000,
                        "doc_count": 642174,
                    },
                    {
                        "key_as_string": "2024-04-08T00:00:00.000Z",
                        "key": 1712534400000,
                        "doc_count": 984864,
                    },
                    {
                        "key_as_string": "2024-04-09T00:00:00.000Z",
                        "key": 1712620800000,
                        "doc_count": 1062724,
                    },
                    {
                        "key_as_string": "2024-04-10T00:00:00.000Z",
                        "key": 1712707200000,
                        "doc_count": 1001588,
                    },
                    {
                        "key_as_string": "2024-04-11T00:00:00.000Z",
                        "key": 1712793600000,
                        "doc_count": 1056250,
                    },
                    {
                        "key_as_string": "2024-04-12T00:00:00.000Z",
                        "key": 1712880000000,
                        "doc_count": 562375,
                    },
                ]
            }
        },
    }


@pytest.fixture
def mock_topic_global_query():
    """Mock response for number of total docs in a topic elastic search query (global trend)."""
    return {
        "took": 125,
        "timed_out": False,
        "num_reduce_phases": 2,
        "_shards": {"total": 720, "successful": 720, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 10000, "relation": "gte"},
            "max_score": None,
            "hits": [],
        },
        "aggregations": {
            "daily_doc_count": {
                "buckets": [
                    {
                        "key_as_string": "2024-01-01T00:00:00.000Z",
                        "key": 1704067200000,
                        "doc_count": 67,
                    },
                    {
                        "key_as_string": "2024-01-02T00:00:00.000Z",
                        "key": 1704153600000,
                        "doc_count": 15,
                    },
                    {
                        "key_as_string": "2024-01-03T00:00:00.000Z",
                        "key": 1704240000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-04T00:00:00.000Z",
                        "key": 1704326400000,
                        "doc_count": 47,
                    },
                    {
                        "key_as_string": "2024-01-05T00:00:00.000Z",
                        "key": 1704412800000,
                        "doc_count": 62,
                    },
                    {
                        "key_as_string": "2024-01-06T00:00:00.000Z",
                        "key": 1704499200000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-07T00:00:00.000Z",
                        "key": 1704585600000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-08T00:00:00.000Z",
                        "key": 1704672000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-09T00:00:00.000Z",
                        "key": 1704758400000,
                        "doc_count": 180,
                    },
                    {
                        "key_as_string": "2024-01-10T00:00:00.000Z",
                        "key": 1704844800000,
                        "doc_count": 765,
                    },
                    {
                        "key_as_string": "2024-01-11T00:00:00.000Z",
                        "key": 1704931200000,
                        "doc_count": 1117,
                    },
                    {
                        "key_as_string": "2024-01-12T00:00:00.000Z",
                        "key": 1705017600000,
                        "doc_count": 814,
                    },
                    {
                        "key_as_string": "2024-01-13T00:00:00.000Z",
                        "key": 1705104000000,
                        "doc_count": 362,
                    },
                    {
                        "key_as_string": "2024-01-14T00:00:00.000Z",
                        "key": 1705190400000,
                        "doc_count": 238,
                    },
                    {
                        "key_as_string": "2024-01-15T00:00:00.000Z",
                        "key": 1705276800000,
                        "doc_count": 574,
                    },
                    {
                        "key_as_string": "2024-01-16T00:00:00.000Z",
                        "key": 1705363200000,
                        "doc_count": 558,
                    },
                    {
                        "key_as_string": "2024-01-17T00:00:00.000Z",
                        "key": 1705449600000,
                        "doc_count": 661,
                    },
                    {
                        "key_as_string": "2024-01-18T00:00:00.000Z",
                        "key": 1705536000000,
                        "doc_count": 593,
                    },
                    {
                        "key_as_string": "2024-01-19T00:00:00.000Z",
                        "key": 1705622400000,
                        "doc_count": 600,
                    },
                    {
                        "key_as_string": "2024-01-20T00:00:00.000Z",
                        "key": 1705708800000,
                        "doc_count": 617,
                    },
                    {
                        "key_as_string": "2024-01-21T00:00:00.000Z",
                        "key": 1705795200000,
                        "doc_count": 307,
                    },
                    {
                        "key_as_string": "2024-01-22T00:00:00.000Z",
                        "key": 1705881600000,
                        "doc_count": 483,
                    },
                    {
                        "key_as_string": "2024-01-23T00:00:00.000Z",
                        "key": 1705968000000,
                        "doc_count": 728,
                    },
                    {
                        "key_as_string": "2024-01-24T00:00:00.000Z",
                        "key": 1706054400000,
                        "doc_count": 659,
                    },
                    {
                        "key_as_string": "2024-01-25T00:00:00.000Z",
                        "key": 1706140800000,
                        "doc_count": 646,
                    },
                    {
                        "key_as_string": "2024-01-26T00:00:00.000Z",
                        "key": 1706227200000,
                        "doc_count": 870,
                    },
                    {
                        "key_as_string": "2024-01-27T00:00:00.000Z",
                        "key": 1706313600000,
                        "doc_count": 540,
                    },
                    {
                        "key_as_string": "2024-01-28T00:00:00.000Z",
                        "key": 1706400000000,
                        "doc_count": 409,
                    },
                    {
                        "key_as_string": "2024-01-29T00:00:00.000Z",
                        "key": 1706486400000,
                        "doc_count": 626,
                    },
                    {
                        "key_as_string": "2024-01-30T00:00:00.000Z",
                        "key": 1706572800000,
                        "doc_count": 739,
                    },
                    {
                        "key_as_string": "2024-01-31T00:00:00.000Z",
                        "key": 1706659200000,
                        "doc_count": 424,
                    },
                    {
                        "key_as_string": "2024-02-01T00:00:00.000Z",
                        "key": 1706745600000,
                        "doc_count": 783,
                    },
                    {
                        "key_as_string": "2024-02-02T00:00:00.000Z",
                        "key": 1706832000000,
                        "doc_count": 808,
                    },
                    {
                        "key_as_string": "2024-02-03T00:00:00.000Z",
                        "key": 1706918400000,
                        "doc_count": 449,
                    },
                    {
                        "key_as_string": "2024-02-04T00:00:00.000Z",
                        "key": 1707004800000,
                        "doc_count": 559,
                    },
                    {
                        "key_as_string": "2024-02-05T00:00:00.000Z",
                        "key": 1707091200000,
                        "doc_count": 910,
                    },
                    {
                        "key_as_string": "2024-02-06T00:00:00.000Z",
                        "key": 1707177600000,
                        "doc_count": 868,
                    },
                    {
                        "key_as_string": "2024-02-07T00:00:00.000Z",
                        "key": 1707264000000,
                        "doc_count": 675,
                    },
                    {
                        "key_as_string": "2024-02-08T00:00:00.000Z",
                        "key": 1707350400000,
                        "doc_count": 661,
                    },
                    {
                        "key_as_string": "2024-02-09T00:00:00.000Z",
                        "key": 1707436800000,
                        "doc_count": 774,
                    },
                    {
                        "key_as_string": "2024-02-10T00:00:00.000Z",
                        "key": 1707523200000,
                        "doc_count": 545,
                    },
                    {
                        "key_as_string": "2024-02-11T00:00:00.000Z",
                        "key": 1707609600000,
                        "doc_count": 413,
                    },
                    {
                        "key_as_string": "2024-02-12T00:00:00.000Z",
                        "key": 1707696000000,
                        "doc_count": 592,
                    },
                    {
                        "key_as_string": "2024-02-13T00:00:00.000Z",
                        "key": 1707782400000,
                        "doc_count": 437,
                    },
                    {
                        "key_as_string": "2024-02-14T00:00:00.000Z",
                        "key": 1707868800000,
                        "doc_count": 1156,
                    },
                    {
                        "key_as_string": "2024-02-15T00:00:00.000Z",
                        "key": 1707955200000,
                        "doc_count": 787,
                    },
                    {
                        "key_as_string": "2024-02-16T00:00:00.000Z",
                        "key": 1708041600000,
                        "doc_count": 888,
                    },
                    {
                        "key_as_string": "2024-02-17T00:00:00.000Z",
                        "key": 1708128000000,
                        "doc_count": 508,
                    },
                    {
                        "key_as_string": "2024-02-18T00:00:00.000Z",
                        "key": 1708214400000,
                        "doc_count": 345,
                    },
                    {
                        "key_as_string": "2024-02-19T00:00:00.000Z",
                        "key": 1708300800000,
                        "doc_count": 532,
                    },
                    {
                        "key_as_string": "2024-02-20T00:00:00.000Z",
                        "key": 1708387200000,
                        "doc_count": 830,
                    },
                    {
                        "key_as_string": "2024-02-21T00:00:00.000Z",
                        "key": 1708473600000,
                        "doc_count": 1015,
                    },
                    {
                        "key_as_string": "2024-02-22T00:00:00.000Z",
                        "key": 1708560000000,
                        "doc_count": 1019,
                    },
                    {
                        "key_as_string": "2024-02-23T00:00:00.000Z",
                        "key": 1708646400000,
                        "doc_count": 1091,
                    },
                    {
                        "key_as_string": "2024-02-24T00:00:00.000Z",
                        "key": 1708732800000,
                        "doc_count": 606,
                    },
                    {
                        "key_as_string": "2024-02-25T00:00:00.000Z",
                        "key": 1708819200000,
                        "doc_count": 303,
                    },
                    {
                        "key_as_string": "2024-02-26T00:00:00.000Z",
                        "key": 1708905600000,
                        "doc_count": 454,
                    },
                    {
                        "key_as_string": "2024-02-27T00:00:00.000Z",
                        "key": 1708992000000,
                        "doc_count": 810,
                    },
                    {
                        "key_as_string": "2024-02-28T00:00:00.000Z",
                        "key": 1709078400000,
                        "doc_count": 1150,
                    },
                    {
                        "key_as_string": "2024-02-29T00:00:00.000Z",
                        "key": 1709164800000,
                        "doc_count": 674,
                    },
                    {
                        "key_as_string": "2024-03-01T00:00:00.000Z",
                        "key": 1709251200000,
                        "doc_count": 672,
                    },
                    {
                        "key_as_string": "2024-03-02T00:00:00.000Z",
                        "key": 1709337600000,
                        "doc_count": 543,
                    },
                    {
                        "key_as_string": "2024-03-03T00:00:00.000Z",
                        "key": 1709424000000,
                        "doc_count": 337,
                    },
                    {
                        "key_as_string": "2024-03-04T00:00:00.000Z",
                        "key": 1709510400000,
                        "doc_count": 470,
                    },
                    {
                        "key_as_string": "2024-03-05T00:00:00.000Z",
                        "key": 1709596800000,
                        "doc_count": 457,
                    },
                    {
                        "key_as_string": "2024-03-06T00:00:00.000Z",
                        "key": 1709683200000,
                        "doc_count": 705,
                    },
                    {
                        "key_as_string": "2024-03-07T00:00:00.000Z",
                        "key": 1709769600000,
                        "doc_count": 676,
                    },
                    {
                        "key_as_string": "2024-03-08T00:00:00.000Z",
                        "key": 1709856000000,
                        "doc_count": 645,
                    },
                    {
                        "key_as_string": "2024-03-09T00:00:00.000Z",
                        "key": 1709942400000,
                        "doc_count": 528,
                    },
                    {
                        "key_as_string": "2024-03-10T00:00:00.000Z",
                        "key": 1710028800000,
                        "doc_count": 358,
                    },
                    {
                        "key_as_string": "2024-03-11T00:00:00.000Z",
                        "key": 1710115200000,
                        "doc_count": 642,
                    },
                    {
                        "key_as_string": "2024-03-12T00:00:00.000Z",
                        "key": 1710201600000,
                        "doc_count": 901,
                    },
                    {
                        "key_as_string": "2024-03-13T00:00:00.000Z",
                        "key": 1710288000000,
                        "doc_count": 1677,
                    },
                    {
                        "key_as_string": "2024-03-14T00:00:00.000Z",
                        "key": 1710374400000,
                        "doc_count": 597,
                    },
                    {
                        "key_as_string": "2024-03-15T00:00:00.000Z",
                        "key": 1710460800000,
                        "doc_count": 712,
                    },
                    {
                        "key_as_string": "2024-03-16T00:00:00.000Z",
                        "key": 1710547200000,
                        "doc_count": 497,
                    },
                    {
                        "key_as_string": "2024-03-17T00:00:00.000Z",
                        "key": 1710633600000,
                        "doc_count": 294,
                    },
                    {
                        "key_as_string": "2024-03-18T00:00:00.000Z",
                        "key": 1710720000000,
                        "doc_count": 392,
                    },
                    {
                        "key_as_string": "2024-03-19T00:00:00.000Z",
                        "key": 1710806400000,
                        "doc_count": 664,
                    },
                    {
                        "key_as_string": "2024-03-20T00:00:00.000Z",
                        "key": 1710892800000,
                        "doc_count": 799,
                    },
                    {
                        "key_as_string": "2024-03-21T00:00:00.000Z",
                        "key": 1710979200000,
                        "doc_count": 723,
                    },
                    {
                        "key_as_string": "2024-03-22T00:00:00.000Z",
                        "key": 1711065600000,
                        "doc_count": 876,
                    },
                    {
                        "key_as_string": "2024-03-23T00:00:00.000Z",
                        "key": 1711152000000,
                        "doc_count": 477,
                    },
                    {
                        "key_as_string": "2024-03-24T00:00:00.000Z",
                        "key": 1711238400000,
                        "doc_count": 344,
                    },
                    {
                        "key_as_string": "2024-03-25T00:00:00.000Z",
                        "key": 1711324800000,
                        "doc_count": 531,
                    },
                    {
                        "key_as_string": "2024-03-26T00:00:00.000Z",
                        "key": 1711411200000,
                        "doc_count": 729,
                    },
                    {
                        "key_as_string": "2024-03-27T00:00:00.000Z",
                        "key": 1711497600000,
                        "doc_count": 875,
                    },
                    {
                        "key_as_string": "2024-03-28T00:00:00.000Z",
                        "key": 1711584000000,
                        "doc_count": 759,
                    },
                    {
                        "key_as_string": "2024-03-29T00:00:00.000Z",
                        "key": 1711670400000,
                        "doc_count": 1087,
                    },
                    {
                        "key_as_string": "2024-03-30T00:00:00.000Z",
                        "key": 1711756800000,
                        "doc_count": 649,
                    },
                    {
                        "key_as_string": "2024-03-31T00:00:00.000Z",
                        "key": 1711843200000,
                        "doc_count": 550,
                    },
                    {
                        "key_as_string": "2024-04-01T00:00:00.000Z",
                        "key": 1711929600000,
                        "doc_count": 531,
                    },
                    {
                        "key_as_string": "2024-04-02T00:00:00.000Z",
                        "key": 1712016000000,
                        "doc_count": 927,
                    },
                    {
                        "key_as_string": "2024-04-03T00:00:00.000Z",
                        "key": 1712102400000,
                        "doc_count": 677,
                    },
                    {
                        "key_as_string": "2024-04-04T00:00:00.000Z",
                        "key": 1712188800000,
                        "doc_count": 655,
                    },
                    {
                        "key_as_string": "2024-04-05T00:00:00.000Z",
                        "key": 1712275200000,
                        "doc_count": 637,
                    },
                    {
                        "key_as_string": "2024-04-06T00:00:00.000Z",
                        "key": 1712361600000,
                        "doc_count": 441,
                    },
                    {
                        "key_as_string": "2024-04-07T00:00:00.000Z",
                        "key": 1712448000000,
                        "doc_count": 389,
                    },
                    {
                        "key_as_string": "2024-04-08T00:00:00.000Z",
                        "key": 1712534400000,
                        "doc_count": 1015,
                    },
                    {
                        "key_as_string": "2024-04-09T00:00:00.000Z",
                        "key": 1712620800000,
                        "doc_count": 942,
                    },
                    {
                        "key_as_string": "2024-04-10T00:00:00.000Z",
                        "key": 1712707200000,
                        "doc_count": 847,
                    },
                    {
                        "key_as_string": "2024-04-11T00:00:00.000Z",
                        "key": 1712793600000,
                        "doc_count": 632,
                    },
                    {
                        "key_as_string": "2024-04-12T00:00:00.000Z",
                        "key": 1712880000000,
                        "doc_count": 329,
                    },
                ]
            }
        },
    }


@pytest.fixture
def mock_all_profile_boolean_query():
    """Mock response for number of total docs of a profile elastic search query (local trend)."""
    return {
        "took": 192,
        "timed_out": False,
        "num_reduce_phases": 2,
        "_shards": {"total": 720, "successful": 720, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 10000, "relation": "gte"},
            "max_score": None,
            "hits": [],
        },
        "aggregations": {
            "daily_doc_count": {
                "buckets": [
                    {
                        "key_as_string": "2024-01-01T00:00:00.000Z",
                        "key": 1704067200000,
                        "doc_count": 49,
                    },
                    {
                        "key_as_string": "2024-01-02T00:00:00.000Z",
                        "key": 1704153600000,
                        "doc_count": 11,
                    },
                    {
                        "key_as_string": "2024-01-03T00:00:00.000Z",
                        "key": 1704240000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-04T00:00:00.000Z",
                        "key": 1704326400000,
                        "doc_count": 24,
                    },
                    {
                        "key_as_string": "2024-01-05T00:00:00.000Z",
                        "key": 1704412800000,
                        "doc_count": 55,
                    },
                    {
                        "key_as_string": "2024-01-06T00:00:00.000Z",
                        "key": 1704499200000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-07T00:00:00.000Z",
                        "key": 1704585600000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-08T00:00:00.000Z",
                        "key": 1704672000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-09T00:00:00.000Z",
                        "key": 1704758400000,
                        "doc_count": 199,
                    },
                    {
                        "key_as_string": "2024-01-10T00:00:00.000Z",
                        "key": 1704844800000,
                        "doc_count": 524,
                    },
                    {
                        "key_as_string": "2024-01-11T00:00:00.000Z",
                        "key": 1704931200000,
                        "doc_count": 455,
                    },
                    {
                        "key_as_string": "2024-01-12T00:00:00.000Z",
                        "key": 1705017600000,
                        "doc_count": 500,
                    },
                    {
                        "key_as_string": "2024-01-13T00:00:00.000Z",
                        "key": 1705104000000,
                        "doc_count": 312,
                    },
                    {
                        "key_as_string": "2024-01-14T00:00:00.000Z",
                        "key": 1705190400000,
                        "doc_count": 303,
                    },
                    {
                        "key_as_string": "2024-01-15T00:00:00.000Z",
                        "key": 1705276800000,
                        "doc_count": 473,
                    },
                    {
                        "key_as_string": "2024-01-16T00:00:00.000Z",
                        "key": 1705363200000,
                        "doc_count": 591,
                    },
                    {
                        "key_as_string": "2024-01-17T00:00:00.000Z",
                        "key": 1705449600000,
                        "doc_count": 318,
                    },
                    {
                        "key_as_string": "2024-01-18T00:00:00.000Z",
                        "key": 1705536000000,
                        "doc_count": 426,
                    },
                    {
                        "key_as_string": "2024-01-19T00:00:00.000Z",
                        "key": 1705622400000,
                        "doc_count": 629,
                    },
                    {
                        "key_as_string": "2024-01-20T00:00:00.000Z",
                        "key": 1705708800000,
                        "doc_count": 345,
                    },
                    {
                        "key_as_string": "2024-01-21T00:00:00.000Z",
                        "key": 1705795200000,
                        "doc_count": 213,
                    },
                    {
                        "key_as_string": "2024-01-22T00:00:00.000Z",
                        "key": 1705881600000,
                        "doc_count": 654,
                    },
                    {
                        "key_as_string": "2024-01-23T00:00:00.000Z",
                        "key": 1705968000000,
                        "doc_count": 695,
                    },
                    {
                        "key_as_string": "2024-01-24T00:00:00.000Z",
                        "key": 1706054400000,
                        "doc_count": 561,
                    },
                    {
                        "key_as_string": "2024-01-25T00:00:00.000Z",
                        "key": 1706140800000,
                        "doc_count": 451,
                    },
                    {
                        "key_as_string": "2024-01-26T00:00:00.000Z",
                        "key": 1706227200000,
                        "doc_count": 523,
                    },
                    {
                        "key_as_string": "2024-01-27T00:00:00.000Z",
                        "key": 1706313600000,
                        "doc_count": 339,
                    },
                    {
                        "key_as_string": "2024-01-28T00:00:00.000Z",
                        "key": 1706400000000,
                        "doc_count": 287,
                    },
                    {
                        "key_as_string": "2024-01-29T00:00:00.000Z",
                        "key": 1706486400000,
                        "doc_count": 499,
                    },
                    {
                        "key_as_string": "2024-01-30T00:00:00.000Z",
                        "key": 1706572800000,
                        "doc_count": 484,
                    },
                    {
                        "key_as_string": "2024-01-31T00:00:00.000Z",
                        "key": 1706659200000,
                        "doc_count": 319,
                    },
                    {
                        "key_as_string": "2024-02-01T00:00:00.000Z",
                        "key": 1706745600000,
                        "doc_count": 540,
                    },
                    {
                        "key_as_string": "2024-02-02T00:00:00.000Z",
                        "key": 1706832000000,
                        "doc_count": 563,
                    },
                    {
                        "key_as_string": "2024-02-03T00:00:00.000Z",
                        "key": 1706918400000,
                        "doc_count": 303,
                    },
                    {
                        "key_as_string": "2024-02-04T00:00:00.000Z",
                        "key": 1707004800000,
                        "doc_count": 277,
                    },
                    {
                        "key_as_string": "2024-02-05T00:00:00.000Z",
                        "key": 1707091200000,
                        "doc_count": 483,
                    },
                    {
                        "key_as_string": "2024-02-06T00:00:00.000Z",
                        "key": 1707177600000,
                        "doc_count": 474,
                    },
                    {
                        "key_as_string": "2024-02-07T00:00:00.000Z",
                        "key": 1707264000000,
                        "doc_count": 394,
                    },
                    {
                        "key_as_string": "2024-02-08T00:00:00.000Z",
                        "key": 1707350400000,
                        "doc_count": 752,
                    },
                    {
                        "key_as_string": "2024-02-09T00:00:00.000Z",
                        "key": 1707436800000,
                        "doc_count": 895,
                    },
                    {
                        "key_as_string": "2024-02-10T00:00:00.000Z",
                        "key": 1707523200000,
                        "doc_count": 502,
                    },
                    {
                        "key_as_string": "2024-02-11T00:00:00.000Z",
                        "key": 1707609600000,
                        "doc_count": 635,
                    },
                    {
                        "key_as_string": "2024-02-12T00:00:00.000Z",
                        "key": 1707696000000,
                        "doc_count": 896,
                    },
                    {
                        "key_as_string": "2024-02-13T00:00:00.000Z",
                        "key": 1707782400000,
                        "doc_count": 366,
                    },
                    {
                        "key_as_string": "2024-02-14T00:00:00.000Z",
                        "key": 1707868800000,
                        "doc_count": 499,
                    },
                    {
                        "key_as_string": "2024-02-15T00:00:00.000Z",
                        "key": 1707955200000,
                        "doc_count": 464,
                    },
                    {
                        "key_as_string": "2024-02-16T00:00:00.000Z",
                        "key": 1708041600000,
                        "doc_count": 666,
                    },
                    {
                        "key_as_string": "2024-02-17T00:00:00.000Z",
                        "key": 1708128000000,
                        "doc_count": 272,
                    },
                    {
                        "key_as_string": "2024-02-18T00:00:00.000Z",
                        "key": 1708214400000,
                        "doc_count": 283,
                    },
                    {
                        "key_as_string": "2024-02-19T00:00:00.000Z",
                        "key": 1708300800000,
                        "doc_count": 496,
                    },
                    {
                        "key_as_string": "2024-02-20T00:00:00.000Z",
                        "key": 1708387200000,
                        "doc_count": 605,
                    },
                    {
                        "key_as_string": "2024-02-21T00:00:00.000Z",
                        "key": 1708473600000,
                        "doc_count": 515,
                    },
                    {
                        "key_as_string": "2024-02-22T00:00:00.000Z",
                        "key": 1708560000000,
                        "doc_count": 514,
                    },
                    {
                        "key_as_string": "2024-02-23T00:00:00.000Z",
                        "key": 1708646400000,
                        "doc_count": 772,
                    },
                    {
                        "key_as_string": "2024-02-24T00:00:00.000Z",
                        "key": 1708732800000,
                        "doc_count": 448,
                    },
                    {
                        "key_as_string": "2024-02-25T00:00:00.000Z",
                        "key": 1708819200000,
                        "doc_count": 202,
                    },
                    {
                        "key_as_string": "2024-02-26T00:00:00.000Z",
                        "key": 1708905600000,
                        "doc_count": 199,
                    },
                    {
                        "key_as_string": "2024-02-27T00:00:00.000Z",
                        "key": 1708992000000,
                        "doc_count": 547,
                    },
                    {
                        "key_as_string": "2024-02-28T00:00:00.000Z",
                        "key": 1709078400000,
                        "doc_count": 512,
                    },
                    {
                        "key_as_string": "2024-02-29T00:00:00.000Z",
                        "key": 1709164800000,
                        "doc_count": 471,
                    },
                    {
                        "key_as_string": "2024-03-01T00:00:00.000Z",
                        "key": 1709251200000,
                        "doc_count": 502,
                    },
                    {
                        "key_as_string": "2024-03-02T00:00:00.000Z",
                        "key": 1709337600000,
                        "doc_count": 346,
                    },
                    {
                        "key_as_string": "2024-03-03T00:00:00.000Z",
                        "key": 1709424000000,
                        "doc_count": 322,
                    },
                    {
                        "key_as_string": "2024-03-04T00:00:00.000Z",
                        "key": 1709510400000,
                        "doc_count": 682,
                    },
                    {
                        "key_as_string": "2024-03-05T00:00:00.000Z",
                        "key": 1709596800000,
                        "doc_count": 512,
                    },
                    {
                        "key_as_string": "2024-03-06T00:00:00.000Z",
                        "key": 1709683200000,
                        "doc_count": 589,
                    },
                    {
                        "key_as_string": "2024-03-07T00:00:00.000Z",
                        "key": 1709769600000,
                        "doc_count": 454,
                    },
                    {
                        "key_as_string": "2024-03-08T00:00:00.000Z",
                        "key": 1709856000000,
                        "doc_count": 477,
                    },
                    {
                        "key_as_string": "2024-03-09T00:00:00.000Z",
                        "key": 1709942400000,
                        "doc_count": 346,
                    },
                    {
                        "key_as_string": "2024-03-10T00:00:00.000Z",
                        "key": 1710028800000,
                        "doc_count": 272,
                    },
                    {
                        "key_as_string": "2024-03-11T00:00:00.000Z",
                        "key": 1710115200000,
                        "doc_count": 343,
                    },
                    {
                        "key_as_string": "2024-03-12T00:00:00.000Z",
                        "key": 1710201600000,
                        "doc_count": 556,
                    },
                    {
                        "key_as_string": "2024-03-13T00:00:00.000Z",
                        "key": 1710288000000,
                        "doc_count": 1887,
                    },
                    {
                        "key_as_string": "2024-03-14T00:00:00.000Z",
                        "key": 1710374400000,
                        "doc_count": 627,
                    },
                    {
                        "key_as_string": "2024-03-15T00:00:00.000Z",
                        "key": 1710460800000,
                        "doc_count": 633,
                    },
                    {
                        "key_as_string": "2024-03-16T00:00:00.000Z",
                        "key": 1710547200000,
                        "doc_count": 426,
                    },
                    {
                        "key_as_string": "2024-03-17T00:00:00.000Z",
                        "key": 1710633600000,
                        "doc_count": 321,
                    },
                    {
                        "key_as_string": "2024-03-18T00:00:00.000Z",
                        "key": 1710720000000,
                        "doc_count": 353,
                    },
                    {
                        "key_as_string": "2024-03-19T00:00:00.000Z",
                        "key": 1710806400000,
                        "doc_count": 320,
                    },
                    {
                        "key_as_string": "2024-03-20T00:00:00.000Z",
                        "key": 1710892800000,
                        "doc_count": 314,
                    },
                    {
                        "key_as_string": "2024-03-21T00:00:00.000Z",
                        "key": 1710979200000,
                        "doc_count": 715,
                    },
                    {
                        "key_as_string": "2024-03-22T00:00:00.000Z",
                        "key": 1711065600000,
                        "doc_count": 467,
                    },
                    {
                        "key_as_string": "2024-03-23T00:00:00.000Z",
                        "key": 1711152000000,
                        "doc_count": 245,
                    },
                    {
                        "key_as_string": "2024-03-24T00:00:00.000Z",
                        "key": 1711238400000,
                        "doc_count": 193,
                    },
                    {
                        "key_as_string": "2024-03-25T00:00:00.000Z",
                        "key": 1711324800000,
                        "doc_count": 323,
                    },
                    {
                        "key_as_string": "2024-03-26T00:00:00.000Z",
                        "key": 1711411200000,
                        "doc_count": 360,
                    },
                    {
                        "key_as_string": "2024-03-27T00:00:00.000Z",
                        "key": 1711497600000,
                        "doc_count": 347,
                    },
                    {
                        "key_as_string": "2024-03-28T00:00:00.000Z",
                        "key": 1711584000000,
                        "doc_count": 361,
                    },
                    {
                        "key_as_string": "2024-03-29T00:00:00.000Z",
                        "key": 1711670400000,
                        "doc_count": 446,
                    },
                    {
                        "key_as_string": "2024-03-30T00:00:00.000Z",
                        "key": 1711756800000,
                        "doc_count": 308,
                    },
                    {
                        "key_as_string": "2024-03-31T00:00:00.000Z",
                        "key": 1711843200000,
                        "doc_count": 258,
                    },
                    {
                        "key_as_string": "2024-04-01T00:00:00.000Z",
                        "key": 1711929600000,
                        "doc_count": 306,
                    },
                    {
                        "key_as_string": "2024-04-02T00:00:00.000Z",
                        "key": 1712016000000,
                        "doc_count": 435,
                    },
                    {
                        "key_as_string": "2024-04-03T00:00:00.000Z",
                        "key": 1712102400000,
                        "doc_count": 539,
                    },
                    {
                        "key_as_string": "2024-04-04T00:00:00.000Z",
                        "key": 1712188800000,
                        "doc_count": 515,
                    },
                    {
                        "key_as_string": "2024-04-05T00:00:00.000Z",
                        "key": 1712275200000,
                        "doc_count": 633,
                    },
                    {
                        "key_as_string": "2024-04-06T00:00:00.000Z",
                        "key": 1712361600000,
                        "doc_count": 347,
                    },
                    {
                        "key_as_string": "2024-04-07T00:00:00.000Z",
                        "key": 1712448000000,
                        "doc_count": 253,
                    },
                    {
                        "key_as_string": "2024-04-08T00:00:00.000Z",
                        "key": 1712534400000,
                        "doc_count": 499,
                    },
                    {
                        "key_as_string": "2024-04-09T00:00:00.000Z",
                        "key": 1712620800000,
                        "doc_count": 401,
                    },
                    {
                        "key_as_string": "2024-04-10T00:00:00.000Z",
                        "key": 1712707200000,
                        "doc_count": 478,
                    },
                    {
                        "key_as_string": "2024-04-11T00:00:00.000Z",
                        "key": 1712793600000,
                        "doc_count": 647,
                    },
                    {
                        "key_as_string": "2024-04-12T00:00:00.000Z",
                        "key": 1712880000000,
                        "doc_count": 240,
                    },
                ]
            }
        },
    }


@pytest.fixture
def mock_topic_profile_query():
    """Mock response for number of total docs of a profile in a topic ES query (local trend)."""
    return {
        "took": 155,
        "timed_out": False,
        "num_reduce_phases": 2,
        "_shards": {"total": 720, "successful": 720, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 414, "relation": "eq"},
            "max_score": None,
            "hits": [],
        },
        "aggregations": {
            "daily_doc_count": {
                "buckets": [
                    {
                        "key_as_string": "2024-01-01T00:00:00.000Z",
                        "key": 1704067200000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-01-02T00:00:00.000Z",
                        "key": 1704153600000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-03T00:00:00.000Z",
                        "key": 1704240000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-04T00:00:00.000Z",
                        "key": 1704326400000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-05T00:00:00.000Z",
                        "key": 1704412800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-01-06T00:00:00.000Z",
                        "key": 1704499200000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-07T00:00:00.000Z",
                        "key": 1704585600000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-08T00:00:00.000Z",
                        "key": 1704672000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-09T00:00:00.000Z",
                        "key": 1704758400000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-01-10T00:00:00.000Z",
                        "key": 1704844800000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-01-11T00:00:00.000Z",
                        "key": 1704931200000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-01-12T00:00:00.000Z",
                        "key": 1705017600000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-01-13T00:00:00.000Z",
                        "key": 1705104000000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-01-14T00:00:00.000Z",
                        "key": 1705190400000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-15T00:00:00.000Z",
                        "key": 1705276800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-01-16T00:00:00.000Z",
                        "key": 1705363200000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-01-17T00:00:00.000Z",
                        "key": 1705449600000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-01-18T00:00:00.000Z",
                        "key": 1705536000000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-01-19T00:00:00.000Z",
                        "key": 1705622400000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-01-20T00:00:00.000Z",
                        "key": 1705708800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-01-21T00:00:00.000Z",
                        "key": 1705795200000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-01-22T00:00:00.000Z",
                        "key": 1705881600000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-01-23T00:00:00.000Z",
                        "key": 1705968000000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-01-24T00:00:00.000Z",
                        "key": 1706054400000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-01-25T00:00:00.000Z",
                        "key": 1706140800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-01-26T00:00:00.000Z",
                        "key": 1706227200000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-01-27T00:00:00.000Z",
                        "key": 1706313600000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-01-28T00:00:00.000Z",
                        "key": 1706400000000,
                        "doc_count": 14,
                    },
                    {
                        "key_as_string": "2024-01-29T00:00:00.000Z",
                        "key": 1706486400000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-01-30T00:00:00.000Z",
                        "key": 1706572800000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-01-31T00:00:00.000Z",
                        "key": 1706659200000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-02-01T00:00:00.000Z",
                        "key": 1706745600000,
                        "doc_count": 8,
                    },
                    {
                        "key_as_string": "2024-02-02T00:00:00.000Z",
                        "key": 1706832000000,
                        "doc_count": 8,
                    },
                    {
                        "key_as_string": "2024-02-03T00:00:00.000Z",
                        "key": 1706918400000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-02-04T00:00:00.000Z",
                        "key": 1707004800000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-02-05T00:00:00.000Z",
                        "key": 1707091200000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-02-06T00:00:00.000Z",
                        "key": 1707177600000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-02-07T00:00:00.000Z",
                        "key": 1707264000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-02-08T00:00:00.000Z",
                        "key": 1707350400000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-02-09T00:00:00.000Z",
                        "key": 1707436800000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-02-10T00:00:00.000Z",
                        "key": 1707523200000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-02-11T00:00:00.000Z",
                        "key": 1707609600000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-02-12T00:00:00.000Z",
                        "key": 1707696000000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-02-13T00:00:00.000Z",
                        "key": 1707782400000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-02-14T00:00:00.000Z",
                        "key": 1707868800000,
                        "doc_count": 10,
                    },
                    {
                        "key_as_string": "2024-02-15T00:00:00.000Z",
                        "key": 1707955200000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-02-16T00:00:00.000Z",
                        "key": 1708041600000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-02-17T00:00:00.000Z",
                        "key": 1708128000000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-02-18T00:00:00.000Z",
                        "key": 1708214400000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-02-19T00:00:00.000Z",
                        "key": 1708300800000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-02-20T00:00:00.000Z",
                        "key": 1708387200000,
                        "doc_count": 7,
                    },
                    {
                        "key_as_string": "2024-02-21T00:00:00.000Z",
                        "key": 1708473600000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-02-22T00:00:00.000Z",
                        "key": 1708560000000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-02-23T00:00:00.000Z",
                        "key": 1708646400000,
                        "doc_count": 10,
                    },
                    {
                        "key_as_string": "2024-02-24T00:00:00.000Z",
                        "key": 1708732800000,
                        "doc_count": 10,
                    },
                    {
                        "key_as_string": "2024-02-25T00:00:00.000Z",
                        "key": 1708819200000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-02-26T00:00:00.000Z",
                        "key": 1708905600000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-02-27T00:00:00.000Z",
                        "key": 1708992000000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-02-28T00:00:00.000Z",
                        "key": 1709078400000,
                        "doc_count": 8,
                    },
                    {
                        "key_as_string": "2024-02-29T00:00:00.000Z",
                        "key": 1709164800000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-01T00:00:00.000Z",
                        "key": 1709251200000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-02T00:00:00.000Z",
                        "key": 1709337600000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-03T00:00:00.000Z",
                        "key": 1709424000000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-04T00:00:00.000Z",
                        "key": 1709510400000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-05T00:00:00.000Z",
                        "key": 1709596800000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-06T00:00:00.000Z",
                        "key": 1709683200000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-07T00:00:00.000Z",
                        "key": 1709769600000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-08T00:00:00.000Z",
                        "key": 1709856000000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-03-09T00:00:00.000Z",
                        "key": 1709942400000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-03-10T00:00:00.000Z",
                        "key": 1710028800000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-11T00:00:00.000Z",
                        "key": 1710115200000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-12T00:00:00.000Z",
                        "key": 1710201600000,
                        "doc_count": 20,
                    },
                    {
                        "key_as_string": "2024-03-13T00:00:00.000Z",
                        "key": 1710288000000,
                        "doc_count": 86,
                    },
                    {
                        "key_as_string": "2024-03-14T00:00:00.000Z",
                        "key": 1710374400000,
                        "doc_count": 16,
                    },
                    {
                        "key_as_string": "2024-03-15T00:00:00.000Z",
                        "key": 1710460800000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-16T00:00:00.000Z",
                        "key": 1710547200000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-17T00:00:00.000Z",
                        "key": 1710633600000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-18T00:00:00.000Z",
                        "key": 1710720000000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-03-19T00:00:00.000Z",
                        "key": 1710806400000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-20T00:00:00.000Z",
                        "key": 1710892800000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-03-21T00:00:00.000Z",
                        "key": 1710979200000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-03-22T00:00:00.000Z",
                        "key": 1711065600000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-03-23T00:00:00.000Z",
                        "key": 1711152000000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-24T00:00:00.000Z",
                        "key": 1711238400000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-03-25T00:00:00.000Z",
                        "key": 1711324800000,
                        "doc_count": 5,
                    },
                    {
                        "key_as_string": "2024-03-26T00:00:00.000Z",
                        "key": 1711411200000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-27T00:00:00.000Z",
                        "key": 1711497600000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-28T00:00:00.000Z",
                        "key": 1711584000000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-03-29T00:00:00.000Z",
                        "key": 1711670400000,
                        "doc_count": 13,
                    },
                    {
                        "key_as_string": "2024-03-30T00:00:00.000Z",
                        "key": 1711756800000,
                        "doc_count": 6,
                    },
                    {
                        "key_as_string": "2024-03-31T00:00:00.000Z",
                        "key": 1711843200000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-04-01T00:00:00.000Z",
                        "key": 1711929600000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-04-02T00:00:00.000Z",
                        "key": 1712016000000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-04-03T00:00:00.000Z",
                        "key": 1712102400000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-04-04T00:00:00.000Z",
                        "key": 1712188800000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-04-05T00:00:00.000Z",
                        "key": 1712275200000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-04-06T00:00:00.000Z",
                        "key": 1712361600000,
                        "doc_count": 0,
                    },
                    {
                        "key_as_string": "2024-04-07T00:00:00.000Z",
                        "key": 1712448000000,
                        "doc_count": 1,
                    },
                    {
                        "key_as_string": "2024-04-08T00:00:00.000Z",
                        "key": 1712534400000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-04-09T00:00:00.000Z",
                        "key": 1712620800000,
                        "doc_count": 3,
                    },
                    {
                        "key_as_string": "2024-04-10T00:00:00.000Z",
                        "key": 1712707200000,
                        "doc_count": 4,
                    },
                    {
                        "key_as_string": "2024-04-11T00:00:00.000Z",
                        "key": 1712793600000,
                        "doc_count": 2,
                    },
                    {
                        "key_as_string": "2024-04-12T00:00:00.000Z",
                        "key": 1712880000000,
                        "doc_count": 2,
                    },
                ]
            }
        },
    }
