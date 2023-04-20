import requests
import time

url = 'http://127.0.0.1:8000'
start_time = time.time()
content = "I love living in England. London is a wonderful city."
entities = [{"text": "England"}, {"text": "London"}]
q = requests.post("{}/entity-linking/fish".format(url), json = {"content": content, "entities": entities})
assert q.status_code == 200
print(q.content)
print("--- %s seconds ---" % (time.time() - start_time))
print(len(q.json()))
