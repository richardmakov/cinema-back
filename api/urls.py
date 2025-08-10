from rest_framework.routers import DefaultRouter

from .views import MovieViewSet, SessionViewSet, BookingViewSet


router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('sessions', SessionViewSet)
router.register('bookings', BookingViewSet)

urlpatterns = router.urls

