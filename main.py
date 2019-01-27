
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
    client_id='',
    client_secret='',
    redirect_uri='https://magni-find.herokuapp.com/exchange',
    scope=['read_vehicle_info','read_odometer', 'control_security',
    'control_security:unlock','read_location' ],
    test_mode=False
)

time2={}
# TODO: Authorization Step 1a: Launch Smartcar authorization dialog

#@app.route('/',methods=['GET'])
odometer2={}

location2={}
# @app.route('/login', methods=['GET'])
# def login():
#     # TODO: Authorization Step 1b: Launch Smartcar authorization dialog
#     auth_url = client.get_auth_url()
#     return '''
#         <h1>!</h1>
#         <a href=%s>
#             <button>Start</button>
#         </a>
#
#     ''' % auth_url



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

    odometer2 = vehicle.odometer()
    print(odometer2)

    return jsonify(info)

    time_start= time.time()
    seconds=0
    minutes=0




@app.route('/timer', methods=['GET'])
def timerpage():
    auth_url = client.get_auth_url()
    return '''
        <h1>!</h1>
        <a href=%s>
            <button>Connect Car</button>
        </a>
        <form action="/timer_start" method="post">
            <button>Start</button>
        </form>
        <form action="/timer_end" method="post">
            <button>Stop</button>
        </form>
        <form action="/final" method="post">
            <button>Fetch All My Data</button>
        </form>
    ''' % auth_url



@app.route('/timer_start', methods=['POST'])
def timer_start():
    time2['timer_start'] = time.time()
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    location2['start_location']=vehicle.location()
    odometer2['start_odometer']= vehicle.odometer()
    print(time2)
    print(odometer2)
    print(location2)
    return redirect('/timer')


@app.route('/timer_end', methods=['POST'])
def timer_end():
    time2['timer_end']= time.time()
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    location2['end_location']=vehicle.location()
    odometer2['end_odometer']= vehicle.odometer()
    print(time2)
    print(odometer2)
    print(location2)
    return redirect('/timer')

@app.route('/final', methods=['POST'])
def final():
    final= time2['timer_end']-time2['timer_start']
    final2= odometer2['end_odometer']['data']['distance']-odometer2['start_odometer']['data']['distance']
    final3=final2/final
    final4=location2
    print(final)
    print(final2)
    print(final3)
    print(final4)
    return redirect('/timer')




if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8000)))
