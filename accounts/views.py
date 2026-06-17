from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .serializers import RegisterSerializer, UserSerializer
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            link = f"http://localhost:5173/reset-password?uid={user.pk}&token={token}"
            send_mail(
                'DrivePro — Reset lozinke',
                f'Klikni na link da resetuješ lozinku:\n\n{link}',
                'noreply@drivepro.rs',
                [email]
            )
        except User.DoesNotExist:
            pass
        return Response({'detail': 'Ako email postoji, poslan je link.'})
    
class UpdateMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class NadolazecaCasoviView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        from autoskola.models import Cas
        from autoskola.serializers import CasSerializer
        casovi = Cas.objects.filter(
            kandidat=request.user,
            status='zakazan',
            datum_vreme__gte=timezone.now()
        ).order_by('datum_vreme')[:5]
        from autoskola.serializers import CasSerializer
        return Response(CasSerializer(casovi, many=True).data)
    
class InstruktoriView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        instruktori = User.objects.filter(role='instruktor')
        return Response(UserSerializer(instruktori, many=True).data)
    
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')
        try:
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({'detail': 'Lozinka uspješno promijenjena.'})
            else:
                return Response({'detail': 'Token nije validan.'}, status=400)
        except User.DoesNotExist:
            return Response({'detail': 'Korisnik ne postoji.'}, status=400)
        
class KorisniciView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role not in ['admin', 'instruktor']:
            return Response({'detail': 'Nemate pristup.'}, status=403)
        korisnici = User.objects.all()
        return Response(UserSerializer(korisnici, many=True).data)

    def delete(self, request, pk):
        if request.user.role not in ['admin', 'instruktor']:
            return Response({'detail': 'Nemate pristup.'}, status=403)
        try:
            korisnik = User.objects.get(pk=pk)
            korisnik.delete()
            return Response({'detail': 'Korisnik obrisan.'})
        except User.DoesNotExist:
            return Response({'detail': 'Korisnik ne postoji.'}, status=404)