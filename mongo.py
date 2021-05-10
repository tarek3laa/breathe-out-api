import pymongo as pymongo

from app import Doctor
from data_model import Patient

client = pymongo.MongoClient(
    "mongodb+srv://tarek:tarek@cluster0.zviss.mongodb.net/breath-out?retryWrites=true&w=majority")
db = client['breath-out']
collection = db['breath-out']


def insert_new_doctor(doctor):
    """
    insert new doctor into db
    :param doctor, an object of Doctor class
    """
    collection.insert(doctor.to_json())


def get_count(key, value):
    """
    :return the count of doctors that match the filter
    example to get the count of doctors that have name = tarek just call the function like that
    get_count('name','tarek')
    """
    return collection.count_documents({key: value})


def get_doctors_by(key, value):
    """:return all doctors that match the filter"""
    res = collection.find({key: value})
    doctors = []
    for doc in res:
        doctors.append(Doctor.from_json(doc))
    return doctors


def get_doctor_by(key, value):
    """:return just a one doctor that match the filter"""
    return collection.find_one({key: value})


def add_new_patient(username, patient):
    """
    :param username of the doctor
    :param patient an object of patient class
    
    """
    collection.update_one({'username': username}, {'$push': {'patients': patient.to_json()}})


def get_patient(user_name, phone_number):
    doctor = get_doctor_by('username', user_name)
    doctor = Doctor.from_json(doctor)
    for patient in doctor.patients:
        if patient.phone_number == phone_number:
            return patient