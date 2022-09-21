from crypt import methods
from email import header
from urllib import response
from urllib.robotparser import RequestRate
from wsgiref import headers
from flask import Flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin
from db.db_handler import Module
import os

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"/*": {"origins": "localhost:3000"}})
dbModule = Module()
path = './react-image-annotate/public/images/images'

@app.route('/save', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type'])
def save_annotate_info():
    try:
        request_data = request.get_json()
        dbModule.handleNewData(request_data)
        # print(request_data)
        return "got it"
    except AssertionError:
        print('error')
    pass

@app.route('/activeImage', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def save_active_image_info():
    try:
        request_data = request.get_json()
        print(request_data)
        dbModule.handleActiveImageData(request_data)
        return 'got it '
    except AssertionError:
        print('error')

@app.route('/imagesName', methods=['GET'])
@cross_origin(origins='localhost', headers=['Content-Type'])
def get_images_name():
    global path
    try:
        imagesName = []
        for(root, dirs, file) in os.walk(path):
            for f in file:
                if ('.png' in f) or ('.jpg' in f) or ('.jpeg' in f):
                    imagesName.append(f)
        
        # print(imagesName)
        response = jsonify({'imagesName': imagesName})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except AssertionError:
        print('error')
@app.route('/', methods=['GET'])
def main():
    return '''
        <h1>Welcome to Lesion Annotator</h1>
        <p>For working with app please start your react annotator project with <i>yarn start</i> <br/><strong>inside raect-annotator folder</strong></p> 
    '''


# If the file is run directly,start the app.
if __name__ == '__main__':
    app.run(debug=False)
    #j