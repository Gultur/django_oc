from datetime import datetime
from django.shortcuts import (render, get_object_or_404)
from django.http import (HttpResponse, Http404)
from blog.models import (Article, Contact, Categorie)
from .forms import ContactForm, NouveauContactForm
from django.views.generic import ListView, DetailView


# Create your views here.


def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon blog !</h1>
        <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>
    """)

# HttpResponse permet de retourner une réponse depuis une chaine de caratère


def view_article(request, id_article):
    """
    Vue qui affiche un article selon son identifiant (ou ID, ici un numéro)
    Son ID est le second paramètre de la fonction (pour rappel, le premier
    paramètre est TOUJOURS la requête de l'utilisateur)
    """
    if id_article > 100:
        raise Http404
    return HttpResponse(
        "Vous avez demandé l'article n° {0} !".format(id_article)
    )


def date_actuelle(request):
    return render(request, 'blog/date.html', {'date': datetime.now()})


def addition(request, nombre1, nombre2):
    total = nombre1 + nombre2

    # retourne nombre1, nombre2 et la somme des deux au template
    return render(request, 'blog/addition.html', locals())

# ancienne methode pour la page d'accueil, remplacée par une vue generique
# def accueil(request):
#    """ Afficher tous les articles de notre blog """
#    articles = Article.objects.all() # Nous sélectionnons tous nos articles
#    return render(request, 'blog/accueil.html', {'derniers_articles': articles})


def lire(request, id, slug):
    """ Afficher un article complet """
    article = get_object_or_404(Article, id=id, slug=slug)
    return render(request, 'blog/lire.html', {'article': article})


def contact(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        renvoi = form.cleaned_data['renvoi']
        # Nous pourrions ici envoyer l'e-mail grâce aux données
        # que nous venons de récupérer
        envoi = True

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'blog/contact.html', locals())


def nouveau_contact(request):

    sauvegarde = False
    form = NouveauContactForm(request.POST or None, request.FILES)
    if form.is_valid():
        contact = Contact()
        contact.nom = form.cleaned_data["nom"]
        contact.adresse = form.cleaned_data["adresse"]
        contact.photo = form.cleaned_data["photo"]
        contact.save()
        sauvegarde = True
    return render(request, 'blog/nouveau_contact.html', {
        'form': form,
        'sauvegarde': sauvegarde
    })


def voir_contacts(request):

    return render(
        request,
        'blog/voir_contacts.html',
        {'contacts': Contact.objects.all()}
    )


class ListeArticles(ListView):
    # infos de bases
    model = Article
    context_object_name = "derniers_articles"
    template_name = "blog/accueil.html"
    # ajout d'une pagination
    paginate_by = 5

    def get_context_data(self, **kwargs):

        # Nous récupérons le contexte depuis la super-classe
        context = super().get_context_data(**kwargs)
        # Nous ajoutons la liste des catégories, sans filtre particulier
        context['categories'] = Categorie.objects.all()
        return context


class ListeArticlesParCategorie(ListView):
    # infos de bases
    model = Article
    context_object_name = "derniers_articles"
    template_name = "blog/accueil.html"
    # ajout d'une pagination
    paginate_by = 5

    def get_queryset(self):

        return Article.objects.filter(categorie__id=self.kwargs['id'])

    def get_context_data(self, **kwargs):

        # Nous récupérons le contexte depuis la super-classe
        context = super().get_context_data(**kwargs)
        # Nous ajoutons la liste des catégories, sans filtre particulier
        context['categories'] = Categorie.objects.all()
        return context

class LireArticle(DetailView):
    context_object_name = "article"
    model = Article
    template_name = "blog/lire.html"
