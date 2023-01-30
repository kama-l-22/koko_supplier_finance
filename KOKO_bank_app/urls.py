from django.urls import path
from KOKO_bank_app import views

urlpatterns = [
    
    path("",views.kologin,name='kologin'),
    path("kosignin/",views.kosignin,name='kosignin'),
    path("kohome/",views.kohome,name='kohome'),
    path('editclient/',views.koeditclient,name='editc'),
    path('kover/',views.kover,name ='kover'),
    path('noway/',views.noway,name='noway')


]
