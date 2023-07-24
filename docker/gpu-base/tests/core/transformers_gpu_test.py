# ML libs
import torch
from transformers import BertModel, BertTokenizer


def test_bert_gpu():
    device = torch.cuda.current_device()
    transformer_device = f"cuda:{device}"

    sentence = "Hello World!"
    tokenizer = BertTokenizer.from_pretrained("prajjwal1/bert-tiny")
    model = BertModel.from_pretrained("prajjwal1/bert-tiny")

    inputs = tokenizer(sentence, return_tensors="pt").to(transformer_device)
    model = model.to(transformer_device)
    model(**inputs)
