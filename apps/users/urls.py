from rest_framework.routers import SimpleRouter
from .views import UserViewSet

router = SimpleRouter(trailing_slash=True)
router.register(r"", UserViewSet, basename="user")

urlpatterns = router.urls
