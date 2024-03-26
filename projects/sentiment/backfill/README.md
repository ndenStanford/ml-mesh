# Sentiment backfill

Implementation of the Sentiment model backfill container.

For details on how to run and maintain the `sentiment` project `backfill` component, please refer
to the
- [the project README](../README.md)
- [the project backfill doc](../../docs/05_backfill.md)

using

- `PROJECT_NAME=sentiment`, and
- `COMPONENT=backfill`

#### Sending Kafka events

When your service is running, you can experiment with the pipeline by sending a dummy message:

```python
from confluent_kafka import Producer
import json

p = Producer({"bootstrap.servers": "localhost:9094"})
p.produce(
    topic="beam-input",
    key="identifier",
    value=json.dumps(
        {
            "content": "London is a nice city.",
            "entities": [
                {"entity_text": "London", "entity_type": "LOC", "score": 0.9997141, "sentence_index": 0},
            ],
            "language": "en"
        }
    )
)
p.flush()
```



```python
from confluent_kafka import Consumer
c = Consumer({'bootstrap.servers': 'localhost:9094','group.id': 'mygroup','auto.offset.reset': 'earliest'})
c.subscribe(['beam-output'])
c.poll().value().decode('utf-8')
```
