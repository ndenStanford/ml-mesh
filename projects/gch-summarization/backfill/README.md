# GCH Summarization backfill

Implementation of the GCH Summarization model backfill container.

For details on how to run and maintain the `gch-summarization` project `backfill` component, please refer
to the
- [the project README](../README.md)
- [the project backfill doc](../../docs/05_backfill.md)

using

- `PROJECT_NAME=gch-summarization`, and
- `COMPONENT=backfill`


#### Sending Kafka events

When your service is running, you can experiment with the pipeline by sending a dummy message:

```python
from confluent_kafka import Producer
import json

p = Producer({"bootstrap.servers": "localhost:9094"})
p.produce("beam-input", key="identifier", value=json.dumps({"content": "A todos los estudiantes de primer año se les ofrece un lugar en el campus. Los funcionarios de salud de la universidad dijeron que el caso fue detectado el 13 de agosto. Se produce en medio de crecientes preocupaciones de que el regreso de las universidades pueda provocar un aumento en los casos de viruela simica, con un total de 14,115 en Estados Unidos. entre los hombres homosexuales o bisexuales en la actualidad, pero se teme que se propague a otros grupos más vulnerables. Un estudiante de la Universidad Penn State dio positivo por viruela simica, ya que los expertos temen que el próximo semestre de otoño provoque brotes del virus. Los funcionarios de salud de la universidad dijeron que el estudiante anónimo se encuentra ahora aislado y que se están rastreando sus contactos cercanos. El individuo asiste al campus de University Park en el centro de Pensilvania, el más grande de la universidad con unos 46.000 estudiantes universitarios, pero reside fuera del campus. El estudiante recibió el resultado positivo el 13 de agosto, aproximadamente una semana antes del inicio del semestre de otoño el 22 de agosto. Existe una creciente preocupación de que el regreso de los colegios y universidades pueda ayudar a impulsar el brote viral, y el último caso marca el segundo en un universidad este mes. El jueves, la Universidad de Maryland dijo que un miembro del personal tenía un presunto caso y que probablemente se detectarán más infecciones en las próximas semanas. Estados Unidos ha detectado más de 14.115 casos de viruela simica hasta ahora, la gran mayoría entre hombres homosexuales o bisexuales, aunque se teme que el virus, que se transmite a través del contacto físico, se propague a otros grupos. Un estudiante dio positivo por viruela simica en la Universidad Penn State. Asisten al campus de University Park (en la foto), el más grande de la universidad, pero no viven en el lugar. El mapa de arriba muestra el número de casos de viruela simica detectados por estado.", "language": "es"}))
```

and check if the enriched document is available in the target topic as follows:


```python
from confluent_kafka import Consumer
c = Consumer({'bootstrap.servers': 'localhost:9094','group.id': 'mygroup','auto.offset.reset': 'earliest'})
c.subscribe(['beam-output'])
c.poll().value().decode('utf-8')
```
