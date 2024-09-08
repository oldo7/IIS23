from django.urls import path, include
from . import views as v
from .forms import UserLoginForm
from django.contrib.auth import views

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'
    ),
    path("",v.home),
    path('', include("django.contrib.auth.urls")),
    path('odhlasenie/', v.odhlasenie),
    path('pridat/', v.adddevice), #TODO toto treba odstranit
    path('registracia/', v.registracia, name="registracia"),
    path('pridatsystem/', v.addsystem),
    path('poziadat/', v.poziadat),
    path('user/<int:id>/systems/', v.systemy),
    path('ziadosti/', v.ziadosti),
    path('ShowDevices/', v.ShowDevices),
    path('profil/', v.profil),
    path('CreateDevice/', v.CreateDevice),
    path('admin/', v.admin),
    path('modifyPrivilege/', v.modifyPrivilege),
    path('MojeSystemy/', v.mysystems),
    path('DetailSystemu/<int:id>/', v.detailsystemu),
    path('DetailSystemu/<int:id>/add', v.pridatzariadenie),
    path('ShowDevices/<int:id>', v.editdevice), 
    path('DetailSystemu/<int:id>/edit', v.upravitsystyem),
    path('metadata', v.metadata),
]