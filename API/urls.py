from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UsersViewSet)
router.register('snapshots', views.SnapshotViewSet)
router.register('websites', views.WebsiteViewSet)
router.register('dummy-users', views.DummyUserViewSet)

urlpatterns =  [
    path('websites/user/<int:userId>', views.WebsiteListByUser.as_view(), name='webs-list'),
    path('snapshots/user/<int:userId>', views.SnapshotListByUser.as_view(), name='snapshot-list-by-user'),
    path('login', views.login_user , name='login_user'),  
    path('authenticate/', views.authenticate_website, name='authenticate_website'),
    path('token/', views.TokenView.as_view(), name='token'),
] + router.urls