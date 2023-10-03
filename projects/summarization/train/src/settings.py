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
class TrackedSumModelSpecs(TrackedModelSpecs):
    """Tracked summarization model specs."""

    project: str = "onclusive/summarization"
    model = "SUM-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):
    """Inputs."""

    sample_documents: List[str] = ["Sky News announces slate of special programming for the appointment of the UK’s new Prime Minister.\nSky News’ political programming will expand ahead of a momentous week in UK politics with the impending announcement of the new Prime Minister. Sky News’ key political programmes will return to bring audiences in-depth discussion and analysis of all the latest news with live coverage from Downing Street and Westminster.\nHead of Sky News, John Ryley:\n“This is a momentous week in British politics, where a new Prime Minister will take on an in-tray bursting with crunch decisions. Sky News will be live in Westminster and hearing from voters in key constituencies to bring our audiences the latest news, and analyse the impact this new government will have on households across the UK.”\nSky News’ slate of dedicated political programming will kick off from 8.30 am on Sunday 4th September with Sophy Ridge on Sunday, focusing on the impending result of the Conservative Party leadership election.\nOn Monday 5th, Tuesday 6th and Wednesday 7th September, Sky News will bring live coverage to audiences from Downing Street and Westminster as power is handed over from outgoing Prime Minister, Boris Johnson to his successor, either Liz Truss or Rishi Sunak.\nSophy Ridge’s The Take will return on Wednesday 7th September and on Thursday 8th September Beth Rigby Interviews… will also return to explore the result of the leadership election.\nOther special programming on Sky News will cover the key moments for the new Prime Minster in their first days in office, including their first meeting with her Majesty the Queen on Tuesday – during which they’ll seek permission to form a government – and their first major statement as Prime Minister from the steps of Downing Street. With millions of households across the UK asking questions about the cost-of-living crisis, this moment will be pivotal for the new Prime Minister and Sky News will bring audiences the full story on-air, online, on our app, and via our podcasts.\nThe first Prime Minister’s Questions will also be broadcast live from the House of Commons on Sky News on Wednesday 7th September. This will be the first time that the new PM faces Labour’s leader across the despatch box, and they will be expected to face questions about future government policy including the possible timing of a general election.\nCoverage of all these events will be available on the Sky News Politics Hub and will continue throughout September and October from the Labour and Conservative Party Conferences from 25th-28th September and 2nd-5th October respectively. Sky News will also be hosting pop-up radio stations at both party conferences.",
                                  ]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumSettings(TrackedParams):
    """Summarization settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumModelParamsEn(TrackedParams):
    """English Summarization model settings."""

    huggingface_model_reference: str = "Yale-LILY/brio-cnndm-uncased"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
        
        
class SumModelParamsFrDe(TrackedParams):
    """French/German Summarization model settings."""

    huggingface_model_reference: str = "ctu-aic/mbart25-multilingual-summarization-multilarge-cs"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
        

class SumModelParamsEs(TrackedParams):
    """Spanish Summarization model settings."""

    huggingface_model_reference: str = "knkarthick/MEETING_SUMMARY"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
        
        
class SumModelParamsCa(TrackedParams):
    """Catalan Summarization model settings."""

    huggingface_model_reference: str = "ELiRF/NASCA"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumModelParamsIt(TrackedParams):
    """Italian Summarization model settings."""

    huggingface_model_reference: str = "morenolq/bart-it-fanpage"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8" 


class TrackedSumModelCard(TrackedModelCard):
    """The model cards for the model of the multilingual Summarization ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params_en: SumModelParamsEn = SumModelParamsEn()
    model_params_frde: SumModelParamsFrDe = SumModelParamsFrDe()
    model_params_es: SumModelParamsEs = SumModelParamsEs()
    model_params_ca: SumModelParamsCa = SumModelParamsCa()
    model_params_it: SumModelParamsIt = SumModelParamsIt()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "sum_model_artifacts")
    logging_level: str = "INFO"

    en_model_subdirectory: str = "/en_sum"
    frde_model_subdirectory: str = "/frde_sum"
    es_model_subdirectory: str = "/es_sum"
    ca_model_subdirectory: str = "/ca_sum"
    it_model_subdirectory: str = "/it_sum"
    
    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"