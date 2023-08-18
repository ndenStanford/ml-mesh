# Standard Library
import os
from typing import List, Tuple, Union

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# --- settings classes
class TrackedKeywordModelSpecs(TrackedModelSpecs):
    project: str = "onclusive/keywords"
    model = "KEYWORDS-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):

    sample_documents: List[str] = [
        """Supervised learning is the machine learning task of learning a function that maps an
        input to an output based on example input-output pairs. It infers a function from labeled
        training data consisting of a set of training examples. In supervised learning, each
        example is a pair consisting of an input object (typically a vector) and a desired output
        value (also called the supervisory signal). A supervised learning algorithm analyzes the
        training data and produces an inferred function, which can be used for mapping new
        examples. An optimal scenario will allow for the algorithm to correctly determine the class
        labels for unseen instances. This requires the learning algorithm to generalize from the
        training data to unseen situations in a 'reasonable' way (see inductive bias).""",
        """Überwachtes Lernen ist die maschinelle Lernaufgabe, eine Funktion zu lernen, die ordnet
        eine Eingabe einer Ausgabe basierend auf beispielhaften Eingabe-Ausgabe-Paaren zu. Es
        folgert a Funktion aus beschrifteten Trainingsdaten, die aus einer Reihe von
        Trainingsbeispielen bestehen. Beim überwachten Lernen ist jedes Beispiel ein Paar, das aus
        einem Eingabeobjekt besteht (typischerweise ein Vektor) und einem gewünschten Ausgangswert
        (auch Überwachungssignal genannt). Ein überwachter Lernalgorithmus analysiert die
        Trainingsdaten und erzeug eine abgeleitete Funktion. die zum Mapping neuer Beispiele
        verwendet werden können. Ein optimales Szenario ermöglicht die Algorithmus, um die
        Klassenbezeichnungen für unsichtbare Instanzen korrekt zu bestimmen. Dafür braucht man den
        Lernalgorithmus zum Verallgemeinern der Trainingsdaten auf ungesehene Situationen in a
        'vernünftiger' Weg (siehe induktive Vorspannung).""",
        """El aprendizaje supervisado es la tarea de aprendizaje automático de aprender una función
        que asigna una entrada a una salida en función de pares de entrada-salida de ejemplo. Se
        infiere un función a partir de datos de entrenamiento etiquetados que consisten en un
        conjunto de ejemplos de entrenamiento. En el aprendizaje supervisado, cada ejemplo es un
        par que consta de un objeto de entrada (típicamente un vector) y un valor de salida deseado
        (también llamado señal de supervisión). Un algoritmo de aprendizaje supervisado analiza los
        datos de entrenamiento y produce una función inferida, que se puede utilizar para mapear
        nuevos ejemplos. Un escenario óptimo permitirá que la algoritmo para determinar
        correctamente las etiquetas de clase para instancias no vistas. Esto requiere el algoritmo
        de aprendizaje para generalizar a partir de los datos de entrenamiento a situaciones no
        vistas en un manera 'razonable' (ver sesgo inductivo).""",
    ]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class KeywordExtractionSettings(TrackedParams):
    keyphrase_ngram_range: Tuple[int, int] = (1, 1)
    stop_words: Union[str, List[str]] = "english"
    top_n: int = 3

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class KeywordModelParams(TrackedParams):
    huggingface_pipeline_task: str = "feature-extraction"
    huggingface_model_reference: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    keyword_extraction_settings: KeywordExtractionSettings = KeywordExtractionSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TrackedKeywordsBaseModelCard(TrackedModelCard):
    """The model card for the base model of the keywords ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: KeywordModelParams = KeywordModelParams()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "keyword_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
