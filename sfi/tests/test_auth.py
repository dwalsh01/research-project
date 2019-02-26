from sfi.server.models import Users
import json
import random

def generate_email():
    emails = ["Sed", "eiusmod", "tempor", "incididunt", "labore", "dolore", "magna", "aliqua"]
    return random.choice(emails) + str(random.randint(0,999)) + "@email.com"

def test_register(client, app):
    f_name = ["Darragh", "Tim", "Ahmad", "Kyle", "Noelie", "Matthew", "Mark", "Luke", "John"]
    l_name = ["Phelan","Walsh","Creedon","Tariq", "Quinlan", "Neylon","Miskella", "Casey"]
    job_title = ["Professor", "Bioloigist","Clinician","Technician","Physicist","Chemist","Engineer"]
    prefix = ["Rev", "Fr", "Mr", "Mrs", "Ms", "Dr", "Capt"]
    suffix = ["MSc", "PhD", "MD", "Esq", ""]
    num_inserts = 5
    num_duplicates = 0
    for i in range(num_inserts):
        test_email = generate_email()
        response = client.post(
            '/register',
            data=json.dumps({
                "first_name": random.choice(f_name),
                "second_name": random.choice(l_name),
                "job_title": random.choice(job_title),
                "prefix":  random.choice(prefix),
                "suffix": random.choice(suffix),
                "phone": str(random.randint(0,999)) +"-"+ str(random.randint(0,9999999)),
                "phone_extension": random.randint(0,999),
                "email": test_email,
                "password": "hashed",
                "orcid": str(random.randint(0,9999))+"-"+str(random.randint(0,9999))+"-"+str(random.randint(0,9999))+"-"+str(random.randint(0,9999))
            }),
            content_type='application/json'
        )

        print(f'resp: {response}')
        with app.app_context():
            query = Users.query.filter_by(email=test_email).all()
            table_length = Users.query.all()
            if len(query) > 1:
                num_duplicates += 1
            assert len(table_length) == (i + 1 - num_duplicates)
