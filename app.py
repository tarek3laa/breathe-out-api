from flask import Flask, request, json, flash, jsonify

from data_model import *
from mongo import *

app = Flask(__name__)


@app.route('/signup', methods=['post'])
def sign_up():
    #  check the email,username & number are unique
    data = json.loads(request.data)
    doctor = Doctor.from_json(data)
    if get_count('phone_number', doctor.phone_number) == 0 and \
            get_count('email', doctor.email) == 0 and \
            get_count('username', doctor.username) == 0:
        insert_new_doctor(doctor)
        jsonify({'msg': 'done', 'code': 200})
    else:
        return jsonify({'msg': 'Email already exists.', 'code': 403})


@app.route('/signin', methods=['post'])
def sign_in():
    data = json.loads(request.data)
    if get_count('username', data['username']) != 0:
        doctor = get_doctor_by('username', data['username'])
        if doctor is not None:
            if doctor.password == data['password']:
                return jsonify(doctor.to_json())
            else:
                return jsonify({'msg': 'password incorrect', 'code': 402})
        else:
            return jsonify({'msg': 'username does not exist.', 'code': 401})
    else:
        return jsonify({'msg': 'username does not exist.', 'code': 401})


if __name__ == '_main_':
    app.run()
