from flask import Flask, request, json, flash, jsonify
import bcrypt
from data_model import *
from mongo import *

app = Flask(__name__)


@app.route('/signup', methods=['post'])
def sign_up():
    #  check the email,username & number are unique
    data = json.loads(request.data)
    doctor = Doctor.from_json(data)
    if get_count('email', doctor.email) != 0:
        return jsonify({'msg': 'Email and already exists.', 'code': 403})
    elif get_count('username', doctor.username) != 0:
        return jsonify({'msg': 'username and already exists.', 'code': 403})

    elif get_count('phone_number', doctor.phone_number) != 0:
        return jsonify({'msg': 'phone number and already exists.', 'code': 403})

    else:
        hashed = bcrypt.hashpw(bytes(doctor.password, 'utf-8'), bcrypt.gensalt())
        doctor.password = hashed
        insert_new_doctor(doctor)
        return jsonify({'msg': 'done', 'code': 200})


@app.route('/signin', methods=['post'])
def sign_in():
    data = json.loads(request.data)
    if get_count('username', data['username']) != 0:
        doctor = get_doctor_by('username', data['username'])
        if doctor is not None:
            if bcrypt.checkpw(bytes(data['password'], 'utf-8'), doctor['password']):
                doctor = Doctor.from_json(doctor)
                return jsonify({'code': 200, 'content': doctor.to_json()})
            else:
                return jsonify({'msg': 'password incorrect', 'code': 402})
        else:
            return jsonify({'msg': 'username does not exist.', 'code': 401})
    else:
        return jsonify({'msg': 'username does not exist.', 'code': 401})

@staticmethodm
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
    return Patient(username,name, phone_number, status, gender, age, first_fvc,
                   first_fvc_date, registered_date, xRay_Url,
               CT_Url, CT_date, address)


@app.route('/upload_files/<username>/<phone>', methods=['post'])
def upload_file(username, phone):
    for r in request.files.values():
        r.save(r.filename)

    return jsonify({'code': 200})


@app.route('/add_new_patient/<username>', methods=['post'])
def add_patient(username):
    data = json.loads(request.data)
    print(data)
    add_new_patient(username, Patient.from_json(data))
    return jsonify({'code': 200})


if __name__ == '_main_':
    app.run()




