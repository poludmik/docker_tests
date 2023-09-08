from flask import Flask, request, jsonify
from nlp.process_search import ProcessSearch


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
        
        # Get a list of available keywords somehow TODO
        keywords = ["sushi", "pizza", "burger", "japanese", "italian", "seafood", 
                    "cheap", "fastfood", "meat", "steak", "fish", "chips", "spaghetti",
                    "american", "wine", "coctail", "russian", "tortilla", "coffee", "capuccino",
                    "breakfast", "dinner", "chinese", "schnitzel", "pirogi", "czech"]

        response_data = {"keywords": ProcessSearch.get_keywords(received_data['user_request'], keywords)}

        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
