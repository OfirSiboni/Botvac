from flask import Flask
#import rsa

app = Flask(__name__)
public_key,private_key = rsa.newkeys(1024)

@app.route('/get_public_key')
def get_public_key():
    return {
        'n':public_key.n,
        'e':public_key.e
    }

@app.route('/update_last_task',methods=['POST'])
def update_last_task():
    print(request.form)



@app.route('/summary_form')
def summary_form():
    return "<h1>summary_form</h1>"


if __name__ == '__main__':
    app.run(port = 8080)