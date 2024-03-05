from . import views
from CameraApp import views as AppViews
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register('users', views.UsersViewSet)
# router.register('user-images', views.UserImageViewSet)
router.register('snapshots', views.SnapshotViewSet)
router.register('websites', views.WebsiteViewSet)
router.register('dummy-users', views.DummyUserViewSet)

urlpatterns =  [
    path('register', AppViews.register_user, name='register_user'),  
    path('login', AppViews.login_user   , name='login_user'),  
] + router.urls
