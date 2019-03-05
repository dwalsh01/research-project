from sfi.server.models import Teams, Users, Funding
import json
import random

def test_teams(client, app):
    start_date = ["2014-7-9", "2010-8-7", "2007-6-9", "2012-4-1"]
    end_date = ["2019-5-1", "2018-11-9", "2017-7-9", "2019-1-1"]
    name = ["A-Team", "S.E.A.L Team Ricks", "Umbrella Academy", "Justice League", "Avengers"]
    position = ["Leader", "Follower", "Limerick", "Intern", "Senior Engineer", "Junior Engineer"]
    status = [True, False]
    num_inserts = 5

    for i in range(num_inserts):
        user_id = None
        primary_attribution = None
        with app.app_context():
            users_query = Users.query.all()
            funding_query = Funding.query.all()
            for user in users_query:
                ident = user.id
                if Teams.query.filter_by(person_id=ident).first():
                    continue
                else:
                    user_id = ident
                    break
            for fund in funding_query:
                ident = fund.id
                if Teams.query.filter_by(primary_attribution=ident).first():
                    continue
                else:
                    primary_attribution = ident
                    break

        response = client.post(
            '/profile/team',
            data=json.dumps({
                "person_id": user_id,
                "start_date": random.choice(start_date),
                "end_date": random.choice(end_date),
                "name": random.choice(name),
                "position": random.choice(position),
                "primary_attribution": primary_attribution
            }),
            content_type='application/json'
        )

    print(f'resp: {response.data}')
    with app.app_context():
        query = Teams.query.all()
    assert len(query) >= num_inserts
