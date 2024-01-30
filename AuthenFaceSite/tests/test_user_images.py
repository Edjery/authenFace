from rest_framework import status
import pytest

@pytest.mark.django_db
class TestUser:
    # test POST method
    def test_post_a_user_image_and_return_201(self, create_user_image):
        assert create_user_image.status_code == status.HTTP_201_CREATED

    # test GET all method
    def test_get_all_user_images_and_return_200(self, api_client, user_image_endpoint):
        response = api_client.get(user_image_endpoint)
        assert response.status_code == status.HTTP_200_OK

    # test GET method
    def test_get_a_user_image_and_return_200(self, api_client, user_image_endpoint_with_id):
        response = api_client.get(user_image_endpoint_with_id)
        assert response.status_code == status.HTTP_200_OK

    # test DELETE method
    def test_delete_a_user_image_and_return_204(self, api_client, user_image_endpoint_with_id):
        response = api_client.delete(user_image_endpoint_with_id)
        assert response.status_code == status.HTTP_204_NO_CONTENT