#Need to find a way to give admin role for this test to work
#Works when @roles_required removed from /api/nrp route in admin.py
from sfi.server.models import NrpArea
import json
import random

def test_nrp(client, app):
    nrp = ["Priority Area A - Future Networks & Communications","Priority Area B - Data Analytics, Management, Security & Privacy",
    "Priority Area C - Digital Platforms, Content & Applications","Priority Area D - Connected Health and Independent Living",
    "Priority Area E - Medical Devices","Priority Area F- Diagnostics","Priority Area G - Therapeutics: Synthesis, Formulation, Processing and Drug Delivery",
    "Priority Area H - Food for Health","Priority Area I - Sustainable Food Production and Processing",
    "Priority Area J - Marine Renewable Energy","Priority Area K - Smart Grids & Smart Cities","Priority Area L - Manufacturing Competitiveness",
    "Priority Area M - Processing Technologies and Novel Materials","Priority Area N - Innovation in Services and Business Processes",
     "Software", "Other"]
    num_inserts = 5
    for i in range(num_inserts):
        response = client.post(
            '/api/nrp',
            data=json.dumps({
                "nrp_title": random.choice(nrp)
            }),
            content_type='application/json'
        )

    print(f'resp: {response}')
    with app.app_context():
        query = NrpArea.query.all()
    assert len(query) >= num_inserts