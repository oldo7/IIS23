from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class System(models.Model):  #System 
    nazov = models.CharField(max_length=200)
    popis = models.CharField(max_length=200)
    uzivatel = models.ManyToManyField(User, through="Vidi", blank=True, related_name="system")

    def __str__(self):
        return self.nazov
    
class Typ(models.Model): # Typ
    nazov = models.CharField(max_length=200)
    popis = models.CharField(max_length=200, blank=True, null=True)
    alias = models.CharField(max_length=200, blank=True, null=True)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, blank=True, null=True)
    uzivatel = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="typ")

    def name(self):
        return self.alias if self.alias else self.nazov
    def __str__(self):
        return self.alias if self.alias else self.nazov 
    
class Vidi(models.Model): # System rights
    uzivatel = models.ForeignKey(User, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    spravuje = models.IntegerField()        #0 = request, 1 = vidi, 2 = spravca
    
class Parameter(models.Model): # Parameter
    nazov = models.CharField(max_length=200)
    hodnota = models.IntegerField()
    kpi_typ = models.IntegerField(default=0) # nejaky enum ako 1 = less, 2 = more, 0 = none
    kpi_hodnota = models.IntegerField(default=0)
    typ = models.ForeignKey(Typ, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nazov

class UserExtend(models.Model): # extends user by privilige 
    privilige_level = models.SmallIntegerField()            #User = 1, Admin = 2, Broker = 3
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
