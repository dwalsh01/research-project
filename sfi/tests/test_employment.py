from sfi.server.models import Employment, Users
import json
import random

def test_employment(client, app):
    institution = ["UCC", "UCD", "TCD", "DCU", "UL", "NUIG", "NUIM"]
    location = ["Cork", "Dublin", "Limerick", "Galway", "Maynooth"]
    num_inserts = 5
    for i in range(num_inserts):
        user_id = None
        with app.app_context():
            query = Users.query.all()
            for user in query:
                ident = user.id
                if Employment.query.filter_by(user_id=ident).first():
                    continue
                else:
                    user_id = ident
                    break

        
        response = client.post(
            '/profile/employment',
            data=json.dumps({
                "user_id": user_id,
                "institution": random.choice(institution),
                "location": random.choice(location),
                "years": round(random.uniform(1,15), 1)
            }),
            content_type='application/json'
        )

    print(f'resp: {response}')
    with app.app_context():
        query = Employment.query.all()
    assert len(query) >= num_inserts