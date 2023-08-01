"""
    PAF Core
    Server for connections to other applications
"""
import json
import subprocess
import logging

from os import truncate
from flask import Flask, send_file
import paf_core.weather as w

import paf_core.settings as st

# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

RUT = st.GFOR

logger = logging.getLogger('log_config')


"""
NOTA IMPORTANTE: añadir modulo csp para las conexiones seguras con los clientes
"""


@app.route('/wea/loc/', methods=['GET'])
def wea():
    try:
        if open('/tmp/paf/forecast/loc.json', 'w') != 0:
            truncate('/tmp/paf/forecast/loc.json', 0)
    except FileNotFoundError:
        subprocess.run(['mkdir', '/tmp/paf'], check=False)
        subprocess.run(['mkdir', '/tmp/paf/forecast/'], check=False)
        subprocess.run(['touch', '/tmp/paf/forecast/loc.json'], check=False)

    rest = w.TemActual()
    dt = rest.dat('Madrid')
    temp = rest.location()
    with open('/tmp/paf/forecast/loc.json', 'w') as file:
        json.dump(temp, file, indent=4)
    return send_file(f"{'/tmp/paf/forecast/loc.json'}", as_attachment=True), 200


@app.route('/wea/forecast/', methods=['GET'])
def forecast():
    try:
        if open(RUT, 'w') != 0:
            truncate(RUT, 0)
    except FileNotFoundError:

        subprocess.run(['mkdir', '/tmp/paf'], check=False)
        subprocess.run(['mkdir', '/tmp/paf/forecast/'], check=False)
        subprocess.run(['touch', RUT], check=False)

    loc = open('/tmp/paf/forecast/loc.json', 'r').read()
    lat = float(json.loads(loc)['lat'])
    lon = float(json.loads(loc)['lon'])

    rest = w.OneCall()
    try:
        rest = rest.dat(lat, lon)
        with open(RUT, 'w') as file:
            json.dump(rest, file, indent=4)
        stat = 200
    except:
        stat = rest.dat(lat, lon)
    return send_file(f'{RUT}', as_attachment=True), stat


@app.route('/')
def index():
    return 'Connected!!', 200


if __name__ == '__main__':
    app.run(debug=False, port=5000)
