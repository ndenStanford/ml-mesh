# Standard Library
import os
from pathlib import Path
from typing import List, Union

# Internal libraries
from onclusiveml.compile import CompiledPipeline


class CompiledNER:
    def __init__(
        self,
        compiled_ner_pipeline: CompiledPipeline,
    ):
        self.compiled_ner_pipeline = compiled_ner_pipeline
        self.id2label = {
            0: "O",
            1: "B-MISC",
            2: "I-MISC",
            3: "B-PER",
            4: "I-PER",
            5: "B-ORG",
            6: "I-ORG",
            7: "B-LOC",
            8: "I-LOC",
        }

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        # export compiled ner pipeline
        self.compiled_ner_pipeline.save_pretrained(
            os.path.join(directory, "compiled_ner_pipeline")
        )

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledNER":
        compiled_ner_pipeline = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_ner_pipeline")
        )

        return cls(
            compiled_ner_pipeline=compiled_ner_pipeline,
        )

    # dummy function while compile module in development
    def extract_entities(
        self, sentences: Union[List[str], str], return_pos: bool
    ) -> str:
        return "hello"
