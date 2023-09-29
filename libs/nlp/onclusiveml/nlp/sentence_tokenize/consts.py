"""Constants."""

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso


class SupportedNLTKLanguagesISO(BaseModel):
    """Class to represent special characters.

    Args:
        lang (LanguageIso): languageISOs that support NLTK sentence tokenizer

    """

    lang: LanguageIso


SUPPORTED_LANGUAGEISO_LIST = [
    SupportedNLTKLanguagesISO(lang=LanguageIso.CS),
    SupportedNLTKLanguagesISO(lang=LanguageIso.DA),
    SupportedNLTKLanguagesISO(lang=LanguageIso.NL),
    SupportedNLTKLanguagesISO(lang=LanguageIso.EN),
    SupportedNLTKLanguagesISO(lang=LanguageIso.ET),
    SupportedNLTKLanguagesISO(lang=LanguageIso.FI),
    SupportedNLTKLanguagesISO(lang=LanguageIso.FR),
    SupportedNLTKLanguagesISO(lang=LanguageIso.DE),
    SupportedNLTKLanguagesISO(lang=LanguageIso.EL),
    SupportedNLTKLanguagesISO(lang=LanguageIso.IT),
    SupportedNLTKLanguagesISO(lang=LanguageIso.NO),
    SupportedNLTKLanguagesISO(lang=LanguageIso.PL),
    SupportedNLTKLanguagesISO(lang=LanguageIso.PT),
    SupportedNLTKLanguagesISO(lang=LanguageIso.RU),
    SupportedNLTKLanguagesISO(lang=LanguageIso.SL),
    SupportedNLTKLanguagesISO(lang=LanguageIso.ES),
    SupportedNLTKLanguagesISO(lang=LanguageIso.SV),
    SupportedNLTKLanguagesISO(lang=LanguageIso.TR),
]

NLTK_SUPPORTED_LANGS = [
    next(iter(item.lang.locales.values()))["en"].lower()
    for item in SUPPORTED_LANGUAGEISO_LIST
]


class SpecialCharacter(BaseModel):
    """Class to represent special characters.

    Args:
        char (str): character
        unicode_int (optional): unicode representation of character in integer format

    """

    char: str
    unicode_int: int


