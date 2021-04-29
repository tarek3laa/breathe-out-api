from flask import Flask, request, json, flash

from data_model import Doctor
from mongo import *

app = Flask(__name__)


@app.route('/signup', methods=['post'])
def sign_up():
    #  check the email,username & number are unique
    data = json.loads(request.data)
    print(data)
    doctor = Doctor.from_json(data)
    print(doctor.to_json())
    if get_count('phone_number', doctor.phone_number) == 0 and \
            get_count('email', doctor.email) == 0 and \
            get_count('username', doctor.username) == 0:
        print('nice')
        insert_new_doctor(doctor)
    else:
        print('shit')
        # flash('Email already exists.', category='error')
    return '200'


@app.route('/signin', methods=['post', 'get'])
def sign_in():
    # todo(1) read the json request ..... hint :the json will be like that {'username':value,'password':value}
    # todo(3) check the username & password are correct
    # todo(4) return doctor object as a json

    if request.method == 'post':
        username = request.form.get('username')
        password = request.form.get('password')
        doctor = get_doctor_by('username', username)
        if doctor is not None:
            if doctor.password == password:
                return doctor.to_json()
            else:
                flash('password incorrect!', category='error')
        else:
            flash('username does not exist.', category='error')
    else:
        return 'hello world'


if __name__ == '_main_':
    app.run()
