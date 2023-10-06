import json
import pytest
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db
from logger import Logger
from settings import DB_USER, DB_PASSWORD

logger = Logger.get_logger(__name__)

app = create_app(test=True)
app.config['TESTING'] = True
database_name = "trivia_test"
database_path = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER,
    DB_PASSWORD,
    'localhost:5432',
    database_name
)
setup_db(app=app, database_path=database_path)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200


def test_get_categories(client):
    response = client.get('/categories')
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 200
    assert list(data['categories'].values()) == [
        'Science', 'Art', 'Geography', 'History', 'Entertainment', 'Sports'
    ]
    assert data['success']


def test_get_questions(client):
    response = client.get('/questions')
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 200
    assert data['success']
    assert data['questions']


def test_create_question(client):
    response = client.post('/questions', json={
        'question': 'What is the capital of Germany?',
        'answer': 'Berlin',
        'category': '3',
        'difficulty': 1
    })
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 200
    assert data['success']


def test_delete_question(client):
    response = client.delete('/questions/5')
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 200
    assert data['success']


def test_delete_question_not_found(client):
    response = client.delete('/questions/1000')
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 404
    assert not data['success']


def test_search_questions(client):
    response = client.post('/questions/search', json={
        'searchTerm': 'Tim Burton'
    })
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 200
    assert data['success']
    assert data['questions']


def test_get_questions_by_category(client):
    response = client.get('/categories/1/questions')
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 200
    assert data['success']
    assert data['questions']


def test_get_questions_by_category_not_found(client):
    response = client.get('/categories/1000/questions')
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 404
    assert not data['success']


def test_quiz(client):
    response = client.post('/quizzes', json={
        'previous_questions': [],
        'quiz_category': {
            'id': 1,
            'type': 'Science'
        }
    })
    data = json.loads(response.data)
    logger.info(data)
    assert response.status_code == 200
    assert data['success']
    assert data['question']
