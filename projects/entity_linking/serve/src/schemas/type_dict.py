from typing_extensions import TypedDict

EntityDictInput = TypedDict('EntityDictInput', {'entity_type': str, 'entity_text': str, 'score': str, 'sentence_index': 1})
 

entity_dict_input_test: EntityDictInput = {
      "entity_type": "PER",
      "entity_text": "Tim Cook",
      "score": "0.99980134",
      "sentence_index": 1
    }