from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from .serializers import RegisterSerializer, LoginSerializer

class MockRegisterSerializer(RegisterSerializer):
    def save(self):
        return True

class MockLoginSerializer(LoginSerializer):
    def get_jwt_token(self, validated_data):
        return {'token': 'mocked_jwt_token'}

class RegisterViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('your_app.views.RegisterSerializer', MockRegisterSerializer)
    def test_register_view_success(self):
        url = 'api/accounts/register'
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('your_app.views.RegisterSerializer', MockRegisterSerializer)
    def test_register_view_failure(self):
        url = 'api/accounts/register'
        data = {}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('your_app.views.LoginSerializer', MockLoginSerializer)
    def test_login_view_success(self):
        url = '/your_login_url/'
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  

    @patch('your_app.views.LoginSerializer', MockLoginSerializer)
    def test_login_view_failure(self):
        url = '/your_login_url/'
        data = {}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
