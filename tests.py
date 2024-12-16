import pytest
from rest_framework.test import APIClient
from rest_framework import status
from forms.models import Form, Question, Answer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_form(api_client):
    """Test creating a form with valid and invalid inputs."""

    # Valid input
    response = api_client.post('/api/forms/', {'title': 'Valid Form Title'})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Valid Form Title'
    print("Test Create Form (Valid Input) Passed")

    # Invalid input (title exceeds max length)
    response = api_client.post('/api/forms/', {'title': 'A' * 101})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'title' in response.data
    print("Test Create Form (Invalid Input) Passed")


@pytest.mark.django_db
def test_create_question(api_client):
    """Test creating a question with valid and invalid inputs."""

    # Create a form for the question
    form = Form.objects.create(title="Sample Form")

    # Valid input
    valid_data = {
        'form': {'id': form.id, 'title': form.title},
        'text': 'What is your name?',
        'required': True,
        'question_type': 'short_text',
        'max_length': 100
    }
    response = api_client.post('/api/questions/', valid_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['text'] == 'What is your name?'
    print("Test Create Question (Valid Input) Passed")

    # Invalid input (max_length exceeds limit for short_text)
    invalid_data = valid_data.copy()
    invalid_data['max_length'] = 300
    response = api_client.post('/api/questions/', invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'max_length' in response.data
    print("Test Create Question (Invalid Input) Passed")


@pytest.mark.django_db
def test_create_answer(api_client):
    """Test creating an answer with valid and invalid inputs."""

    # Create a form and a question for the answer
    form = Form.objects.create(title="Sample Form")
    question = Question.objects.create(
        form=form,
        text="What is your age?",
        required=True,
        question_type="number",
        min_value=10,
        max_value=50
    )

    # Valid input
    valid_data = {'question': question.id, 'numeric_answer': 25}
    response = api_client.post('/api/answers/', valid_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['numeric_answer'] == 25
    print("Test Create Answer (Valid Input) Passed")

    # Invalid input (numeric_answer out of range)
    invalid_data = {'question': question.id, 'numeric_answer': 5}
    response = api_client.post('/api/answers/', invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    print("Test Create Answer (Invalid Input) Passed")


@pytest.mark.django_db
def test_retrieve_form(api_client):
    """Test retrieving a form by ID."""
    # Create a form
    form = Form.objects.create(title="Sample Form")
    response = api_client.get(f'/api/forms/{form.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == form.title
    print("Test Retrieve Form Passed")


@pytest.mark.django_db
def test_retrieve_questions(api_client):
    """Test retrieving questions for a specific form."""
    # Create a form and a question
    form = Form.objects.create(title="Sample Form")
    Question.objects.create(
        form=form,
        text="What is your age?",
        required=True,
        question_type="number"
    )
    response = api_client.get(f'/api/forms/{form.id}/questions/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['text'] == "What is your age?"
    print("Test Retrieve Questions Passed")






#----------------------------------------------------------------------------
# import pytest
# from rest_framework.test import APIClient
# from rest_framework import status
# from forms.models import Form, Question
#
# # Helper function to create a sample form
# @pytest.fixture
# def sample_form():
#     return Form.objects.create(title="Sample Form")
#
# @pytest.fixture
# def api_client():
#     return APIClient()
#
# # Test for Form APIs
# @pytest.mark.django_db
# def test_create_form(api_client):
#     # Valid input
#     response = api_client.post('/api/forms/', {'title': 'Test Form'})
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['title'] == 'Test Form'
#     print("Test Create Form (Valid Input) Passed")
#
#     # Invalid input (title too long)
#     response = api_client.post('/api/forms/', {'title': 'A' * 101})
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert 'title' in response.data
#     print("Test Create Form (Invalid Input) Passed")
#
# @pytest.mark.django_db
# def test_retrieve_form(api_client, sample_form):
#     response = api_client.get(f'/api/forms/{sample_form.id}/')
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['title'] == sample_form.title
#     print("Test Retrieve Form Passed")
#
# # Test for Question APIs
# @pytest.mark.django_db
# def test_create_question(api_client, sample_form):
#     # Valid input
#     valid_data = {
#         'form': {'id': sample_form.id, 'title': sample_form.title},
#         'text': 'What is your name?',
#         'required': True,
#         'question_type': 'short_text',
#         'max_length': 100
#     }
#     response = api_client.post('/api/questions/', valid_data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['text'] == 'What is your name?'
#     print("Test Create Question (Valid Input) Passed")
#
#     # Invalid input (max_length exceeds limit for short_text)
#     invalid_data = valid_data.copy()
#     invalid_data['max_length'] = 300
#     response = api_client.post('/api/questions/', invalid_data, format='json')
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert 'max_length' in response.data
#     print("Test Create Question (Invalid Input) Passed")
#
# @pytest.mark.django_db
# def test_retrieve_questions(api_client, sample_form):
#     # Add sample question
#     Question.objects.create(
#         form=sample_form,
#         text="What is your age?",
#         required=True,
#         question_type="number",
#         max_length=None
#     )
#     response = api_client.get(f'/api/forms/{sample_form.id}/questions/')
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) == 1
#     assert response.data[0]['text'] == "What is your age?"
#     print("Test Retrieve Questions Passed")
#
# # Test for Answer APIs
# @pytest.mark.django_db
# def test_create_answer(api_client, sample_form):
#     # Create question
#     question = Question.objects.create(
#         form=sample_form,
#         text="What is your age?",
#         required=True,
#         question_type="number"
#     )
#
#     # Valid input
#     valid_data = {
#         'question': question.id,
#         'numeric_answer': 25
#     }
#     response = api_client.post('/api/answers/', valid_data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['numeric_answer'] == 25
#     print("Test Create Answer (Valid Input) Passed")
#
#     # Invalid input (numeric_answer out of range)
#     invalid_data = {
#         'question': question.id,
#         'numeric_answer': -5  # Assuming validation fails for negative answers
#     }
#     response = api_client.post('/api/answers/', invalid_data, format='json')
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     print("Test Create Answer (Invalid Input) Passed")
#
#
#
#
#


















