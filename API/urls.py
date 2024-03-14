from django.urls import path
from rest_framework.routers import DefaultRouter

from .serializers import AuthenFaceUserSerializer
from .models import AuthenFaceUser
from . import views
from CameraApp import views as AppViews

router = DefaultRouter()
router.register('users', views.UsersViewSet)
router.register('snapshots', views.SnapshotViewSet)
router.register('websites', views.WebsiteViewSet)
router.register('dummy-users', views.DummyUserViewSet)

urlpatterns =  [
    path('websites/user/<int:user_id>', views.WebsiteListByUser.as_view(), name='webs-list'),
    path('snapshots/user/<int:user_id>', views.SnapshotListByUser.as_view(), name='snapshot-list-by-user'),
    path('register', AppViews.register_user, name='register_user'),  
    path('login', AppViews.login_user   , name='login_user'),  
] + router.urls