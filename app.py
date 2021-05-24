from datetime import datetime

from flask import Flask, request, json, flash, jsonify
import bcrypt
from data_model import *
from mongo import *
import os
import matplotlib.pyplot as plt
from pydicom import dcmread
import pandas as pd
from utils.utils import get_view
import numpy as np
from model import predict_fvc

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
        insert_new_doctor(doctor)
        return jsonify({'msg': 'done', 'code': 200})


@app.route('/signin', methods=['post'])
def sign_in():
    data = json.loads(request.data)
    if get_count('username', data['username']) != 0:
        doctor = get_doctor_by('username', data['username'])
        if doctor is not None:
            if data['password'] == doctor['password']:
                print(doctor)
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


@app.route('/mk_dir/<username>/<phone>')
def mk_dir(username, phone):
    try:
        os.mkdir(f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}')
    except:
        pass
    try:

        os.mkdir(f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}')
    except:
        pass
    try:
        os.mkdir(f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}/dicom')
        os.mkdir(f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}/axial')
        os.mkdir(f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}/coronal')
        os.mkdir(f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}/sagittal')
    except:
        pass
    return jsonify({'code': 200})


@app.route('/upload_files/<username>/<phone>', methods=['post'])
def upload_file(username, phone):
    for r in request.files.values():
        r.save(f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}/dicom/{r.filename}')
        x = dcmread(
            f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}/dicom/{r.filename}')
        plt.imsave(
            f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}/axial/{r.filename.split(".")[0]}.jpg',
            x.pixel_array, cmap='gray')
    return jsonify({'code': 200})


@app.route('/convert/<username>/<phone>')
def convert(username, phone):
    dir = f'/home/tarek/AndroidStudioProjects/breathe-out/assets/images/{username}/{phone}/'
    img3d = get_view(dir + 'dicom/')
    print(img3d.shape)
    for i in range(img3d.shape[0]):
        plt.imsave(dir + f'coronal/{i}.jpg', img3d[i, :, :].T, cmap='gray')
        plt.imsave(dir + f'sagittal/{i}.jpg', img3d[:, i, :].T, cmap='gray')
    return jsonify({'code': 200})


@app.route('/add_new_patient/<username>', methods=['post'])
def add_patient(username):
    data = json.loads(request.data)
    add_new_patient(username, data)
    return jsonify({'code': 200})


@app.route('/predict/<username>/<phone>')
def predict(username, phone):
    patient = get_patient(username, phone)
    print(patient.to_json())
    intersect = patient.first_fvc
    base_week = patient.fvcWeek
    # Percent 	Sex 	Ex-smoker 	Never-smoked 	Currently-smokes 	decade
    features = np.array([[base_week, patient.percent, patient.gender, (patient.status == 1), (patient.status == 0),
                          (patient.status == 2), patient.age // 10]]).astype(np.float32)
    res = []
    for i in range(1, 12):
        res.append(predict_fvc(intersect=intersect, base_week=base_week, current_week=1, features=features).item())
    return jsonify({'code': 200, 'content': res})


if __name__ == '_main_':
    app.run()




