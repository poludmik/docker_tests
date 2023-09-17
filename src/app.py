import os
from flask import Flask, request, jsonify, g
from src.nlp.process_search import ProcessSearch
from src.data.data import Data
# from src.data.db_connection import DBconnection as db
import src.data.db_connection as db
# from src.data.db_connection import get_db
# import psycopg2
import atexit


app = Flask(__name__)

def check_data():
    global data
    if data is None:
        data = Data()
    return data


@app.route('/process_string', methods=['GET'])
def process_string():
    try:
        received_data = request.get_json()

        if 'input_string' not in received_data:
            return jsonify({'error': 'Missing input_string in the request'}), 400
        
        response_data = {"You say": received_data['input_string'], "I say": "Flask is better than Spring"}
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/extract_keywords', methods=['GET'])
def extract_keywords():
    try:

        data = check_data()

        received_data = request.get_json()

        if 'user_request' not in received_data:
            return jsonify({'error': 'Missing user_request string in the request'}), 400

        print(received_data['user_request'])
        filters, filters_to_exclude = ProcessSearch.get_keywords(received_data['user_request'], data)
        response_data = {"filters": filters, "filters_to_exclude": filters_to_exclude}

        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def close_db():
    db.conn.close()
    if db.conn.closed:
        print("DB CONNECTION CLOSED")
    else:
        print("DB CONNECTION WASN'T CLOSED")


atexit.register(close_db)


def start():
    global data
    data = None

    db.DBconnection.connect()
    app.run(host='0.0.0.0', port=5000, debug=False)

