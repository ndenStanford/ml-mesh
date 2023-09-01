"""Constants tests."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp.language.constants import _LOCALES, LanguageIso


list_of_langIso_non_empty_stopwords = [
    LanguageIso.AF,
    LanguageIso.AR,
    LanguageIso.BG,
    LanguageIso.BN,
    LanguageIso.CA,
    LanguageIso.CS,
    LanguageIso.DA,
    LanguageIso.DE,
    LanguageIso.EL,
    LanguageIso.EN,
    LanguageIso.ES,
    LanguageIso.ET,
    LanguageIso.FA,
    LanguageIso.FI,
    LanguageIso.FR,
    LanguageIso.GU,
    LanguageIso.HE,
    LanguageIso.HI,
    LanguageIso.HR,
    LanguageIso.HU,
    LanguageIso.ID,
    LanguageIso.IT,
    LanguageIso.JA,
    LanguageIso.KO,
    LanguageIso.LT,
    LanguageIso.LV,
    LanguageIso.MR,
    LanguageIso.NL,
    LanguageIso.NO,
    LanguageIso.PL,
    LanguageIso.PT,
    LanguageIso.RO,
    LanguageIso.RU,
    LanguageIso.SK,
    LanguageIso.SL,
    LanguageIso.SO,
    LanguageIso.SV,
    LanguageIso.SW,
    LanguageIso.TH,
    LanguageIso.TR,
    LanguageIso.UK,
    LanguageIso.UR,
    LanguageIso.VI,
    LanguageIso.ZH,
]

list_of_langIso_empty_stopwords = [
    LanguageIso.CY,
    LanguageIso.KN,
    LanguageIso.MK,
    LanguageIso.ML,
    LanguageIso.NE,
    # LanguageIso.PA, #PA has no stopwords and locales
    LanguageIso.SQ,
    LanguageIso.TA,
    LanguageIso.TE,
]

list_of_langIso = list_of_langIso_non_empty_stopwords + list_of_langIso_empty_stopwords


@pytest.mark.parametrize("language", list_of_langIso_non_empty_stopwords)
def test_languageIso_get_stopwords_list(language):
    """Test stop words list getter."""
    assert len(language.get_stop_words()) > 0


@pytest.mark.parametrize("language", list_of_langIso_empty_stopwords)
def test_languageIso_get_empty_stopwords_list(language):
    """Test empty stop words list getter."""
    assert len(language.get_stop_words()) == 0


@pytest.mark.parametrize("language", list_of_langIso)
def test_languageIso_locales(language):
    """Test locales."""
    assert language.locales == _LOCALES[language]
