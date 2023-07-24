"""LSH handler."""

# Standard Library
import re
from typing import Any, Dict, List, Optional

# 3rd party libraries
import nltk
import stopwordsiso
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as nltk_word_tokenize

# Internal libraries
# Internal library
from onclusiveml.core.logging import get_default_logger
from onclusiveml.datasketch import MinHash, MinHashLSH


nltk.download("punkt")
nltk.download("stopwords")
STOP_WORDS = {lang: stopwordsiso.stopwords(lang) for lang in stopwordsiso.langs()}
STOP_WORDS["en"] = set(stopwords.words("english"))


logger = get_default_logger(__name__)


class LshHandler:
    def k_shingle(self, words: List[str], k: int = 5) -> List[str]:
        num_words = len(words)

        if k > num_words:
            return []
        return [" ".join(words[i : i + k]) for i in range(len(words) - k + 1)]  # noqa

    def generate_lsh_signature(
        self, shingle_list: List[str], num_perm: int = 128, threshold: float = 0.6
    ) -> str:
        shingle_set = set(shingle_list)

        m = MinHash(num_perm)
        for s in shingle_set:
            m.update(s.encode("utf8"))

        lsh = MinHashLSH(threshold, num_perm)
        signature = lsh.generate_signature(m)
        return signature

    def word_tokenizer(self, text: str, lang: str) -> List[str]:
        word_tokenizers = {"en": nltk_word_tokenize}
        if lang in word_tokenizers:
            words = word_tokenizers[lang](text)
        else:
            words = word_tokenizers["en"](text)
        return words

    def stop_word_remover(self, words: List[str], lang: str) -> List[str]:
        if lang in STOP_WORDS:
            cur_stopwords = STOP_WORDS[lang]
            words = [word for word in words if word not in cur_stopwords]

        return words


_service = LshHandler()


def handle(data: Any) -> Optional[Dict[str, Optional[List[str]]]]:
    # Setup stopwords
    STOP_WORDS = {lang: stopwordsiso.stopwords(lang) for lang in stopwordsiso.langs()}
    STOP_WORDS["en"] = set(stopwords.words("english"))
    try:
        if data is None:
            return None

        if "body" not in data[0]:
            logger.warning(
                "Malformed request, content does not contain a body key."
                "Is your request properly formatted as json?"
            )
            return None

        data = data[0]["body"]

        if type(data) == bytearray:
            data = eval(data)
        text = data["content"]
        if text == "" or text is None:
            logger.warning(
                "Content field is empty. This will result in no signature being returned"
            )
            return {"signature": None}  # Returning None here if text is empty or None
        else:
            logger.warning(text)
        # Simple text pre-processing
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        text = text.rstrip()
        language = data["language"]
        words = _service.word_tokenizer(text, language)
        words = _service.stop_word_remover(words, language)

        shingle_list = _service.k_shingle(words, k=data["shingle_list"])
        if len(shingle_list) < 1:
            return {"signature": None}

        shingle_set = set(shingle_list)

        m = MinHash(data["num_perm"])
        # change this to bulk update later
        for s in shingle_set:
            m.update(s.encode("utf8"))

        lsh = MinHashLSH(data["threshold"], data["num_perm"], data["weights"])
        signature = lsh.generate_signature(m)
        return {"signature": signature}
    except Exception as e:
        raise e
