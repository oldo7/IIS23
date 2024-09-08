
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import *

class Command(BaseCommand):
    help = 'Seeds the database.'
    def handle(self, *args, **options):
        # Clear database
        verbose = True if options['verbosity'] > 0 else False
        print("Clearing database...") if verbose else None
        Clear()
        # Create users
        print("Creating users...") if verbose else None
        admin = User.objects.create_user(username='lesnar17', password='kolohousenka')
        UserExtend.objects.create(user=admin, privilige_level=2)
        broker = User.objects.create_user(username='broker', password='broker')
        UserExtend.objects.create(user=broker, privilige_level=3)
        matej = User.objects.create_user(username='matej', password='matej')
        UserExtend.objects.create(user=matej, privilige_level=1)
        ronnie = User.objects.create_user(username='ronnie', password='ronnie')
        UserExtend.objects.create(user=ronnie, privilige_level=1)

        # Create systems
        print("Creating systems...") if verbose else None
        system1 = System.objects.create(nazov="System1", popis="System1")
        system2 = System.objects.create(nazov="System2", popis="System2")

        # Create types
        print("Creating types...") if verbose else None
        typ1 = Typ.objects.create(nazov="V sys1", popis="zariadenie 1", system=system1, uzivatel=matej)
        typ2 = Typ.objects.create(nazov="bez", popis="bez", uzivatel=matej)
        typ3 = Typ.objects.create(nazov="V sys2", popis="zariadenie 2", system=system2, uzivatel=matej)
        typ4 = Typ.objects.create(nazov="ronnieho zariadenie", popis="zariadenie 3", uzivatel=ronnie) 

        # Create parameters
        print("Creating parameters...") if verbose else None
        Parameter.objects.create(nazov="parameter1", hodnota=1, typ=typ1)
        Parameter.objects.create(nazov="parameter2", hodnota=48, typ=typ1)
        Parameter.objects.create(nazov="parameter3", hodnota=2, typ=typ3)
        Parameter.objects.create(nazov="parameter4", hodnota=1, typ=typ3)
        Parameter.objects.create(nazov="parameter5", hodnota=1, typ=typ4)

        # grant vidi rights
        print("Granting vidi rights...") if verbose else None
        Vidi.objects.create(uzivatel=matej, system=system1, spravuje=2) # admin
        Vidi.objects.create(uzivatel=matej, system=system2, spravuje=2) # admin
        Vidi.objects.create(uzivatel=ronnie, system=system1, spravuje=1) # sees
        Vidi.objects.create(uzivatel=ronnie, system=system2, spravuje=0) # request



def Clear():
    User.objects.all().delete()
    System.objects.all().delete()
    Typ.objects.all().delete()
    Vidi.objects.all().delete()
    Parameter.objects.all().delete()
    UserExtend.objects.all().delete()