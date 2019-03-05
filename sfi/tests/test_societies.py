from sfi.server.models import Societies, Users
import json
import random

def test_societies(client, app):
    start_date = ["2014-7-9", "2010-8-7", "2007-6-9", "2012-4-1"]
    end_date = ["2019-5-1", "2018-11-9", "2017-7-9", "2019-1-1"]
    society_name = ["California Botanical Society", "Cardiac Electrophysiology Society", "Chinese-American Chemical Society"]
    membership_type = [True, False]
    num_inserts = 5
    
    for i in range(num_inserts):
        user_id = None
        with app.app_context():
            query = Users.query.all()
            for user in query:
                ident = user.id
                if Societies.query.filter_by(user_id=ident).first():
                    continue
                else:
                    user_id = ident
                    break

        response = client.post(
            '/profile/societies',
            data=json.dumps({
                "user_id": user_id,
                "start_date": random.choice(start_date),
                "end_date": random.choice(end_date),
                "society_name": random.choice(society_name),
                "membership_type": random.choice(membership_type),
            }),
            content_type='application/json'
        )

    print(f'resp: {response}')
    with app.app_context():
        query = Societies.query.all()
    assert len(query) >= num_inserts