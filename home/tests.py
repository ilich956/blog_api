from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from .models import Post
from .serializers import BlogSerializer

class MockBlogSerializer(BlogSerializer):
    def save(self):
        post = Post.objects.create(**self.validated_data)
        return post

class MockJWTAuthentication:
    def authenticate(self, request):
        return (request.user, None)


