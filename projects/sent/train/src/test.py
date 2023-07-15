# ML libs
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)


checkpoint = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
print("a")
model = AutoModelForSequenceClassification.from_pretrained(
    checkpoint, return_dict=False
)
print("b")
print(model)

hf_pipeline = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
)
