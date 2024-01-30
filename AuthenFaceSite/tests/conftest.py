from rest_framework.test import APIClient
import pytest

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_endpoint() -> str:
    return '/authenface/users/'

@pytest.fixture
def new_user_data() -> dict:
    return { 'email': 'edje@gmail.com', 'password': '12345' }

@pytest.fixture
def create_user(api_client, user_endpoint, new_user_data):
    response = api_client.post(user_endpoint, new_user_data)
    return response

@pytest.fixture
def endpoint_with_id(user_endpoint, create_user) -> str:
    return f'{user_endpoint}{create_user.data['id']}/'