from django.urls import path
from . import views
from .models import Article
from django.views.generic import ListView

urlpatterns = [
    path('accueil', views.home),
    # path('article/<int:id_article>', views.view_article, name='afficher_article'),
    path('date', views.date_actuelle),
    path('addition/<int:nombre1>/<int:nombre2>/', views.addition),
    # url passant par une methode dans views
    # path('', views.accueil, name='accueil'),
    # url passant par une vue générique ListView
    # path('', ListView.as_view(model=Article,
    #                          context_object_name="derniers_articles",
    #                          template_name="blog/accueil.html")),
    # url passant par une classe pour la vue génrique
    path('', views.ListeArticles.as_view(), name="blog_liste"),
    # on utilise la même classe pour une autre vue mais en utilisant un argument
    # l'id de la catégorie servant de filtre
    path('categorie/<int:id>', views.ListeArticlesParCategorie.as_view(), name="blog_categorie"),
    # path('article/<int:id>', views.lire, name='lire'),
    path('article/<int:id>-<slug:slug>', views.lire, name='lire'),
    path('article/generic/<int:pk>', views.LireArticle.as_view(), name="blog_lire"),
    path('contact/', views.contact, name='contact'),
    path('nouveaucontact/', views.nouveau_contact, name='nouveau_contact'),
    path('voircontacts/', views.voir_contacts, name='voir_contacts'),
]
