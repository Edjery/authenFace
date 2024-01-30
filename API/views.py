from rest_framework.viewsets import ModelViewSet
from .serializers import AuthenFaceUserSerializer, UserImageSerializer, SnapshotSerializer, WebsiteSerializer, DummyUserSerializer
from .models import AuthenFaceUser, UserImage, Snapshot, Website, DummyUser

class UsersViewSet(ModelViewSet): 
    queryset = AuthenFaceUser.objects.all()
    serializer_class = AuthenFaceUserSerializer

class UserImageViewSet(ModelViewSet): 
    queryset = UserImage.objects.all()
    serializer_class = UserImageSerializer

class SnapshotViewSet(ModelViewSet): 
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer

class WebsiteViewSet(ModelViewSet): 
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer

class DummyUserViewSet(ModelViewSet): 
    queryset = DummyUser.objects.all()
    serializer_class = DummyUserSerializer