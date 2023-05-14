import requests

#curl -X 'GET' 'http://0.0.0.0:4000/api/v1/prompts' -H 'accept: application/json' -H 'x-api-key: 1234'

url = 'http://0.0.0.0:4000'
headers = {'x-api-key': "1234"}

q = requests.get("{}/api/v1/prompts".format(url), headers = headers)

english_summarization_template = "{content} Summarize the article in 20 words"
english_summarization_alias = "english_summarization_prompt"

q = requests.post(f"{url}/api/v1/prompts?template={english_summarization_template}&alias={english_summarization_alias}", headers = headers)
q

#q = requests.post("{}/api/v1/prompts".format(url), json = {"template": english_summarization_template, "alias": "english_summarization_prompt"}, headers = headers)
q = requests.get("{}/api/v1/prompts".format(url), headers = headers)
q

prompt_id = "c454b675-91fd-4499-9c37-ff0a5487bf02"
values = {"content": ARTICLE}
q = requests.post(f"{url}/api/v1/prompts/{prompt_id}/generate", headers = headers, json=values)
q