from openai import AzureOpenAI
import os
import dotenv

# import dotenv
dotenv.load_dotenv()

# configure Azure OpenAI service client 
client = AzureOpenAI(
  azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"], 
  api_key=os.environ['AZURE_OPENAI_KEY'],  
  api_version = "2023-10-01-preview"
  )

deployment=os.environ['AZURE_OPENAI_DEPLOYMENT']

character = input("Enter the historical character you want to learn more about: ")

question = input(f"What do you like to know about {character} ? ")


# interpolate the number of recipes into the prompt an ingredients
prompt = f"Get more info about this historical character {character} specifically this information: {question}."
messages = [{"role": "user", "content": prompt}]

completion = client.chat.completions.create(model=deployment, messages=messages, max_tokens=600, temperature = 0.1)


# print response
print("Query")
print(prompt)
print("Answer")
print(completion.choices[0].message.content)