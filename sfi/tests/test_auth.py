from sfi.server.models import Users

def test_register(client, app):
    test_email = 'hola@ytree.com'

    response = client.post(
        '/register',
        data={
            'first_name': 'Mattias',
            'second_name': 'Wilson',
            'job_title': 'Researcher',
            'prefix':  'Mr',
            'suffix': 'III',
            'phone': '082-4593822',
            'phone_extension': '353',
            'email': test_email,
            'password': 'hashed',
            'orcid': '0000-0002-0141-7356'
        },
        content_type='application/json'
    )

    print(f'resp: {response}')
    with app.app_context():
        query = Users.query.filter_by(email=test_email).first()
        print(f'q: {query}')
