from rest_framework import serializers
from .models import Cas, NapredakKandidata, Vozilo

class CasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cas
        fields = '__all__'

class NapredakSerializer(serializers.ModelSerializer):
    class Meta:
        model = NapredakKandidata
        fields = '__all__'

class VoziloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vozilo
        fields = '__all__'