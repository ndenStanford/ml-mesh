# `Entity Fishing`


## Overview

The entity-fishing backend powers our entity linking capabilities. It as a java based application that leverages a panel of algorithm to retrieve entities:

![Entity Linking](entity-fishing.png)


## Downloading knowledge bases

In order to run the entity-fishing backend, knowledge bases need to be available on the process system.


| Language      | Type                      | URL                                                                       |
| ------------- | ------------------------- | ------------------------------------------------------------------------- |
| English       | Generic Knowledge Base    | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-kb.zip     |
| English       | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-en.zip     |
| French        | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-fr.zip     |
| German        | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-de.zip     |
| Spanish       | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-es.zip     |
| Italian       | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-it.zip     |
| Arabic        | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-ar.zip     |
| Chinese       | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-zh.zip     |
| Russian       | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-ru.zip     |
| Japanese      | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-ja.zip     |
| Portuguese    | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-pt.zip     |
| Persian       | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-fa.zip     |
| Ukranian      | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-uk.zip     |
| Swedish       | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-sv.zip     |
| Bengali       | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-bn.zip     |
| Hindi         | Language specific KB      | https://science-miner.s3.amazonaws.com/entity-fishing/0.0.6/db-hi.zip     |


We don't have a written script to download the models. This app is not officially supported by the ml-team. In order to download the models run the following script
and read the instructions carefully:

```
bin/entity-fishing-download-kb
```

## Generating new knowledge bases

This is not currently supported.

## References

- [entity fishing documentation](https://nerd.readthedocs.io/en/latest/)
- [github](https://github.com/kermitt2/entity-fishing)
- [knowledge base](https://github.com/kermitt2/grisp)
