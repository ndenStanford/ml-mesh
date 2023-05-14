import requests
from article import ARTICLE

url = 'http://0.0.0.0:5000'
headers = {'x-api-key': "1234"}

q = requests.get("{}/health".format(url))

values = {"content": ARTICLE}
q = requests.post("{}/v1/summarization/gpt3/predict".format(url), json=values)
q