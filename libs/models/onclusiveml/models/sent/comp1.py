    def _add_entity_sentiment(sentences, res, entities):
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
                    logger.info(f'can not find indexes for entity: {entity}')
                    entity['sentiment'] = "neutral"
                else:
                    pos = pos / i
                    neg = neg / i
                    neu = neu / i
                    entity['sentiment'] = "positive" if (pos > neg) and (pos > neu) else \
                        "neutral" if (neu > neg) and (neu > pos) else \
                            "negative" if (neg > pos) and (neg > neu) else \
                                "neutral"
                entity_sentiment.append(entity)
            except Exception as e:
                logger.error((f"invalid entity..."
                              f"entity = {entity}..."), exc_info=True)
                entity['sentiment'] = "neutral"
                entity_sentiment.append(entity)

        return (entity_sentiment)