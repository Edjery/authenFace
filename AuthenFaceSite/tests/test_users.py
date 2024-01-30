from rest_framework import status
import pytest

@pytest.mark.django_db
class TestUser:
    # test POST method
    def test_post_a_user_and_returning_201(self, create_user):
        assert create_user.status_code == status.HTTP_201_CREATED

    # test GET all method
    def test_get_all_user_and_returning_200(self, api_client, user_endpoint):
        response = api_client.get(user_endpoint)
        assert response.status_code == status.HTTP_200_OK

    # test GET method
    def test_get_a_user_and_returning_200(self, api_client, endpoint_with_id):
        response = api_client.get(endpoint_with_id)
        assert response.status_code == status.HTTP_200_OK

    # test PUT method
    def test_update_a_user_and_returning_200(self, api_client, endpoint_with_id):
        new_details = { 'password': '54321' }
        response = api_client.put(endpoint_with_id, new_details)
        assert response.data['password'] == new_details['password']
        assert response.status_code == status.HTTP_200_OK

    # test DELETE method
    def test_delete_a_user_and_returning_204(self, api_client, endpoint_with_id):
        response = api_client.delete(endpoint_with_id)
        assert response.status_code == status.HTTP_204_NO_CONTENT