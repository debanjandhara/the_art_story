# from pyngrok import ngrok
from flask import Flask, request
import json

from refresh.vectorisation.vector_create_n_query import *
from refresh.website_n_xml_utils import *

app = Flask(__name__)

# # Define your function
# def add_numbers(a, b):
#     result = a + b
#     return f"The sum of {a} and {b} is {result}"

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
    response4 = query_from_vector(query)
    return response4

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    app.run()