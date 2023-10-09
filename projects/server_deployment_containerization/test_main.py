'''
Tests for jwt flask app.
'''
import os
import json
import pytest

import main

SECRET = 'KhoiVN-secret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTc5NjUyNjcsIm5iZiI6MTY5Njc1NTY2NywiZW1haWwiOiJraG9pdm5AZW1haWwuY29tIn0.hZr2RQqnroNdly_j9yRKpO7Z6yEwx7pNleFfB25IjHs'
EMAIL = 'khoivn@email.com'
PASSWORD = 'mypwd'


@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()
    yield client


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post(
        '/auth',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None
