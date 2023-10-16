"""Settings."""

# Standard Library
import os
from typing import List

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# --- settings classes
class TrackedSummarizationModelSpecs(TrackedModelSpecs):
    """Tracked summarization model specs."""

    project: str = "onclusive/gch-summarization"
    model = "SUMMARIZATION-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):
    """Inputs."""

    sample_documents: List[str] = [
        "Sky News announces slate of special programming for the appointment of the UK's new \
Prime Minister.\nSky News' political programming will expand ahead of a momentous week \
in UK politics with the impending announcement of the new Prime Minister. Sky News' key \
political programmes will return to bring audiences in-depth discussion and analysis of \
all the latest news with live coverage from Downing Street and Westminster.\nHead of Sky \
News, John Ryley:\n'This is a momentous week in British politics, where a new Prime Minister \
will take on an in-tray bursting with crunch decisions.",
        "L ancée en 2020, Exaion est une filiale du groupe EDF et compte une trentaine de salariés. \
Elle propose à ses clients «d'entrer dans le domaine du digital sous plusieurs volets», \
explique à L'Agefi son directeur général Fatih Balyeli. L'entreprise «accompagne des projets \
Web 3 avec une approche éco-responsable» et a logiquement choisi dès 2021 de gérer des noeuds \
de la blockchain Ethereum pour participer au Merge, le changement de consensus intervenu \
mi-septembre qui avait pour objectif de réduire sa consommation énergétique de plus de 95%.",
        "Isdin logra evitar una sanción de la CNMC G. Trindade. Barcelona El laboratorio de \
cosmética Isdin ha llegado a un acuerdo con la Comisión Nacional del Mercado y la \
Competencia (CNMC) para cerrar un expediente sancionador sobre prácticas restrictivas \
en la venta por Internet. De esta forma, la compañía catalana, propiedad a partes iguales \
de Puig y Esteve, evitará una sanción económica. La CNMC comunicó la incoación \
de un expediente a Isdin por la fijación de precios en la reventa en Internet \
de productos de protección solar en noviembre de 2020.",
        "Tossuderia, curiositat, tenacitat, no témer el fracàs, envoltar-se d'un bon equip, \
aprofitar les oportunitats... El doctor Pere-Joan Cardona va donar un munt de consells \
als nois i noies que, ahir al migdia, van omplir la sala d'actes de la FUB, on \
va avançar que el seu probiòtic antituberculosi està a punt per poder sortir al mercat. \
S'hi van presentar tres dels millors projectes de la 7a Mostra de Treballs de Recerca \
i Crèdits de Síntesi de l'Escola Joviat. Cardona és doctor en Medicina i especialista \
en Microbiologia Clínica; cap de la Unitat de Tuberculosi Experimental de l'Institut \
Germans Trias i Pujol; professor associat de la UAB i inventor de la vacuna contra \
la tuberculosi Ruti -aturada per manca de finançament- i del probiòtic Nyaditum resae (NR),\
que té per objectiu immunitzar el cos contra la malaltia acostumant-lo a ella.",
        "Capodanno 'amaro' per un quarantenne modenese, libero professionista, \
e un operaio 36enne di Nonantola. I due - controllati dai carabinieri \
verso le 17 di ieri a Modena, in via Nonantolana, a bordo di una Golf - \
sono stati trovati in possesso di 28 grammi di cocaina, suddivisi in tre involucri \
di cellophane. Sono stati arrestati per detenzione ai fini di spaccio \
di stupefacenti e portati in carcere.",
    ]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SummarizationSettings(TrackedParams):
    """Summarization settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SummarizationModelParams(TrackedParams):
    """summarization model settings."""

    summarization_settings: SummarizationSettings = SummarizationSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SummarizationModelParamsEn(SummarizationModelParams):
    """English Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference_en: str = "Yale-LILY/brio-cnndm-uncased"


class SummarizationModelParamsFrDe(SummarizationModelParams):
    """French/German Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference_frde: str = (
        "ctu-aic/mbart25-multilingual-summarization-multilarge-cs"
    )


class SummarizationModelParamsEs(SummarizationModelParams):
    """Spanish Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference_es: str = "knkarthick/MEETING_SUMMARY"


class SummarizationModelParamsCa(SummarizationModelParams):
    """Catalan Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference_ca: str = "ELiRF/NASCA"


class SummarizationModelParamsIt(SummarizationModelParams):
    """Italian Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference_it: str = "morenolq/bart-it-fanpage"


class TrackedSummarizationModelCard(TrackedModelCard):
    """The model cards for the model of the multilingual Summarization ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params_en: SummarizationModelParamsEn = SummarizationModelParamsEn()
    model_params_frde: SummarizationModelParamsFrDe = SummarizationModelParamsFrDe()
    model_params_es: SummarizationModelParamsEs = SummarizationModelParamsEs()
    model_params_ca: SummarizationModelParamsCa = SummarizationModelParamsCa()
    model_params_it: SummarizationModelParamsIt = SummarizationModelParamsIt()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "summarization_model_artifacts")
    logging_level: str = "INFO"

    en_model_subdirectory: str = "/english_summarization"
    frde_model_subdirectory: str = "/french_german_summarization"
    es_model_subdirectory: str = "/spanish_summarization"
    ca_model_subdirectory: str = "/catalan_summarization"
    it_model_subdirectory: str = "/italian_summarization"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
