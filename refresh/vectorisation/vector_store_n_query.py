from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
import openai
import json
import re

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def query_from_vector(query):

    vector_folder_name = f"data/merged_vector"
    
    if not os.path.exists(vector_folder_name):
        response_for_empty_folder = "Sorry ! You need to upload documents first to be able to chat with it..."
        return response_for_empty_folder


    # if os.path.exists(f"{vector_name}.pkl"):
    #     with open(f"{vector_name}.pkl", "rb") as f:
    #         VectorStore = pickle.load(f)
    
    embeddings = OpenAIEmbeddings()    
    VectorStore = FAISS.load_local(vector_folder_name, embeddings=embeddings)


    # query = "what colour is the sky"

    docs = VectorStore.similarity_search(query=query, k=3)

    # llm = OpenAI()
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=query)
        print(cb)
    # print("\n\nResponse : ",response)
    
    # Use regular expressions to extract all key-value pairs
    matches = re.findall(r'(\w+(?:\s+\w+)*):\s*([$0-9.]+)', str(cb))

    # Handle special case for "Total Cost" to capture the entire cost string
    total_cost_match = re.search(r'Total Cost \(USD\):\s*([$0-9.]+)', str(cb))
    if total_cost_match:
        matches.append(('Total Cost (USD)', total_cost_match.group(1)))

    # Create a dictionary from the matches
    response_dict = dict(matches)

    # Convert the dictionary to JSON format
    json_response = json.dumps(response_dict, indent=2)
    
    response_dict = {"result": response, "cb" : json.loads(json_response)}
    

    return json.dumps(response_dict, indent=2)

query_from_vector("tell me about af klint hilma and tell me about the source of the docement, live the link of https://www.theartstory.org/")