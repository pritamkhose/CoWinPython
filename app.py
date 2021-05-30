# Import lib
from datetime import datetime
from flask import Flask, Response, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
import json
import requests
import pandas as pd
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
schedule = BlockingScheduler()

DEBUG = os.environ.get('DEBUG')
if(DEBUG != None and DEBUG == "True"):
    DEBUG = True
else:
    DEBUG = False

JOBRUN = os.environ.get('JOBRUN')
if(JOBRUN != None and JOBRUN == "True"):
    JOBRUN = True
else:
    JOBRUN = False

HEADERS = os.environ.get('HEADERS')
if(HEADERS == None):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Host': 'cdn-api.co-vin.in',
        'Accept-Language': 'hi_IN'
    }

MONGODBNAME = os.environ.get('MONGODB')
MONGOURL = os.environ.get('MONGOURL')

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
        res = {'body': json.loads(page.content), 'status': page.status_code, 'headers': str(
            page.headers), 'req_url': url, 'req_headers': HEADERS}
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'time': str(datetime.now().strftime("%c")), 'errorMsg': str(e)}), 500


@ app.route('/test', methods=['GET'])
def getPincodeJOBTest():
    getPincodeJOB()
    return jsonify({'msg': 'ok'}), 200


# Scheduler Jobs Function
@schedule.scheduled_job('interval', minutes=1)
def timed_job():
    getPincodeJOB()


schedule.start()


def getPincodeJOB():
    pincodeList = ['414001', '414002', '414003', '414004', '414005', '414006']
    date = str(datetime.now().strftime("%d-%m-%Y"))
    time = str(datetime.now().strftime("%c"))
    print('getPincodeJOB started = ', time)
    content = []
    for pincode in pincodeList:
        try:
            url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=' + \
                str(pincode) + '&date=' + date
            page = requests.get(url, HEADERS)
            res = {'body': json.loads(
                page.content), 'status': page.status_code, 'req_url': url}
            content.append({'pincode': pincode, 'date': time, 'result': res})
        except Exception as e:
            content.append({'pincode': pincode, 'date': time, 'error': str(e)})
    col = 'Slots'
    print('getPincodeJOB content = ', content)
    try:
        mongoClient = pymongo.MongoClient(MONGOURL)
        mongoDB = mongoClient[MONGODBNAME][col]
        data = mongoDB.insert_many(content).inserted_ids
        print(date, str(data))
    except Exception as e:
        print('mongo error', str(e))


# Error Handling
@ app.errorhandler(404)
def page_not_found(e):
    data = {'time': str(datetime.now().strftime("%c")), 'errorMsg': str(e)}
    return jsonify(data), 404


# Flask server invoke
if __name__ == '__main__':
    # if(JOBRUN):
    #     job = scheduler.add_job(getPincodeJOB, 'interval', minutes=1)
    #     scheduler.start()
    app.run(debug=DEBUG, use_reloader=True)
