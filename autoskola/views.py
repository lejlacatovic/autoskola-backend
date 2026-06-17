from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cas, NapredakKandidata, Vozilo
from .serializers import CasSerializer, NapredakSerializer, VoziloSerializer

class CasViewSet(viewsets.ModelViewSet):
    queryset = Cas.objects.all()
    serializer_class = CasSerializer
    permission_classes = [permissions.IsAuthenticated]

class NapredakViewSet(viewsets.ModelViewSet):
    queryset = NapredakKandidata.objects.all()
    serializer_class = NapredakSerializer
    permission_classes = [permissions.IsAuthenticated]

class VoziloViewSet(viewsets.ModelViewSet):
    queryset = Vozilo.objects.all()
    serializer_class = VoziloSerializer
    permission_classes = [permissions.IsAuthenticated]

class OcijeniInstruktoraView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ocjena = request.data.get('ocjena')
        instruktor_id = request.data.get('instruktor_id')

        if not ocjena or not instruktor_id:
            return Response({'detail': 'Nedostaju podaci.'}, status=400)

        if not (1 <= float(ocjena) <= 5):
            return Response({'detail': 'Ocjena mora biti između 1 i 5.'}, status=400)

        try:
            from accounts.models import User
            instruktor = User.objects.get(pk=instruktor_id, role='instruktor')
            napredak = NapredakKandidata.objects.filter(kandidat=request.user).first()
            if napredak:
                napredak.ocena_instruktora = ocjena
                napredak.save()
            return Response({'detail': 'Ocjena uspješno dodata!'})
        except Exception as e:
            return Response({'detail': str(e)}, status=400)