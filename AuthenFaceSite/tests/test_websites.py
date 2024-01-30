from rest_framework import status
import pytest

@pytest.mark.django_db
class TestWebsite:
    # test POST method
    def test_post_a_website_and_return_201(self, create_website):
        assert create_website.status_code == status.HTTP_201_CREATED

    # test GET all method
    def test_get_all_website_and_return_200(self, api_client, website_endpoint):
        response = api_client.get(website_endpoint)
        assert response.status_code == status.HTTP_200_OK

    # test GET method
    def test_get_a_website_and_return_200(self, api_client, website_endpoint_with_id):
        response = api_client.get(website_endpoint_with_id)
        assert response.status_code == status.HTTP_200_OK

    # test PUT method
    def test_update_a_website_and_return_200(self, api_client, website_endpoint_with_id):
        new_details = { 
            'name': 'new Website',
            'url': 'https://new-example.com',
            'account_name': 'new_example_account',
        }
        response = api_client.patch(website_endpoint_with_id, new_details)
        assert response.data['name'] == new_details['name']
        assert response.status_code == status.HTTP_200_OK

    # test DELETE method
    def test_delete_a_user_and_return_204(self, api_client, website_endpoint_with_id):
        response = api_client.delete(website_endpoint_with_id)
        assert response.status_code == status.HTTP_204_NO_CONTENT