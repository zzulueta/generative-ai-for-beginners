# load the environment variables file
from dotenv import load_dotenv
import os
import openai
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextEmbedding,
)
from semantic_kernel.connectors.memory.azure_cosmosdb import (
    AzureCosmosDBMemoryStore,
)
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.prompt_template.input_variable import InputVariable

import asyncio
import warnings

async def main(query_term):
    # Load environment variables from a .env file
    load_dotenv()

    # Environment variable obtained for Azure Cosmos DB for MongoDB vCore
    AZCOSMOS_CONNSTR=os.getenv("AZCOSMOS_CONNSTR")
    AZCOSMOS_API=os.getenv("AZCOSMOS_API")
    AZCOSMOS_DATABASE_NAME="dbm"
    AZCOSMOS_CONTAINER_NAME="dbm_saro"

    # Envrionment variables obtained for Azure OpenAI
    openai.api_type = "azure"
    openai.api_key = os.getenv("AZURE_OPENAI_KEY") 
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
    openai.api_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    openai.api_embeddings_deployment_name = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT")
    openai.api_version = "2023-07-01-preview"


    # Vector search index parameters
    index_name = "VectorSearchIndex"
    vector_dimensions = (
        1536  # text-embedding-ada-002 uses a 1536-dimensional embedding vector
    )
    num_lists = 1
    similarity = "COS"  # cosine distance

    # Initialize the kernel
    kernel = sk.Kernel()

    # Load the chat deployment name, initialize the chat completions with the required parameters 
    # Add the created chat service to the semantic kernel instance.
    kernel.add_service(
        AzureChatCompletion(
            service_id="chat_completion",
            deployment_name=openai.api_deployment_name,
            endpoint=openai.api_base,
            api_key=openai.api_key,
        )
    )

    # Load the embeddings deployment name and initialize the text embedding with the required parameters, 
    # Add the created embedding service to the semantic kernel instance.
    kernel.add_service(
        AzureTextEmbedding(
            service_id="text_embedding",
            deployment_name=openai.api_embeddings_deployment_name,
            endpoint=openai.api_base,
            api_key=openai.api_key,
        )
    )

    # Suppress specific warning from semantic_kernel
    warnings.filterwarnings("ignore", message="You appear to be connected to a CosmosDB cluster")

    # Create an Azure Cosmos DB Memory Store with the required parameters
    store = await AzureCosmosDBMemoryStore.create(
        cosmos_connstr=AZCOSMOS_CONNSTR,
        cosmos_api=AZCOSMOS_API,
        database_name=AZCOSMOS_DATABASE_NAME,
        collection_name=AZCOSMOS_CONTAINER_NAME,
        index_name=index_name,
        vector_dimensions=vector_dimensions,
        num_lists=num_lists,
        similarity=similarity,
    )

    # Add the created memory store to the semantic kernel instance.
    memory = SemanticTextMemory(storage=store, embeddings_generator=kernel.get_service("text_embedding"))
    kernel.import_plugin_from_object(TextMemoryPlugin(memory), "TextMemoryPluginACDB")

    # each time it calls the embedding model to generate embeddings from your query
    result = await memory.search(AZCOSMOS_CONTAINER_NAME, query_term)

    # Create a chat function with the provided prompt and the required parameters

    # Define a prompt template for the chatbot
    prompt = """
        You are a chatbot that can have a conversations about any topic related to the provided context.
        You will always provide answers in this sample format:
        Saro Number:  SARO-ROVI-24-0006759
        Amount: 1,000,000
        Department: 21 - Department of Education 
        Agency: 002-Bureau of Elementary Education 
        Operating Unit: 210001 - National Capital Region 
        Purpose: Release of allotment for the construction of additional classrooms in selected public elementary schools in the National Capital Region.
        
        Give explicit answers from the provided context or say 'I don't know' if it does not have an answer.
        provided context: {{$db_record}}

        User: {{$query_term}}
        Chatbot:"""

    # Set up execution settings for the OpenAI text prompt.
    execution_settings = sk_oai.OpenAITextPromptExecutionSettings(
    service_id="chat_completion",
        ai_model_id=openai.api_deployment_name,
        max_tokens=500,
        temperature=0.0,
        top_p=0.5
    )

    # Configure the prompt template with necessary input variables and execution settings
    chat_prompt_template_config = sk.PromptTemplateConfig(
        template=prompt,
        name="grounded_response",
        template_format="semantic-kernel",
        input_variables=[
            InputVariable(name="db_record", description="The database record", is_required=True),
            InputVariable(name="query_term", description="The user input", is_required=True),
        ],
        execution_settings=execution_settings
    )

    # Create a chat function using the defined prompt and template configuration
    chat_function = kernel.create_function_from_prompt(
        prompt=prompt,
        function_name= "ChatGPTFunc2", 
        plugin_name="chatGPTPlugin2", 
        prompt_template_config=chat_prompt_template_config
    )

    # Invoke the chat function with the query term and the database record
    completions_result = await kernel.invoke(chat_function, sk.KernelArguments(query_term=query_term, db_record=result[0].additional_metadata))

    print(completions_result)


# Run the main function
asyncio.run(main("Bigyan mo ako ng detalye para sa improvement of kidney transplant facilities in Zamboanga Peninsula."))


