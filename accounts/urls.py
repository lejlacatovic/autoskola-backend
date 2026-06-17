from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MeView, ForgotPasswordView, UpdateMeView, NadolazecaCasoviView, InstruktoriView, ResetPasswordView, KorisniciView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('me/', MeView.as_view()),
    path('me/update/', UpdateMeView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('nadolazeci-casovi/', NadolazecaCasoviView.as_view()),
    path('instruktori/', InstruktoriView.as_view()),
    path('korisnici/', KorisniciView.as_view()),
    path('korisnici/<int:pk>/', KorisniciView.as_view()),
]