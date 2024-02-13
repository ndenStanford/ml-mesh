# NER backfill

Implementation of the NER model backfill container.

For details on how to run and maintain the `ner` project `backfill` component, please refer
to the
- [the project README](../README.md)
- [the project backfill doc](../../docs/05_backfill.md)

using

- `PROJECT_NAME=ner`, and
- `COMPONENT=backfill`


#### Sending Kafka events

When your service is running, you can experiment with the pipeline by sending a dummy message:

```python
from confluent_kafka import Producer
import json

p = Producer({"bootstrap.servers": "localhost:9094"})
p.produce("beam-input", key="identifier", value=json.dumps({"content": "Google is a tech company", "language": "en"}))
```

and check if the enriched document is available in the target topic as follows:


```python
from confluent_kafka import Consumer
c = Consumer({'bootstrap.servers': 'localhost:9094','group.id': 'mygroup','auto.offset.reset': 'earliest'})
c.subscribe(['beam-output'])
c.poll().value().decode('utf-8')
```
