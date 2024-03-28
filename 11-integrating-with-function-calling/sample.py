import os
import requests
import json
import logging
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

load_dotenv()

# Set up logging
#logging.basicConfig(level=logging.INFO)

# Initialize Azure OpenAI client
client = AzureOpenAI(
  api_key=os.environ['AZURE_OPENAI_KEY'],  # this is also the default, it can be omitted
  api_version = "2023-07-01-preview"
  )
deployment=os.environ['AZURE_OPENAI_DEPLOYMENT']

# Initialize Cosmos Client
url = os.getenv('COSMOS_DB_ENDPOINT')
key = os.getenv('COSMOS_DB_KEY')
cosmosClient = CosmosClient(url, key)
# Select database
database_name = 'students'
database = cosmosClient.get_database_client(database_name)
# Select container
container_name = 'students'
container = database.get_container_client(container_name)

# Get user input
user_input = input("What do you like to find?\n")

# Define the messages and functions
messages= [ {"role": "user", "content": f"{user_input}"} ]
functions = [
   {
      "name":"search_courses",
      "description":"Retrieves courses from the search index based on the parameters provided",
      "parameters":{
         "type":"object",
         "properties":{
            "role":{
               "type":"string",
               "description":"The role of the learner (administrator, ai-edge-engineer, ai-engineer, auditor, business-analyst, business-owner, business-user, data-analyst, data-engineer, data-scientist, database-administrator, developer, devops-engineer, functional-consultant, higher-ed-educator, identity-access-admin, ip-admin, k-12-educator, maker, network-engineer, parent-guardian, privacy-manager, risk-practitioner, school-leader, security-engineer, security-operations-analyst, service-adoption-specialist, solution-architect, startup-founder, student, support-engineer, technical-writer, technology-manager)."
            },
            "product":{
               "type":"string",
               "description":"The product that the lesson is covering (dotnet, azure, bing, clarity, consumer, dynamics-365, entra, fabric, flip, github, hololens, industry-solutions, internet-explorer, intune, m365, microsoft-authentication-library, microsoft-edge, mem, ms-graph, makecode, power-platform, priva, office-teams, viva, microsoft-defender, microsoft-purview, minecraft, mrtk, ms-copilot, ms-website, nuance, office-365, bonsai, qdk, sql-server, sysinternals, vs, vs-app-center, vs-code, windows, xbox)."
            },
            "level":{
               "type":"string",
               "description":"The level of experience the learner has prior to taking the course (i.e. beginner, intermediate, advanced)"
            }
         },
         "required":[
            "role"
         ]
      }
   },
   {
      "name":"search_exams",
      "description":"Retrieves exams from the search index based on the parameters provided",
      "parameters":{
         "type":"object",
         "properties":{
            "role":{
               "type":"string",
               "description":"The role of the examiner (administrator, ai-edge-engineer, ai-engineer, auditor, business-analyst, business-owner, business-user, data-analyst, data-engineer, data-scientist, database-administrator, developer, devops-engineer, functional-consultant, higher-ed-educator, identity-access-admin, ip-admin, k-12-educator, maker, network-engineer, parent-guardian, privacy-manager, risk-practitioner, school-leader, security-engineer, security-operations-analyst, service-adoption-specialist, solution-architect, startup-founder, student, support-engineer, technical-writer, technology-manager)"
            },
            "product":{
               "type":"string",
               "description":"The product that the lesson is covering (dotnet, azure, bing, clarity, consumer, dynamics-365, entra, fabric, flip, github, hololens, industry-solutions, internet-explorer, intune, m365, microsoft-authentication-library, microsoft-edge, mem, ms-graph, makecode, power-platform, priva, office-teams, viva, microsoft-defender, microsoft-purview, minecraft, mrtk, ms-copilot, ms-website, nuance, office-365, bonsai, qdk, sql-server, sysinternals, vs, vs-app-center, vs-code, windows, xbox)"
            }
         },
         "required":[
            "role"
         ]
      }
   },
   {
      "name":"search_student",
      "description":"Retrieves student based on the parameters provided",
      "parameters":{
         "type":"object",
         "properties":{
            "name":{
               "type":"string",
               "description":"The name of the student"},
            }
         },
         "required":[
             "name"
         ]
   }
]

# Call the API, Determine the function to call
response = client.chat.completions.create(model=deployment, 
                                        messages=messages,
                                        functions=functions, 
                                        function_call="auto") 
response_message = response.choices[0].message

#logging.info(response_message)

# search_courses("developer", "azure", "beginner")
def search_courses(role='student', product='azure', level='beginner'):
    url = "https://learn.microsoft.com/api/catalog/"
    params = {
        "role": role,
        "product": product,
        "level": level
    }
    response = requests.get(url, params=params)
    modules = response.json()["modules"]
    results = []

    # Convert the role and product to lowercase and replace spaces with hyphens
    role = role.replace(' ', '-').lower()
    product = product.replace(' ', '-').lower()

    # Loop through the modules and get the first 5
    for module in modules[:5]:
        title = module["title"]
        url = module["url"]
        if any(product in p for p in module["products"]) or any(role in r for r in module["roles"]):
            results.append({"title": title, "url": url})
    return str(results)

# search_exams("developer", "azure")
def search_exams(role='student', product='azure'):
    url = "https://learn.microsoft.com/api/catalog/"
    params = {
        "type": "exams"
    }

    # get response from the API then get the exams
    response = requests.get(url, params=params)
    exams = response.json()["exams"]
    
    # Convert the role and product to lowercase and replace spaces with hyphens
    role = role.replace(' ', '-').lower()
    product = product.replace(' ', '-').lower()
    
    results = []
    # Loop through the exams and get the first 5
    for exam in exams[:5]:
        title = exam["title"]
        url = exam["url"]
        # Check if the role or product is in the exams
        if any(product in p for p in exam["products"]) or any(role in r for r in exam["roles"]):
            results.append({"title": title, "url": url})
    return str(results)

# search_student("John Doe")
def search_student(name):
    name=name.lower()
    query = f"SELECT * FROM c WHERE LOWER(c.name) = '{name}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return json.dumps(items)


# Check if the model wants to call a function
if response_message.function_call.name:
    #logging.info("Recommended Function call:")
    #logging.info(response_message.function_call.name)
    

    # Call the function. 
    function_name = response_message.function_call.name
    
    available_functions = {
            "search_courses": search_courses,
            "search_exams": search_exams,
            "search_student": search_student
    }
    function_to_call = available_functions[function_name] 
   
    function_args = json.loads(response_message.function_call.arguments)
    function_response = function_to_call(**function_args)

    #logging.info("Output of function call:")
    #logging.info(function_response)
    #logging.info(type(function_response))


    # Add the assistant response and function response to the messages
    messages.append( 
        {
            "role": response_message.role,
            "function_call": {
                "name": function_name,
                "arguments": response_message.function_call.arguments,
            },
            "content": None
        }
    )
    messages.append( 
        {
            "role": "function",
            "name": function_name,
            "content":function_response,
        }
    )

#logging.info("Messages in next request:")
#logging.info(messages)


second_response = client.chat.completions.create(
    messages=messages,
    model=deployment,
    function_call="auto",
    functions=functions,
    temperature=0
        )  # get a new response from GPT where it can see the function response


print(second_response.choices[0].message.content)


