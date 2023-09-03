from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/process_string', methods=['POST'])
def process_string():
    try:
        received_data = request.get_json()

        if 'input_string' not in received_data:
            return jsonify({'error': 'Missing input_string in the request'}), 400
        
        response_data = {"You say": received_data['input_string'], "I say": "Flask is better than Spring"}
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
