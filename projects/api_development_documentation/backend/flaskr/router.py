import random
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from models import Category, Question
from logger import Logger
from config import QUESTIONS_PER_PAGE

category_router = Blueprint('category', __name__)
question_router = Blueprint('question', __name__)
logger = Logger.get_logger(__name__)


def paginate_questions(selection):
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


@category_router.route('/categories', methods=['GET'])
def get_categories():
    """Create an endpoint to handle GET requests for all available categories."""
    logger.info('Requesting categories')
    current_categories = paginate_questions(
        Category.query.all()
    )

    if len(current_categories) == 0:
        abort(404)

    final_categories = {}
    for x in current_categories:
        final_categories.update({x['id']: x['type']})
    return jsonify({
        'success': True,
        'categories': final_categories
    })


@question_router.route('/questions', methods=['GET'])
def get_questions():
    """Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, categories.
    """
    logger.info('Requesting questions')
    questions = Question.query.all()
    formatted_questions = paginate_questions(
        questions
    )
    current_categories = [category.format()
                          for category in Category.query.all()]
    final_categories = {}
    for x in current_categories:
        final_categories.update({x['id']: x['type']})

    return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(questions),
        'current_category': 1,
        'categories': final_categories
    })


@question_router.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Create an endpoint to DELETE question using a question ID."""
    logger.info(f'Requesting question {question_id}')
    question = Question.query.get(question_id)
    logger.info(f'Question: {question}')
    if question is None:
        return abort(404)
    question.delete()
    return jsonify({
        'success': True,
        'deleted': question_id
    })


@question_router.route('/questions', methods=['POST'])
def create_question():
    """Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """
    logger.info('Creating question')
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')
    category = data.get('category')
    difficulty = data.get('difficulty')
    if not question or not answer or not category or not difficulty:
        abort(400)
    question = Question(
        question=question,
        answer=answer,
        category=category,
        difficulty=difficulty)
    question.insert()
    return jsonify({
        'success': True,
        'created': question.id
    })


@question_router.route('/questions/search', methods=['POST'])
def search_questions():
    """Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """
    logger.info('Searching questions')
    data = request.get_json()
    search_term = data.get('searchTerm')
    if not search_term:
        abort(400)
    questions = Question.query.filter(
        Question.question.ilike(f'%{search_term}%')).all()
    formatted_questions = [question.format() for question in questions]
    return jsonify({
        'success': True,
        'questions': formatted_questions
    })


@question_router.route('/categories/<int:category_id>/questions',
                       methods=['GET'])
def get_questions_by_category(category_id):
    """Create a GET endpoint to get questions based on category."""
    logger.info(f'Requesting questions for category {category_id}')
    current_category = Category.query.get(category_id)
    if current_category is None:
        abort(404)

    questions = Question.query.filter(Question.category == category_id).all()
    logger.info(f'Questions: {questions}')
    if not questions:
        return abort(404)
    formatted_questions = [question.format() for question in questions]
    return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(formatted_questions),
        'current_category': current_category.format(),
        'categories': [category.format() for category in Category.query.all()]
    })


@question_router.route('/quizzes', methods=['POST'])
def play_quiz():
    """Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    logger.info('Playing quiz')
    data = request.get_json()
    previous_questions = data.get('previous_questions')
    quiz_category = data.get('quiz_category')
    if not quiz_category:
        abort(400)
    category_id = quiz_category.get('id')
    if category_id == 0:
        questions = Question.query.all()
    else:
        questions = Question.query.filter(
            Question.category == category_id).all()
    formatted_questions = [question.format() for question in questions]
    if previous_questions:
        formatted_questions = [question for question in formatted_questions if question.get(
            'id') not in previous_questions]
    if len(formatted_questions) == 0:
        return jsonify({
            'success': False
        })
    question = random.choice(formatted_questions)
    return jsonify({
        'success': True,
        'question': question
    })


@category_router.errorhandler(404)
@question_router.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found'
    }), 404


@category_router.errorhandler(422)
@question_router.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
    }), 422
