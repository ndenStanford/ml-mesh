# Topic backfill

Implementation of the topic model backfill container.

For details on how to run and maintain the `topic` project `backfill` component, please refer
to the
- [the project README](../README.md)
- [the project backfill doc](../../docs/05_backfill.md)

using

- `PROJECT_NAME=topic`, and
- `COMPONENT=backfill`

#### Sending Kafka events

When your service is running, you can experiment with the pipeline by sending a dummy message:

```python
from confluent_kafka import Producer
import json

p = Producer({"bootstrap.servers": "localhost:9094"})
p.produce(
    "beam-input",
    key="identifier",
    value=json.dumps(
        {
            "content": "Ten-year US yields approached 4.5%. The S&P 500 fluctuated, with the benchmark headed toward its fourth straight week of gains. Stocks will finish trading at 1 p.m. New York time in observance of Thanksgiving, and the recommended close for the Treasury cash"
        }
    ),
)
p.flush()
```

and check if the enriched document is available in the target topic as follows:


```python
from confluent_kafka import Consumer
c = Consumer({'bootstrap.servers': 'localhost:9094','group.id': 'mygroup','auto.offset.reset': 'earliest'})
c.subscribe(['beam-output'])
c.poll().value().decode('utf-8')
```
