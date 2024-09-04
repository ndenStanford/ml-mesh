"""Bela Model script."""

# Standard Library
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

# ML libs
import torch

# 3rd party libraries
import numpy as np
from redis.commands.search.query import Query
from tqdm import tqdm

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.models.bela.datamodule.joint_el_datamodule import (
    JointELDataModule,
)
from onclusiveml.models.bela.settings import BelaSettings
from onclusiveml.models.bela.task.joint_el_task import JointELTask
from onclusiveml.models.bela.transforms.joint_el_transform import (
    JointELXlmrRawTextTransform,
)
from onclusiveml.models.bela.utils.client import get_client
from onclusiveml.models.bela.utils.index import get_index


logger = get_default_logger(__name__, level=20)
settings = BelaSettings()


def load_file(path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Load the files."""
    all_data = []
    with open(path, "rt") as fd:
        for line in tqdm(fd):
            data = json.loads(line)
            all_data.append(data)
    return all_data


def convert_sp_to_char_offsets(
    text: str,
    sp_offsets: List[int],
    sp_lengths: List[int],
    sp_tokens_boundaries: List[List[int]],
) -> Tuple[List[int], List[int]]:
    """Convert sentecepiece offsets and lengths to character level offsets and lengths for a given `text`."""  # noqa
    char_offsets: List[int] = []
    char_lengths: List[int] = []
    text_utf8_chars: List[str] = [char for char in text]

    for sp_offset, sp_length in zip(sp_offsets, sp_lengths):
        # sp_offsets include cls_token, while boundaries doesn't
        if sp_offset == 0:
            continue

        sp_offset = sp_offset - 1
        char_offset = sp_tokens_boundaries[sp_offset][0]
        char_end = sp_tokens_boundaries[sp_offset + sp_length - 1][1]
        # sp token boundaries include whitespaces, so remove them
        while text_utf8_chars[char_offset].isspace():
            char_offset += 1
            assert char_offset < len(text_utf8_chars)

        char_offsets.append(char_offset)
        char_lengths.append(char_end - char_offset)

    return char_offsets, char_lengths


class BelaModel:
    """BelaModel."""

    def __init__(
        self,
        checkpoint_path,
        config_name="joint_el_mel",
        ent_catalogue_idx_path=None,
        device="cuda:0",
    ):
        """Initialize the model with specified parameters.

        Args:
            checkpoint_path (str): Path to the checkpoint file.
            config_name (str, optional): Name of the configuration. Defaults to "joint_el_mel".
            ent_catalogue_idx_path (str, optional): Path to the entity catalogue
                                                    index file. Defaults None.
            device (str, optional): Device to use for computations. Defaults to "cuda:0".
        """
        self.device = torch.device(device)

        logger.info("Create task")
        # Load configuration using Pydantic
        settings.task.load_from_checkpoint = checkpoint_path
        settings.datamodule.ent_catalogue_idx_path = (
            ent_catalogue_idx_path or settings.datamodule.ent_catalogue_idx_path
        )
        settings.datamodule.train_path = None
        settings.datamodule.val_path = None
        settings.datamodule.test_path = None

        self.checkpoint_path = checkpoint_path
        #     self.model=HFEncoder(model_path = settings.task.model.model_path)
        self.transform = JointELXlmrRawTextTransform(
            max_seq_len=settings.task.transform.max_seq_len
        )
        datamodule = JointELDataModule(
            transform=self.transform,
            batch_size=settings.datamodule.batch_size,
            train_path=settings.datamodule.train_path,
            val_path=settings.datamodule.val_path,
            test_path=settings.datamodule.test_path,
            ent_catalogue_idx_path=settings.datamodule.ent_catalogue_idx_path,
        )
        self.task = JointELTask(
            transform=self.transform,
            model=settings.task.model,
            datamodule=datamodule,
            optim=settings.task.optim,
            only_train_disambiguation=settings.task.only_train_disambiguation,
            train_saliency=settings.task.train_saliency,
            load_from_checkpoint=settings.task.load_from_checkpoint,
        )

        self.task.setup("train")
        self.task = self.task.eval()
        self.task = self.task.to(self.device)
        # Connect to Redis vector store
        self.client = get_client(
            url=settings.redis.REDIS_CONNECTION_STRING.get_secret_value()
        )

        get_index(
            client=self.client,
            index_name=settings.redis.INDEX_NAME,
            vector_dimensions=settings.redis.EMBEDDINGS_SHAPE[1],
        )

        logger.info("Create ent index")
        self.ent_idx = []
        for ent in datamodule.ent_catalogue.idx:
            self.ent_idx.append(ent)

        self.max_length = 256

    def lookup_faiss(
        self,
        query: torch.Tensor,
    ):
        """Search for nearest neighbors in the Faiss index.

        Args:
            self: The instance of the class.
            query (torch.Tensor): Tensor containing query vectors.
        """
        scores, indices = self.faiss_index.search(query, k=1)

        return scores.squeeze(-1).to(self.device), indices.squeeze(-1).to(self.device)

    def lookup(self, query: torch.Tensor):
        """Search for nearest neighbors in the Redis index.

        Args:
            query (torch.Tensor): Tensor containing query vectors.
        """
        results_scores = []
        results_indices = []
        # Ensure the tensor is on the CPU before converting to numpy
        query_vectors = query.cpu().numpy().astype(np.float32)
        ef_runtime = settings.redis.EF_RUNTIME
        for single_query_vector in query_vectors:
            single_query_vector_bytes = single_query_vector.tobytes()
            # Construct the query
            k = 1
            query_redis = (
                Query(
                    f"*=>[KNN {k} @embedding $query_vector as score]=>{{$EF_RUNTIME: {ef_runtime}}}"
                )
                .sort_by("score")
                .return_fields("id", "score")
                .paging(0, k)
                .dialect(2)
            )
            # Run the query search
            query_params = {"query_vector": single_query_vector_bytes}
            results = (
                self.client.ft(settings.redis.INDEX_NAME)
                .search(query_redis, query_params)
                .docs
            )
            scores = torch.tensor(
                [float(doc.score) for doc in results], device=self.device
            )
            indices = [doc.id for doc in results]

            results_scores.append(scores)
            results_indices.append(indices)
        # Combine results into single tensors
        combined_scores = torch.cat(results_scores).unsqueeze(
            -1
        )  # Adding an extra dimension to match expected output
        combined_indices = sum(results_indices, [])  # Flatten the list of lists

        return combined_scores, combined_indices

    def process_batch(self, texts):
        """Process a batch of texts for mention and entity extraction.

        Args:
            self: The instance of the class.
            texts (list): A list of strings representing the texts to process.

        Returns:
            list: A list of dictionaries representing the extracted mentions and entities.
        """
        batch: Dict[str, Any] = {"texts": texts}
        model_inputs = self.transform(batch)

        token_ids = model_inputs["input_ids"].to(self.device)
        text_pad_mask = model_inputs["attention_mask"].to(self.device)
        tokens_mapping = model_inputs["tokens_mapping"].to(self.device)
        sp_tokens_boundaries = model_inputs["sp_tokens_boundaries"].tolist()

        with torch.no_grad():
            _, last_layer = self.task.encoder(token_ids)
            text_encodings = last_layer
            text_encodings = self.task.project_encoder_op(text_encodings)

            mention_logits, mention_bounds = self.task.mention_encoder(
                text_encodings, text_pad_mask, tokens_mapping
            )

            (
                chosen_mention_logits,
                chosen_mention_bounds,
                chosen_mention_mask,
                mention_pos_mask,
            ) = self.task.mention_encoder.prune_ctxt_mentions(
                mention_logits,
                mention_bounds,
                num_cand_mentions=50,
                threshold=self.task.md_threshold,
            )

            mention_offsets = chosen_mention_bounds[:, :, 0]
            mention_lengths = (
                chosen_mention_bounds[:, :, 1] - chosen_mention_bounds[:, :, 0] + 1
            )
            mention_lengths[mention_offsets == 0] = 0

            mentions_repr = self.task.span_encoder(
                text_encodings, mention_offsets, mention_lengths
            )
            # flat mentions and entities indices (mentions_num x embedding_dim)
            flat_mentions_repr = mentions_repr[mention_lengths != 0]
            mentions_scores = torch.sigmoid(chosen_mention_logits)
            # retrieve candidates top-1 ids and scores
            cand_scores, cand_indices = self.lookup(flat_mentions_repr.detach())
            cand_scores = cand_scores.unsqueeze(-1)

        predictions = []
        cand_idx = 0
        example_idx = 0
        for offsets, lengths, md_scores in zip(
            mention_offsets, mention_lengths, mentions_scores
        ):
            ex_sp_offsets = []
            ex_sp_lengths = []
            ex_entities = []
            ex_md_scores = []
            for offset, length, md_score in zip(offsets, lengths, md_scores):
                if length != 0:
                    if md_score >= self.task.md_threshold:
                        ex_sp_offsets.append(offset.detach().cpu().item())
                        ex_sp_lengths.append(length.detach().cpu().item())
                        ex_entities.append(cand_indices[cand_idx])
                        ex_md_scores.append(md_score.item())
                    cand_idx += 1

            char_offsets, char_lengths = convert_sp_to_char_offsets(
                texts[example_idx],
                ex_sp_offsets,
                ex_sp_lengths,
                sp_tokens_boundaries[example_idx],
            )

            predictions.append(
                {
                    "offsets": char_offsets,
                    "lengths": char_lengths,
                    "entities": ex_entities,
                    "md_scores": ex_md_scores,
                }
            )
            example_idx += 1

        return predictions

    def apply_transformation_with_max_mention_pos(
        self,
        texts,
        mention_offsets,
        mention_lengths,
        entities,
        transform,
        max_mention_token_pos_in_text=192,
    ):
        """Apply transformations to a batch of texts with respect to maximum mention position.

        Args:
            self: The instance of the class.
            texts (list of str): A list of texts to be processed.
            mention_offsets (list of list of int): A list of mention offsets for each text.
            mention_lengths (list of list of int): A list of mention lengths for each text.
            entities (list of list of int): A list of entity identifiers corresponding to mentions.
            transform (callable): A transformation function to apply to the texts.
            max_mention_token_pos_in_text (int, optional): The maximum allowed token position
                for a mention within a text. Defaults to 192.

        Returns:
            dict: A dictionary containing the transformed texts, mention offsets,
                mention lengths, and entities.
        """
        old_max_seq_len = transform.max_seq_len
        transform.max_seq_len = (
            10000  # temporarily set to a large number to get the full token boundaries
        )

        transformed_texts = []
        transformed_mention_offsets = []
        transformed_mention_lengths = []
        transformed_entities = []

        for text, offsets, lengths, ents in zip(
            texts, mention_offsets, mention_lengths, entities
        ):
            new_mention_offsets = []
            new_mention_lengths = []
            new_entities = []

            outputs = transform(dict(texts=[text]))
            sp_token_boundaries = outputs["sp_tokens_boundaries"][0]

            offset = offsets[0]
            length = lengths[0]
            ent = ents[0]
            token_pos = 0
            while (
                token_pos < len(sp_token_boundaries)
                and offset >= sp_token_boundaries[token_pos][1]
            ):
                token_pos += 1

            new_text = text
            new_offset = offset
            if token_pos > max_mention_token_pos_in_text:
                shift = sp_token_boundaries[token_pos - max_mention_token_pos_in_text][
                    0
                ].item()
                new_text = text[shift:]
                new_offset = offset - shift

            assert (
                text[offset : offset + length]  # noqa
                == new_text[new_offset : new_offset + length]  # noqa
            )

            new_mention_offsets.append(new_offset)
            new_mention_lengths.append(length)
            new_entities.append(ent)

            transformed_texts.append(new_text)
            transformed_mention_offsets.append(new_mention_offsets)
            transformed_mention_lengths.append(new_mention_lengths)
            transformed_entities.append(new_entities)

        transform.max_seq_len = old_max_seq_len

        return {
            "texts": transformed_texts,
            "mention_offsets": transformed_mention_offsets,
            "mention_lengths": transformed_mention_lengths,
            "entities": transformed_entities,
        }

    def process_disambiguation_batch(
        self, texts, mention_offsets, mention_lengths, entities
    ):
        """Process a batch for entity disambiguation.

        Args:
            self: The instance of the class.
            texts (list): A list of strings representing the original texts.
            mention_offsets (list): A list of lists containing mention offsets for each text.
            mention_lengths (list): A list of lists containing mention lengths for each text.
            entities (list): A list of lists containing entity IDs for each mention.

        Returns:
            list: A list of dictionaries representing predictions for each text.
        """
        batch: Dict[str, Any] = {
            "texts": texts,
            "mention_offsets": mention_offsets,
            "mention_lengths": mention_lengths,
            "entities": entities,
        }

        logger.info(f"TEXTS length: {len(texts)}")

        logger.info(f"PRE transformation offsets: {mention_offsets}")

        # Apply transformation with max mention position logic
        transformed_batch = self.apply_transformation_with_max_mention_pos(
            texts=batch["texts"],
            mention_offsets=batch["mention_offsets"],
            mention_lengths=batch["mention_lengths"],
            entities=batch["entities"],
            transform=self.transform,
        )

        logger.info(f"transformed_btach: {transformed_batch}")

        model_inputs = self.transform(transformed_batch)

        logger.info(f"model_inputs: {model_inputs}")

        token_ids = model_inputs["input_ids"]

        if token_ids.shape[1] > self.max_length:
            token_ids = token_ids[:, : self.max_length]


        logger.info(
            f"Are the token IDs contiguous? {'Yes' if token_ids.is_contiguous() else 'No'}"
        )
        if torch.isnan(token_ids).any() or torch.isinf(token_ids).any():
            logger.error("Token IDs contain NaNs or Infs!")
        logger.info(f"Token IDs dtype: {token_ids.dtype}")
        logger.info(f"Token IDs shape: {token_ids.shape}")

        test_tensor = torch.randn(len(token_ids)).to(self.device)
        test_tensor.to(self.device)

        token_ids = token_ids.to(self.device)

        mention_offsets = model_inputs["mention_offsets"]
        mention_lengths = model_inputs["mention_lengths"]
        sp_tokens_boundaries = model_inputs["sp_tokens_boundaries"].tolist()

        logger.info("mention_offsets: {}".format(mention_offsets))
        logger.info("mention_offsets_shape: {}".format(mention_offsets.shape))

        with torch.no_grad():
            _, last_layer = self.task.encoder(token_ids)
            text_encodings = last_layer
            text_encodings = self.task.project_encoder_op(text_encodings)

            mentions_repr = self.task.span_encoder(
                text_encodings, mention_offsets, mention_lengths
            )

            flat_mentions_repr = mentions_repr[mention_lengths != 0]
            # retrieve candidates top-1 ids and scores
            cand_scores, cand_indices = self.lookup(flat_mentions_repr.detach())
            predictions = []
            cand_idx = 0
            example_idx = 0
            for offsets, lengths in zip(
                mention_offsets,
                mention_lengths,
            ):
                ex_sp_offsets = []
                ex_sp_lengths = []
                ex_entities = []
                ex_dis_scores = []
                for offset, length in zip(offsets, lengths):
                    if length != 0:
                        ex_sp_offsets.append(offset.detach().cpu().item())
                        ex_sp_lengths.append(length.detach().cpu().item())
                        ex_entities.append(cand_indices[cand_idx])
                        ex_dis_scores.append(
                            cand_scores[cand_idx].detach().cpu().item()
                        )
                        cand_idx += 1

                char_offsets, char_lengths = convert_sp_to_char_offsets(
                    texts[example_idx],
                    ex_sp_offsets,
                    ex_sp_lengths,
                    sp_tokens_boundaries[example_idx],
                )

                predictions.append(
                    {
                        "offsets": char_offsets,
                        "lengths": char_lengths,
                        "entities": ex_entities,
                        "scores": ex_dis_scores,
                    }
                )
                example_idx += 1

        return predictions

    def get_predictions(self, test_data, batch_size=256):
        """Get predictions for a dataset using batch processing.

        Args:
            self: The instance of the class.
            test_data (list): A list of dictionaries representing the test data.
            batch_size (int, optional): The size of each processing batch. Defaults to 256.

        Returns:
            list: A list of dictionaries representing disambiguation predictions for the test data.
        """
        all_predictions = []
        for batch_start in tqdm(range(0, len(test_data), batch_size)):
            batch = test_data[batch_start : batch_start + batch_size]  # noqa
            texts = [example["original_text"] for example in batch]
            predictions = self.process_batch(texts)
            all_predictions.extend(predictions)
        return all_predictions

    def get_disambiguation_predictions(self, test_data, batch_size=256):
        """Get disambiguation predictions for a dataset using batch processing.

        Args:
            self: The instance of the class.
            test_data (list): A list of dictionaries representing the test data.
            batch_size (int, optional): The size of each processing batch. Defaults to 256.

        Returns:
            list: A list of dictionaries representing disambiguation predictions for the test data.
        """
        all_predictions = []
        for batch_start in tqdm(range(0, len(test_data), batch_size)):
            batch = test_data[batch_start : batch_start + batch_size]  # noqa
            texts = [example["original_text"] for example in batch]
            mention_offsets = [
                [offset for _, _, _, _, offset, _ in example["gt_entities"]]
                for example in batch
            ]
            mention_lengths = [
                [length for _, _, _, _, _, length in example["gt_entities"]]
                for example in batch
            ]
            entities = [
                [0 for _, _, _, _, _, _ in example["gt_entities"]] for example in batch
            ]

            predictions = self.process_disambiguation_batch(
                texts, mention_offsets, mention_lengths, entities
            )
            all_predictions.extend(predictions)
        return all_predictions

    @staticmethod
    def compute_scores(data, predictions, md_threshold=0.2, el_threshold=0.05):
        """Compute evaluation scores based on predicted and ground truth entities.

        Args:
            data (list): A list of dictionaries representing data examples.
            predictions (list): A list of dictionaries representing predictions for each data example.
            md_threshold (float, optional): Threshold for matching score of predicted entities. Defaults to 0.2.
            el_threshold (float, optional): Threshold for linking score of predicted entities. Defaults to 0.05.
        """  # noqa
        tp, fp, support = 0, 0, 0
        tp_boe, fp_boe, support_boe = 0, 0, 0
        predictions_per_example = []
        for example, example_predictions in zip(data, predictions):

            example_targets = {
                (offset, length): ent_id
                for _, _, ent_id, _, offset, length in example["gt_entities"]
            }

            example_predictions = {
                (offset, length): ent_id
                for offset, length, ent_id, md_score in zip(
                    example_predictions["offsets"],
                    example_predictions["lengths"],
                    example_predictions["entities"],
                    example_predictions["md_scores"],
                )
                if (md_score > md_threshold)
            }

            predictions_per_example.append(
                (len(example_targets), len(example_predictions))
            )

            for pos, ent in example_targets.items():
                support += 1
                if pos in example_predictions and example_predictions[pos] == ent:
                    tp += 1
            for pos, ent in example_predictions.items():
                if pos not in example_targets or example_targets[pos] != ent:
                    fp += 1

            example_targets_set = set(example_targets.values())
            example_predictions_set = set(example_predictions.values())

            for ent in example_targets_set:
                support_boe += 1
                if ent in example_predictions_set:
                    tp_boe += 1
            for ent in example_predictions_set:
                if ent not in example_targets_set:
                    fp_boe += 1

        def safe_division(a, b):
            """Division with case for division by zero."""
            if b == 0:
                return 0
            else:
                return a / b

        def compute_f1_p_r(tp, fp, fn):
            """F1 scores computing."""
            precision = safe_division(tp, (tp + fp))
            recall = safe_division(tp, (tp + fn))
            f1 = safe_division(2 * tp, (2 * tp + fp + fn))
            return f1, precision, recall

        fn = support - tp
        fn_boe = support_boe - tp_boe
        return compute_f1_p_r(tp, fp, fn), compute_f1_p_r(tp_boe, fp_boe, fn_boe)
