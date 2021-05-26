# Import lib
from datetime import datetime
from flask import Flask, Response, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
import json
import requests
import numpy as np
import pandas as pd
app = Flask(__name__)

DEBUG = os.environ.get('DEBUG')
if(DEBUG != None and DEBUG == "True"):
    DEBUG = True
else:
    DEBUG = False

HEADERS = os.environ.get('HEADERS')
if(HEADERS == None):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Host': 'cdn-api.co-vin.in',
        'Accept-Language': 'hi_IN'
    }

# Initialize Data
path = Path(os.path.dirname(os.path.realpath(__file__)))
pathData = os.path.join(str(path.parent), 'data')

folderList = ['data']
for x in folderList:
    try:
        if not os.path.exists(x):
            os.makedirs(x)
    except OSError as err:
        print(err)


# API


@ app.route('/')
def homepage():
    the_time = datetime.now().strftime("%c")

    return """
    <h1>Welcome to CoWin Python!</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)


@ app.route('/json', methods=['GET'])
def jsonHome():
    data = {'name': 'Welcome to CoWin Python!',
            'time': str(datetime.now().strftime("%c")),
            'dataPath': pathData}
    if(DEBUG):
        data['env'] = dict(os.environ)
    return jsonify(data), 201


@ app.route('/postman', methods=['GET'])
def postmanAPI():
    # Read json file in folder
    return json.load(open('CoWin.postman_collection.json'))


@ app.route('/file', methods=['GET'])
def getFile():
    try:
        id = request.args.get('id')
        if(id != None and id != ''):
            id = id.lower()
            filePath = 'data/' + id + '.json'
            # Read json file in folder
            if os.path.isfile(filePath):
                with open(filePath) as f:
                    fdata = json.load(f)
                return jsonify({'chart': fdata}), 200
            else:
                return jsonify({'errorMsg': filePath + ' not Found'}), 204
        else:
            return jsonify({'errorMsg': 'ID not provided'}), 401
    except Exception as e:
        data = {'time': str(datetime.now().strftime("%c")), 'errorMsg': str(e)}
        return jsonify(data), 500


@ app.route('/api/pincode', methods=['GET'])
def getPincodeAPI():
    try:
        pincode = request.args.get('pincode')
        if(pincode != None and pincode != ''):
            pass
        else:
            pincode = '414001'
        date = str(datetime.now().strftime("%d-%m-%Y"))
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=' + \
            str(pincode) + '&date=' + date
        page = requests.get(url, HEADERS)
        return jsonify({'body': str(page.content), 'headers': str(page.headers), 'req_url': url, 'req_headers': HEADERS}), page.status_code
    except Exception as e:
        return jsonify({'time': str(datetime.now().strftime("%c")), 'errorMsg': str(e)}), 500

# Error Handling


@ app.errorhandler(404)
def page_not_found(e):
    data = {'time': str(datetime.now().strftime("%c")), 'errorMsg': str(e)}
    return jsonify(data), 404


# Flask server invoke
if __name__ == '__main__':
    app.run(debug=DEBUG, use_reloader=True)
