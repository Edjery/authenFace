from rest_framework.test import APIClient
import pytest

@pytest.fixture
def api_client():
    return APIClient()

# users
@pytest.fixture
def user_endpoint() -> str:
    return '/authenface/users/'

@pytest.fixture
def new_user_data() -> dict:
    return { 'email': 'edje@gmail.com', 'password': '12345' }

@pytest.fixture
def create_user(api_client, user_endpoint, new_user_data):
    return api_client.post(user_endpoint, new_user_data)

@pytest.fixture
def user_endpoint_with_id(user_endpoint, create_user) -> str:
    return f'{user_endpoint}{create_user.data['id']}/'

# user images
@pytest.fixture
def user_image_endpoint() -> str:
    return '/authenface/user-images/'

@pytest.fixture
def new_user_image_data(create_user) -> dict:
    return { 'name': 'example_image', 'user': create_user.data['id'] }

@pytest.fixture
def create_user_image(api_client, user_image_endpoint, new_user_image_data):
    return api_client.post(user_image_endpoint, new_user_image_data)

@pytest.fixture
def user_image_endpoint_with_id(user_image_endpoint, create_user_image) -> str:
    return f'{user_image_endpoint}{create_user_image.data['id']}/'