from django.test import TestCase

# Create your tests here.
from openai import OpenAI

client = OpenAI(api_key='API_KEY')

response = client.embeddings.create(
  model="gpt-4o-mini",
  input= "How to analyse images of flood events for modelling"
)

print(response)