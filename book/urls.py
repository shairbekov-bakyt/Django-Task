from rest_framework.routers import DefaultRouter

from book.viewsets import BookViewSet


router = DefaultRouter()
router.register("books", BookViewSet)


urlpatterns = router.urls
