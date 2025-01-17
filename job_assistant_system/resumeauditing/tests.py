from django.test import TestCase

# Create your tests here.
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "what is the capital of nepal?"}
  ],
  max_tokens=50
)

content = completion.choices[0].message.content
print(content)