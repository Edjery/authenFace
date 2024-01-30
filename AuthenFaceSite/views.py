from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .serializers import AuthenFaceUserSerializer, UserImageSerializer, SnapshotSerializer, WebsiteSerializer
from .models import AuthenFaceUser, UserImage, Snapshot, Website

class UsersAPI:
    @api_view(['GET', 'POST'])
    def manage_all(request):
        match request.method:
            case 'GET':
                queryset = AuthenFaceUser.objects.all()
                serializer = AuthenFaceUserSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            case 'POST':
                serializer = AuthenFaceUserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            case _:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @api_view(['GET', 'PUT', 'DELETE'])
    def manage(request, id):
        authen_face_user = get_object_or_404(AuthenFaceUser, pk=id)
        match request.method:
            case 'GET':
                serializer = AuthenFaceUserSerializer(authen_face_user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            case 'PUT':
                serializer = AuthenFaceUserSerializer(authen_face_user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save(password=request.data.get('password'))
                return Response(serializer.data, status=status.HTTP_200_OK)
            case 'DELETE':
                authen_face_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            case _:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserImagesAPI:
    @api_view(['GET', 'POST'])
    def manage_all(request):
        match request.method:
            case 'GET':
                queryset = UserImage.objects.all()
                serializer = UserImageSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            case 'POST':
                serializer = UserImageSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            case _:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @api_view(['GET', 'DELETE'])
    def manage(request, id):
        user_image = get_object_or_404(UserImage, pk=id)
        match request.method:
            case 'GET':
                serializer = UserImageSerializer(user_image)
                return Response(serializer.data, status=status.HTTP_200_OK)
            case 'DELETE':
                user_image.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            case _:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SnapshotsAPI:
    @api_view(['GET', 'POST'])
    def manage_all(request):
        match request.method:
            case 'GET':
                queryset = Snapshot.objects.all()
                serializer = SnapshotSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            case 'POST':
                serializer = SnapshotSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            case _:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @api_view(['GET', 'DELETE'])
    def manage(request, id):
        snapshot = get_object_or_404(Snapshot, pk=id)
        match request.method:
            case 'GET':
                serializer = SnapshotSerializer(snapshot)
                return Response(serializer.data, status=status.HTTP_200_OK)  
            case 'DELETE':
                snapshot.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            case _:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
                
class WebsiteAPI:
    @api_view(['GET', 'POST'])
    def manage_all(request):
        match request.method:
            case 'GET':
                queryset = Website.objects.all()
                serializer = WebsiteSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            case 'POST':
                serializer = WebsiteSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            case _:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @api_view(['GET', 'PUT', 'DELETE'])
    def manage(request, id):
        website = get_object_or_404(Website, pk=id)
        match request.method:
            case 'GET':
                serializer = WebsiteSerializer(website)
                return Response(serializer.data, status=status.HTTP_200_OK)  
            case 'PUT':
                serializer = WebsiteSerializer(website, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            case 'DELETE':
                website.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            case _:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
