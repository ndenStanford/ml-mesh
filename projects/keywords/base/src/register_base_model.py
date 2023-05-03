# Standard Library
import os
from typing import List, Tuple

# ML libs
from keybert import KeyBERT
from transformers import pipeline

# Internal libraries
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import tracked_keywords_base_model_card as config


if not os.path.isdir(config.local_output_dir):
    os.makedirs(config.local_output_dir)
# initialize registered model on neptune ai
model_version = TrackedModelVersion(**config.model_specs.dict())
# --- initialize models
# get specified huggingface transformer pipeline
hf_pipeline = pipeline(
    task=config.model_params.huggingface_pipeline_task,
    model=config.model_params.huggingface_model_reference,
)
# initialize keybert model with huggingface pipeline backend
keybert_model = KeyBERT(model=hf_pipeline)
# --- create prediction files
sample_inputs = [
    """Supervised learning is the machine learning task of learning a function that
         maps an input to an output based on example input-output pairs. It infers a
         function from labeled training data consisting of a set of training examples.
         In supervised learning, each example is a pair consisting of an input object
         (typically a vector) and a desired output value (also called the supervisory signal).
         A supervised learning algorithm analyzes the training data and produces an inferred
         function,
         which can be used for mapping new examples. An optimal scenario will allow for the
         algorithm to correctly determine the class labels for unseen instances. This requires
         the learning algorithm to generalize from the training data to unseen situations in a
         'reasonable' way (see inductive bias).""",
    """Überwachtes Lernen ist die maschinelle Lernaufgabe, eine
    Funktion zu lernen, die
         ordnet eine Eingabe einer Ausgabe basierend auf beispielhaften
         Eingabe-Ausgabe-Paaren zu. Es folgert a
         Funktion aus beschrifteten Trainingsdaten, die aus einer Reihe
         von Trainingsbeispielen bestehen.
         Beim überwachten Lernen ist jedes Beispiel ein Paar, das aus einem
         Eingabeobjekt besteht
         (typischerweise ein Vektor) und einem gewünschten Ausgangswert (auch
         Überwachungssignal genannt).
         Ein überwachter Lernalgorithmus analysiert die Trainingsdaten und erzeug
         eine abgeleitete Funktion.
         die zum Mapping neuer Beispiele verwendet werden können. Ein optimales
         Szenario ermöglicht die
         Algorithmus, um die Klassenbezeichnungen für unsichtbare Instanzen korrekt
         zu bestimmen. Dafür braucht man
         den Lernalgorithmus zum Verallgemeinern der Trainingsdaten auf ungesehene
         Situationen in a
         'vernünftiger' Weg (siehe induktive Vorspannung).""",
    """El aprendizaje supervisado es la tarea de aprendizaje automático de
    aprender una función que
         asigna una entrada a una salida en función de pares de entrada-salida de
         ejemplo. Se infiere un
         función a partir de datos de entrenamiento etiquetados que consisten en un conjunto de
         ejemplos de entrenamiento.
         En el aprendizaje supervisado, cada ejemplo es un par que consta de un
         objeto de entrada
         (típicamente un vector) y un valor de salida deseado (también llamado señal
         de supervisión).
         Un algoritmo de aprendizaje supervisado analiza los datos de entrenamiento y
         produce una función inferida,
         que se puede utilizar para mapear nuevos ejemplos. Un escenario óptimo
         permitirá que la
         algoritmo para determinar correctamente las etiquetas de clase para instancias
         no vistas. Esto requiere
         el algoritmo de aprendizaje para generalizar a partir de los datos de entrenamiento
         a situaciones no vistas en un
         manera 'razonable' (ver sesgo inductivo).""",
]
# keybert model
# list of tuples (ngram/word, prob)
keyword_extraction_settings = config.model_params.keyword_extraction_settings.dict()
keybert_predictions: List[Tuple[str, float]] = keybert_model.extract_keywords(
    sample_inputs, **keyword_extraction_settings
)
# --- add assets to registered model version on neptune ai
# testing assets - inputs, inference specs and outputs
for (test_file, test_file_attribute_path) in [
    (sample_inputs, config.model_test_files.inputs),
    (keyword_extraction_settings, config.model_test_files.inference_params),
    (keybert_predictions, config.model_test_files.predictions),
]:
    model_version.upload_config_to_model_version(
        config=test_file, neptune_attribute_path=test_file_attribute_path
    )
# model artifact
hf_pipeline_local_dir = os.path.join(config.local_output_dir, "hf_pipeline")
hf_pipeline.save_pretrained(hf_pipeline_local_dir)

model_version.upload_directory_to_model_version(
    local_directory_path=hf_pipeline_local_dir,
    neptune_attribute_path=config.model_artifact_attribute_path,
)
# # model card
model_version.upload_config_to_model_version(
    config=config.dict(), neptune_attribute_path="model/model_card"
)

model_version.stop()
