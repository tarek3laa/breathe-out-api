import json


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
        patients = data['patients']
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
            'patients': self.patients,
        }
        return doctor


'''patient class that contains all patient properties and also 
   contains a static method that map from json to patient object'''


class Patient:

    def __init__(self, name, phone_number, status, gender, age, first_fvc=None, first_fvc_date=None,
                 registered_date=None, xRay_Url=None,
                 CT_Url=None, CT_date=None, address=None):
        self.name = name
        self.phone_number = phone_number
        self.status = status
        self.gender = gender
        self.first_fvc = first_fvc
        self.age = age
        self.first_fvc_date = first_fvc_date
        self.registered_date = registered_date
        self.xRay_Url = xRay_Url
        self.CT_Url = CT_Url
        self.CT_date = CT_date
        self.address = address

    @staticmethod
    def from_json(data):
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

    def to_json(self, ):
        # code that map from object into json(dict)
        patient = {
            'name': self.name,
            'phone_number': self.phone_number,
            'status': self.status,
            'gender': self.gender,
            'first_fvc': self.first_fvc,
            'age': self.age,
            'first_fvc_date': self.first_fvc_date,
            'registered_date': self.registered_date,
            'xRay_Url': self.xRay_Url,
            'CT_Url': self.CT_Url,
            'CT_date': self.CT_date,
            'address': self.address,
        }
        return patient
