import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import time
import sys


import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    scope=['read_vehicle_info','read_odometer', 'control_security', 'control_security:unlock','read_location' ],
    test_mode=False
)

time2={}
# TODO: Authorization Step 1a: Launch Smartcar authorization dialog

#@app.route('/',methods=['GET'])


@app.route('/login', methods=['GET'])
def login():
    # TODO: Authorization Step 1b: Launch Smartcar authorization dialog
    auth_url = client.get_auth_url()
    return '''
        <h1>!</h1>
        <a href=%s>
            <button>Start</button>
        </a>

    ''' % auth_url



@app.route('/exchange', methods=['GET'])
def exchange():
    # TODO: Authorization Step 3: Handle Smartcar response
    code = request.args.get('code')
    # TODO: Request Step 1: Obtain an access token
    global access

    access = client.exchange_code(code)
    return '', 200


@app.route('/vehicle', methods=['GET'])
def vehicle():
    # TODO: Request Step 2: Get vehicle ids
    global access
    # TODO: Request Step 3: Create a vehicle
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    # TODO: Request Step 4: Make a request to Smartcar API
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()
    print(info)

    #response = vehicle.permissions()
    #print(response)

    response3 = vehicle.location()
    print(response3)

    vehicle.unlock()

    response2 = vehicle.odometer()
    print(response2)

    time_start= time.time()
    seconds=0
    minutes=0



@app.route('/timer', methods=['GET'])
def timerpage():
    return '''
        <h1>!</h1>
        <form action="/timer_start" method="post">
            <button>Start</button>
        </form>
        <form action="/timer_stop" method="post">

        <button>Stop</button>
        </form>
        <form action="/final" method="post">

        <button>Fetch Data</button>
        </form>
    '''



@app.route('/timer_start', methods=['POST'])
def timer_start():
    time2['timer_start'] = time.time()
    print time2
    return redirect('/timer')

@app.route('/timer_stop', methods=['POST'])
def timer_end():
    time2['timer_end']= time.time()
    print time2
    return redirect('/timer')


@app.route('/final', methods =['POST'])
def final():
    final = time2['timer_end']-time2['timer_start']
    print final
    return redirect('/timer')

if __name__ == '__main__':
    app.run(port=8000)
