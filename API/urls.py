from django.urls import path

from . import views
from CameraApp import views as AppViews

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UsersViewSet)
router.register('snapshots', views.SnapshotViewSet)
router.register('websites', views.WebsiteViewSet)
router.register('dummy-users', views.DummyUserViewSet)

urlpatterns =  [
    path('websites/user/<int:userId>', views.WebsiteListByUser.as_view(), name='webs-list'),
    path('snapshots/user/<int:userId>', views.SnapshotListByUser.as_view(), name='snapshot-list-by-user'),
    path('login', AppViews.login_user   , name='login_user'),  
] + router.urls