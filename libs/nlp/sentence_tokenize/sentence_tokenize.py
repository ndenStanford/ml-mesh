"Sentence Tokenize"

# Standard Library
import re
from typing import Any, Dict, List

# 3rd party libraries
import nltk

class SentenceTokenize:
    extra_tokens = ["。"]
    other_tokens = [
        "։",
        "؟",
        "۔",
        "܀",
        "܁",
        "܂",
        "߹",
        "।",
        "॥",
        "၊",
        "။",
        "።",
        "፧",
        "፨",
        "᙮",
        "᜵",
        "᜶",
        "᠃",
        "᠉",
        "᥄",
        "᥅",
        "᪨",
        "᪩",
        "᪪",
        "᪫",
        "᭚",
        "᭛",
        "᭞",
        "᭟",
        "᰻",
        "᰼",
        "᱾",
        "᱿",
        "‼",
        "‽",
        "⁇",
        "⁈",
        "⁉",
        "⸮",
        "⸼",
        "꓿",
        "꘎",
        "꘏",
        "꛳",
        "꛷",
        "꡶",
        "꡷",
        "꣎",
        "꣏",
        "꤯",
        "꧈",
        "꧉",
        "꩝",
        "꩞",
        "꩟",
        "꫰",
        "꫱",
        "꯫",
        "﹒",
        "﹖",
        "﹗",
        "！",
        "．",
        "？",
        "𐩖",
        "𐩗",
        "𑁇",
        "𑁈",
        "𑂾",
        "𑂿",
        "𑃀",
        "𑃁",
        "𑅁",
        "𑅂",
        "𑅃",
        "𑇅",
        "𑇆",
        "𑇍",
        "𑇞",
        "𑇟",
        "𑈸",
        "𑈹",
        "𑈻",
        "𑈼",
        "𑊩",
        "𑑋",
        "𑑌",
        "𑗂",
        "𑗃",
        "𑗉",
        "𑗊",
        "𑗋",
        "𑗌",
        "𑗍",
        "𑗎",
        "𑗏",
        "𑗐",
        "𑗑",
        "𑗒",
        "𑗓",
        "𑗔",
        "𑗕",
        "𑗖",
        "𑗗",
        "𑙁",
        "𑙂",
        "𑜼",
        "𑜽",
        "𑜾",
        "𑩂",
        "𑩃",
        "𑪛",
        "𑪜",
        "𑱁",
        "𑱂",
        "𖩮",
        "𖩯",
        "𖫵",
        "𖬷",
        "𖬸",
        "𖭄",
        "𛲟",
        "𝪈",
    ]

    extra_tokens += other_tokens

    regex = re.compile(r"|".join(extra_tokens))

    def tokenize(self, content: str, language: str = "english") -> Dict[str, List[Any]]:

        sentences_first = nltk.sent_tokenize(content, language)
        sentences = []

        for sentence in sentences_first:
            s = self.regex.split(sentence)
            sentences += s

        ret = {"sentences": sentences}

        return ret
