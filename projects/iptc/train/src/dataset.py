"""IPTC Dataset."""

# ML libs
import torch

# Internal libraries
from onclusiveml.feature_store.on_demand.iptc.class_dict import (
    CANDIDATE_DICT_FIRST,
    CANDIDATE_DICT_FOURTH,
    CANDIDATE_DICT_SECOND,
    CANDIDATE_DICT_THIRD,
)


# Dataset class
class IPTCDataset(torch.utils.data.Dataset):  # type: ignore[no-untyped-def]
    """Custom Dataset class for IPTC data.

    Attributes:
        df (DataFrame): The dataset containing the textual content and labels.
        tokenizer (Tokenizer): The tokenizer used for converting text to tokens.
        level (int): The classification level (1, 2, or 3) indicating the depth of the topic.
        selected_text (str): The column name from the DataFrame to use as text input.
        first_level_root (str, optional): The root topic for level 2 classification.
        second_level_root (str, optional): The root topic for level 3 classification.
        is_on_demand (bool): Whether the dataset is on-demand or not.
    """

    def __init__(  # type: ignore[no-untyped-def]
        self,
        df,
        tokenizer,
        level,
        selected_text,
        first_level_root=None,
        second_level_root=None,
        third_level_root=None,
        max_length=128,
        is_on_demand=False,  # New parameter to handle on-demand dataset
    ):
        self.df = df
        self.level = level
        self.selected_text = selected_text
        self.first_level_root = first_level_root
        self.second_level_root = second_level_root
        self.third_level_root = third_level_root
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.is_on_demand = is_on_demand  # Initialize is_on_demand

    def __len__(self):  # type: ignore[no-untyped-def]
        return len(self.df)

    def get_label(self, idx):  # type: ignore[no-untyped-def]
        """Get the label index for a data point based on classification level.

        Args:
            idx (int): The index of the data point in the DataFrame.

        Returns:
            int: The label index corresponding to the classification level and topic hierarchy.

        Raises:
            Exception: If the classification level is undefined.
        """

        def get_index_from_dict(candidate_dict, label):
            """Helper function to get the index of a label from a nested dictionary's 'name' field."""
            return list(
                candidate["name"] for candidate in candidate_dict.values()
            ).index(label)

        if self.is_on_demand:  # If on-demand, use the LLM labels
            if self.level == 1:
                return get_index_from_dict(
                    CANDIDATE_DICT_FIRST["root"], self.df.iloc[idx]["topic_1_llm"]
                )
            elif self.level == 2:
                return get_index_from_dict(
                    CANDIDATE_DICT_SECOND[self.first_level_root],
                    self.df.iloc[idx]["topic_2_llm"],
                )
            elif self.level == 3:
                return get_index_from_dict(
                    CANDIDATE_DICT_THIRD[self.second_level_root],
                    self.df.iloc[idx]["topic_3_llm"],
                )
            elif self.level == 4:
                return get_index_from_dict(
                    CANDIDATE_DICT_FOURTH[self.third_level_root],
                    self.df.iloc[idx]["topic_4_llm"],
                )
            else:
                raise ValueError("undefined level")
        else:  # If not on-demand, use the original labels
            if self.level == 1:
                return get_index_from_dict(
                    CANDIDATE_DICT_FIRST["root"], self.df.iloc[idx]["topic_1"]
                )
            elif self.level == 2:
                return get_index_from_dict(
                    CANDIDATE_DICT_SECOND[self.first_level_root],
                    self.df.iloc[idx]["topic_2"],
                )
            elif self.level == 3:
                return get_index_from_dict(
                    CANDIDATE_DICT_THIRD[self.second_level_root],
                    self.df.iloc[idx]["topic_3"],
                )
            elif self.level == 4:
                return get_index_from_dict(
                    CANDIDATE_DICT_FOURTH[self.third_level_root],
                    self.df.iloc[idx]["topic_4"],
                )
            else:
                raise ValueError("undefined level")

    def __getitem__(self, idx):  # type: ignore[no-untyped-def]
        text = self.df.iloc[idx][self.selected_text]
        inputs = self.tokenizer(
            text=text, padding="max_length", max_length=self.max_length, truncation=True
        )
        labels = self.get_label(idx)
        inputs["labels"] = labels
        return inputs
