from flask import Flask

app = Flask(__name__)

def start():
    import sys
    print("Python version:", sys.version)

    app.run(host='0.0.0.0', port=5000, debug=False)
