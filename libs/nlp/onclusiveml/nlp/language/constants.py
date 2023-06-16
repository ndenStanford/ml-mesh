"""Constants."""

# Standard Library
from enum import Enum
from typing import Dict, List, Optional

# Internal libraries
from onclusiveml.nlp.language.helpers import load_stop_words_file


class LanguageIso(Enum):
    """List of languages in ISO 639-1 format.

    References:
      https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    """

    AF = "af"
    AR = "ar"
    BG = "bg"
    BN = "bn"
    CA = "ca"
    CS = "cs"
    CY = "cy"  # TODO: empty list
    DA = "da"
    DE = "de"
    EL = "el"
    EN = "en"
    ES = "es"
    ET = "et"
    FA = "fa"
    FI = "fi"
    FR = "fr"
    GU = "gu"
    HE = "he"
    HI = "hi"
    HR = "hr"
    HU = "hu"
    ID = "id"
    IT = "it"
    JA = "ja"
    KN = "kn"  # TODO: empty list
    KO = "ko"
    LT = "lt"
    LV = "lv"
    MK = "mk"  # TODO: empty list
    ML = "ml"  # TODO: empty list
    MR = "mr"
    NE = "ne"
    NL = "nl"
    NO = "no"
    PA = "pa"  # TODO: empty list
    PL = "pl"
    PT = "pt"
    RO = "ro"
    RU = "ru"
    SK = "sk"
    SL = "sl"
    SO = "so"
    SQ = "sq"  # TODO: empty list
    SV = "sv"
    SW = "sw"
    TA = "ta"  # TODO: empty list
    TE = "te"
    TH = "th"
    TR = "tr"
    UK = "uk"
    UR = "ur"
    VI = "vi"
    ZH = "zh"

    @property
    def locales(self) -> Dict[str, Dict[str, str]]:
        """Returns all locales for a given language."""
        return _LOCALES[self]

    def get_stop_words(self) -> List[str]:
        """Returns list of stop words for language."""
        return load_stop_words_file(self.value)

    @classmethod
    def exists(cls, lang: str) -> bool:
        """Checks if a language exists in the supported list."""
        return lang.lower() in [iso for iso in LanguageIso]

    @classmethod
    def from_locale(cls, locale: str) -> Optional["LanguageIso"]:
        """Returns Language ISO from locale."""
        _lang, _locale = locale.split("-")
        iso = cls.from_language_iso(_lang.lower())
        if iso is None or iso.locales.get(f"{_lang.lower()}-{_locale.upper()}") is None:
            return None
        return iso

    @classmethod
    def from_language_iso(cls, lang: str) -> Optional["LanguageIso"]:
        """Returns LanguageIso from string input"""
        reverse: Dict[str, "LanguageIso"] = {iso.value: iso for iso in LanguageIso}
        return reverse.get(lang.lower())


