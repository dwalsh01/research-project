'''
Very basic initial tests.
Some of these tests aren't that useful.
(Page can return code 200 and still have problems)

Tests to add:
    authorisation related tests

'''

def test_init(app):
    assert app.testing

def test_serve_root(client):
    response = client.get('/')
    assert response.status_code == 200

def test_serve_index(client):
    response = client.get('/index.html')
    assert response.status_code == 200
