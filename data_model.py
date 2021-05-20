import json


def patients_to_json(patients):
    res = []
    for patient in patients:
        res.append(patient.to_json())
    return res


def patients_from_json(patients):
    res = []
    for patient in patients:
        res.append(Patient.from_json(patient))

    return res


class Doctor:

    def __init__(self, name, email, username, phone_number, password, plan, patients):
        self.name = name
        self.email = email
        self.username = username
        self.phone_number = phone_number
        self.password = password
        self.plan = plan
        self.patients = patients

    # a function that map from json into doctor object
    @staticmethod
    def from_json(data):
        name = data['name']
        email = data['email']
        username = data['username']
        phone_number = data['phone_number']
        password = data['password']
        plan = data['plan']
        patients = patients_from_json(data['patients'])
        return Doctor(name, email, username, phone_number, password, plan, patients)

    def to_json(self, ):
        # code that map from object into json(dict)
        doctor = {

            'name': self.name,
            'email': self.email,
            'username': self.username,
            'phone_number': self.phone_number,
            'password': self.password,
            'plan': self.plan,
            'patients': patients_to_json(self.patients),
        }
        return doctor


'''patient class that contains all patient properties and also 
   contains a static method that map from json to patient object'''


class Patient:

    def __init__(self, name, phone_number, status, gender, firstFvc, age,
                 registered_date, axial, address, notes, fvcWeek, percent):
        self.name = name
        self.phone_number = phone_number
        self.status = status
        self.gender = gender
        self.first_fvc = firstFvc
        self.age = age
        self.first_fvc_date = firstFvc
        self.registered_date = registered_date
        self.address = address
        self.notes = notes
        self.percent = percent
        self.axial = axial
        self.fvcWeek = fvcWeek

    @staticmethod
    def from_json(data):
        name = data['name']
        phone_number = data['phone_number']
        status = data['status']
        gender = data['gender']
        age = data['age']
        address = data['address']
        registered_date = data['registered_date']
        axial = data['axial']
        notes = data['notes']
        firstFvc = data['first_fvc']
        fvcWeek = data['fvc_week']
        percent = data['percent']
        return Patient(name, phone_number, status, gender, firstFvc, age,
                       registered_date, axial, address, notes, fvcWeek, percent)

    def to_json(self, ):
        # code that map from object into json(dict)
        patient = {
            'name': self.name,
            'phone_number': self.phone_number,
            'status': self.status,
            'gender': self.gender,
            'age': self.age,
            'address': self.address,
            'registered_date': self.registered_date,
            'first_fvc': self.first_fvc,
            'axial': self.axial,
            'notes': self.notes,
            'fvc_week': self.fvcWeek,
            'percent': self.percent
        }
        return patient