_LOCALES: Dict[LanguageIso, Dict[str, Dict[str, str]]] = {
    LanguageIso.AF: {
        "af": {"name": "Afrikaans", "en": "Afrikaans"},
        "af-NA": {"name": "Afrikaans (Namibia)", "en": "Afrikaans (Namibia)"},
        "af-ZA": {"name": "Afrikaans (South Africa)", "en": "Afrikaans (South Africa)"},
    },
    LanguageIso.AR: {
        "ar": {"name": "العربية", "en": "Arabic"},
        "ar-AR": {"name": "العربية", "en": "Arabic"},
        "ar-MA": {"name": "العربية", "en": "Arabic (Morocco)"},
        "ar-SA": {"name": "العربية (السعودية)", "en": "Arabic (Saudi Arabia)"},
    },
    LanguageIso.BG: {
        "bg": {"name": "Български", "en": "Bulgarian"},
        "bg-BG": {"name": "Български", "en": "Bulgarian"},
    },
    LanguageIso.BN: {
        "bn": {"name": "বাংলা", "en": "Bengali"},
        "bn-IN": {"name": "বাংলা (ভারত)", "en": "Bengali (India)"},
        "bn-BD": {"name": "বাংলা(বাংলাদেশ)", "en": "Bengali (Bangladesh)"},
    },
    LanguageIso.CA: {
        "ca": {"name": "Català", "en": "Catalan"},
        "ca-ES": {"name": "Català", "en": "Catalan"},
    },
    LanguageIso.CS: {
        "cs": {"name": "Čeština", "en": "Czech"},
        "cs-CZ": {"name": "Čeština", "en": "Czech"},
    },
    LanguageIso.CY: {
        "cy": {"name": "Cymraeg", "en": "Welsh"},
        "cy-GB": {"name": "Cymraeg", "en": "Welsh"},
    },
    LanguageIso.DA: {
        "da": {"name": "Dansk", "en": "Danish"},
        "da-DK": {"name": "Dansk", "en": "Danish"},
    },
    LanguageIso.DE: {
        "de": {"name": "Deutsch", "en": "German"},
        "de-AT": {"name": "Deutsch (Österreich)", "en": "German (Austria)"},
        "de-DE": {"name": "Deutsch (Deutschland)", "en": "German (Germany)"},
        "de-CH": {"name": "Deutsch (Schweiz)", "en": "German (Switzerland)"},
    },
    LanguageIso.EL: {
        "el": {"name": "Ελληνικά", "en": "Greek"},
        "el-GR": {"name": "Ελληνικά", "en": "Greek (Greece)"},
    },
    LanguageIso.EN: {
        "en": {"name": "English", "en": "English"},
        "en-GB": {"name": "English (UK)", "en": "English (UK)"},
        "en-AU": {"name": "English (Australia)", "en": "English (Australia)"},
        "en-CA": {"name": "English (Canada)", "en": "English (Canada)"},
        "en-IE": {"name": "English (Ireland)", "en": "English (Ireland)"},
        "en-IN": {"name": "English (India)", "en": "English (India)"},
        "en-PI": {"name": "English (Pirate)", "en": "English (Pirate)"},
        "en-SG": {"name": "English (Singapore)", "en": "English (Singapore)"},
        "en-UD": {"name": "English (Upside Down)", "en": "English (Upside Down)"},
        "en-US": {"name": "English (US)", "en": "English (US)"},
        "en-ZA": {"name": "English (South Africa)", "en": "English (South Africa)"},
    },
    LanguageIso.ES: {
        "es": {"name": "Español", "en": "Spanish"},
        "es-AR": {"name": "Español (Argentine)", "en": "Spanish (Argentina)"},
        "es-419": {"name": "Español (Latinoamérica)", "en": "Spanish (Latin America)"},
        "es-CL": {"name": "Español (Chile)", "en": "Spanish (Chile)"},
        "es-CO": {"name": "Español (Colombia)", "en": "Spanish (Colombia)"},
        "es-EC": {"name": "Español (Ecuador)", "en": "Spanish (Ecuador)"},
        "es-ES": {"name": "Español (España)", "en": "Spanish (Spain)"},
        "es-LA": {"name": "Español (Latinoamérica)", "en": "Spanish (Latin America)"},
        "es-NI": {"name": "Español (Nicaragua)", "en": "Spanish (Nicaragua)"},
        "es-MX": {"name": "Español (México)", "en": "Spanish (Mexico)"},
        "es-US": {"name": "Español (Estados Unidos)", "en": "Spanish (United States)"},
        "es-VE": {"name": "Español (Venezuela)", "en": "Spanish (Venezuela)"},
    },
    LanguageIso.ET: {
        "et": {"name": "eesti keel", "en": "Estonian"},
        "et-EE": {"name": "Eesti (Estonia)", "en": "Estonian (Estonia)"},
    },
    LanguageIso.FA: {
        "fa": {"name": "فارسی", "en": "Persian"},
        "fa-IR": {"name": "فارسی", "en": "Persian"},
    },
    LanguageIso.FI: {
        "fi": {"name": "Suomi", "en": "Finnish"},
        "fi-FI": {"name": "Suomi", "en": "Finnish"},
    },
    LanguageIso.FR: {
        "fr": {"name": "Français", "en": "French"},
        "fr-CA": {"name": "Français (Canada)", "en": "French (Canada)"},
        "fr-FR": {"name": "Français (France)", "en": "French (France)"},
        "fr-BE": {"name": "Français (Belgique)", "en": "French (Belgium)"},
        "fr-CH": {"name": "Français (Suisse)", "en": "French (Switzerland)"},
    },
    LanguageIso.GU: {"gu-IN": {"name": "ગુજરાતી", "en": "Gujarati"}},
    LanguageIso.HE: {
        "he": {"name": "עברית‏", "en": "Hebrew"},
        "he-IL": {"name": "עברית‏", "en": "Hebrew"},
    },
    LanguageIso.HI: {
        "hi": {"name": "हिन्दी", "en": "Hindi"},
        "hi-IN": {"name": "हिन्दी", "en": "Hindi"},
    },
    LanguageIso.HR: {
        "hr": {"name": "Hrvatski", "en": "Croatian"},
        "hr-HR": {"name": "Hrvatski", "en": "Croatian"},
    },
    LanguageIso.HU: {
        "hu": {"name": "Magyar", "en": "Hungarian"},
        "hu-HU": {"name": "Magyar", "en": "Hungarian"},
    },
    LanguageIso.ID: {
        "id": {"name": "Bahasa Indonesia", "en": "Indonesian"},
        "id-ID": {"name": "Bahasa Indonesia", "en": "Indonesian"},
    },
    LanguageIso.IT: {
        "it": {"name": "Italiano", "en": "Italian"},
        "it-IT": {"name": "Italiano", "en": "Italian"},
    },
    LanguageIso.JA: {
        "ja": {"name": "日本語", "en": "Japanese"},
        "ja-JP": {"name": "日本語 (日本)", "en": "Japanese (Japan)"},
    },
    LanguageIso.KN: {
        "kn": {"name": "ಕನ್ನಡ", "en": "Kannada"},
        "kn-IN": {"name": "ಕನ್ನಡ (India)", "en": "Kannada (India)"},
    },
    LanguageIso.KO: {
        "ko": {"name": "한국어", "en": "Korean"},
        "ko-KR": {"name": "한국어 (한국)", "en": "Korean (Korea)"},
    },
    LanguageIso.LT: {
        "lt": {"name": "Lietuvių", "en": "Lithuanian"},
        "lt-LT": {"name": "Lietuvių", "en": "Lithuanian"},
    },
    LanguageIso.LV: {
        "lv": {"name": "Latviešu", "en": "Latvian"},
        "lv-LV": {"name": "Latviešu", "en": "Latvian"},
    },
    LanguageIso.MK: {
        "mk": {"name": "Македонски", "en": "Macedonian"},
        "mk-MK": {"name": "Македонски (Македонски)", "en": "Macedonian (Macedonian)"},
    },
    LanguageIso.ML: {
        "ml": {"name": "മലയാളം", "en": "Malayalam"},
        "ml-IN": {"name": "മലയാളം", "en": "Malayalam"},
    },
    LanguageIso.MR: {
        "mr": {"name": "मराठी", "en": "Marathi"},
        "mr-IN": {"name": "मराठी", "en": "Marathi"},
    },
    LanguageIso.NE: {
        "ne": {"name": "नेपाली", "en": "Nepali"},
        "ne-NP": {"name": "नेपाली", "en": "Nepali"},
    },
    LanguageIso.NL: {
        "nl": {"name": "Nederlands", "en": "Dutch"},
        "nl-BE": {"name": "Nederlands (België)", "en": "Dutch (Belgium)"},
        "nl-NL": {"name": "Nederlands (Nederland)", "en": "Dutch (Netherlands)"},
    },
    LanguageIso.NO: {"no": {"name": "Norsk", "en": "Norwegian"}},
    LanguageIso.PL: {
        "pl": {"name": "Polski", "en": "Polish"},
        "pl-PL": {"name": "Polski", "en": "Polish"},
    },
    LanguageIso.PT: {
        "pt": {"name": "Português", "en": "Portuguese"},
        "pt-BR": {"name": "Português (Brasil)", "en": "Portuguese (Brazil)"},
        "pt-PT": {"name": "Português (Portugal)", "en": "Portuguese (Portugal)"},
    },
    LanguageIso.RO: {
        "ro": {"name": "Română", "en": "Romanian"},
        "ro-RO": {"name": "Română", "en": "Romanian"},
    },
    LanguageIso.RU: {
        "ru": {"name": "Русский", "en": "Russian"},
        "ru-RU": {"name": "Русский", "en": "Russian"},
    },
    LanguageIso.SK: {
        "sk": {"name": "Slovenčina", "en": "Slovak"},
        "sk-SK": {"name": "Slovenčina (Slovakia)", "en": "Slovak (Slovakia)"},
    },
    LanguageIso.SL: {
        "sl": {"name": "Slovenščina", "en": "Slovenian"},
        "sl-SI": {"name": "Slovenščina", "en": "Slovenian"},
    },
    LanguageIso.SO: {"so-SO": {"name": "Soomaaliga", "en": "Somali"}},
    LanguageIso.SQ: {
        "sq": {"name": "Shqip", "en": "Albanian"},
        "sq-AL": {"name": "Shqip", "en": "Albanian"},
    },
    LanguageIso.SV: {
        "sv": {"name": "Svenska", "en": "Swedish"},
        "sv-SE": {"name": "Svenska", "en": "Swedish"},
    },
    LanguageIso.SW: {
        "sw": {"name": "Kiswahili", "en": "Swahili"},
        "sw-KE": {"name": "Kiswahili", "en": "Swahili (Kenya)"},
    },
    LanguageIso.TA: {
        "ta": {"name": "தமிழ்", "en": "Tamil"},
        "ta-IN": {"name": "தமிழ்", "en": "Tamil"},
    },
    LanguageIso.TE: {
        "te": {"name": "తెలుగు", "en": "Telugu"},
        "te-IN": {"name": "తెలుగు", "en": "Telugu"},
    },
    LanguageIso.TH: {
        "th": {"name": "ภาษาไทย", "en": "Thai"},
        "th-TH": {"name": "ภาษาไทย (ประเทศไทย)", "en": "Thai (Thailand)"},
    },
    LanguageIso.TR: {
        "tr": {"name": "Türkçe", "en": "Turkish"},
        "tr-TR": {"name": "Türkçe", "en": "Turkish"},
    },
    LanguageIso.UK: {
        "uk": {"name": "Українська", "en": "Ukrainian"},
        "uk-UA": {"name": "Українська", "en": "Ukrainian"},
    },
    LanguageIso.UR: {
        "ur": {"name": "اردو", "en": "Urdu"},
        "ur-PK": {"name": "اردو", "en": "Urdu"},
    },
    LanguageIso.VI: {
        "vi": {"name": "Tiếng Việt", "en": "Vietnamese"},
        "vi-VN": {"name": "Tiếng Việt", "en": "Vietnamese"},
    },
    LanguageIso.ZH: {
        "zh": {"name": "中文", "en": "Chinese"},
        "zh-Hans": {"name": "中文简体", "en": "Chinese Simplified"},
        "zh-Hant": {"name": "中文繁體", "en": "Chinese Traditional"},
        "zh-CN": {"name": "中文（中国大陆）", "en": "Chinese Simplified (China)"},
        "zh-HK": {"name": "中文（香港）", "en": "Chinese Traditional (Hong Kong)"},
        "zh-SG": {"name": "中文（新加坡）", "en": "Chinese Simplified (Singapore)"},
        "zh-TW": {"name": "中文（台灣）", "en": "Chinese Traditional (Taiwan)"},
    },
}
