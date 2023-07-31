import os
import openai
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()

api_key = os.getenv('OPENAI_KEY')
openai.api_key = api_key

#returns a list of all OpenAI models
modelsFromOpenAI = openai.Model.list()
print(modelsFromOpenAI)

# converts the list of OpenAI models to a Pandas DataFrame
data = pd.DataFrame(models["data"])
data.head(20)