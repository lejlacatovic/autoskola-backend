from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User

class Cas(models.Model):
    TIP = [('teorija', 'Teorija'), ('voznja', 'Vožnja')]
    STATUS = [('slobodan', 'Slobodan'), ('zakazan', 'Zakazan'), ('odrzan', 'Održan')]

    kandidat = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='casovi', null=True, blank=True)
    instruktor = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='predaje')
    tip = models.CharField(max_length=10, choices=TIP)
    status = models.CharField(max_length=10, choices=STATUS, default='slobodan')
    datum_vreme = models.DateTimeField()
    trajanje_min = models.IntegerField(default=60)
    napomena = models.TextField(blank=True)

    class Meta:
        ordering = ['datum_vreme']

class NapredakKandidata(models.Model):
    kandidat = models.OneToOneField(User, on_delete=models.CASCADE,
                                     related_name='napredak')
    teorija_odradjeno = models.IntegerField(default=0)
    teorija_ukupno = models.IntegerField(default=10)
    voznja_odradjeno = models.IntegerField(default=0)
    voznja_ukupno = models.IntegerField(default=40)
    ocena_instruktora = models.FloatField(default=0)

class Vozilo(models.Model):
    STATUS = [('dostupan', 'Dostupan'), ('zauzet', 'Zauzet'), ('servis', 'Na servisu')]
    KATEGORIJA = [('B', 'B'), ('C', 'C'), ('A', 'A')]

    model = models.CharField(max_length=100)
    kategorija = models.CharField(max_length=2, choices=KATEGORIJA)
    tip_menjaca = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default='dostupan')
    napomena_statusa = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.model