from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
import openai
import json
import re
import shutil

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def delete_folder(folder_path):
    try:
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Remove the folder and its contents
            shutil.rmtree(folder_path)
            print(f"The folder '{folder_path}' has been successfully deleted.")
        else:
            print(f"The folder '{folder_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    response = "success"

    return response


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

def read_file_to_string(file_path):
    try:
        # Initialize an empty string to store the file contents
        file_contents = ""

        # Open the file and read its contents
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        return file_contents
    except FileNotFoundError:
        return "File not found."


def create_vector(content, vector_folder_name):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
    chunks = text_splitter.split_text(text=content)
    
    embeddings = OpenAIEmbeddings()
    
    print(vector_folder_name)
    
    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    
    # os.makedirs(os.path.dirname(f"{vector_name}.pkl"), exist_ok=True)
    
    # directory = os.path.dirname(vector_name)
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    
    if os.path.exists(vector_folder_name):
        try:
            shutil.rmtree(vector_folder_name)
            print(f"Folder '{vector_folder_name}' and its contents deleted successfully.")
        except Exception as e:
            print(f"Error deleting folder '{vector_folder_name}': {e}")
    else:
        print(f"Folder '{vector_folder_name}' does not exist.")
        
    VectorStore.save_local(vector_folder_name)
    
    # with open(f"{vector_name}.pkl", "wb") as f:
    #     print("Dumping in ",f"{vector_name}.pkl")
    #     pickle.dump(VectorStore, f)

    return vector_folder_name


def read_document(file_path):
    
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Convert the extension to lowercase for case-insensitive comparison
    file_extension = file_extension.lower()

    # Check file type based on extension
    if file_extension == '.txt':
        print(f"The file {file_path} is a Text file.")
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            content = txt_file.read()
    return content

def merge_db():
    vector_base_folder = f"data/vectors"
    final_folder = f"data/merged_vector"
    delete_folder(final_folder)
    os.makedirs(final_folder, exist_ok=True)
    print(f"----------\n\n{vector_base_folder}\n\n{final_folder}\n\n--------")
    embeddings = OpenAIEmbeddings()
    all_items  = os.listdir(vector_base_folder)
    folders = [item for item in all_items if os.path.isdir(os.path.join(vector_base_folder, item))]
    print(len(folders))
    if len(folders)==1:
        VectorStore1 = FAISS.load_local(f"{vector_base_folder}/{folders[0]}", embeddings=embeddings)
        VectorStore1.save_local(final_folder)
        # return "Merged - Single"
        return "success"
    VectorStore1 = FAISS.load_local(f"{vector_base_folder}/{folders[0]}", embeddings=embeddings)
    VectorStore2 = FAISS.load_local(f"{vector_base_folder}/{folders[1]}", embeddings=embeddings)
    VectorStore2.merge_from(VectorStore1)
    VectorStore2.save_local(final_folder)
    for i in range(1,len(folders)):
        VectorStore1 = FAISS.load_local(final_folder, embeddings=embeddings)
        VectorStore2 = FAISS.load_local(f"{vector_base_folder}/{folders[i]}", embeddings=embeddings)
        VectorStore2.merge_from(VectorStore1)
        VectorStore2.save_local(final_folder)

    # response = "Merged - Multiple"
    response = "success"

    return response

def vectorise(xml_id, type):
    data_file_path = f"data/filtered_txts/{type}s/{xml_id}.txt"
    content = read_document(data_file_path)
    vector_folder_name = f"data/vectors/{type}_{xml_id}"
    create_vector(content, vector_folder_name)