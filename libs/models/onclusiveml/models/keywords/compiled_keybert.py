# Standard Library
import os
from pathlib import Path
from typing import Any, List, Tuple, Union

# ML libs
from keybert import KeyBERT
from keybert._highlight import highlight_document
from keybert._maxsum import max_sum_distance
from keybert._mmr import mmr
from transformers.pipelines import Pipeline, pipeline

# 3rd party libraries
import numpy as np
from packaging import version
from sklearn import __version__ as sklearn_version
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.models.keywords import CustomHFTransformerBackend


class CompiledKeyBERT(KeyBERT):

    """Compilation wrapper around the KeyBERT to provide support for two compiled backends that
    are exclusively used for document and keywords/seed words embeddings, respectively.

    Uses custom CompiledHFTransformerBackend instances, which are in turn using ml_compile's
    custom CompiledPipeline instances.
    """

    def __init__(
        self,
        document_pipeline: CompiledPipeline,
        compiled_word_pipeline: Union[CompiledPipeline, Pipeline],
    ):
        """Updated constructor to support initialization and attaching of two, not one, backend of
            type CustomHFTransformerBackend:
            - `document_backend`; to be used do embed documents, and
            - `compiled_word_backend`; to be used to embed keywords and seeded keywords (if
                applicable)

        Args:
            document_pipeline (Union[CompiledPipeline,Pipeline]): A pipeline used to embed entire
                documents. Both compiled and uncompiled are supported. Unless incoming token
                sequence length are equal to the model_max_length for 90% of the time or more, an
                uncompiled pipeline gives better latency results than a (neuron) compiled one.
            compiled_word_pipeline (CompiledPipeline): A pipeline that has been compiled to embed
                keywords of token sequence lengths no more than 25. Only (neuron) compiled
                pipelines are supported here as they provide a speed up of 3x - 4x.

        Args:
            copmiled_document_pipeline (CompiledPipeline): A pipeline that has been compiled to
                embed entire documents.
            compiled_word_pipeline (CompiledPipeline): A pipeline that has been compiled
                to embed keywords of lengths no more than 10.
        """

        self.document_backend = CustomHFTransformerBackend(document_pipeline)
        self.compiled_word_backend = CustomHFTransformerBackend(compiled_word_pipeline)

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        """Canonic huggingface transformers export method. Only supports exporting to local file
        system.

        Args:
            directory (Path,str): Directory on local file system to export model artifact to. Will
                be created if it doesnt exist.
        """
        # since document pipelines are supported in both compiled and uncompiled formats, we use
        # different subdirectories during export to be able to disambiguate at import time
        if isinstance(self.document_backend.embedding_model, CompiledPipeline):
            document_export_subdir = "compiled_document_pipeline"
        else:
            document_export_subdir = "document_pipeline"
        # for pipeline_subdir in ("compiled_word_pipeline", document_export_subdir):
        #     os.makedirs(os.path.join(directory, pipeline_subdir))
        # export word embedding pipeline
        self.compiled_word_backend.embedding_model.save_pretrained(
            os.path.join(directory, "compiled_word_pipeline")
        )
        # export compiled or uncompiled document embedding pipeline
        self.document_backend.embedding_model.save_pretrained(
            os.path.join(directory, document_export_subdir)
        )

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledKeyBERT":
        """Canonic huggingface transformers import method. Only supports importing from local file
        system.

        Args:
            directory (Path,str): Directory on local file system to import model artifact from."""

        compiled_word_pipeline = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_word_pipeline")
        )

        if os.path.isdir(os.path.join(directory, "compiled_document_pipeline")):
            document_pipeline = CompiledPipeline.from_pretrained(
                os.path.join(directory, "compiled_document_pipeline")
            )
        else:
            document_pipeline = pipeline(
                task="feature-extraction",
                model=os.path.join(directory, "document_pipeline"),
            )

        return cls(
            document_pipeline=document_pipeline,
            compiled_word_pipeline=compiled_word_pipeline,
        )

    def extract_keywords(  # noqa: ignore=C901
        self,
        docs: Union[str, List[str]],
        candidates: Union[List[str], None] = None,
        keyphrase_ngram_range: Tuple[int, int] = (1, 1),
        stop_words: Union[str, List[str]] = "english",
        top_n: int = 5,
        min_df: int = 1,
        use_maxsum: bool = False,
        use_mmr: bool = False,
        diversity: float = 0.5,
        nr_candidates: int = 20,
        vectorizer: CountVectorizer = None,
        highlight: bool = False,
        seed_keywords: Union[List[str], List[List[str]], None] = None,
        doc_embeddings: np.array = None,
        word_embeddings: np.array = None,
    ) -> Union[List[Tuple[str, float]], List[List[Tuple[str, float]]]]:
        """Extract keywords and/or keyphrases
        To get the biggest speed-up, make sure to pass multiple documents
        at once instead of iterating over a single document.
        Arguments:
            docs: The document(s) for which to extract keywords/keyphrases
            candidates: Candidate keywords/keyphrases to use instead of extracting them from the
                document(s)
                NOTE: This is not used if you passed a `vectorizer`.
            keyphrase_ngram_range: Length, in words, of the extracted keywords/keyphrases.
                                   NOTE: This is not used if you passed a `vectorizer`.
            stop_words: Stopwords to remove from the document.
                        NOTE: This is not used if you passed a `vectorizer`.
            top_n: Return the top n keywords/keyphrases
            min_df: Minimum document frequency of a word across all documents
                    if keywords for multiple documents need to be extracted.
                    NOTE: This is not used if you passed a `vectorizer`.
            use_maxsum: Whether to use Max Sum Distance for the selection
                        of keywords/keyphrases.
            use_mmr: Whether to use Maximal Marginal Relevance (MMR) for the
                     selection of keywords/keyphrases.
            diversity: The diversity of the results between 0 and 1 if `use_mmr`
                       is set to True.
            nr_candidates: The number of candidates to consider if `use_maxsum` is
                           set to True.
            vectorizer: Pass in your own `CountVectorizer` from
                        `sklearn.feature_extraction.text.CountVectorizer`
            highlight: Whether to print the document and highlight its keywords/keyphrases.
                       NOTE: This does not work if multiple documents are passed.
            seed_keywords: Seed keywords that may guide the extraction of keywords by
                           steering the similarities towards the seeded keywords.
                           NOTE: when multiple documents are passed,
                           `seed_keywords`funtions in either of the two ways below:
                           - globally: when a flat list of str is passed, keywords are shared by
                                all documents,
                           - locally: when a nested list of str is passed, keywords differs among
                                documents.
            doc_embeddings: The embeddings of each document.
            word_embeddings: The embeddings of each potential keyword/keyphrase across
                             across the vocabulary of the set of input documents.
                             NOTE: The `word_embeddings` should be generated through
                             `.extract_embeddings` as the order of these embeddings depend
                             on the vectorizer that was used to generate its vocabulary.
        Returns:
            keywords: The top n keywords for a document with their respective distances
                      to the input document.
        Usage:
        To extract keywords from a single document:
        ```python
        from keybert import KeyBERT
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(doc)
        ```
        To extract keywords from multiple documents, which is typically quite a bit faster:
        ```python
        from keybert import KeyBERT
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(docs)
        ```
        """
        # Check for a single, empty document
        if isinstance(docs, str):
            if docs:
                docs = [docs]
            else:
                raise ValueError(f"No documents specified: {docs}")
        # Extract potential words using a vectorizer / tokenizer
        if vectorizer:
            count = vectorizer.fit(docs)
        else:

            if isinstance(keyphrase_ngram_range, list):
                keyphrase_ngram_range = tuple(keyphrase_ngram_range)  # type: ignore[unreachable]

            count = CountVectorizer(
                ngram_range=keyphrase_ngram_range,
                stop_words=stop_words,
                min_df=min_df,
                vocabulary=candidates,
            ).fit(docs)
        # Scikit-Learn Deprecation: get_feature_names is deprecated in 1.0
        # and will be removed in 1.2. Please use get_feature_names_out instead.
        if version.parse(sklearn_version) >= version.parse("1.0.0"):
            words = count.get_feature_names_out()
        else:
            words = count.get_feature_names()
        df = count.transform(docs)
        # Check if the right number of word embeddings are generated compared with the vectorizer
        if word_embeddings is not None:
            if word_embeddings.shape[0] != len(words):
                raise ValueError(
                    "Make sure that the `word_embeddings` are generated from the function "
                    "`.extract_embeddings`. \nMoreover, the `candidates`, `keyphrase_ngram_range`,"
                    "`stop_words`, and `min_df` parameters need to have the same values in both "
                    "`.extract_embeddings` and `.extract_keywords`."
                )
        # Extract embeddings
        if doc_embeddings is None:
            doc_embeddings = self.document_backend.embed(docs)
        if word_embeddings is None:
            word_embeddings = self.compiled_word_backend.embed(words)
        # Guided KeyBERT either local (keywords shared among documents) or global (keywords per
        # document)
        if seed_keywords is not None:
            if isinstance(seed_keywords[0], str):
                seed_embeddings = self.compiled_word_backend.embed(seed_keywords).mean(
                    axis=0, keepdims=True
                )
            elif len(docs) != len(seed_keywords):
                raise ValueError(
                    "The length of docs must match the length of seed_keywords"
                )
            else:
                seed_embeddings = np.vstack(
                    [
                        self.compiled_word_backend.embed(keywords).mean(
                            axis=0, keepdims=True
                        )
                        for keywords in seed_keywords
                    ]
                )
            doc_embeddings = (doc_embeddings * 3 + seed_embeddings) / 4
        # Find keywords
        all_keywords = []
        for index, _ in enumerate(docs):

            try:
                # Select embeddings
                candidate_indices = df[index].nonzero()[1]
                candidates = [words[index] for index in candidate_indices]
                candidate_embeddings = word_embeddings[candidate_indices]
                doc_embedding = doc_embeddings[index].reshape(1, -1)
                # Maximal Marginal Relevance (MMR)
                if use_mmr:
                    keywords = mmr(
                        doc_embedding,
                        candidate_embeddings,
                        candidates,
                        top_n,
                        diversity,
                    )
                # Max Sum Distance
                elif use_maxsum:
                    keywords = max_sum_distance(
                        doc_embedding,
                        candidate_embeddings,
                        candidates,
                        top_n,
                        nr_candidates,
                    )
                # Cosine-based keyword extraction
                else:
                    distances = cosine_similarity(doc_embedding, candidate_embeddings)
                    keywords = [
                        (candidates[index], round(float(distances[0][index]), 4))
                        for index in distances.argsort()[0][-top_n:]
                    ][::-1]

                all_keywords.append(keywords)
            # Capturing empty keywords
            except ValueError:
                all_keywords.append([])
        # Highlight keywords in the document
        if len(all_keywords) == 1:
            if highlight:
                highlight_document(docs[0], all_keywords[0], count)
            all_keywords = all_keywords[0]

        return all_keywords

    def extract_embeddings(
        self,
        docs: Union[str, List[str]],
        candidates: Union[List[str], None] = None,
        keyphrase_ngram_range: Tuple[int, int] = (1, 1),
        stop_words: Union[str, List[str]] = "english",
        min_df: int = 1,
        vectorizer: CountVectorizer = None,
    ) -> Tuple[Any, Any]:
        """Extract document and word embeddings for the input documents and the
        generated candidate keywords/keyphrases respectively.
        Note that all potential keywords/keyphrases are not returned but only their
        word embeddings. This means that the values of `candidates`, `keyphrase_ngram_range`,
        `stop_words`, and `min_df` need to be the same between using `.extract_embeddings` and
        `.extract_keywords`.
        Arguments:
            docs: The document(s) for which to extract keywords/keyphrases
            candidates: Candidate keywords/keyphrases to use instead of extracting them from the
                document(s)
                NOTE: This is not used if you passed a `vectorizer`.
            keyphrase_ngram_range: Length, in words, of the extracted keywords/keyphrases.
                NOTE: This is not used if you passed a `vectorizer`.
            stop_words: Stopwords to remove from the document.
                NOTE: This is not used if you passed a `vectorizer`.
            min_df: Minimum document frequency of a word across all documents if keywords for
                multiple documents need to be extracted.
                NOTE: This is not used if you passed a `vectorizer`.
            vectorizer: Pass in your own `CountVectorizer` from
                        `sklearn.feature_extraction.text.CountVectorizer`
        Returns:
            doc_embeddings: The embeddings of each document.
            word_embeddings: The embeddings of each potential keyword/keyphrase across across the
                vocabulary of the set of input documents.
                NOTE: The `word_embeddings` should be generated through `.extract_embeddings` as
                the order of these embeddings depend on the vectorizer that was used to generate
                its vocabulary.
        Usage:
        To generate the word and document embeddings from a set of documents:
        ```python
        from keybert import KeyBERT
        kw_model = KeyBERT()
        doc_embeddings, word_embeddings = kw_model.extract_embeddings(docs)
        ```
        You can then use these embeddings and pass them to `.extract_keywords` to speed up the
            tuning the model:
        ```python
        keywords = kw_model.extract_keywords(docs, doc_embeddings=doc_embeddings,
        word_embeddings=word_embeddings)
        ```
        """
        # Check for a single, empty document
        if isinstance(docs, str):
            if docs:
                docs = [docs]
            else:
                raise ValueError(f"No documents specified: {docs}")
        # Extract potential words using a vectorizer / tokenizer
        if vectorizer:
            count = vectorizer.fit(docs)
        else:

            if isinstance(keyphrase_ngram_range, list):
                keyphrase_ngram_range = tuple(keyphrase_ngram_range)  # type: ignore[unreachable]

            count = CountVectorizer(
                ngram_range=keyphrase_ngram_range,
                stop_words=stop_words,
                min_df=min_df,
                vocabulary=candidates,
            ).fit(docs)
        # Scikit-Learn Deprecation: get_feature_names is deprecated in 1.0
        # and will be removed in 1.2. Please use get_feature_names_out instead.
        if version.parse(sklearn_version) >= version.parse("1.0.0"):
            words = count.get_feature_names_out()
        else:
            words = count.get_feature_names()

        doc_embeddings = self.document_backend.embed(docs)
        word_embeddings = self.compiled_word_backend.embed(words)

        return doc_embeddings, word_embeddings
