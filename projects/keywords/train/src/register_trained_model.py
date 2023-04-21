# Standard Library
import json
import os
from typing import Dict, List, Tuple

# ML libs
import torch
from keybert import KeyBERT
from transformers import pipeline

# 3rd party libraries
import neptune

# Source
from src.settings import KEYWORD_TRAIN_SETTINGS


settings = KEYWORD_TRAIN_SETTINGS.dict()

if not os.path.isdir(settings["LOCAL_OUTPUT_DIR"]):
    os.makedirs(settings["LOCAL_OUTPUT_DIR"])
# --- initialize models
# get specified huggingface transformer pipeline
hf_pipeline = pipeline("feature-extraction", settings["HF_MODEL_REFERENCE"])
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
tokenizer_settings = settings["TOKENIZER_SETTINGS"]

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
keybert_predictions: List[Tuple[str, float]] = keybert_model.extract_keywords(
    sample_inputs, keyphrase_ngram_range=(1, 1), stop_words=None
)
# --- register model on neptune ai
model_version = neptune.init_model_version(
    model=settings["NEPTUNE_MODEL_ID"],
    project=settings["NEPTUNE_PROJECT"],
    api_token=settings["NEPTUNE_API_TOKEN"],  # your credentials
)
# inputs & outputs
for (data, data_file_reference) in [
    (sample_inputs, "text_inputs"),
    (tokenizer_settings, "tokenizer_settings"),
    (tokenized_sample_inputs, "tokenized_inputs"),
    (hf_model_predictions, "hf_model_predictions"),
    (hf_pipeline_predictions, "hf_pipeline_predictions"),
    (keybert_predictions, "keybert_predictions"),
]:
    # export locally to make use of neptune ai's uoload method
    test_file_path = os.path.join(
        settings["LOCAL_OUTPUT_DIR"], f"{data_file_reference}.json"
    )

    with open(test_file_path, "w") as local_file:
        json.dump(data, local_file)

    neptune_data_reference = f"model/test_files/{data_file_reference}"

    print(
        f"Uploading {data_file_reference} from local path {test_file_path}",
        f"to meta data path {neptune_data_reference}.",
    )

    model_version[neptune_data_reference].upload(test_file_path)

    print(
        f"Uploaded {data_file_reference} from local path {test_file_path}",
        f"to meta data path {neptune_data_reference}",
    )
# huggingface artifacts
for (artifact, artifact_reference) in (
    (
        hf_pipeline,
        "hf_pipeline",
    ),
):
    artifact_local_dir = os.path.join(settings["LOCAL_OUTPUT_DIR"], artifact_reference)
    artifact.save_pretrained(artifact_local_dir)

    for artifact_file in os.listdir(artifact_local_dir):
        artifact_file_path = os.path.join(artifact_local_dir, artifact_file)

        print(
            f"Uploading {artifact_file_path} to meta data path",
            f"model/{artifact_reference}/{artifact_file}.",
        )

        model_version[f"model/{artifact_reference}/{artifact_file}"].upload(
            artifact_file_path
        )

        print(
            f"Uploaded {artifact_file_path} to meta data path ",
            f"model/{artifact_reference}/{artifact_file}.",
        )
    # test params upload
    # Define and log metadata
    TEST_PARAMS = {
        "batch_size": 64,
        "dropout": 0.2,
        "learning_rate": 0.001,
        "optimizer": "Adam",
        "config": {"a": 1, "b": 2},
    }

    model_version["model/test_params"] = TEST_PARAMS  # ?
    model_version["model/test_text_inputs"] = {"content": sample_inputs}  # ?
    model_version["model/test_tokenizer_settings"] = tokenizer_settings  # succeeds
    model_version["model/test_tokenized_inputs"] = tokenized_sample_inputs  # fails
    model_version["model/test_hf_model_predictions"] = {
        "content": hf_model_predictions
    }  # fails
    # looks like dicts with array type values or
model_version.stop()
