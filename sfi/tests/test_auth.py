from sfi.server.models import Users, Role
import json
import random


def test_add_user_types(client, app):
    types = ["researcher", "admin", "reviewer"]
    with app.app_context():
        query = Role.query.all()
        if len(query) != len(types):
            for type in types:
                new_type = Role(name=type)
                new_type.saveToDB()

        query = Role.query.all()
        assert len(query) == len(types)


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

        with app.app_context():
            query = Users.query.filter_by(email=test_email).first()
            assert query is not None and response.status_code == 201


def test_insert_users(client, app):
    f_name = ["Jeff", "Matthias", "Joe", "Al"]
    l_name = ["Jobs", "Wilson", "Johnson", "Cal"]
    job_title = ["SFI admin", "Test Researcher", "Test Reviewer 1", "Test Reviewer 2"]
    prefix = ["Mr"]
    suffix = ["PhD"]

    email = ["admin@sfi.com", "researcher@sfi.com", "reviewer1@sfi.com", "reviewer2@sfi.com"]
    roles = ["admin", "researcher", "reviewer", "reviewer"]
    for i in range(len(email)):
        data = {
            "f_name": random.choice(f_name),
            "l_name": random.choice(l_name),
            "job_title": job_title[i],
            "prefix":  random.choice(prefix),
            "suffix": random.choice(suffix),
            "phone": str(random.randint(0,999)) +"-"+ str(random.randint(0,9999999)),
            "phone_ext": random.randint(0,999),
            "email": email[i],
            "password": "hashed"
        }
        with app.app_context():
            # Initial check
            query = Users.query.filter_by(email=email[i]).first()
            if not query:
                user_type = Role.query.filter_by(name=roles[i]).first()
                data["roles"] = [user_type]
                admin = Users(**data)
                admin.saveToDB()

                query = Users.query.filter_by(email=email[i]).first()
                assert query is not None

