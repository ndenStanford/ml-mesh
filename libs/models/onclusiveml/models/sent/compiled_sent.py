from abc import ABC
import json
import logging
import os
import pickle
import requests
import string
import datetime

import numpy as np
import torch

import regex
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple, Union

from ts.torch_handler.base_handler import BaseHandler

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.nlp.sentence_tokenize import SentenceTokenizer

#from transformers import AutoTokenizer, AutoModelForSequenceClassification

os.environ['NEURONCORE_GROUP_SIZES'] = '1'
os.environ['NEURON_MAX_NUM_INFERS'] = '-1'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import torch.neuron
except:
    logger.warn("COULD NOT IMPORT NEURON. HOPEFULLY YOU ARE RUNNING TESTS")

#sentence_tokenizer_endpoint = "https://eks-data-prod.onclusive.com/sentence_tokenize"
sentence_tokenizer_endpoint = 'http://sent-tokenize:80/sentence_tokenize'

class CompiledSent(BaseHandler, ABC):
    """Class for performing sentiment analysis using neuron compiled Sent pipeline"""
    
    def __init__(
        self,
        compiled_sent_pipeline: CompiledPipeline,
    ):
        """
        Initalize the CompiledSent object.
        Args:
            compiled_sent_pipeline (CompiledPipeline): The compiled Sent pipline used for inference
        """
        self.compiled_sent_pipeline = compiled_sent_pipeline
        self.unicode_strp = regex.compile(r'\p{P}')
        self.NUM_LABELS = 3
        self.MAX_SEQ_LENGTH = 128
        self.MAX_BATCH_SIZE = 6
        self.device: str = "cpu"

    # def initialize(self, ctx):
    #     self.manifest = ctx.manifest

    #     properties = ctx.system_properties
    #     model_dir = properties.get("model_dir")

    #     self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

    #     self.unicode_strp = regex.compile(r'\p{P}')
    #     #print("Envs at infer time = {} {}".format(curr_ng_sizes,curr_ninfer))
        
    #     # Read model serialize/pt file
    #     self.model = torch.jit.load(model_dir + "/sent_neuron_v2.pt")
    #     self.tokenizer = pickle.load(open(model_dir + "/tokenizer_v2.vocab", "rb"))
        
    #     #self.arr_err = pickle.load(open(model_dir + "/sent_err_arr.pkl", 'rb'))

    #     self.model.to(self.device)
    #     self.model.eval()

    #     self.initialized = True
    #     self.NUM_LABELS = 3
    #     self.MAX_SEQ_LENGTH = 128
    #     self.MAX_BATCH_SIZE = 6

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        """
        Save compiled Sent pipeline to specified directory
        Args:
            Directory (Union[Path, str]): Directory to save the compiled Sent pipeline
        """
        self.compiled_sent_pipeline.save_pretrained(
            os.path.join(directory, "compiled_sent_pipeline")
        )

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledSent":
        """
        Load compiledSent object from specfied directory
        Args:
            directory (Union[Path, str]): The directory path contained the pretrained compiled
                sent pipeline
        Returns:
            CompiledSent: The loaded pre-trained CompiledSent object
        """
        compiled_sent_pipeline = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_sent_pipeline")
        )

        return cls(
            compiled_sent_pipeline=compiled_sent_pipeline,
        )

    
    def pad_sequence(self, seq, value):
        """
        Add dead characters so all sequences are the same length
        Args:
            seq (list): Input list
            value (str): Padded value
        Returns:
            seq (list): Ourpur list with padded value
        """
        seq = seq[0:self.MAX_LEN]
        seq = seq + [value] * (self.MAX_LEN - len(seq))
        return(seq)

    # Handles preprocessing of sentences into, tokens, masks, and tags if labels are avaiable
    # -- This function is written to try to minimize errors caused by different tokenizaiton during training or testing
    #    However, it ends up doing basically two different things depending on which one, so any changes to it should be 
    #    checked in both contexts (and copied to both contexts) to avoid regression. I suspect patrick will tell me a better
    #    way of handling this
    def _preprocess(self, sentences):
        
        tags = None
        
        tokenized_texts = [self.tokenizer.tokenize(sentence) for sentence in sentences]
        input_ids = [self.pad_sequence(self.tokenizer.convert_tokens_to_ids(txt), 0) for txt in tokenized_texts]
        attention_masks = [[float(i>0) for i in ii] for ii in input_ids]
        return(input_ids, attention_masks, tags, tokenized_texts)


    # ###MODEL INTERPRETATION HELPERS
    # #convenience functions for extracting entities as a list of dicts
    # def get_label_name(self, label_val):
    #     label_str = {
    #         0: 'negative',
    #         1: 'neutral',
    #         2: 'positive'
    #     }
    #     return label_str.get(label_val, "Invalid label value")

    # def _add_entity_sentiment(sentences, res, entities):
    #     sentence_pos_probs = res['sentence_pos_probs']
    #     sentence_neg_probs = res['sentence_neg_probs']
    #     sentence_neu_probs = [1 - pos - neg for pos, neg
    #                           in zip(sentence_pos_probs, sentence_neg_probs)]

    #     entity_sentiment = []
    #     for entity in entities:
    #         try:
    #             entity_text = entity.get('text')
    #             indexes = [i for i, sentence in enumerate(sentences) if (sentence.find(entity_text) != -1)]

    #             i = 0
    #             pos = 0
    #             neg = 0
    #             neu = 0
    #             for index in indexes:
    #                 pos += sentence_pos_probs[index]
    #                 neg += sentence_neg_probs[index]
    #                 neu += sentence_neu_probs[index]
    #                 i += 1

    #             if i == 0:
    #                 logger.info(f'can not find indexes for entity: {entity}')
    #                 entity['sentiment'] = "neutral"
    #             else:
    #                 pos = pos / i
    #                 neg = neg / i
    #                 neu = neu / i
    #                 entity['sentiment'] = "positive" if (pos > neg) and (pos > neu) else \
    #                     "neutral" if (neu > neg) and (neu > pos) else \
    #                         "negative" if (neg > pos) and (neg > neu) else \
    #                             "neutral"
    #             entity_sentiment.append(entity)
    #         except Exception as e:
    #             logger.error((f"invalid entity..."
    #                           f"entity = {entity}..."), exc_info=True)
    #             entity['sentiment'] = "neutral"
    #             entity_sentiment.append(entity)

    #     return (entity_sentiment)


    #Make text into ids, also handles sentence splitting
    def preprocess(self, sentences):
        
        sentences = [self.unicode_strp.sub('', sentence) for sentence in sentences]
        sentences = [sentence.translate(str.maketrans('', '', string.punctuation)) for sentence in sentences]

        input_ids, attention_masks, _, tokenized_texts = self._preprocess(sentences)

        input_ids = np.array(input_ids, dtype=np.int64).tolist()
        attention_masks = np.array(attention_masks, dtype=np.float32).tolist()

        inputs = (input_ids, attention_masks)

        return inputs

    #Put Preprocessed IDs into the model
    def inference(self, inputs):
        
        probs = []

        input_ids, attention_masks = inputs
        n_sentence = len(input_ids)
        
        while len(input_ids) > 0:
            it_input_ids = torch.tensor(input_ids[:self.MAX_BATCH_SIZE])
            it_attention_masks = torch.tensor(attention_masks[:self.MAX_BATCH_SIZE])
            
            diff_size = self.MAX_BATCH_SIZE - it_input_ids.size()[0]
            
            if diff_size > 0:
                it_input_ids = torch.cat((it_input_ids, torch.tensor(np.zeros([diff_size, 128]), 
                                                                     dtype = torch.int64)), 0)
                it_attention_masks = torch.cat((it_attention_masks, torch.tensor(np.zeros([diff_size, 128]), 
                                                                                dtype = torch.float32)), 0)
            res = self.model(*(it_input_ids, it_attention_masks))[0]
            
            if diff_size > 0:
                res = res[:(self.MAX_BATCH_SIZE - diff_size)]

            try:
                probs += res.tolist()
            #except KeyError:
            #    probs += np.array([])
            #    logger.info('Content = {}'.format(item.content))
            except Exception as e:
                raise e

            input_ids = input_ids[self.MAX_BATCH_SIZE:]
            attention_masks = attention_masks[self.MAX_BATCH_SIZE:]

        probs = np.array(probs)

        assert(probs.shape[0] == n_sentence)
        return(probs)

    #Process probs into list of entities
    def postprocess(self, probs, sentences):

        logits = np.exp(probs.reshape(-1, self.NUM_LABELS))

        probs = np.around(logits / np.sum(logits, axis=1).reshape(-1, 1), 4)

        agg_probs = np.around(np.mean(probs, axis=0), 4)

        datum = {}
        datum['label'] = self._decide_label(agg_probs[2], agg_probs[1], agg_probs[0])#agg_probs:neg,neu,pos
        datum['sentence_pos_probs'] = probs[:, 2].tolist()
        datum['sentence_neg_probs'] = probs[:, 0].tolist()
        datum['negative_prob'] = agg_probs[0]
        datum['positive_prob'] = agg_probs[2]

        return(datum)

    def _add_entity_sentiment(self, sentences, res, entities):
        """
        Augment the entity with the corresponding sentiment

        Args:
            sentences (List[str]): List of sentences from the article
            res (List[dict]): List of sentiment probability corresponding to sentences
            entities (List[dict]): List of detected entities from the NER model

        Returns:
            entity_sentiment (List[dict]): List of detected entities with sentiment attached to them
        """
        sentence_pos_probs = res['sentence_pos_probs']
        sentence_neg_probs = res['sentence_neg_probs']
        sentence_neu_probs = [1 - pos - neg for pos, neg
                              in zip(sentence_pos_probs, sentence_neg_probs)]

        entity_sentiment = []
        for entity in entities:
            try:
                entity_text = entity.get('text')
                indexes = entity.get('sentence_indexes', None)
                if indexes is None:
                    indexes = [i for i, sentence in enumerate(sentences) if (sentence.find(entity_text) != -1)]

                i = 0
                pos = 0
                neg = 0
                neu = 0
                for index in indexes:
                    pos += sentence_pos_probs[index]
                    neg += sentence_neg_probs[index]
                    neu += sentence_neu_probs[index]
                    i += 1

                if i == 0:
                    logger.error('Error, no indexes provided for entity: {}'.format(entity_text.encode('utf8')))
                    entity['sentiment'] = "neutral"
                else:
                    pos = pos / i
                    neg = neg / i
                    neu = neu / i
                    entity['sentiment'] = self._decide_label(pos, neu, neg)
                entity_sentiment.append(entity)
            except Exception as e:
                logger.error(("invalid entity... entity = {}...".format(entity_text.encode('utf8'))), exc_info=True)
                entity['sentiment'] = "neutral"
                entity_sentiment.append(entity)

        return (entity_sentiment)

    def _decide_label(self, pos, neu, neg):
        """
        Helper function to decide final sentiment. The threshold has been calibrated to align with the customer expectation

        Args:
            pos (float): Probability of positive sentiment
            neu (float): Probability of neutral sentiment
            neg (float): Probability of negative sentiment

        Returns:
            val (str): Final sentiment label
        """
        neg=neg-0.2*pos
        pos=pos*1.7
        if pos>1 or neg<0:
            pos=1
            neg=0
        neu=1-pos-neg
        val = "positive" if (pos > neg) and (pos > neu) else \
                "neutral" if (neu > neg) and (neu > pos) else \
                    "negative" if (neg > pos) and (neg > neu) else \
                        "neutral"
        return(val)

    # def initialize_test(self):

    #     self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

    #     self.unicode_strp = regex.compile(r'\p{P}')

    #     self.model = torch.jit.load("model_dir/sent_neuron_v2.pt")
    #     self.tokenizer = pickle.load(open("neuron/tokenizer_v2.vocab", "rb"))

    #     #self.arr_err = pickle.load(open("./neuron/sent_err_arr.pkl", 'rb'))

    #     self.model.to(self.device)
    #     self.model.eval()

    #     self.initialized = True
    #     self.NUM_LABELS = 3
    #     self.MAX_SEQ_LENGTH = 128
    #     self.MAX_BATCH_SIZE = 6