SPECIAL_CHARACTERS_AND_UNICODE = [
    SpecialCharacter(char="։", unicode_int=1417),
    SpecialCharacter(char="؟", unicode_int=1567),
    SpecialCharacter(char="۔", unicode_int=1748),
    SpecialCharacter(char="܀", unicode_int=1792),
    SpecialCharacter(char="܁", unicode_int=1793),
    SpecialCharacter(char="܂", unicode_int=1794),
    SpecialCharacter(char="߹", unicode_int=2041),
    SpecialCharacter(char="।", unicode_int=2404),
    SpecialCharacter(char="॥", unicode_int=2405),
    SpecialCharacter(char="၊", unicode_int=4170),
    SpecialCharacter(char="။", unicode_int=4171),
    SpecialCharacter(char="።", unicode_int=4962),
    SpecialCharacter(char="፧", unicode_int=4967),
    SpecialCharacter(char="፨", unicode_int=4968),
    SpecialCharacter(char="᙮", unicode_int=5742),
    SpecialCharacter(char="᜵", unicode_int=5941),
    SpecialCharacter(char="᜶", unicode_int=5942),
    SpecialCharacter(char="᠃", unicode_int=6147),
    SpecialCharacter(char="᠉", unicode_int=6153),
    SpecialCharacter(char="᥄", unicode_int=6468),
    SpecialCharacter(char="᥅", unicode_int=6469),
    SpecialCharacter(char="᪨", unicode_int=6824),
    SpecialCharacter(char="᪩", unicode_int=6825),
    SpecialCharacter(char="᪪", unicode_int=6826),
    SpecialCharacter(char="᪫", unicode_int=6827),
    SpecialCharacter(char="᭚", unicode_int=7002),
    SpecialCharacter(char="᭛", unicode_int=7003),
    SpecialCharacter(char="᭞", unicode_int=7006),
    SpecialCharacter(char="᭟", unicode_int=7007),
    SpecialCharacter(char="᰻", unicode_int=7227),
    SpecialCharacter(char="᰼", unicode_int=7228),
    SpecialCharacter(char="᱾", unicode_int=7294),
    SpecialCharacter(char="᱿", unicode_int=7295),
    SpecialCharacter(char="‼", unicode_int=8252),
    SpecialCharacter(char="‽", unicode_int=8253),
    SpecialCharacter(char="⁇", unicode_int=8263),
    SpecialCharacter(char="⁈", unicode_int=8264),
    SpecialCharacter(char="⁉", unicode_int=8265),
    SpecialCharacter(char="⸮", unicode_int=11822),
    SpecialCharacter(char="⸼", unicode_int=11836),
    SpecialCharacter(char="꓿", unicode_int=42239),
    SpecialCharacter(char="꘎", unicode_int=42510),
    SpecialCharacter(char="꘏", unicode_int=42511),
    SpecialCharacter(char="꛳", unicode_int=42739),
    SpecialCharacter(char="꛷", unicode_int=42743),
    SpecialCharacter(char="꡶", unicode_int=43126),
    SpecialCharacter(char="꡷", unicode_int=43127),
    SpecialCharacter(char="꣎", unicode_int=43214),
    SpecialCharacter(char="꣏", unicode_int=43215),
    SpecialCharacter(char="꤯", unicode_int=43311),
    SpecialCharacter(char="꧈", unicode_int=43464),
    SpecialCharacter(char="꧉", unicode_int=43465),
    SpecialCharacter(char="꩝", unicode_int=43613),
    SpecialCharacter(char="꩞", unicode_int=43614),
    SpecialCharacter(char="꩟", unicode_int=43615),
    SpecialCharacter(char="꫰", unicode_int=43760),
    SpecialCharacter(char="꫱", unicode_int=43761),
    SpecialCharacter(char="꯫", unicode_int=44011),
    SpecialCharacter(char="﹒", unicode_int=65106),
    SpecialCharacter(char="﹖", unicode_int=65110),
    SpecialCharacter(char="﹗", unicode_int=65111),
    SpecialCharacter(char="！", unicode_int=65281),
    SpecialCharacter(char="．", unicode_int=65294),
    SpecialCharacter(char="？", unicode_int=65311),
    SpecialCharacter(char="𐩖", unicode_int=68182),
    SpecialCharacter(char="𐩗", unicode_int=68183),
    SpecialCharacter(char="𑁇", unicode_int=69703),
    SpecialCharacter(char="𑁈", unicode_int=69704),
    SpecialCharacter(char="𑂾", unicode_int=69822),
    SpecialCharacter(char="𑂿", unicode_int=69823),
    SpecialCharacter(char="𑃀", unicode_int=69824),
    SpecialCharacter(char="𑃁", unicode_int=69825),
    SpecialCharacter(char="𑅁", unicode_int=69953),
    SpecialCharacter(char="𑅂", unicode_int=69954),
    SpecialCharacter(char="𑅃", unicode_int=69955),
    SpecialCharacter(char="𑇅", unicode_int=70085),
    SpecialCharacter(char="𑇆", unicode_int=70086),
    SpecialCharacter(char="𑇍", unicode_int=70093),
    SpecialCharacter(char="𑇞", unicode_int=70110),
    SpecialCharacter(char="𑇟", unicode_int=70111),
    SpecialCharacter(char="𑈸", unicode_int=70200),
    SpecialCharacter(char="𑈹", unicode_int=70201),
    SpecialCharacter(char="𑈻", unicode_int=70203),
    SpecialCharacter(char="𑈼", unicode_int=70204),
    SpecialCharacter(char="𑊩", unicode_int=70313),
    SpecialCharacter(char="𑑋", unicode_int=70731),
    SpecialCharacter(char="𑑌", unicode_int=70732),
    SpecialCharacter(char="𑗂", unicode_int=71106),
    SpecialCharacter(char="𑗃", unicode_int=71107),
    SpecialCharacter(char="𑗉", unicode_int=71113),
    SpecialCharacter(char="𑗊", unicode_int=71114),
    SpecialCharacter(char="𑗋", unicode_int=71115),
    SpecialCharacter(char="𑗌", unicode_int=71116),
    SpecialCharacter(char="𑗍", unicode_int=71117),
    SpecialCharacter(char="𑗎", unicode_int=71118),
    SpecialCharacter(char="𑗏", unicode_int=71119),
    SpecialCharacter(char="𑗐", unicode_int=71120),
    SpecialCharacter(char="𑗑", unicode_int=71121),
    SpecialCharacter(char="𑗒", unicode_int=71122),
    SpecialCharacter(char="𑗓", unicode_int=71123),
    SpecialCharacter(char="𑗔", unicode_int=71124),
    SpecialCharacter(char="𑗕", unicode_int=71125),
    SpecialCharacter(char="𑗖", unicode_int=71126),
    SpecialCharacter(char="𑗗", unicode_int=71127),
    SpecialCharacter(char="𑙁", unicode_int=71233),
    SpecialCharacter(char="𑙂", unicode_int=71234),
    SpecialCharacter(char="𑜼", unicode_int=71484),
    SpecialCharacter(char="𑜽", unicode_int=71485),
    SpecialCharacter(char="𑜾", unicode_int=71486),
    SpecialCharacter(char="𑩂", unicode_int=72258),
    SpecialCharacter(char="𑩃", unicode_int=72259),
    SpecialCharacter(char="𑪛", unicode_int=72347),
    SpecialCharacter(char="𑪜", unicode_int=72348),
    SpecialCharacter(char="𑱁", unicode_int=72769),
    SpecialCharacter(char="𑱂", unicode_int=72770),
    SpecialCharacter(char="𖩮", unicode_int=92782),
    SpecialCharacter(char="𖩯", unicode_int=92783),
    SpecialCharacter(char="𖫵", unicode_int=92917),
    SpecialCharacter(char="𖬷", unicode_int=92983),
    SpecialCharacter(char="𖬸", unicode_int=92984),
    SpecialCharacter(char="𖭄", unicode_int=92996),
    SpecialCharacter(char="𛲟", unicode_int=113823),
    SpecialCharacter(char="𝪈", unicode_int=121480),
    SpecialCharacter(char="。", unicode_int=12290),
]

SPECIAL_CHARACTERS = [item.char for item in SPECIAL_CHARACTERS_AND_UNICODE]
