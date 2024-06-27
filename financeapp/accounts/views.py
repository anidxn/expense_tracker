from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# -------- for user registration -------
from .serializers import UserSerializer
from django.contrib.auth.models import User

# --------- For user login ---------
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

# ---------- for user logout -----------
"""     NOT required if DEFAULT Authentication class is SET GLOBALLY in Settings.py
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
"""
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# from .models import CustomUser

# ------------- USER REGISTRATION ---------------
@api_view(['POST']) #@api_view(['POST','GET'])
def register_user(request):

    if request.method == 'POST':

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # generate token here (optional)
            newuser = User.objects.get(username = serializer.data['username'])
            tokenobj, _ = Token.objects.get_or_create(user=newuser)

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                'payload' : serializer.data, 
                'token' : str(tokenobj)
                },
                status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
POST
http://localhost:8085/authapi/register/
{
    "username": "testuser", 
    "password": "testpassword", 
    "email": "test@example.com"
}
"""


# ----------------- LOGIN ------------------
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        """user = None
        if '@' in username:   # login by email
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user: # login by username"""
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

"""
POST
http://localhost:8085/authapi/login/

{
    "username": "testuser",
    "password": "testpassword"
}
"""

# ----------- LOGOUT ----------------
@api_view(['POST'])
# @authentication_classes([TokenAuthentication])  =>=>=> Not required if DEFAULT Authentication class is SET GLOBALLY in Settings.py
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            print("Supplied token for logout - "+ request.user.auth_token)
            # Delete the user's token to logout
            request.user.auth_token.delete()
            print("Logout success")
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
"""
POST
http://localhost:8085/authapi/logout/

Authorization: Token YOUR_AUTH_TOKEN"
"""
