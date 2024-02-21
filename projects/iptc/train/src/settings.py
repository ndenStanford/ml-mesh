"""Settings."""

# Standard Library
import os
from typing import List

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# --- atomic settings and models
CLASS_DICT_FIRST = {
    "root": {
        "LABEL_0": "arts, culture, entertainment and media",
        "LABEL_1": "conflict, war and peace",
        "LABEL_2": "crime, law and justice",
        "LABEL_3": "disaster, accident and emergency incident",
        "LABEL_4": "economy, business and finance",
        "LABEL_5": "education",
        "LABEL_6": "environment",
        "LABEL_7": "health",
        "LABEL_8": "labour",
        "LABEL_9": "lifestyle and leisure",
        "LABEL_10": "politics",
        "LABEL_11": "religion",
        "LABEL_12": "science and technology",
        "LABEL_13": "society",
        "LABEL_14": "sport",
        "LABEL_15": "weather",
    }
}

CLASS_DICT_SECOND = {
    "arts, culture, entertainment and media": {
        "LABEL_0": "arts and entertainment",
        "LABEL_1": "culture",
        "LABEL_2": "mass media",
    },
    "conflict, war and peace": {
        "LABEL_0": "armed conflict",
        "LABEL_1": "civil unrest",
        "LABEL_2": "act of terror",
        "LABEL_3": "massacre",
        "LABEL_4": "peace process",
        "LABEL_5": "post-war reconstruction",
        "LABEL_6": "coup d'etat",
    },
    "crime, law and justice": {
        "LABEL_0": "judiciary",
        "LABEL_1": "law enforcement",
        "LABEL_2": "law",
        "LABEL_3": "crime",
        "LABEL_4": "justice and rights",
    },
    "disaster, accident and emergency incident": {
        "LABEL_0": "disaster",
        "LABEL_1": "accident and emergency incident",
        "LABEL_2": "emergency response",
    },
    "economy, business and finance": {
        "LABEL_0": "economy",
        "LABEL_1": "economic sector",
        "LABEL_2": "business information",
        "LABEL_3": "market and exchange",
    },
    "education": {
        "LABEL_0": "school",
        "LABEL_1": "religious education",
        "LABEL_2": "teaching and learning",
    },
    "environment": {
        "LABEL_0": "natural resources",
        "LABEL_1": "conservation",
        "LABEL_2": "environmental pollution",
        "LABEL_3": "climate change",
        "LABEL_4": "nature",
        "LABEL_5": "environmental politics",
    },
    "health": {
        "LABEL_0": "health treatment and procedure",
        "LABEL_1": "disease and condition",
        "LABEL_2": "government health care",
        "LABEL_3": "health insurance",
        "LABEL_4": "health facility",
        "LABEL_5": "medical profession",
        "LABEL_6": "non-human diseases",
    },
    "labour": {
        "LABEL_0": "employment",
        "LABEL_1": "retirement",
        "LABEL_2": "unemployment",
        "LABEL_3": "employment legislation",
        "LABEL_4": "labour relations",
        "LABEL_5": "unions",
    },
    "lifestyle and leisure": {"LABEL_0": "leisure", "LABEL_1": "lifestyle"},
    "politics": {
        "LABEL_0": "government",
        "LABEL_1": "election",
        "LABEL_2": "international relations",
        "LABEL_3": "government policy",
        "LABEL_4": "fundamental rights",
        "LABEL_5": "political process",
    },
    "religion": {
        "LABEL_0": "belief systems",
        "LABEL_1": "religious text",
        "LABEL_2": "religious facility",
        "LABEL_3": "religious festival or holiday",
    },
    "science and technology": {
        "LABEL_0": "natural science",
        "LABEL_1": "technology and engineering",
        "LABEL_2": "biomedical science",
        "LABEL_3": "social sciences",
        "LABEL_4": "mathematics",
        "LABEL_5": "scientific research",
        "LABEL_6": "mechanical engineering",
    },
    "society": {
        "LABEL_0": "demographics",
        "LABEL_1": "family",
        "LABEL_2": "values",
        "LABEL_3": "social problem",
        "LABEL_4": "discrimination",
        "LABEL_5": "welfare",
        "LABEL_6": "social condition",
        "LABEL_7": "mankind",
        "LABEL_8": "communities",
    },
    "sport": {"LABEL_0": "competition discipline", "LABEL_1": "drug use in sport"},
    "weather": {"LABEL_0": "weather forecast", "LABEL_1": "weather warning"},
}

CLASS_DICT = {**CLASS_DICT_FIRST, **CLASS_DICT_SECOND}

MODEL_ID = os.environ["MODEL_ID"]
MODEL_VERSION = os.environ["MODEL_VERSION"]


# --- settings classes
class TrackedIPTCModelSpecs(TrackedModelSpecs):
    """Tracked iptc model settings."""

    project: str = f"onclusive/iptc-{MODEL_ID}"
    model = f"IP{MODEL_ID}-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class BaseTrackedModelSpecs(TrackedModelSpecs):
    """Trained model settings."""

    project: str = f"onclusive/iptc-{MODEL_ID}"
    model: str = f"IP{MODEL_ID}-BASE"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = f"IP{MODEL_ID}-{MODEL_VERSION}"
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY)

    class Config:
        env_prefix = "base_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):
    """iptc input parameters."""

    sample_documents: List[str] = [""]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IPTCSettings(TrackedParams):
    """IPTC settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IPTCModelParams(TrackedParams):
    """IPTC Model parameters."""

    huggingface_pipeline_task: str = "text-classification"
    base_model_reference: BaseTrackedModelSpecs = BaseTrackedModelSpecs()
    iptc_settings: IPTCSettings = IPTCSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TrackedIPTCBaseModelCard(TrackedModelCard):
    """The model card for the base model of the iptc ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: IPTCModelParams = IPTCModelParams()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "iptc_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


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
