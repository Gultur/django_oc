from django.urls import path, re_path
from . import views

urlpatterns = [
    path('liste/<int:page>', views.lister_mini_urls, name='liste_url'),
    # affichage formulaire en dur
    path('formulaire', views.creer_mini_url, name='formulaire_mini_urls'),
    # affichage formulaire via vue générique
    path('nouveau', views.URLCreate.as_view(), name='url_nouveau'),
    # pour utiliser une rexgex, il faut utiliser la methode re_path
    re_path(r'^edition/(?P<code>\w{6})$', views.URLUpdate.as_view(), name='url_update'),
    re_path(r'^supprimer/(?P<code>\w{6})$', views.URLDelete.as_view(), name='url_delete'),
    path('m/<code>', views.acceder_url, name='redirection_mini'),

]
