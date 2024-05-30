# Vector Similarity Search in Entity Linking

To implement Vector Similarity Search, refer to the [Redis example](https://redis-py.readthedocs.io/en/stable/examples/search_vector_similarity_examples.html).

Additional examples from OpenAI Cookbook:
- [Using Redis for Embeddings Search](https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/redis/Using_Redis_for_embeddings_search.ipynb)
- [Using Redis as a Vector Database with OpenAI](https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/redis/getting-started-with-redis-and-openai.ipynb)

## Querying vector store

### 1. Connect to Redis vector store

To start querying, connect to the Redis vector store with `REDIS_CONNECTION_STRING`.

```python
from src.settings import get_settings
from src.utils.client import get_client
from src.utils.index import get_index

settings = get_settings()

client = get_client(url=settings.REDIS_CONNECTION_STRING)
get_index(
    client=client,
    index_name=settings.INDEX_NAME,
    vector_dimensions=settings.EMBEDDINGS_SHAPE[1],
)
```

### 2. Construct the query

The script below sets up the query to perform kNN search with `k=3`. It finds the top N most similar vectors in the vector store given the query vector.
```python
from redis.commands.search.query import Query

query = (
    Query(f"*=>[KNN 3 @embedding $query_vector as score]")
    .sort_by("score")
    .return_fields("id", "score")
    .paging(0, 3)
    .dialect(2)
)
```

#### Random query vector

The query vector below is a random vector with the dimensions matching the vectors dimensions in the store.

```python
query_vector = (
    np.random.rand(settings.EMBEDDINGS_SHAPE[1]).astype(np.float32).tobytes()
)
```

#### Query vector from the existing embeddings index

To query the vector store by the wikidata id `query_index` (`QXXX`), download and load `index.txt` and `embeddings.pt` to memory, index the embeddings tensor with the `query index` and convert the embeddings vector to bytes.

```python
import numpy as np
from src.utils.embeddings import get_embeddings

wiki_embeddings, _ = get_embeddings(
    embeddings_file=settings.EMBEDDINGS_FILE, index_file=settings.INDEX_FILE
)
if query_index not in wiki_embeddings.index:
    raise ValueError(
        f"Query_index {query_index} is not in the embeddings index."
    )
query_vector = (
    wiki_embeddings.embeddings[wiki_embeddings.index.index(query_index)]
    .numpy()
    .astype(np.float32)
    .tobytes()
)
```

**When constructung the query vector from an encoded vector, make sure to convert its elements to float32 and then to bytes.**

### 3. Run the query search

```python
query_params = {"query_vector": query_vector}
client.ft(settings.INDEX_NAME).search(query, query_params).docs
```
### 4. Results

At the time of querying the vector store contained total of 8103248 keys.

Example of the ouput with the `query_index="Q99"` [California](https://en.wikipedia.org/wiki/California):

```
Document {'id': 'Q99', 'payload': None, 'score': '0'}
Document {'id': 'Q732125', 'payload': None, 'score': '0.295504391193'}
Document {'id': 'Q844837', 'payload': None, 'score': '0.29739177227'}
Document {'id': 'Q1066807', 'payload': None, 'score': '0.309080123901'}
Document {'id': 'Q6942029', 'payload': None, 'score': '0.311744213104'}
```

Example of the ouput with the `query_index="Q42"` [Douglas Adams](https://en.wikipedia.org/wiki/Douglas_Adams):

```
Document {'id': 'Q42', 'payload': None, 'score': '0'}
Document {'id': 'Q5211260', 'payload': None, 'score': '0.223291158676'}
Document {'id': 'Q354538', 'payload': None, 'score': '0.261555433273'}
Document {'id': 'Q28421831', 'payload': None, 'score': '0.262495398521'}
Document {'id': 'Q5302026', 'payload': None, 'score': '0.272435545921'}
```

[Wikidata website](https://www.wikidata.org/) allows to look up the wikidata entity by its Q-number id.
