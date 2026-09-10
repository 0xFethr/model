import requests
import sys
import json

if __name__ == "__main__":
	headline = sys.argv[1].strip()
	content = sys.argv[2].strip()
	article = headline + '\n' + content
	API_TOKEN = "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"
	API_URL = "https://api-inference.huggingface.co/models/Hate-speech-CNERG/dehatebert-mono-english"
	headers = {"Authorization": f"Bearer {API_TOKEN}"}

	def query(payload):
		response = requests.post(API_URL, headers=headers, json=payload)
		return response.json()
		
	output = query({
		"inputs": article,
	})
	res = "NA"
	try:
		if(output[0][0]['score'] > output[0][1]['score']):
			res = output[0][0]['label']
		else:
			res = output[0][1]['label']
	except:
		res = "NA"

	print(res,end="")