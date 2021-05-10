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

@staticmethod
def from_json(data):
    username = data['username']
    name = data['name']
    phone_number = data['phone_number']
    status = data['status']
    gender = data['gender']
    first_fvc = data['first_fvc']
    age = data['age']
    first_fvc_date = data['first_fvc_date']
    registered_date = data['registered_date']
    xRay_Url = data['xRay_Url']
    CT_Url = data['CT_Url']
    CT_date = data['CT_date ']
    address = data['address']
    return Patient(name, phone_number, status, gender, age, first_fvc, first_fvc_date, registered_date, xRay_Url,
               CT_Url, CT_date, address)
    return Doctor(username)

if __name__ == '_main_':
    app.run()