_service = TransformersSequenceClassificationHandler()
#_service.initialize_test()

def handle(data, context, testing = False):

    try:
        if not _service.initialized:
            if testing:
                _service.initialize_test()
            else: 
                _service.initialize(context)

        if data is None:
            return None

        if 'body' not in data[0]:
            logger.error("Malformed request, payload does not contain a body key. \
                          Is your request properly formatted as json?")
            return None
    
        data = data[0]['body']

        if type(data) == bytearray:
            data = eval(data)

        content = data.get('content', None)
        detail_flag = data.get('detail', False)

        if content is None:
            logger.error("Malformed request, content is not present in the payload. \
                            Check your payload names.")
            return None

        try:
            splits = requests.post(sentence_tokenizer_endpoint, json={"content": content})
            splits.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return respond(str(e), e.response.status_code)
        
        sentences = splits.json()['sentences']
        sentences = [sentence for sentence in sentences if len(sentence) > 5] #very short sentences are likely somehow wrong 
                                                                              #(that is 5 characters, not 5 words)

        if len(sentences) == 0:
            return [json.dumps({"label": "neutral", "positive_prob": .25, "negative_prob": .25,
                    "sentence_pos_probs": [], "sentence_neg_probs": []})]
        tokens = _service.preprocess(sentences)

        starttime = datetime.datetime.utcnow()
        probs = _service.inference(tokens)
        endtime = datetime.datetime.utcnow()
        logger.info('Total Time in milliseconds = {}'.format((endtime - starttime).total_seconds()*1000))
        logger.info('Average Time per sentence = {}'.format((endtime - starttime).total_seconds()*1000/len(sentences)))

        #if np.all(probs[0] == _service.arr_err):
        #	logger.error("Prediction appears to be from CPU, returning none.")
        #	return None

        datum = _service.postprocess(probs, sentences)

        if 'entities' in data:
            datum['entities'] = _service._add_entity_sentiment(sentences, datum, data['entities'])

        if detail_flag:
            datum['sentences'] = sentences
            return [json.dumps(datum)]

        else:
            datum.pop('sentence_pos_probs')
            datum.pop('sentence_neg_probs')
            return [json.dumps(datum)]
    except Exception as e:
        raise e