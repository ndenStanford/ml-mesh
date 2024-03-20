"""Define the Dataset class for preprocessing custom IPTC data."""

# ML libs
import torch

# Source
from src.class_dict import CLASS_DICT_FIRST, CLASS_DICT_SECOND, CLASS_DICT_THIRD


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
    """

    def __init__(  # type: ignore[no-untyped-def]
        self,
        df,
        tokenizer,
        level,
        selected_text,
        first_level_root,
        second_level_root,
        max_length,
    ):
        self.df = df
        self.level = level
        self.selected_text = selected_text
        self.first_level_root = first_level_root
        self.second_level_root = second_level_root
        self.tokenizer = tokenizer
        self.max_length = max_length

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
        if self.level == 1:
            return list(CLASS_DICT_FIRST["root"].values()).index(
                self.df.iloc[idx]["topic_1"]
            )
        elif self.level == 2:
            return list(CLASS_DICT_SECOND[self.first_level_root].values()).index(
                self.df.iloc[idx]["topic_2"]
            )
        elif self.level == 3:
            return int(
                list(
                    CLASS_DICT_THIRD[self.first_level_root][
                        self.second_level_root
                    ].values()
                ).index(self.df.iloc[idx]["topic_3"])
            )
        else:
            raise ("undefined level")  # type: ignore[misc]

    def __getitem__(self, idx):  # type: ignore[no-untyped-def]
        text = self.df.iloc[idx][self.selected_text]
        inputs = self.tokenizer(
            text=text, padding="max_length", max_length=self.max_length, truncation=True
        )
        labels = self.get_label(idx)
        inputs["labels"] = labels
        return inputs
