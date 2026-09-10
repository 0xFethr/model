import requests

API_TOKEN = ""
API_URL = "https://api-inference.huggingface.co/models/Hate-speech-CNERG/dehatebert-mono-english"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "lets kill them",
})

res = ""
if(output[0][0]['score'] > output[0][1]['score']):
    res = output[0][0]['label']
else:
    res = output[0][1]['label']

print(res)
