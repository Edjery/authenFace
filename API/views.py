import os
import jwt
import requests

from datetime import datetime, timedelta

import django.contrib.auth.password_validation as validators
from django.conf import settings
from django.core import exceptions
from django.core.files import File
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, redirect

from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView

from .pagination import DefaultPagination
from .serializers import AuthenFaceUserSerializer, SnapshotSerializer, WebsiteSerializer, DummyUserSerializer
from .models import AuthenFaceUser, Snapshot, Website, DummyUser

from CameraApp.views import index as camera

# TODO add a view template to list all apis

def generate_jwt_token(user_id, email, expiration_time_minutes = 30):
    expiration_time = datetime.now() + timedelta(minutes=expiration_time_minutes)
    payload = {'id': user_id, 'email': email, 'exp' : expiration_time}
    jwt_token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return jwt_token

class UsersViewSet(ModelViewSet): 
    queryset = AuthenFaceUser.objects.all()
    serializer_class = AuthenFaceUserSerializer

    def create(self, request, *args, **kwargs):
        imageFile = request.data.get('userImage')
        password = request.data.get('password')
    
        if password != request.data.get('confirmPassword'):
            return Response({'error' : 'password did not match'}, status=status.HTTP_400_BAD_REQUEST)          
        try:
            validators.validate_password(password)
        except exceptions.ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        userInput = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': password,
            'image': imageFile
        }

        serializer = AuthenFaceUserSerializer(data=userInput)

        if serializer.is_valid() and imageFile:
            user = serializer.create(serializer.validated_data)
            token = generate_jwt_token(user.id, user.email)
            userData = {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
            return Response({'message': 'User registered successfully', 'token': token, 'userData': userData}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnapshotViewSet(ModelViewSet): 
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer
    pagination_class = DefaultPagination

class WebsiteViewSet(ModelViewSet): 
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    pagination_class = DefaultPagination

class DummyUserViewSet(ModelViewSet): 
    queryset = DummyUser.objects.all()
    serializer_class = DummyUserSerializer

class WebsiteListByUser(generics.ListCreateAPIView):
    serializer_class = WebsiteSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        userId = self.kwargs.get('userId') 
        if userId is not None:
            return Website.objects.filter(user=userId)
        else:
            return Website.objects.all()
    
class SnapshotListByUser(generics.ListAPIView):
    serializer_class = SnapshotSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        fileImageName = 'EJ.png_temp_image_20240315015853.png'
        userId = self.kwargs.get('userId') 
        if userId is not None:
            user = AuthenFaceUser.objects.get(id=userId)
            # generate_snapshot(fileImageName, user)
            return Snapshot.objects.filter(user=userId)
        else:
            return Snapshot.objects.all()

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_object_or_404(AuthenFaceUser, email=email)

        if user and check_password(password, user.password):
            token = generate_jwt_token(user.id, user.email)
            userData = {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
            return Response({'message': 'User sign in successfully', 'token' : token, 'userData' : userData}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
def generate_snapshot(imageFilename, user):
    imagePath = os.path.join(settings.MEDIA_ROOT, 'TempImages', imageFilename)
    
    if not os.path.exists(imagePath):
        print(f"Image file '{imageFilename}' not found in MEDIA_ROOT.")
        return None
    
    with open(imagePath, 'rb') as imageFIle:
        snapshot = Snapshot(name=imageFilename, user=user)
        snapshot.image.save(imageFilename, File(imageFIle))
        snapshot.save()
        
        return snapshot

@api_view(['GET'])
def authenticate_website(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        redirect_url = request.GET.get('redirect_url')

        print('email', email, redirect_url)
        data = {
            'email': email,
            'redirect_url': redirect_url
        }

        required_inputs = ['email', 'redirect_url']
        missing_inputs = [field for field in required_inputs if request.GET.get(field) == None]
        print(missing_inputs)

        if missing_inputs:
            return Response({"error": "Missing input data", "missing_inputs": missing_inputs}, status=400)

        return camera(request, data)
    return Response({"error": "Method Not Allowed"}, status=405)
from django.shortcuts import redirect

def generate_token(user: AuthenFaceUser, redirect_url):
    token = generate_jwt_token(user.id, user.email)
    userData = {
        'id': user.id,
        'email': user.email,
        'name': user.name
    }

    redirect_url_with_token = f"{redirect_url}?token={token}"
    return redirect_url_with_token


@api_view(['POST'])
def forward_to_external_api(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        website_url = request.POST.get('websiteUrl')
        website_api = 'http://localhost:3000/api/authenFace'

        data_to_send = {
            'email': email,
            'password': password,
            'websiteUrl': website_url,
            'websiteAPI': website_api
        }

        try:
            response = requests.post(website_api, json=data_to_send)
            data = response.json()

            if 'redirectURL' in data:
                print(data['redirectURL'])
                return redirect(data['redirectURL'])    
            elif 'error' in data:
                return Response({"error": data['error']}, status=response.status_code)
            return Response({"error": "missing redirectURL"}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to connect to external API", "message": str(e)}, status=500)

    # Return response for invalid HTTP method
    return Response({"error": "Method Not Allowed"}, status=405)

class AuthorizeView(APIView):
    def get(self, request):
        scope = request.GET.get('scope')
        redirect_uri = request.GET.get('redirect_uri')
        state = request.GET.get('state')
        if redirect_uri:
            redirect_uri_with_state = f"{redirect_uri}?state={state}&scope={scope}"
            return redirect(redirect_uri_with_state)
        else:
            return Response({"error": "redirect_uri not provided"}, status=400)

class TokenView(APIView):
    def post(self, request):
        id = request.data.get('id')
        email = request.data.get('email')
        name = request.data.get('name')

        token = generate_jwt_token(id, email)
        userData = {
            'id': id,
            'email': email,
            'name': name
        }

        return Response({'message': 'User registered successfully', 'token' : token, 'userData' : userData}, status=status.HTTP_201_CREATED)
        
        # return Response({
        #     "access_token":"gho_16C7e42F292c6912E7710c838347Ae178B4a",
        #     "scope":"repo,gist",
        #     "token_type":"bearer"
        # })

        # code = request.GET.get('code')
        # state = request.GET.get('state')
        # redirect_uri = request.GET.get('redirect_uri')

        # if not code:
        #     return Response({"error": "code not provided"}, status=400)
        # if not redirect_uri:
        #     return Response({"error": "redirect_uri not provided"}, status=400)

        # # Perform token exchange with authorization server
        # token_endpoint = 'http://localhost:8000/api/token/'  # Adjust this to your token endpoint
        # client_id = 'AuthenFace'  # Your client ID
        # client_secret = 'your_client_secret'  # Your client secret
        # data = {
        #     'grant_type': 'authorization_code',
        #     'code': code,
        #     'redirect_uri': redirect_uri,
        #     'client_id': client_id,
        #     'client_secret': client_secret,
        # }

        # response = requests.post(token_endpoint, data=data)
        # if response.status_code == 200:
        #     # Redirect to the provided redirect URI with access token as query parameter
        #     # access_token = response.json().get('access_token')
        #     access_token = 'asdsdaACCESSTOKENasdasd'
        #     redirect_uri_with_token = f"{redirect_uri}?state={state}&access_token={access_token}"
        #     return redirect(redirect_uri_with_token)
        # else:
        #     return Response({"error": "Failed to obtain access token"}, status=response.status_code)
        
class UserView(APIView):
    def get(self, request):

        response = requests.post("http://localhost:3000/api/login/", data={  
            "email": "mikasa@gmail.com",
            "password": "mikasa@gmail.com"
        })

        print('response', response)
        
        return Response({"profile": response})
         
class WellKnownView(APIView):
    def get(self, request):
        
        return Response(
            {
                "issuer": "https://accounts.google.com",
                "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
                "device_authorization_endpoint": "https://oauth2.googleapis.com/device/code",
                "token_endpoint": "https://oauth2.googleapis.com/token",
                "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
                "revocation_endpoint": "https://oauth2.googleapis.com/revoke",
                "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
                "response_types_supported": [
                "code",
                "token",
                "id_token",
                "code token",
                "code id_token",
                "token id_token",
                "code token id_token",
                "none"
                ],
                "subject_types_supported": [
                "public"
                ],
                "id_token_signing_alg_values_supported": [
                "RS256"
                ],
                "scopes_supported": [
                "openid",
                "email",
                "profile"
                ],
                "token_endpoint_auth_methods_supported": [
                "client_secret_post",
                "client_secret_basic"
                ],
                "claims_supported": [
                "aud",
                "email",
                "email_verified",
                "exp",
                "family_name",
                "given_name",
                "iat",
                "iss",
                "name",
                "picture",
                "sub"
                ],
                "code_challenge_methods_supported": [
                "plain",
                "S256"
                ],
                "grant_types_supported": [
                "authorization_code",
                "refresh_token",
                "urn:ietf:params:oauth:grant-type:device_code",
                "urn:ietf:params:oauth:grant-type:jwt-bearer"
                ]
            }

        )
    
