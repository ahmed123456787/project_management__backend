"""Views for the user"""

from rest_framework.generics import CreateAPIView , RetrieveUpdateAPIView
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class UserView (CreateAPIView):
    """Create a user"""
    serializer_class = UserSerializer
       

class ManagerUserView (RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]