from flask import Flask, request
import json

import os
# from pyngrok import ngrok
# from dotenv import load_dotenv
# load_dotenv()
# ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))


from refresh.vectorisation.vector_create_n_query import *
from refresh.website_n_xml_utils import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/refresh', methods=['POST'])
def refresh():
    response = filter_and_store_paths()
    json_response = json.dumps({"result": response})
    return json.loads(json_response)

@app.route('/query_vectors', methods=['POST'])
def query_vector():
    query = request.args.get('query')
    print("Creation of Agent --> ", create_agent())
    response2 = search_docs("Give me the following answers from the context you have", query)
    json_response = json.dumps({"result": response2})
    return json.loads(json_response)

# # Opening tunnel
# public_url = ngrok.connect("5000", "http")

# # Print the public URL
# print(f'\n\nNgrock Public URL --> \"{public_url}\"\n\n')

if __name__ == '__main__':
    app.run()
