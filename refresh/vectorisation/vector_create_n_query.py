from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
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

def process_docs():

    from langchain.document_loaders import PyPDFLoader
    from langchain.document_loaders import DirectoryLoader
    from langchain.document_loaders import TextLoader
    from langchain.document_loaders import Docx2txtLoader
    from langchain.document_loaders.csv_loader import CSVLoader
    from langchain.document_loaders import UnstructuredExcelLoader
    from langchain.vectorstores import FAISS
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # loader1 = DirectoryLoader('data/filtered_txts/artists/', glob="./*.pdf", loader_cls=PyPDFLoader)
    # document1 = loader1.load()

    # loader2 = DirectoryLoader('data/filtered_txts/artists/', glob="./*.txt", loader_cls=TextLoader)
    # document2 = loader2.load()

    # loader3 = DirectoryLoader('data/filtered_txts/artists/', glob="./*.docx", loader_cls=Docx2txtLoader)
    # document3 = loader3.load()

    # loader4 = DirectoryLoader('data/filtered_txts/artists/', glob="./*.csv", loader_cls=CSVLoader)
    # document4 = loader4.load()

    # loader5 = DirectoryLoader('data/filtered_txts/artists/', glob="./*.xlsx", loader_cls=UnstructuredExcelLoader)
    # document5 = loader5.load()
    
    loader1 = DirectoryLoader('data/filtered_txts/artists/', glob="./atget_eugene.txt", loader_cls=TextLoader)
    document1 = loader1.load()

    # document1.extend(document2)
    # document1.extend(document3)
    # document1.extend(document4)
    # document1.extend(document5)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    docs = text_splitter.split_documents(document1)
    embeddings = OpenAIEmbeddings()

    docs_db = FAISS.from_documents(docs, embeddings)
    docs_db.save_local("data/vectors/atget_eugene.txt")

    return "Successful!"

global agent

def create_agent():

    from langchain.chat_models import ChatOpenAI
    from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
    from langchain.chains import ConversationChain
    global agent

    llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k')
    memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=1000)
    agent = ConversationChain(llm=llm, memory=memory, verbose=True)

    return "Successful!"

def formatted_response(docs, question, response, state):

    formatted_output = response + "\n\nSources"

    for i, doc in enumerate(docs):
        source_info = doc.metadata.get('source', 'Unknown source')
        page_info = doc.metadata.get('page', None)

        doc_name = source_info.split('/')[-1].strip()

        if page_info is not None:
            formatted_output += f"\n{doc_name}\tpage no {page_info}"
        else:
            formatted_output += f"\n{doc_name}"

    state.append((question, formatted_output))
    return state, state

def search_docs(prompt, question):

    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.callbacks import get_openai_callback
    global agent
    agent = agent

    state = state or []

    embeddings = OpenAIEmbeddings()
    docs_db = FAISS.load_local("/content/docs_db/", embeddings)
    docs = docs_db.similarity_search(question)

    prompt += "\n\n"
    prompt += question
    prompt += "\n\n"
    prompt += str(docs)

    with get_openai_callback() as cb:
        response = agent.predict(input=prompt)
        print(cb)

    # return formatted_response(docs, question, response, state)
    return response

def merge_db():
    vector_base_folder = f"data/vectors"
    final_folder = f"data/merged_vector"
    print(f"----------\n\n{vector_base_folder}\n\n{final_folder}\n\n--------")
    embeddings = OpenAIEmbeddings()
    all_items  = os.listdir(vector_base_folder)
    folders = [item for item in all_items if os.path.isdir(os.path.join(vector_base_folder, item))]
    print(len(folders))
    if len(folders)==1:
        VectorStore1 = FAISS.load_local(f"{vector_base_folder}/{folders[0]}", embeddings=embeddings)
        VectorStore1.save_local(final_folder)
        print("\n\nRunning Folder 1 only")
        # return "Merged - Single"
        return "success"
    print("\n\nRunning Multi Folders")
    print(f"\n\n{vector_base_folder}/{folders[0]}")
    VectorStore1 = FAISS.load_local(f"{vector_base_folder}/{folders[0]}", embeddings=embeddings)
    print(f"\n\n{vector_base_folder}/{folders[1]}")
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

# print(process_docs())
# print(create_agent())
# print(search_docs("Give me the following answers from the context you have", "Who is klint hilma"))

# print(merge_db())