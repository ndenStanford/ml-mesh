"""LSH handler."""

# Standard Library
import re
from typing import Any, Dict, List, Optional

# Internal libraries
# Internal library
from onclusiveml.core.logging import get_default_logger
from onclusiveml.datasketch import MinHash, MinHashLSH
from onclusiveml.nlp.stopwords import stopwords as stop_word_remover
from onclusiveml.nlp.word_tokenize import WordTokenizer


logger = get_default_logger(__name__)


class LshHandler:
    def __init__(self) -> None:
        self.tokenizer = WordTokenizer()

    def k_shingle(self, words: List[str], k: int = 5) -> List[str]:
        """
        Generates k-shingles from a list of words.

        Args:
            words (List[str]): List of words to generate k-shingles from.
            k (int, optional): The length of the shingles (default is 5).

        Returns:
            List[str]: A list of k-shingles generated from the input words.
        """
        num_words = len(words)

        if k > num_words:
            return []
        return [" ".join(words[i : i + k]) for i in range(len(words) - k + 1)]  # noqa

    def generate_lsh_signature(
        self, shingle_list: List[str], num_perm: int = 128, threshold: float = 0.6
    ) -> str:
        """
        Generates an LSH signature for a list of shingles.

        Args:
            shingle_list (List[str]): List of shingles for which to generate the signature.
            num_perm (int, optional): Number of permutations for MinHash (default is 128).
            threshold (float, optional): Jaccard similarity threshold for LSH (default is 0.6).

        Returns:
            str: The LSH signature generated for the input shingles.
        """
        shingle_set = set(shingle_list)

        m = MinHash(num_perm)
        for s in shingle_set:
            m.update(s.encode("utf8"))

        lsh = MinHashLSH(threshold, num_perm)
        signature = lsh.generate_signature(m)
        return signature

    def pre_processing(self, text: str, lang: str = "en") -> List[str]:
        """
        Pre-processes the input text for further analysis.

        Args:
            text (str): The input text to be pre-processed.
            lang (str, optional): Language of the text (default is "en").

        Returns:
            List[str]: A list of pre-processed words after tokenization and stop-word removal.
        """
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        text = text.rstrip()
        language = lang
        words = self.tokenizer.tokenize(content=text, language="english")
        words = words["words"]
        words = stop_word_remover(content=words, lang=language)
        return words


_service = LshHandler()


def handle(data: Any) -> Optional[Dict[str, Optional[List[str]]]]:
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
        language = data["language"]
        words = _service.pre_processing(text=text, lang=language)

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
