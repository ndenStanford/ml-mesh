# isort: skip_file
"""Conftest."""

# Standard Library
from typing import Dict

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.schema import BioResponseSchema
from src.serve.__main__ import get_model_server


@pytest.fixture
def test_serving_params():
    """Serving params fixture."""
    return ServingParams()


@pytest.fixture
def test_inference_params() -> str:
    """Predict parameter fixture."""
    return {}


@pytest.fixture
def test_client():
    """Client fixture."""
    model_server = get_model_server()

    return TestClient(model_server)


@pytest.fixture
def test_predict_input() -> str:
    """Predict input fixture."""
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
def test_expected_predict_output() -> Dict[str, str]:
    """Expected predict output fixture. Temporarily unused bc GPT responses drift within 30mins."""
    return {
        "version": 1,
        "data": {
            "identifier": None,
            "namespace": "topic-summarization",
            "attributes": {
                "topic": {
                    "Opportunities": {
                        "Opportunities analysis ": "The composite analysis of the given articles reveals significant opportunities across different sectors within the scope of scientific and technological advancements. India is at the cusp of a semiconductor revolution, potentially leading to substantial economic development in local manufacturing. Concurrently, the chemical fluorophore market, vital for biological research, reflects a growing niche for specialized chemical production and related technological progress. Additionally, the imaging of Sagittarius A heralds a new frontier in astrophysics, promising unprecedented insights into cosmic phenomena and propelling further scientific and technological exploration.",  # noqa: E501
                        "Opportunities theme ": "Scientific and Technological Expansion as a Springboard for Economic and Knowledge Growth",  # noqa: E501
                        "Opportunities impact ": "High",
                    },  # noqa: E501
                    "Risk detection": {
                        "Risk detection analysis ": "In the context of risk detection within the semiconductor industry, advancements are focusing on coping with the challenges posed by the digital transformation, particularly in the burgeoning Indian market which faces cyber and operational risks. Additionally, there is an exploration of chemical fluorophores as innovative tools for environmental and biological monitoring. This scientific pursuit is complemented by natural models, such as redundancy in sensory systems that propel the design of more robust risk detection methods. Together, these advances represent a multifaceted approach to risk detection, integrating technology, biology, and design principles derived from nature.",  # noqa: E501
                        "Risk detection theme ": "Integrative improvements in risk detection blending technology, biological science, and natural design principles.",  # noqa: E501
                        "Risk detection impact ": "High",
                    },  # noqa: E501
                    "Threats for the brand": {
                        "Threats for the brand analysis ": "Brands in the target industry are presently facing multifaceted threats that range from supply chain disruptions, particularly in the import of semiconductors, to resource scarcity driven by environmental changes. Additionally, there's a pressing need for brands to stay at the forefront of technological advancements in biochemistry to sustain competitiveness. A particular challenge is the adaptation of products to circumvent biological redundancies in certain organisms, such as mosquitoes, which could render some products ineffective. The adaptability and innovation of brands are crucial in overcoming these threats; those that fail to evolve may confront significant setbacks.",  # noqa: E501
                        "Threats for the brand theme ": "Adaptation and Innovation in the Face of Technological and Environmental Challenges",  # noqa: E501
                        "Threats for the brand impact ": "High",
                    },  # noqa: E501
                    "Company or spokespersons": {
                        "Company or spokespersons analysis ": "Industry thought leaders, including Krishna Moorthy of IESA, Neil Shah of Counterpoint Research, Avi Loeb, a representative from Alfa Chemistry, and Geoffrey Bower of the EHT Project, are actively contributing to the discourse in their respective sectors. Their insights are not only shaping the semiconductor market, particularly in India, but also expanding knowledge in the search for extraterrestrial life, the use of chemical fluorophores in biosciences, and in understanding the universe through black hole observations. These spokespersons symbolize the forefront of innovation, scientific exploration, and market intelligence.",  # noqa: E501
                        "Company or spokespersons theme ": "Advancing Industry Frontiers: Influencers Shaping Future Dialogue and Innovation",  # noqa: E501
                        "Company or spokespersons impact ": "High",
                    },  # noqa: E501
                    "Brand Reputation": {
                        "Brand Reputation analysis ": "The collective insights from various articles suggest a trend of positive developments within specialized fields that significantly enhance brand reputations. India's venture into the semiconductor market has poised it to fortify a global electronics reputation, while Alfa Chemistry has augmented its standing in the scientific community through chemical innovations. Furthermore, the EHT Collaboration's successful black hole imaging has notably propelled the prestige of involved research institutions. These advancements serve as testament to the entities' commitment to innovation and expertise, which are fundamental to their brand reputations.",  # noqa: E501
                        "Brand Reputation theme ": "Innovation leading to enhanced global recognition and prestige in specialized sectors.",  # noqa: E501
                        "Brand Reputation impact ": "High",
                    },  # noqa: E501
                    "CEO Reputation": {
                        "CEO Reputation analysis ": "Leaders within the scientific and technological community are solidifying their reputations by spearheading significant advancements and innovations. Krishna Moorthy has cemented his status as a progressive leader in the semiconductor industry with his foresight into chip applications. Avi Loeb's reputation as a visionary is supported by his scholarly work on extraterrestrial life and contributions to astrophysics. Meanwhile, Geoffrey Bower's reputation benefits from his role in making pioneering scientific breakthroughs. Each of these leaders demonstrate how contributing to the collective knowledge and progress within their fields is a strong path to enhancing personal and professional reputation.",  # noqa: E501
                        "CEO Reputation theme ": "Futuristic Vision and Pioneering Innovations as Pillars of CEO Reputation",  # noqa: E501
                        "CEO Reputation impact ": "High",
                    },  # noqa: E501
                    "Customer Response": {
                        "Customer Response analysis ": "The input articles suggest that various developments in technology and environmental changes could lead to a diverse range of customer responses across multiple sectors. While there's an implication of increased demand for advanced electronics, eco-friendly gardening solutions, and products like mosquito repellants, the articles lack direct evidence of customer response. This indicates that although there might be shifts in consumer demands due to these factors, the actual impact on customer behavior is not conclusively reported and warrants further examination.",  # noqa: E501
                        "Customer Response theme ": "Implications of Evolving Customer Demand in Response to Technological and Environmental Changes",  # noqa: E501
                        "Customer Response impact ": "Low",
                    },  # noqa: E501
                    "Stock Price Impact": {
                        "Stock Price Impact analysis ": "The expected growth in India's semiconductor market could lead to a positive impact on the stock prices of companies within the semiconductor industry, as increases in demand typically drive financial performance. Additionally, the advancements or increased usage of chemical fluorophores in biochemical applications could similarly influence the stock prices of companies that produce or utilize these chemicals. However, these influences appear to be specific and related to certain companies or sectors within the broader industry.",  # noqa: E501
                        "Stock Price Impact theme ": "Sector-Specific Growth and Technological Applications Driving Stock Prices",  # noqa: E501
                        "Stock Price Impact impact ": "Medium",
                    },  # noqa: E501
                    "Industry trends": {
                        "Industry trends analysis ": "The industry trends demonstrate robust expansion, with the semiconductor market notably surging in regions like India due to escalating demands for high-tech components in diverse industries. Additionally, the biological sciences have observed a surge in innovation, with the broadening application of chemical fluorophores signaling an enhancement in research and analytical capabilities. Collectively, these developments suggest a momentous drive towards technological enhancement and intricacy across different sectors of the industry.",  # noqa: E501
                        "Industry trends theme ": "Technological Enhancement and Market Expansion",  # noqa: E501
                        "Industry trends impact ": "High",
                    },  # noqa: E501
                    "Environmental, social and governance": {
                        "Environmental, social and governance analysis ": "The Environmental, social and governance (ESG) considerations within the target industry encompass a spectrum of initiatives and challenges. These include the integration of semiconductors in clean vehicles, which demonstrates the commitment to sustainable practices and technology adoption. Water conservation techniques showcase proactive measures to manage natural resources prudently, while the acknowledgment of climate change's role in exacerbating extreme weather conditions highlights the environmental risks businesses face. The employment of fluorophores for environmental monitoring is indicative of emerging tools for ecological assessment. On the social dimension, the focus is on public health and disease prevention, which is integral to the ESG's social pillar. Finally, the mention of fermentation in gardening signals a nod towards innovative yet sustainable agricultural practices. While other articles seem less connected to ESG, the collected insights point towards a sector grappling with environmental challenges and social responsibilities, aiming to adopt best practices in both realms.",  # noqa: E501
                        "Environmental, social and governance theme ": "Adopting Sustainable Technologies and Practices",  # noqa: E501
                        "Environmental, social and governance impact ": "Medium",
                    },  # noqa: E501
                    "Summary": "The recent diaspora of global developments encapsulates technological progress, environmental challenges, and socio-political concerns. India's semiconductor market is on an upsurge, paralleled by a global emphasis on water conservation amid climate change. As Taiwan braces for a typhoon, Germany and Italy underscore the vital need for meteorological foresight. Scientific curiosity probes both the microcosm, in advances in fluorescence and skin care tech, and the macrocosm, through unveiling cosmic mysteries and pursuing lunar exploration. Marine biology and botany burgeon, driven by patents and public interest, while health and security issues engender responses to mosquito-borne diseases, drug trafficking, and airspace violations. Collectively, these snapshots from diverse fields illustrate an era marked by an adaptive humanity as it navigates a balance between exploiting and conserving its natural and intellectual resources.",  # noqa: E501
                    "Theme": "Adaptive Progress in a Changing World",
                },  # noqa: E501
            },
        },
    }


@pytest.fixture
def test_model_name() -> str:
    """Test model name fixture."""
    return "topic-summarization"


@pytest.fixture
def test_expected_bio_output(test_model_name):
    """Test expected bio output."""
    return BioResponseSchema.from_data(
        version=1,
        namespace="topic-summarization",
        attributes={"model_name": "topic-summarization"},
    )
