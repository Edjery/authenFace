from rest_framework.test import APIClient
from rest_framework import status

class TestUser:
    def test_posting_user_and_returning_404(self):
        client = APIClient()
        newUser = { 'email': 'ed@gmail.com', 'passowrd': '12345' }
        response = client.post('AuthenFaceSite/users', newUser)

        assert response.status_code == status.HTTP_404_NOT_FOUND