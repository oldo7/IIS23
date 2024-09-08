from django.shortcuts import render, redirect
from .forms import  CreateNewDevice, CreateNewSystem, CreateDeviceForm
from .models import Typ, System, Vidi, Parameter, UserExtend
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

# Create your views here.
def registracia(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            p = form.cleaned_data["username"]
            t = UserExtend(user = User.objects.get(username=p), privilige_level = 1)
            t.save()
            return HttpResponseRedirect("/login")

    else:
        form = UserCreationForm()

    return render(request, "registracia.html", {"form" : form})

def home(request):
    if request.user.is_authenticated:
        if UserExtend.objects.get(user=request.user).privilige_level == 3:
            if request.method == "POST":
                p = request.POST
                for x in p:
                    if x.isnumeric():
                        Parameter.objects.filter(id=x).update(hodnota=p[x])
            zariadenia_neprazdne = []
            zariadenia = Typ.objects.all()
            for z in zariadenia:
                if z.parameter_set.all():
                    zariadenia_neprazdne.append(z)
            return render(request, 'broker.html', {"zariadenia" : zariadenia_neprazdne})
        else:
            return HttpResponseRedirect("/MojeSystemy/")
    else: 
        return HttpResponseRedirect("/login")

def odhlasenie(request):
    return render(request, "logout.html")

def adddevice(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = CreateNewDevice(request.POST)

        if form.is_valid():
            p = form.cleaned_data["popis"]
            t = Typ(popis=p)
            t.save()
            request.user.Typ.add(t)
        
        return HttpResponseRedirect("")
    else:
        form = CreateNewDevice()
    return render(request, 'createdevice.html', {"form" : form})

def addsystem(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        x = request.POST
        p = x["popis"]
        n = x["nazov"]
        if n == "":
            return HttpResponseRedirect("/MojeSystemy/")
        u = request.user
        t = System(popis=p, nazov=n)
        t.save()
        v1 = Vidi(
            uzivatel=request.user,
            system = t,
            spravuje = 2,
        )
        v1.save()

        return HttpResponseRedirect("/MojeSystemy/")
    else:
        form = CreateNewSystem()
    return render(request, 'createsystem.html', {"form" : form})

def poziadat(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    users =User.objects.all()
    systems = System.objects.all()
    userSystemCount = {}
    for user in users:
        userSystemCount[user.id] = 0
        for system in systems:
            if Vidi.objects.filter(uzivatel=user, system=system, spravuje=2).exists():
                userSystemCount[user.id] += 1
    return render(request, 'userlist.html', {"users" : users, "userSystemCount" : userSystemCount})

def systemy(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    user = User.objects.get(id=id)
    systemy = user.system.all()
    requested = []
    approved = []
    systemy2 = []

    if request.method == "POST":
        p = request.POST
        id = p['req']
        ziadanysys = System.objects.get(id=id)
        ownsystem = Vidi.objects.filter(system=ziadanysys, spravuje=2, uzivatel=request.user).exists() or Vidi.objects.filter(system=ziadanysys, spravuje=1, uzivatel=request.user).exists()
        alreadyrequested = Vidi.objects.filter(system=ziadanysys, spravuje=0, uzivatel=request.user).exists()
        if ownsystem or alreadyrequested:
            pass
        else:
            v1 = Vidi(
                    uzivatel=request.user,
                    system = ziadanysys,
                    spravuje = 0,
                )
            v1.save()

    for s in systemy:
        if Vidi.objects.filter(system=s, spravuje=2, uzivatel=user).exists():
            systemy2.append(s)      #v systemy2 su vsetky systemy ktore vlastni vybrany uzivatel

    for s in systemy2:
        if Vidi.objects.filter(system=s, spravuje=0, uzivatel=request.user).exists():           #uz boli requestnute
            requested.append(s)
        elif Vidi.objects.filter(system=s, spravuje=1, uzivatel=request.user).exists():         #uz boli approvnute
            approved.append(s)
    return render(request, 'systemlist.html', {"zariadenia" : systemy2, "requested" : requested, "approved" : approved})

def ziadosti(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    systemy = request.user.system.all()         #systemy aktualneho pouzivatela
    requested = []

    if request.method == "POST":
        p = request.POST
        if 'deny' in p:
            system = Vidi.objects.get(id=p['deny']).system
            if Vidi.objects.filter(uzivatel=request.user, spravuje=2, system=system).exists():
                Vidi.objects.get(id=p['deny']).delete()
            else:
                return HttpResponse('Unauthorized', status=401)
        elif 'conf' in p:
            system = Vidi.objects.get(id=p['conf']).system
            if Vidi.objects.filter(uzivatel=request.user, spravuje=2, system=system).exists():
                Vidi.objects.filter(id=p['conf']).update(spravuje=1)
            else:
                return HttpResponse('Unauthorized', status=401)

    for s in systemy:
        if not Vidi.objects.filter(system=s, spravuje=2, uzivatel=request.user).exists():
            continue
        if Vidi.objects.filter(system=s, spravuje=0).exclude(uzivatel=request.user).exists():           #z vsetkych systemov aktualneho pouzivatela sa najdu tie ktore niekto vyziadal, odstrania sa tie ktore vyzadoval uzivatel sam
            req = Vidi.objects.filter(system=s, spravuje=0).exclude(uzivatel=request.user)
            for x in req:
                requested.append({"system" : x.system,"user": x.uzivatel, "id" : x.id})
    return render(request, 'requests.html', {"systemy" : requested})

def ShowDevices(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    user = request.user
    if request.user.is_authenticated:
        devices = request.user.typ.all()
        username = request.user.username
        if request.method == "POST":
            if request.POST.get("delete"):
                victim = Typ.objects.get(id=request.POST.get("delete"))
                if victim.uzivatel == request.user:
                    victim.delete()
                else:
                    return HttpResponse('Unauthorized', status=401)
        return render(request, 'ShowDevices.html', {"devices" : devices, "user" : user})
    else:
        return render(request, 'ShowDevices.html', {"devices" : [], "user" : ""})
    
def profil(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profil.html', {"form" : form})

def CreateDevice(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST
        nazov, popis, alias = content['nazov'], content['popis'], content['alias']
        typ = Typ(nazov=nazov, popis=popis, alias=alias, uzivatel=request.user)
        typ.save()
        return redirect('/ShowDevices/')
    elif request.user.is_authenticated:
        form = CreateDeviceForm()
        return render(request, 'CreateDevice.html', {"form" : form})

def modifyPrivilege(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    if request.method == "POST" and request.user.is_authenticated and request.user.userextend.privilige_level == 2:
        content = request.POST
        if not 'privilegeLevel' in content or not 'userId' in content or content['userId'] == request.user.id:
            return redirect('/admin/')
        targetUserId = content['userId']
        privilegeLevel = content['privilegeLevel']
        targetUser = User.objects.get(id=targetUserId)
        newobject = UserExtend(user=targetUser, privilige_level=privilegeLevel)
        newobject.save()  
    return redirect('/admin/')

def admin(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    if request.user.is_authenticated and request.method == "GET":
            users = User.objects.all()
            userDevices = {}
            for user in users:
                filteredDevices = Typ.objects.filter(uzivatel=user)
                userDevices[user.id] = []
                for device in filteredDevices:
                    userDevices[user.id].append(device)
            return render(request, 'admin.html', {"users" : users, "userDevices" : userDevices})
    else:
        return render(request, 'admin.html')
    
def mysystems(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    user = request.user
    systemy2 = []
    systemy = []
    mojesystemy = []
    parametre = []
    systemy2 = Vidi.objects.filter(uzivatel=user).exclude(spravuje = 0) #vsetky systemy co vidi/vlastni dany uzivatel

    for x in systemy2:
        paramok = 1
        vlastnik = Vidi.objects.filter(spravuje = 2, system = x.system).first().uzivatel
        zariadenia = Typ.objects.filter(system = x.system)
        for z in zariadenia:
            parametre = Parameter.objects.filter(typ = z)
            for p in parametre:
                if (p.kpi_typ == 1 and p.kpi_hodnota < p.hodnota) or (p.kpi_typ == 2 and p.kpi_hodnota > p.hodnota):
                    paramok=0

        if vlastnik == request.user:
            mojesystemy.append({"id" : x.system.id, "system" : x.system.nazov, "popis" : x.system.popis,"vlastnik": vlastnik.username, "paramok" : paramok})
        else:
            systemy.append({"id" : x.system.id, "system" : x.system.nazov, "popis" : x.system.popis, "vlastnik": vlastnik.username, "paramok" : paramok})


    return render(request, 'mysystemlist.html', {"systemy" : systemy, "mojesystemy" : mojesystemy})

def detailsystemu(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        p = request.POST
        zar = p['del']
        Typ.objects.filter(id=zar, uzivatel=request.user).update(system = None)

    system = System.objects.get(id = id)
    owner = Vidi.objects.filter(spravuje = 2, system = system).first().uzivatel
    zariadenia = Typ.objects.filter(system = system)

    return render(request, 'detailsystemu.html', {"system" : system, "owner" : owner, "zariadenia" : zariadenia})

def pridatzariadenie(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    system = System.objects.get(id = id)
    owner = Vidi.objects.filter(spravuje = 2, system = system).first().uzivatel
    user = request.user
    zariadenia = user.typ.filter(system = None)

    if request.method == "POST":
        p = request.POST
        zar = p['add']
        Typ.objects.filter(id=zar, uzivatel=request.user).update(system = system)

    return render(request, 'adddevice.html', {"system" : system, "owner" : owner, "zariadenia" : zariadenia})

def editdevice(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    device = Typ.objects.get(id=id)
    params = device.parameter_set.all()

    if request.method == "POST":
        if request.POST.get("Save")=="":
            for param in params:
                if request.POST.get("n"+str(param.id)):
                    param.nazov = request.POST.get("n"+str(param.id))
                if request.POST.get("v"+str(param.id)):
                    hodnota = request.POST.get("v"+str(param.id))
                    if hodnota.isdigit():
                        param.hodnota = hodnota
                    else:
                        param.hodnota = 0
                if request.POST.get("k"+str(param.id)):
                    kpi_typ = request.POST.get("k"+str(param.id))
                    if kpi_typ.isdigit():
                        param.kpi_typ = kpi_typ if int(kpi_typ) < 3 and int(kpi_typ) > 0 else 0
                    else:
                        param.kpi_typ = 0
                if request.POST.get("kv"+str(param.id)):
                    kpi_hodnota = request.POST.get("kv"+str(param.id))
                    if kpi_hodnota.isdigit():
                        param.kpi_hodnota = kpi_hodnota
                    else:
                        param.kpi_hodnota = 0
                param.save()
        if request.POST.get("newParameter")== "":
            newparam = Parameter(nazov="new param", hodnota=0, typ=device)
            newparam.save()

    return render(request, 'EditDevice.html', {"device": device, "params": params})
            
def upravitsystyem(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.userextend.privilige_level == 3:
        return HttpResponseRedirect("/")
    system = System.objects.get(id = id)
    owner = Vidi.objects.filter(spravuje = 2, system = system).first().uzivatel
    user = request.user
    zariadenia = user.typ.filter(system = None)

    if request.method == "POST":
        p = request.POST
        if p.get("delsys"):
            x = System.objects.get(id=p["delsys"])
            owner = Vidi.objects.filter(spravuje = 2, system = x).first().uzivatel
            if user.id == owner.id:
                x.delete()
            else:
                return HttpResponse('Unauthorized', status=401)
        elif p.get("id") and p.get("nazov") and p.get("popis"):
            x = System.objects.get(id=p["id"])
            owner = Vidi.objects.filter(spravuje = 2, system = x).first().uzivatel
            if user.id == owner.id:
                System.objects.filter(id=p["id"]).update(nazov=p["nazov"], popis=p["popis"])
            else:
                return HttpResponse('Unauthorized', status=401)
        return HttpResponseRedirect("/MojeSystemy/")

    return render(request, 'editsystem.html', {"system" : system, "owner" : owner, "zariadenia" : zariadenia})

def metadata(request):
    userscount = len(User.objects.all())
    systemcount = len(System.objects.all())
    devicecount = len(Typ.objects.all())


    systemy = System.objects.all()
    systemystruct = []

    for s in systemy:
        spravca = Vidi.objects.filter(system=s, spravuje=2).first().uzivatel
        pocet_zariadeni = len(s.typ_set.all())
        systemystruct.append({"nazov" : s.nazov, "popis" : s.popis, "spravca" : spravca.username, "pocet_z": pocet_zariadeni})


    return render(request, 'metadata.html', {"userscount" : userscount,"systemcount": systemcount, "devicecount":devicecount, "systemy" : systemystruct})
    
    