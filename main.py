import os
from flask import Flask


if __name__ == '__main__':
    app = Flask(__name__)
    app.run(debug=True, host='127.0.0.1')