from crypt import methods
from flask import Flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin
from db.db_handler import Module

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"/": {"origins": "localhost:3000"}})
dbModule = Module()

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