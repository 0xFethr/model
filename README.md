# 0xFethr AI Integration
The article recommender is based on the fasttext model by Facebook(Meta) to generate word embeddings, and based on the embedding of the headlines and their categories we recommend the users the appropiate articles based on their previolus readings and warden category preferences.
On addition of new articles we need to execute the data_maintainer file to update the dataset and reset the model with new embeddings.

The hatespeech detection API is based on BERT model and has api deployment with huggingface.
