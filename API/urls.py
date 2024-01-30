from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UsersViewSet)
router.register('user-images', views.UserImageViewSet)
router.register('snapshots', views.SnapshotViewSet)
router.register('websites', views.WebsiteViewSet)
router.register('dummy-users', views.DummyUserViewSet)

urlpatterns = router.urls
