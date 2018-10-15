from django.urls import path
from . import views

urlpatterns = [
    path('connexion/', views.connexion, name='formulaire_connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('prive/', views.vue_privee, name='prive'),

]
