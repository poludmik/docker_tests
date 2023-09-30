from flask import Flask, request, jsonify, g
from src.nlp.process_search import ProcessSearch
from src.data.data import Data
import src.data.db_connection as db
import signal


app = Flask(__name__)


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
        global data

        received_data = request.get_json()

        if 'user_request' not in received_data:
            return jsonify({'error': 'Missing user_request string in the request'}), 400

        print(received_data['user_request'])
        filters, filters_to_exclude = ProcessSearch.get_keywords(received_data['user_request'], data)
        response_data = {"filters": filters, "filters_to_exclude": filters_to_exclude}

        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/autocomplete', methods=['GET'])
def autocomplete():

    try:
        sentence = request.args.get('sentence')
        max_len = int(request.args.get('max_len')) if request.args.get('max_len') is not None else 10
        max_proposals = int(request.args.get('max_proposals')) if request.args.get('max_proposals') is not None else 5
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    try:
        ridiculous_sentence, next_words, the_case = data.autocomplete.autocomplete_sentence(sentence, max_length=max_len, N_proposed_words=max_proposals)
        return jsonify({"lol": ridiculous_sentence, "kek": next_words, "situation": the_case})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Close connection to DB on:
signal.signal(signal.SIGTERM, db.DBconnection.close_db_docker) # docker stop
signal.signal(signal.SIGHUP, db.DBconnection.close_db_docker) # terminal closed
signal.signal(signal.SIGINT, db.DBconnection.close_db_docker) # CTRL+C (works also in docker, see container logs)


def start():
    db.DBconnection.connect()

    global data
    data = Data()
    
    app.run(host='0.0.0.0', port=5000, debug=False)

