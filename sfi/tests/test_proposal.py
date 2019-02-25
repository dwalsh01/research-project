from sfi.server.models import ProposalCall
import json

def test_add_proposal(client, app):

    response = client.post(
        'api/calls/add',
        data=json.dumps({
            "deadline_text": "Rolling",
            "deadline_time": "1 month",
            "award_amount": "Up to 40,000",
            "title": "Slick new program",
            "short_text": "A really nice programme",
            "text_description": "I'll update this later.",
            "target_audience": "Researchers",
            "eligibil_text": "none, really",
            "duration": "3 days",
            "report_guidelines": "please look at pdf",
            "contact": "test@email.com"
        }),
        content_type='application/json'
    )

    print(f'resp: {response}')
    with app.app_context():
        query = ProposalCall.query.first()
        print(f'q: {query}')

def test_edit_prop(client, app):
    pass

def test_apply_draft(client, app):
    pass

def test_apply_submit(client, app):
    pass


