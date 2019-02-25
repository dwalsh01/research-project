from sfi.server.models import ProposalCall
import json
import random
def test_add_proposal(client, app):
    deadline_text = ["Rolling", "1/2/2020", "2/4/2019"]
    award_amount = ["90000", "20000", "30000", "500000", "2000000", "100000"]
    title = ["Frontiers for the Future ", "Brussels Conference Programme ",
    "SFI Discover Programme ", "SFI Research Centres ",
    "SFI Strategic Partnerships Programme"]
    short_text = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit",
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
    "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in"]
    text_description = ["voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    " Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
    "deserunt mollit anim id est laborum."]
    audience = ["Researchers", "Universities", "Scientfic Institutions"]
    eligibil_text = ["","","",""]
    emails = ["Sed", "eiusmod", "tempor", "incididunt", "labore", "dolore", "magna", "aliqua"]

    num_inserts = 5
    for i in range(num_inserts):
        response = client.post(
            '/calls/add',
            data=json.dumps({
                "deadline_text": random.choice(deadline_text),
                "deadline_time": str(random.randint(1,7)) + "years",
                "award_amount": random.choice(award_amount),
                "title": random.choice(title) + str(random.randint(1,7)),
                "short_text": random.choice(short_text),
                "text_description": random.choice(text_description),
                "target_audience": random.choice(audience),
                "eligibil_text": random.choice(eligibil_text),
                "duration": str(random.randint(1,7)) + "months",
                "report_guidelines": "Click here for a list of guidelines",
                "contact": random.choice(emails) + str(random.randint(0,999)) + "@email.com"
            }),
            content_type='application/json'
        )
    print(f'resp: {response}')
    with app.app_context():
        query = ProposalCall.query.all()
        assert len(query) >= num_inserts
