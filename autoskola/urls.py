from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CasViewSet, NapredakViewSet, VoziloViewSet, OcijeniInstruktoraView

router = DefaultRouter()
router.register(r'casovi', CasViewSet)
router.register(r'napredak', NapredakViewSet)
router.register(r'vozila', VoziloViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ocijeni-instruktora/', OcijeniInstruktoraView.as_view()),
]