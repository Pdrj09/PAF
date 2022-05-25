from crypt import methods
from os import truncate
from flask import Flask, send_file
import paf_core.weather as w
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

"""
NOTA IMPORTANTE: añadir modulo csp para las conexiones seguras con los clientes
"""

@app.route('/wea/loc/', methods=['GET'])
def wea():
    if open('loc.json', 'w') != 0:
        truncate('loc.json', 0)
    rest = w.tem_actual()
    dt = rest.dat('Madrid')
    temp = rest.location()
    with open('loc.json', 'w') as file:
        json.dump(temp, file, indent=4)
    return send_file(f"{'loc.json'}", as_attachment=True), 200

@app.route('/wea/forecast/', methods=['GET'])
def forecast():
    if open('forecast.json', 'w') != 0:
        truncate('forecast.json', 0)
    """loc = open('loc.json', 'r').read()
    lat = float(json.loads(loc)['lat'])
    lon = float(json.loads(loc)['lon'])"""
    lat = 40.416775
    lon = -3.703790 
    rest = w.one_call()
    dt = rest.dat(lat, lon)
    with open('forecast.json', 'w') as file:
        json.dump(dt, file, indent=4)
    return send_file(f"{'forecast.json'}", as_attachment=True), 200



@app.route('/')
def index():
    return '<h1>200</h1>'

if __name__ == '__main__':
    app.run(debug=False, port=5000)

