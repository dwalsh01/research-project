from sfi.server.models import Funding, Users
import json
import random

def test_funding(client, app, auth):
    auth.login_researcher()
    start_date = ["2014-7-9", "2010-8-7", "2007-6-9", "2012-4-1"]
    end_date = ["2019-5-1", "2018-11-9", "2017-7-9", "2019-1-1"]
    funding_body = ["AHRC", "BBSRC", "EPSRC", "ESRC"]
    programme = ["Computer Science", "Biology", "Chemistry", "Physics", "Engineering", "Mathematics"]
    status = [True, False]
    num_inserts = 5

    for i in range(num_inserts):
        user_id = None
        with app.app_context():
            query = Users.query.all()
            for user in query:
                ident = user.id
                if Funding.query.filter_by(user_id=ident).first():
                    continue
                else:
                    user_id = ident
                    break

        response = client.post(
            '/profile/funding',
            data=json.dumps({
                "user_id": user_id,
                "start_date": random.choice(start_date),
                "end_date": random.choice(end_date),
                "funding_amt": round(random.uniform(10000,1000000), 1),
                "funding_body": random.choice(funding_body),
                "programme": random.choice(programme),
                "status": random.choice(status)
            }),
            content_type='application/json'
        )

    print(f'resp: {response}')
    with app.app_context():
        query = Funding.query.all()
    assert len(query) >= num_inserts
