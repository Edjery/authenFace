from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .serializers import AuthenFaceUserSerializer
from .models import AuthenFaceUser, Snapshot, UserImage, Website


@api_view()
def userList(request):
    queryset = AuthenFaceUser.objects.all()
    serializer = AuthenFaceUserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def user(request, id):
    authenFaceUser = get_object_or_404(AuthenFaceUser, pk=id)
    match request.method:
        case "GET":
            serializer = AuthenFaceUserSerializer(authenFaceUser)
            return Response(serializer.data)
        case "PUT":
            serializer = AuthenFaceUserSerializer(authenFaceUser, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        case _:
            return Response(status=status.HTTP_400_BAD_REQUEST)

