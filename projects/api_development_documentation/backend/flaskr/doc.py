from flask import Blueprint, jsonify, request

doc_router = Blueprint('doc', __name__)
version = 'v1.0'


@doc_router.route(f'/api/{version}/categories', methods=['GET'])
def document_categories():
    """
    Query all categories
    """
    return jsonify({
        'success': True,
        'categories': [
            {
                "id": 1,
                "type": "Science"
            },
            {
                "id": 2,
                "type": "Art"
            },
            {
                "id": 3,
                "type": "Geography"
            },
            {
                "id": 4,
                "type": "History"
            },
            {
                "id": 5,
                "type": "Entertainment"
            },
            {
                "id": 6,
                "type": "Sports"
            }
        ]
    })


@doc_router.route(f'/api/{version}/questions', methods=['GET'])
def document_questions():
    """
    Query all question
    """
    return jsonify({'success': True,
                    'questions': [{"id": 1,
                                   "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
                                   "answer": "Apollo 13",
                                   "category": "5",
                                   "difficulty": 4},
                                  {"id": 2,
                                   "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
                                   "answer": "Tom Cruise",
                                   "category": "5",
                                   "difficulty": 4},
                                  {"id": 3,
                                   "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                                   "answer": "Maya Angelou",
                                   "category": "4",
                                   "difficulty": 2}],
                    'total_questions': 3,
                    'current_category': 1,
                    'categories': {"1": "Science",
                                   "2": "Art",
                                   "3": "Geography",
                                   "4": "History",
                                   "5": "Entertainment",
                                   "6": "Sports"}})


@doc_router.route(f'/api/{version}/questions', methods=['POST'])
def document_create_question():
    """
    Create a new question
    """
    return jsonify({
        'success': True,
        'created': 1
    })


@doc_router.route(f'/api/{version}/questions/<int:question_id>',
                  methods=['DELETE'])
def document_delete_question(question_id):
    """
    Delete a question
    """
    return jsonify({
        'success': True,
        'deleted': question_id
    })


@doc_router.route(f'/api/{version}/questions/search', methods=['POST'])
def document_search_question():
    """
    Search questions
    """
    return jsonify({
        'success': True,
        'questions': [
            {
                "id": 1,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
                "answer": "Apollo 13",
                "category": "5",
                "difficulty": 4
            }
        ]
    })


@doc_router.route(
    f'/api/{version}/categories/<int:category_id>/questions',
    methods=['GET'])
def document_get_questions_by_category(category_id):
    """
    Get questions by category
    """
    return jsonify({"current_category": "Science",
                    "questions": [{"id": 1,
                                   "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
                                   "answer": "Apollo 13",
                                   "category": "5",
                                   "difficulty": 4},
                                  {"id": 2,
                                   "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
                                   "answer": "Tom Cruise",
                                   "category": "5",
                                   "difficulty": 4}],
                    "success": True,
                    "total_questions": 2,
                    "current_category": "Science",
                    "categories": {"1": "Science",
                                   "2": "Art",
                                   "3": "Geography",
                                   "4": "History",
                                   "5": "Entertainment",
                                   "6": "Sports"}})


@doc_router.route(f'/api/{version}/quizzes', methods=['POST'])
def document_quizzes():
    """
    Get quizzes
    """
    return jsonify({
        "question": {
            "answer": "Apollo 13",
            "category": "5",
            "difficulty": 4,
            "id": 1,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        "success": True
    })
