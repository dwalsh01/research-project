from sfi.server.models import Education, Users
import json
import random

def test_education(client, app):
    degree = ["Associate's degree", "Bachelor's degree", "Master's degree", "Doctoral degree"]
    field_of_study = ["Computer Science", "Biology", "Chemistry", "Physics", "Engineering", "Mathematics"]
    institution = ["UCC", "UCD", "TCD", "DCU", "UL", "NUIG", "NUIM"]
    location = ["Cork", "Dublin", "Limerick", "Galway", "Maynooth"]
    year_degree_award = ["2014-1-1", "2010-1-1", "2007-1-1", "2012-1-1"]
    num_inserts = 5
    for i in range(num_inserts):
        user_id = None
        with app.app_context():
            query = Users.query.all()
            for user in query:
                ident = user.id
                if Education.query.filter_by(user_id=ident).first():
                    continue
                else:
                    user_id = ident
                    break

        response = client.post(
            '/profile/education',
            data=json.dumps({
                "user_id": user_id,
                "degree": random.choice(degree),
                "field_of_study": random.choice(field_of_study),
                "institution": random.choice(institution),
                "location": random.choice(location),
                "year_degree_award": random.choice(year_degree_award)
            }),
            content_type='application/json'
        )

    print(f'resp: {response}')
    with app.app_context():
        query = Education.query.all()
    assert len(query) >= num_inserts