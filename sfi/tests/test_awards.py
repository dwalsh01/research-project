from sfi.server.models import Awards, Users
import json
import random

def test_awards(client, app, auth):
    auth.login_researcher()

    degree = ["Associate's degree", "Bachelor's degree", "Master's degree", "Doctoral degree"]
    awarding_body = ["SFI", "IICT", "PYF", "JKLOL", "IDC", "IDK"]
    award_details = ["Award for staying awake", "Award for Excellence in Existence", "Award for Participation"]
    num_inserts = 5
    for i in range(num_inserts):
        user_id = None
        with app.app_context():
            query = Users.query.all()
            for user in query:
                ident = user.id
                if Awards.query.filter_by(user_id=ident).first():
                    continue
                else:
                    user_id = ident
                    break

        response = client.post(
            '/profile/awards',
            data=json.dumps({
                "user_id": user_id,
                "year": random.randint(2000,2019),
                "awarding_body": random.choice(awarding_body),
                "award_details": random.choice(award_details)
            }),
            content_type='application/json'
        )

    print(f'resp: {response}')
    with app.app_context():
        query = Awards.query.all()
    assert len(query) >= num_inserts
