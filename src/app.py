from flask import Flask, request, jsonify
from src.nlp.process_search import ProcessSearch
from src.data.data import Data


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
        received_data = request.get_json()

        if 'user_request' not in received_data:
            return jsonify({'error': 'Missing user_request string in the request'}), 400

        print(received_data['user_request'])
        filters, filters_to_exclude = ProcessSearch.get_keywords(received_data['user_request'], data)
        response_data = {"filters": filters, "filters_to_exclude": filters_to_exclude}

        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def start(docker=False):
    global data
    data = Data(docker=docker)
    app.run(host='0.0.0.0', port=5000, debug=False)


# if __name__ == '__main__':
#     import sys
#     print("Python version:", sys.version)

#     args = parser.parse_args([] if "__file__" not in globals() else None)

#     global data
#     data = Data(docker=args.docker)

#     app.run(host='0.0.0.0', port=5000, debug=True)
