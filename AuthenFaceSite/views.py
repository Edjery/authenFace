from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .serializers import AuthenFaceUserSerializer
from .models import AuthenFaceUser, Snapshot, UserImage, Website


@api_view(['GET', 'POST'])
def user_list(request):
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
def user(request, id):
    authenFaceUser = get_object_or_404(AuthenFaceUser, pk=id)
    match request.method:
        case 'GET':
            serializer = AuthenFaceUserSerializer(authenFaceUser)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'PUT':
            serializer = AuthenFaceUserSerializer(authenFaceUser, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(password=request.data.get('password'))
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'DELETE':
            authenFaceUser.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        case _:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

