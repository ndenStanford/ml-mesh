# Standard Library
import os
from typing import Dict, List, Tuple

# ML libs
import torch
from keybert import KeyBERT
from transformers import pipeline

# Internal libraries
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import KEYWORD_TRAIN_SETTINGS


keyword_train_settings = KEYWORD_TRAIN_SETTINGS.dict()

if not os.path.isdir(keyword_train_settings["LOCAL_OUTPUT_DIR"]):
    os.makedirs(keyword_train_settings["LOCAL_OUTPUT_DIR"])
# --- initialize models
# get specified huggingface transformer pipeline
hf_pipeline = pipeline(
    "feature-extraction", keyword_train_settings["HF_MODEL_REFERENCE"]
)
hf_tokenizer = hf_pipeline.tokenizer
hf_model = hf_pipeline.model
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
# tokenizer
# has max_token_length=512
# classic tokenizer output dict with keys 'input_ids'->List[Tuple[int]] and
# 'attention_mask'->:List[Tuple[int]],
# if not setting padding = max_length, this would give a list with each array being of dim
# n_batch x min(max(n_tokens),max_token_length) = n_batch x min(max(n_tokens),512),
# where max(n_tokens) is the maximum sequence length across the batch
# setting padding = max_length ensures all arrays have the same dimension
tokenizer_settings = keyword_train_settings["TOKENIZER_SETTINGS"]

tokenized_sample_inputs: Dict[str, List[Tuple[int]]] = dict(
    hf_pipeline.tokenizer(sample_inputs, **tokenizer_settings)
)
tokenized_sample_inputs_tensor: Dict[str, torch.Tensor] = hf_pipeline.tokenizer(
    sample_inputs, return_tensors="pt", **tokenizer_settings
)
# hugginface transformer model
# has n_embed=384
# torch tensor converted to nested list of dim n_batch x max_token_length x n_embed
# = n_batch x 512 x 384
hf_model_predictions: List[Tuple[Tuple[float]]] = hf_pipeline.model(
    **tokenized_sample_inputs_tensor
).last_hidden_state.tolist()
# huggingface pipeline
# note: # if not setting padding = max_length, this would give an array as nested lists of
# dim n_batch x 1 x n_tokens x n_embed = n_batch x 1 x min(n_tokens,512) x 384
# the n_tokens dim is input dependent regardless of padding approach chosen for tokenization, as the
# embeddings of the trivial padding tokens seem to get removed by the head section
# of the pipeline wrapper
# specifying tokenizer settings via the tokenize_kwargs arg ensures deterministic, consistently
# shaped outputs
hf_pipeline_predictions: List[List[Tuple[float]]] = hf_pipeline(
    sample_inputs, tokenize_kwargs=tokenizer_settings
)
# keybert model
# list of tuples (ngram/word, prob)
keybert_settings = {"keyphrase_ngram_range": (1, 1), "stopwords": None}
keybert_predictions: List[Tuple[str, float]] = keybert_model.extract_keywords(
    sample_inputs, keyphrase_ngram_range=(1, 1), stop_words=None
)
# --- register model on neptune ai
model_version = TrackedModelVersion(
    model=keyword_train_settings["NEPTUNE_MODEL_ID"],
    project=keyword_train_settings["NEPTUNE_PROJECT"],
    api_token=keyword_train_settings["NEPTUNE_API_TOKEN"],
)
# inputs & outputs
for (data, data_file_reference) in [
    (sample_inputs, "text_inputs"),
    (tokenizer_settings, "tokenizer_settings"),
    (tokenized_sample_inputs, "tokenized_inputs"),
    (hf_model_predictions, "hf_model_predictions"),
    (hf_pipeline_predictions, "hf_pipeline_predictions"),
    (keybert_settings, "keybert_settings"),
    (keybert_predictions, "keybert_predictions"),
]:
    neptune_attribute_path = f"model/test_files/{data_file_reference}"

    model_version.upload_config_to_model_version(
        config=data, neptune_attribute_path=neptune_attribute_path
    )

hf_pipeline_local_dir = os.path.join(
    keyword_train_settings["LOCAL_OUTPUT_DIR"], "hf_pipeline"
)
hf_pipeline.save_pretrained(hf_pipeline_local_dir)

model_version.upload_directory_to_model_version(
    local_directory_path=hf_pipeline_local_dir,
    neptune_attribute_path="model/hf_pipeline",
)

model_version.stop()
