    def _add_entity_sentiment(self, sentences, res, entities):
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