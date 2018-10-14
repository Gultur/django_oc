# erreur de migration
try python manage.py makemigrations <appname_thats_missing_tables>
and python manage.py migrate <appname_thats_missing_tables>

# passer des arguements à un url
path('article/<id_article>')
=> on ne regarde pas le type de données, c'est par défaut une chaine de caractères non vide
=> on peut spécifier 5 types de données
str  : c'est le format par défaut (celui utilisé pour notre id_article par exemple). Cela permet de récupérer une chaine de caractères non vide, excepté le caractère "/";  : c'est le format par défaut (celui utilisé pour notre id_article par exemple). Cela permet de récupérer une chaine de caractères non vide, excepté le caractère "/" ;
- int  : correspond à une suite de chiffres, et renverra donc un entier à notre vue ;
- slug  : correspond à une chaine de caractères sans accents ou caractères spéciaux. Un exemple de slug peut être mon-1er-article-de-blog ;
- uuid  : format standardisé de données, souvent utiliser pour avoir des identifiants uniques.
- path  : Similaire à str mais accepte également le "/". Cela permet de récupérer n'importe quel URL quelque soit son nombre de segments
=> cela assure en plus une conversion du type entré, que ne sera donc pas à coder soit même dans la vue
=> exemples:
path('articles/<str:tag>', views.list_articles_by_tag),
path('articles/<int:year>/<int:month>', views.list_articles),

=> on peut avoir des arguments optionnels en mettant une valeur par défaut dans la methode
def list_articles(request, year, month=1):
    return HttpResponse('Articles de %s/%s' % (year, month))

# une ancienne methode utilise des regex
re_path(r'^article/(?P<id_article>.+)', views.view_article),
re_path(r'^articles/(?P<tag>.+)', views.list_articles_by_tag),
re_path(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})', views.list_articles),  

=> A savoir : django recupère les arguments selon leur nommage dans l'url, ce n'est pas grave sir dans les methodes de vue, l'ordre est différent, les paramètres seront correctement affectés
path('articles/<int:year>/<int:month>', views.list_articles)
def list_articles(request, month, year):
    """ Liste des articles d'un mois précis. """
    return HttpResponse(
        "Vous avez demandé les articles de {0} {1}.".format(month, year)  
    )
=> il faut donc que les noms de variables soient les mêmes

# on peut raise une erreur 404
from django.http import HttpResponse, Http404
  raise Http404

#redirection
=> methode redirect
from django.shortcuts import redirect

def list_articles(request, year, month):
    # Il veut des articles ? Soyons fourbe et redirigeons-le vers djangoproject.com
    return redirect("https://www.djangoproject.com")
=> en cas de redirection interne il est préférable de dissocier configuration des URL et des vues
=> dans views
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

def view_article(request, id_article):
    if id_article > 100:
        raise Http404
    return redirect(view_redirection)

def view_redirection(request):
    return HttpResponse("Vous avez été redirigé.")
=> dans urls
path('redirection', views.view_redirection),
=> il est possible de mettre des paramètres dans le return redirection
=> par exemple permanent=True/False indique si la redirection est permanent ou temporaire

# nommage des urls dans le fichier urls
=> il est possible d'associer un nom à la route
path('article/<int:id_article>$', views.view_article, name='afficher_article'),
=> on peut utliser le nom à la place de views.view.article
return redirect('afficher_article', id_article=42)

# generation d'URL via la methode reverse() / django.urls.reverse
=> retourne une chaine de caractère contenant l'url vers la vue

#les TEMPLATES
=> Django possède un moteur de template integré mais il est possible d'en choisir un autre
=> on utilise la methode render (django.shortcut)pour generer un objet HttpResponse après avoir traité le template
render(requete_http, chemin_du_template, dictionnaire_de_variables)
=> on peut utiliser une methode locals() à la place du dictionnaire, cela va retourner un dictionnaire contenant toutes les variables de la fonction, les clés étant leurs noms dans la fonction, y compris la variable request
=> Django cherche les templates dans :
- la liste des dossiers fournis du paramètre DIR  de la variable de configurationTEMPLATES
- dans un sous-dossier "templates" de l'application.
=> il est recommandé de crééer un dossier template à la racine du projet pour les templates propres au projet (error 404, squelette de design, page statique)
=> dans chaque application créer un dossier templates avec un sous dossier portant le nom de l'application concernée

## affichage des variables dans un template
=> dans un template une variable s'affiche en ecrivant {{ nom_variable }}
=> si la variable n'est pas une chaine de caractère le template appelle la methode to string
=> lorsque la variable est un objet, on peut acceder aux attributs en ecrivant {{nom_objet.nom_attribut}}
=> Si jamais une variable n'existe pas, ou n'a pas été envoyée au template, Django n'affiche rien par défaut. Il est possible de forcer l'affichage d'une erreur en spécifiant l'option  'string_if_invalid'  dans les options du backend de templates.
=> on peut ajouter des filtres pour la variable sur le template: {{ nom_variable|filtre}}
{{ texte|truncatewords: 80}} # n'affiche que les premiers 80 mots
=> accorde automatique si le nombre est > 1 , ici on spécifie même l'accord , sinon c'est "s" par défaut
Il y a {{ nb_chevaux }} chev{{ nb_chevaux|pluralize:"al,aux" }} dans l'écurie.
=> on peut mettre une valeur par défaut
Bienvenue {{ pseudo|default:"visiteur" }}

## tag dans un template
=> il est possible de faire des conditions : {% if condition %}... {% else %}... {% endif %}
=> des boucles: {% for element in tableau %} ... {% endfor %}
{% for cle, valeur in dictionnaire.items %}
{% empty %} ... est un tag qui s'insère dans et qui agit si la liste est vide
=> Rappelez-vous que la manipulation de données doit être faite au maximum dans les vues. Ces tags doivent juste servir à l'affichage !
=> on peut definir des blocs {% block nom_block%}, cela generera des balises du même nom
=> on peut hériter d'un autre template: {% extends "nom_du_template" %}
=> lien vers une vue, l'url sera construite : {% url "nom_vue" parametre %}
=>des commentaires: {# mon commentaire #} pour une ligne
{% comment %} pour un commentaire multiligne {% endcomment %}

## les fichiers statiques (css, js , images)
=> deux endroits possibles
le dossier static de l'application concernée
dans un ou plusieurs dossiers définis dans la configuration du projet, courrament un dossier static à la racine du projet, comme pour les TEMPLATES
=> pour y faire apppel dans un template
{% load static %} # au debut du template
<img src="{% static 'blog/crepes.jpg' %}" alt="Mon image" />

# les modeles
=> un modele est une classe et représente une table de base de données
=> les attributs sont les champs de la table
=> les modeles sont rédigés dans les fichiers models.py de chaque application
=> tout modele hérite de model.model :
from j.django.db import models

## les types de champs du modèle:
CharField : chaîne de caractèref à taille limitée
TextField: chaîne de caractère sans taille limitée
DateTimeField: instance datetime du module du même nom
=>Un champ de modèle peu prendre plusieurs argument (selon le type)
default (indique une valeur par defaut), verbose_name(précision sur le nom du champ), null (indique si le champ peut être null)
etc...

# classe meta
=> classe optionnelle incluse dans la classe du model, elle permet d'ajouter des infos pour Django, comme les comportements propres au model
ordering indique le champ pour le tri par defaut
verbose_name permet de dire à django ce que represente le model

# creation d'une table sql
python manage.py makemigrations # liste les modifications
python manage.py migrate # les applique

# le shell
python manage.py shell
=> permet de manipuler les modèles  comme si nous etions dans une vue
article = Article(titre="Bonjour", auteur="Maxime")
article.contenu = "Les crêpes bretonnes sont trop bonnes !"
article.save() # pour enregister les modifications
article.delete() # supprimes une entrée dans la base de données
Articles.objects.all() # retourne toutes les entrées d'un modèle
=> on peut boucler sur les objets, et les filtrer (plusieurs champs possibles)
for article in Article.objects.all():
... print(article.titre)
for article in Article.objects.filter(titre="La Bretagne", auteur="Maxime"):
... print(article.titre, "par", article.auteur)
=> en mettant exclude à la place de filter, on indique des filtres pour ignorer certains objets
=> il est possible de faire des filtres personnalisées
=> ajout de __contains    ___  à un champ, permet d'indiquer que la chaîne doit être présente dans le titre
Article.objects.filter(titre__contains="crêpe")
=> on peut aussi avoir : __gt, __lt, __lte, __gte, __startswith    ___
=> ordonner les resultats, order_by, on peut passer plusieurs attributs, en cas d'égalité du premier, le second servira à departager .. etc
Article.objects.order_by('date') # tri par ordre ascendant
Article.objects.order_by('-date') # tri par ordre descendant
reverse() # inverse les élements
=> on peut cumuler les instructions
Article.objects.filter(date__lt=timezone.now()).order_by('date','titre').reverse()
=> .toutes ces methodes retournent un QuerySet

=> méthodes ne retournant qu'une entrée d'un modele
=> objects.get(titre="") , prend les mêmes arguments qu'un filter/exclude
=> get_or_create créé l'objet s'il n'existe pas

# liaisons entre modèles
## ForeignKey
=> il est possible de lier un modèle à un autre, par exemple un article aura un champ categorie
categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)
=> ForeignKey() a deux options obligatoires: le modèle vers lequel pointer et que faire en cas de suppression:
CASACADE : en cas de suppression de la catégorie, tous les articles ayant cette catégorie seront également supprimé (provoquant une cascade de suppression) ;
SET_NULL : vide le champ  categorie  de chaque objet utilisant si la valeur étrangère étant supprimé (il faut alors que le champ accepte les valeurs vides bien sûr) ;
PROTECT : empêche de supprimer une valeur si elle est utilisé, via une exception Python

=> on peut acceder à la liste des objets liès à un model ForeignKey
cat.article_set.all() # permet de liste les articles associés à la catégorie
=> on peut utiliser les mêmes methodes (filter/exclude...) que pour un objet (voir shell)
=> il est possible d'accéder aux attributs du modèle lié par une clé étrangère depuis unfilter, exclude, order_by
Article.objects.filter(categorie__nom__contains="crêpes") # liste les articles dont la catégorie contient "crêpes"
=> Accéder à un élément d'une clé étrangère se fait en ajoutant deux underscores « __ », comme avec les méthodes de recherche spécifiques, suivis du nom de l'attribut recherché


## OneToOneField
=> Un autre type de liaison existe, très similaire au principe des clés étrangères : le OneToOneField
=> c'est une relation unique, une fois liés les deux objets ne pourront pas être liés à d'autres objets du modèle concerné
=>on peut acceder à chaque objet par l'object qui lui est lié
moteur.voiture # retourne <Voiture: Crêpes-mobile>
voiture.moteur # retourne <Moteur: Vroum>

=> il est possible de changer le nom de la variable créée par la relation inverse : il faut utiliser l'argument related_name  duForeignKey  ou OneToOneField  et lui passer une chaîne de caractères désignant le nouveau nom de l'attribut
=> Accessoirement, il est même possible de désactiver la relation inverse en donnant related_name='+'

## ManyToManyField
=> un  ManyToManyField  va toujours créer une table intermédiaire qui enregistrera les clés étrangères des différents objets des modèles associés
=>Nous pouvons soit laisser Django s'en occuper tout seul, soit la créer nous-mêmes pour y ajouter des attributs supplémentaires. Dans ce deuxième cas, il faut spécifier le modèle faisant la liaison via l'argument  through  du champ et ne surtout pas oublier d'ajouter des  ForeignKey  vers les deux modèles qui seront liés.

from blog.models import Vendeur, Produit, Offre
vendeur = Vendeur.objects.create(nom="Carouf")
p1 = Produit.objects.create(nom="Lait")
p2 = Produit.objects.create(nom="Farine")

=>Dans le cas de la relation avec le modèle intermédiaire, Django nous laisse gérer le modèle  Offre  comme un modèle classique, où l'on peut créer, modifier et supprimer des relations :

o1 = Offre.objects.create(vendeur=vendeur, produit=p1, prix=10)
o2 = Offre.objects.create(vendeur=vendeur, produit=p2, prix=42)
o1.prix = 15
o1.delete()

=>Dans le cas de la relation sans modèle intermédiaire, on gère les éléments liés à notre vendeur via l'attribut  produits_sans_prix  , qui se gère tel un ensemble où l'on peut ajouter, supprimer et lister les objets
vendeur.produits.add(p1, p1, p2) # un element ne peut etre présent qu'une fois
vendeur.produits_sans_prix.all()
<QuerySet [<Produit: Lait>, <Produit: Farine>]>
vendeur.produits_sans_prix.remove(p2)

=> Les relations ManyToManyField se comportent également comme un QuerySet et il est donc possible de manier les produits avec les critères habituels (filter, exclude, order_by, reverse...)
p1.vendeurs.all()
<QuerySet [<Vendeur: Carouf>]>
=> en cas de modèle intermediaire
Offre.objects.get(vendeur=vendeur, produit=p1).prix

=> pour supprimer toutes les liaisons d'un ManyToManyField (dans les deux cas) : methode clear()
vendeur.produits.clear()
vendeur.produits_sans_prix.clear()

# modeles dans les vues
=> les modeles ont des attributs et champs sql plus nombreux que ceux indiqué dans le fichier model (primary key,  not null...)
=> pour voir la structure sql via le shell
python manage.py sqlmigrate blog 0001_initial # le 0001_initial indique la première migration faite
=> chaque table à un id auto incrémenté
=> dans les methodes get_object_or_404() permet d'eviter un try and except pour tester l'existence d'un id

# les slugs
=> il existe un type de champ dans les modeles : SlugField
=> un slug est un label permettant d'eviter de passer par les id pour les liens

# administration

## adminisration de base
=> étant optionnelle, elle passe part un module, le module django.contrib, comprenant entre autres django.contrib.admin (administration) , django.contrib.messages (notifications aux visiteurs), django.contrib.auth  (authentification et gestion des utilisateurs)
=> il faut créér un compte super-utilisateur
python manage.py createsuperuser
=> il faut lier une adresse au module d'administration, par defaut une adresse /admin est déjà présente, il suffit de l'afficher et se connecter avec le compte super-utilisateur créé
=> la page d'administration permet d'agir sur les modeles par defaut comme la gestion les utilisateurs (ajout/suppression, gestion des groupes)
=> Django impose des règles de validation sur le mot de passe afin d'éviter les mots de passe trop facile à deviner et forcer. Il est possible d'ajouter ou supprimer des contraintes en modifiant la liste  AUTH_PASSWORD_VALIDATORS  dans le fichier de configuration.
=> a niveau des permissions d'un utilisateur, "statut equipe" indique que l'utilisteur peut accèder au panel d'administration, "statut super-utilisateur" donne les pleins pouvoirs
=> chaque action effectué via l'administration est inscrite dans un journal des actions, accessible via un bouton "historique"

## administration des modeles personnalisés
=> il faut modifier le fichier application/admin.py
from django.contrib import admin
from .models import nom_du_modele

admin.site.register(nom_du_modele)
=> un panneau concernant l'application s'est ajoutée à la page d'administration
=> les clés etrangéres sont pris en compte dans la gestion
=> au lancement, django va charcher le fichier admin.py de chaque application enregistrée dans le fichier settings (INSTALLED_APPS)
=> l'affichage du tableau du modele dépend de la methode __str__ definie dans le model
=> l'administration utilise le verbose_name de la class Meta
=> Pour améliorer le tableau d'administration du modele, il faut ajouter une classe dans le fichier admin.py
<nom_classeAdmin(admin.ModelAdmin):
list_display = Liste des champs du modèle à afficher dans le tableau
list_filter = Liste des champs à partir desquels nous pourrons filtrer les entrées
date_hierarchy = Permet de filtrer par date de façon intuitive
ordering = Tri par défaut du tableau
search_fields = Configuration du champ de recherche
=> il faut ensuite ajouter cette classe nom_classeAdmin dans admin.site.register():
admin.site.register(Article, ArticleAdmin)

=> il est possible de définir des methodes dans le ModelAdmin pour creer des colonnes plus complexes, pouvant necessiter un traitement (ex : 40 premiers caractères d'un article)
=> la methode prend en argument l'instance du model (self, instance_model)
=> on peut ensuite la traiter comme un champ dans le list_display du ModelAdmin
=> pour modifier l'entete de ce champ, il faut ajouter:
nom_methode.short_description = 'Description'

=> pour modifier le formulaire d'édition d'un model (cacher des champs, reordonner les autres), il faut ajouter un attribut fields dans le ModelAdmin
fields = ('titre', 'auteur', 'categorie', 'contenu')
=> pour hierarchiser (mettre plusieurs zones de champs par exemple),
il faut ajouter un champ fieldsets, qui est un tuple composé de chaque fieldset que l'on desire
=> chaque fieldset est lui meme un tuple de deux informations, le nom et un dictionnaire représentant le contenu
=> ce dictionnaire contient 3 types de données:
 - fields  : liste des champs à afficher dans le fieldset ;
 - description  : une description qui sera affichée en haut du fieldset, avant le premier champ ;
- classes  : des classes CSS supplémentaires à appliquer sur le fieldset (par défaut il en existe trois :wide, extrapretty  et collapse).

=> il est possible de préremplir des champs grace à une option executant un script JS, par exemple pour le slug:
prepopulated_fields = {'slug': ('titre', ), }
=> lors d'un ajout d'une instance du model, ce champs se remplira tout seul

# Les formulaires
## creation
=> la déclaration d'un formulaire est semblable à celle d'un modele
=> par convention on reunies les formulaires d'une application dans un fichier forms.py
from djando import forms
class NomForm(forms.Form):
  attribut = forms.Type_de_champ(arguments_du_champ)
=> le type TextField est remplacé par le type CharField
=> on peut modifier les champs grace aux widgets (un widget forms.Textarea pour un champ CharField par exemple)
=> autres widgets : PasswordInput, DateInput, CheckBoxInput ...
=> les types ont un widget par defaut, on le spécifie uniquement quand on veut modifier
=> les types ont une validation par defaut qui verifie la donnée entrée par l'utilisateur ( EmailField par exemple)
=> arguments :
- label : modifie le nom de la boite de saisie
- help_text :  ajout un texte d'aide
- required : indique une obligation de remplir ce champ pour valider le formulaires

## ajout dans une vue
=> attribut method d'un objet request (requetes http) : POST (contrairement à GET qui ne concerne pas les formulaires)
=> dans view
from .forms import NomForm

def nom_method(request):
  form = NomForm(request.POST or None)
  if form.is_valid():
    champ = form.cleaned_data['champ']
    ...
  return render(request, 'url_du_formulaire', locals())
=> un dictionnaire des champs remplis est constitué
=> si des champs ne sont pas valides, django renvoie vers le formulaire sans le vider et en ajoutant des messages d'aide
=> il faut ajouter dans URLS, exemple
path('contact/', views.contact, name='contact')
=> dans le template, il suffit de spécifier une balise form et un bouton
<form action="{% url "contact" %}" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit" />
</form>
=> un form a plusieurs methodes pour definir la generation du code html
=> form.as_p : suite de paragraphe
=> le crsf est le token de sécurité

## les regles de validation
=> il y a deux façon d'ajouter de nouvelles regles de validation
=> soit le filtre ne s'applique qu'à un seul champ
=>  il  faut  ajouter une methode à la classe NomForm, dont le nom commence par clean_suivi du nom du champ
def clean_message(self):
    message = self.cleaned_data['message']
    if "pizza" in message:
        raise forms.ValidationError("On ne veut pas entendre parler de pizza !")
    return message
=> soit le filtre dépend des données des autres champs
=> il faut ecraser la methode clean() heritée de la class form, elle renvoie un dictionnaire
def clean(self):
    cleaned_data = super(ContactForm, self).clean() # on appelle la methode clean parente (Form)
    sujet = cleaned_data.get('sujet') # .get() renvoie None si vide
    message = cleaned_data.get('message')
    if sujet and message:  # Est-ce que sujet et message sont valides ?
        if "pizza" in sujet and "pizza" in message:
            raise forms.ValidationError(
                "Vous parlez de pizzas dans le sujet ET le message ? Non mais ho !"
            )
    return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK
=> le message d'erreur dans ce cas là n'est pas associé à un seul champ donc il s'affiche par défaut en haut
=> on peut remplacer le rasie error par add_error() qui permet de spécifier où placer l'erreur, de plus il supprimer l'entrée correspondante au champ
    self.add_error("message",
                "Vous parlez déjà de pizzas dans le sujet, "
                "n'en parlez plus dans le message !"
            )
## LEs formulaires issus de modeles
=> ModelForm : généré automatiquement à partir d'un model
=> dans le fichier forms.py
from .models import NomDuModel

class NomDuModelForm(forms.ModelForm):
    class Meta:
        model = NomDuModel
        fields = '__all__'

=> il fait le lien avec les clés etrangères, et utilise des paramètres des champs du modele (verbose_name, label...)
=> il a une methode save() qui met à jour la base de données
=> pour l'edition, il suffit de passer en argument l'instance de l'objet à éditer dans la vue, exemple :
form = ArticleForm(instance=article)  
et pour la récupération
form = ArticleForm(request.POST, instance=article)
=> on peut exclure des champs de ce formulaire en ajoutant la methode exclude() dans la class Meta, ou juste selectionner certains dans fields (et changer leur ordre si besoin)
=> Attention, il faudra remplir les champs exclus après reception du formulaire s'ils sont obligatoire, la methode save a un argument (commit=false) permettant de ne pas faire de sauvegarde en BDD et de renvoyer à la place les données du formulaire que l'on peut completer ensuite
article = form.save(commit=False)

# La gestion des fichiers
=> Django se sert de la librairie Pillow pour faire des traitements sur les images
pip install pillow
=> dans un model on utilise un type ImageField , avec un argument upload_to qui indique l'endroit où sont stocké les images pour l'instance du model
=> dans le fichier settings.py il faut ajouter une variable MEDIA_ROOT qui sert de racine à upload_to
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
=> dans un formulaire on utilise forms.ImageField() , avec champ ImageField  Django vérifira qu'il s'agit d'une image valide
=> attention dans a vue il faut ajouter request.FILES lors de la création du form vu que request.POST ne traine que des données textuelles
form = NouveauContactForm(request.POST or None, request.FILES)
=> le champ ImageField renvoie une variable du type UploadedFile, qui est une classe définie par Django (héritant de django.core.files.File)
=> sans formulaire, par exemple avec la console, il faut créér un objet File
from django.core.files import File
c = Contact(nom="Jean Dupont", adresse="Rue Neuve 34, Paris")
c.photo = File(open('/mon/projet/media/photos/dupont.jpg', 'rb'))
=> la balise "form" doit posseder l'attribut enctype="multipart/form-data" pour accepter le fichier
=> si un fichier dans le dossier upload porte le même nom que celui déposé par le formulaire, Django ajoute une chaine de caractères aléatoire à la fin pour éviter de l'écraser

## Afficher une images
=> Par défaut Django ne s'occupa pas du service de fichiers media (images, musiques, videos..) et il est conseillée de laisser un autre serveur s'en occuper
=> en développement, il est possible de le faire tout de même et changer lors du déploiement
=> Il faut compléter la variable MEDIA_URL dans settings.py
MEDIA_URL = '/media/'
=> il faut ajouter dans le fichiers urls.py global
from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=> les fichiers sont maintenant accessibles depuis l'adresse MEDIA_URL

=>Chaque fichier dans Django a un attribut url #chemin absolu, en lecture seule, renvoyant l'URL complet vers le fichier. On peut donc l'utiliser au sein d'une balise <img />  sans soucis.
<img src="{{ contact.photo.url }}"/>
=> la variable ImageField possède deux attributs pour la taille : width #largeur et height #hauteur
=> autres attributs : size # taille en bytes, path #chemin relatif depuis MEDIA_ROOT

## les fichiers non Images
=> on utilise le type générique FileField, qui retourne aussi un objet django.core.files.File
=> il possede des attributs semblables à ImageField
=> possède les methodes read() et write()
=> il est possible de renommer les fichiers uploadés, Au lieu de passer une chaîne de caractères comme paramètre upload_to  dans le modèle, il faut lui passer une fonction qui retournera le nouveau nom du fichier. Cette fonction prend deux arguments : l'instance du modèle où le FileField  est défini, et le nom d'origine du fichier.
def renommage(instance, nom_fichier):
    return "{}-{}".format(instance.id, nom_fichier)
class Document(models.Model):
    nom = models.CharField(max_length=100)
    doc = models.FileField(upload_to=renommage, verbose_name="Document")


# Les vues génériques
=> systeme integré à Django pour eviter certaines lignes de code
=> un vue générique n'est pas une fonction (pas de def action:)
=> il faut un import , il existe plusieurs type de vue
from django.views.generic import TemplateView
=> Deux methodes pour les vues génériques
=> Soit on créé une classe, héritant d'un type de vue générique et surchargant ses attributs
- dans le fichier views (attention, ce n'est pas du django 2.0 !)
from django.views.generic import TemplateView

class FAQView(TemplateView):
   template_name = "blog/faq.html"  # chemin vers le template à afficher
- dans le fichier urls
from django.conf.urls import patterns, url, include
from . import views  # N'oubliez pas d'importer les vues

urlpatterns = [
    url(r'^faq$', views.FAQView.as_view()),   # Nous demandons la vue correspondant à la classe FAQView
]
 => Soit on appelle la classe générique avec les infos à utliser en arguments
 => on ne modifie que le fichier urls
 from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView  # L'import a changé, attention

urlpatterns = [
   url(r'^faq', TemplateView.as_view(template_name='blog/faq.html')),
]
## lister et afficher des données : ListView et DetailView
=> request est accible dans les views generiques
### ListView
=> on peut directement l'ajouter dans le fichier URLS
=> le template doit s'appeler <app>/<model>_list.html     __
=> l'unique variable, utilisable dans le template, retournée par la vue générique est object_list
=> mais cela est renommable dans les arguments du path dans urls
urlpatterns = [
    url(r'^$', ListView.as_view(model=Article,
                    context_object_name="derniers_articles",
                    template_name="blog/accueil.html")),
    ...
]
=> en passant par une classe, recommandé pour par exemple ajouter une pagination
=> dans le fichier urls
from . import views

urlpatterns = [
    # Via la fonction as_view, comme vu tout à l'heure
    url(r'^$', views.ListeArticles.as_view(), name="blog_liste"),  
    ...
]
=> dans le fichier view
class ListeArticles(ListView):
    model = Article
    context_object_name = "derniers_articles"
    template_name = "blog/accueil.html"
=> il est possible d'ajouter des filtres:
  paginate_by = 5 # créé une pagination avec 5 objects par page
  queryset = Article.objects.filter(categorie__id=1) # selection une valeur de catégorie
=> il est possible d'ajouter des arguments dans le path urls
=> mais il faut definir la methode queryset(self) dans la classe de vue generique
def get_queryset(self):
   #return Article.objects.filter(categorie__id=self.args[0])
   return Article.objects.filter(categorie__id=self.kwargs['id'])
=> ajouter des éléments au contexte , des variables envoyées au templates
=> il faut ecrire une méthode get_context_data(self, ** kwargs) :  
def get_context_data(self, ** kwargs):

    # Nous récupérons le contexte depuis la super-classe
    context = super().get_context_data( ** kwargs)
    # Nous ajoutons la liste des catégories, sans filtre particulier
    context['categories'] = Categorie.objects.all()
    return context
### DetailView
=> DetailView est dans ls principes similaire avec ListView
=> on doit passer un paramètre <int:pk> (primakey) dans l'url
=> on peut aussi utiliser get_queryset pour filtrer
=> il est possible de modifier l'objet via get_object avant affichage
def get_object(self):
    # Nous récupérons l'objet, via la super-classe
    article = super(LireArticle, self).get_object()
    article.nb_vues += 1  # Imaginons un attribut « Nombre de vues »
    article.save()
    return article  # Et nous retournons l'objet à afficher

## Agir sur les données (CRUD)
### CreateView
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy # django < 2
from django.urls import reverse_lazy # django 2

class URLCreate(CreateView):
    model = MiniURL
    template_name = 'mini_url/nouveau.html'
    form_class = MiniURLForm
    success_url = reverse_lazy(liste) # django <2
    success_url = reverse_lazy('liste') # django 2
=> form_class permet de spécifier quel formulaire utilisteur
=> success_url indique la redirection, reverse_lazy permet d'utiliser une methode reverse() même si la configuration des URL n'a pas encore eu lieu (ce qui est le cas ici, puisque les vues génériques sont interprétées en Python avant l'éxécution des urls.py).
### UpdateView
=> la classe à définir est quasiment la même que pour CreateView
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy # django < 2
from django.urls import reverse_lazy # django 2

class URLUpdate(UpdateView):

    model = MiniURL
    template_name = 'mini_url/nouveau.html'
    form_class = MiniURLForm
    success_url = reverse_lazy(liste) # django <2
    success_url = reverse_lazy('liste') # django 2
=> par defaut le nom du template pour une vue UpdateView est <app>/<model>_update_form.html __
=> la balise form du template doit affcher une action vide ( action="")
=> on peut utiliser la methode get_object pour améliorer la récupération de l'objet à editer
=> par exemple recuperer par un slug au lieu de l'id
def get_object(self, queryset=None):
    code = self.kwargs.get('code', None)
    return get_object_or_404(MiniURL, code=code)
=> il est possible de changer le comportement de la validation form_valid()
def form_valid(self, form):
    self.object = form.save()
    # Envoi d'un message à l'utilisateur
    messages.success(self.request, "Votre profil a été mis à jour avec succès.")
    return HttpResponseRedirect(self.get_success_url())
### DeleteView
=> cette vue charge un objet et demande une confirmation de suppression
=> les attributs sont les mêmes

# technique avancée dans les modeles
## l'outil Q
from django.db.models import Q
=> permet decréer des requetes complexes sur les modèles
=> ajouter une clause "ou" : |
Eleve.objects.filter(Q(moyenne__gt=16) | Q(moyenne__lt=8))
=> ajouter une clause "et" : &
Eleve.objects.filter(Q(moyenne=10) & Q(nom="Sofiane"))
Eleve.objects.filter(Q(moyenne=10), Q(nom="Sofiane")) # les deux sont équivalents
=> ajouter une négation : ~
Eleve.objects.filter(Q(moyenne=10), ~Q(nom="Sofiane"))
=> un objet Q peut se construire de deux façons:
Q(moyenne=10) est équivalent à Q(('moyenne',10))
=> la seconde écriture permet de construire des requetes de la façon suivante :
conditions = [('moyenne', 15), ('nom', 'Bastien'), ('moyenne', 18)]
objets_q = [Q(x) for x in conditions]
=> et de les traiter ainsi
import operator
from functools import reduce
 Eleve.objects.filter(reduce(operator.or_, objets_q))
=> reduce est une fonction de functools qui permet d'appliquer une fonction successivement à plusieurs valeurs
)> cela equivaut à
Eleve.objects.filter(objets_q[0] | objets_q[1] | objets_q[2])
## l'agrégation / annotation
=> methode aggregate
from django.db.models import Avg
Eleve.objects.aggregate(Avg('moyenne'))
=> elle prend en paramètre une fonction spécifique et l'applique sur un champ du modèle, sur toutes les entrées
=> elle retourne un dictionnaire dont la clé est genérée automatiquement champ__fonction
ici ce serait 'moyenne__avg'
=> mais il est possivble de la spécifier : aggregate(Moyenne=Avg('moyenne'))
=> fonctions possibles : Avg (moyenne), Max (plus grande valeur), Min (plus petite valeur), Count (nombre d'entrées)
=> on peut appliquer plusieurs fonctions à la fois
Eleve.objects.aggregate(Avg('moyenne'), Min('moyenne'), Max('moyenne'))
{'moyenne__max': 18, 'moyenne__avg': 11.25, 'moyenne__min': 7}
=> on peut aggregate un QuerySet obtenu par filter
Eleve.objects.filter(nom__startswith="Ma").aggregate(Avg('moyenne'), Count('moyenne'))
=> un QuerySet possède une methode count() rendant parfois inutile celle d'aggregate
=> mais la methode count dans aggregate peut s'applique ren cas de liaisons entre deux modèles
Le modele Cours a une liaison ManyToManyField avec eleve
 Cours.objects.aggregate(Max("eleves__moyenne")) # la moyenne la plus élévée de tous les cours
 Cours.objects.aggregate(Count("eleves")) # le nombre d'élèves dans les cours (compte plusieurs fois un eleve s'il est dans plusieurs cours)
 => il est possible d'ajouter des attributs à un objet selon les objets auquels il est lité
 Cours.objects.annotate(Avg("eleves__moyenne"))[0].eleves__moyenne__avg # L'objet Cours[0] possède maintenant un attribut eleves__moyenne
 => on peut renommer l'attribut par default
 Cours.objects.annotate(Moyenne=Avg("eleves__moyenne"))[1].Moyenne # le cours [1] a un attribut moyenne
=> Et pour terminer en beauté, il est même possible d'utiliser l'attribut créé dans des méthodes du QuerySet comme filter,exclude ou order_by
Cours.objects.annotate(Moyenne=Avg("eleves__moyenne")).filter(Moyenne__gte=12)

# Heritage de modèles
=> Django propose 3 methodes pour gerer l'héritage de modèles
## les modeles parents abstraits
=> Django n'utilisera pas le modèle pour crééer une table et on ne peut pas faire de requetes dessus
=>  ce modèle permettra de décrire des attributs et methodes qui seront reutilisées dans d'autres modeles
=> il faut assigner l'attribut abstract=True dans sa classe Meta
class Meta:
    abstract = True
=> l'héritage des modeles est identique à celui des classes
class ModeleEnfant(ModelParent)
## Modele parent classique
=> des tables seront créés pour le modele parent et les modeles enfants
=> les enfants auront automatiquement les attributs du modele parent
=> un objet ModelEnfant est aussi un objet ModelParent et sera listé dans sa table
=> Django crée une relation Parent vers Enfant pour y acceder
ModelParent.ModelEnfant.attribut
## Modele Proxy
=> un modèle proxy hérite de tous les attributs et méthodes du modèle parent, mais aucune table ne sera créée dans la base de données pour le modèle fils, le modele fils est une passerelle pour modele parent
=> tout objet créé avec le modèle parent sera accessible depuis le modèle fils, et vice-versa
=> on peut modifier le modele proxy sans alterer le modele d'origine
=> on indique proxy=True dans la classe Meta du modele fils
## L'application ContentType
=> application installée par defaut dans INSTALLED_APPS du settings.py de django:
'django.contrib.contenttypes'
=> ce modele permet de representer un autre modele
from blog.models import Eleve
from django.contrib.contenttypes.models import ContentType
ct = ContentType.objects.get(app_label="blog", model="eleve")
ct => <ContentType: eleve>
=> ContentType possède deux methodes :
- model_class : renvoie la classe du modèle représenté
 - get_object_for_this_type : raccourci de ct.model_class().objects.get(attr=arg)
=> l'interêt? Il existe des modeles Article, Image, Video, on veut pouvoir les commenter sans changer leur code
=> relations générique des ContentType
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Commentaire(models.Model):

    auteur = models.CharField(max_length=255)
    contenu = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "Commentaire de {0} sur {1}".format(self.auteur, self.content_object)

=> contrairement à une relation ciblée, le modele associé n'est pas defini précisement lors de la declaration
=> le ContentType permet de representer le modele, l'object_id contiendra l'ID de l'entrée
=> Le champ content_object est une combinaison  des deux champs
e = Eleve.objects.get(nom="Sofiane")
c = Commentaire.objects.create(auteur="Le professeur",contenu="Sofiane ne travaille pas assez.", content_object=e)
=> il est également possible d'ajouter une relation générique « en sens inverse ». Contrairement à une ForeignKey classique, aucune relation inverse n'est créée. Pour  en créer une sur un modèle bien précis, il suffit d'ajouter un champ nommé GenericRelation.
  commentaires = GenericRelation('Commentaire')
=> il est possible de personnaliser les noms content_type / object_id , il faut les preciser si l'on fait la relation inverse
commentaires = GenericRelation(Commentaire,
    content_type_field="le_champ_du_content_type",
    object_id_field="le champ_de_l_id")

# filtes et tags
=> soit on les place dans l'application concernée
=> soit on crée une application qui regroupe les filtres et tags, il faudra l'ajouter dans INSTALLED_APPS de  settings.py
=> on crée un repertoire templatetags , dans lequel on crée un fichier python par groupe de filtres/tags et un fichier __init__.py
=> il faut spécifier une instance de classe pour enregistrer le filtres/tags
from django import template

register = template.Library()
=> on pourra inclure les tags/filtres dans les template en ecrivant  {% load nom_fichier_python %} # ici ce sera blog_extra, on peut écrire plusieurs noms de fichier
=> un redemarrage du serveur est necessaire !
=> Tous les dossiers templatetagsde toutes les applications partagent le même espace de noms. il faut veiller à ce que leur noms de fichiers soient différents, afin qu'il n'y ait pas de conflit.

=> une fois un filtre defini, il y  a deux possibilité pour l'utilisera
 - Soit en ajoutant la ligne @register.filter comme décorateur de la fonction. L'argument name peut être indiqué pour choisir le nom du filtre ;
 - Soit en appelant la méthode register.filter('citation', citation)
=> ces trois écritures sont équivalents
 @register.filter
 def citation(texte):   
     return "&laquo; {} &raquo;".format(texte)

@register.filter(name='mon_filtre_citation')
 def citation2(texte):
     return "&laquo; {} &raquo;".format(texte)

 def citation3(texte):
     return "&laquo; {} &raquo;".format(texte)
 register.filter('un_autre_filtre_citation', citation3)
=> si l'on utilise des caractères spéciaux on doit ajouter l'argument is_safe=True pour eviter que Django les enleve
=> il est préférable de limiter l'escape aux caractères du filtre, sinon cela s'appliquerait aussi sur la chaine de caractère sur lequel le filtre est appliqué
=> Cela peut être fait via la fonction espace du moduledjango.utils.html
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def citation(texte):
    """
    Affiche le texte passé en paramètre, encadré de guillemets
    français doubles et d'espaces insécables.
    """
    res = "&laquo; {} &raquo;".format(escape(texte))
    return mark_safe(res)

## filtres avec argument
{{ ma_chaine|smart_truncate:40 }}
=> il faut ajouter un paramètre dans la definition du filtre
def nom_filtre(element_sur_lequel_le filtre_est_applique, argument)

## template context processor / contexte de template
=> un contexte est l'ensemble des variables disponibles dans un templates
=> le but des template context processor est de préremplir le contexte de la requete et de disposer les données dans tous les templates du projet
=> lors d'un render, on envoie des variables à ce contexte, mais il en contient d'autres
=> si par exemple on veut qu'une donnees soit sur tous les templates, on va creer une fonction appelée à chaque page et qui incorporera cette donnée de façon automatique
=> il faut créer un fichier context_processors.py dans un application, idéalement dans le sous-dossier ayant le même nom que le projet. Les fonctions y seront définies
=> django execute la vue avant le contexte, il faut des noms de variables n'existant pas dans les vues
=> une fois la fonction définie, il faut modifier TEMPLATES dans le fichier settings.py en rajoutant le chemin vers la fonctions dans 'context_processors'
'context_processors': [
    ...,
    'crepes_bretonnes.context_processors.get_infos',
],
=> render est une fonction executant plusieurs actions en interne, dont le chargement des context_processors=> mais par exemple render_to_response ne le fait pas, il faut preciser le contexte dans l'appelerreturn render_to_response('blog/archives.html', locals(), context_instance=RequestContext(request))

## custom templatetags
=> un tag est décomposé en deux parties : sa structure et son rendu. Il faut préciser comment l'écrire et ce qu'il renvoie.
=> un template est divisé et parcouru par un parseur, lorsqu'il rencontre un tag il appele la methode correspondante au nom du tag (la fonction vérifie les paramètres)
=> exemple, création d'un tag {% random 0 42 %} renvoyant un nombre aléatoire entre 0 et 42
=> la methode doit prendre deux arguments précis :
- parser (l'objet parsant le template actuel)
- token qui contient les informations sur le tag, dont les paramtètres et des methodes dont la méhode split_contents() qui sépare les arguments
=> si un tag est malformé , une erreur HTTP 500 est levé
=> la methode random, pour note exemple, verifie les paramètre (nombres, type) et qui retourne un RandomNode(begin, end)
=> il faut définir la classe RandomNode (classe __init__  avec les attributs begin et end, et la classe obligatoire render(self, context))
=> Django faisant une concaténation des noeuds, le render doit être une chaine de caractères
=> enregistrement du tags, comme pour les filtres 3 méthodes:
 - @register.tag au debut de la fonction
 - @register.tag(name="nom_du_tag") si on veut le renommer
 - register.tag('nom_du_tag', random) après la déclaration de la fonction

# signaux et midllewares
## Les signaux
=> un signal est une notification envoyée par une application à Django quand une action se réroule et renvoyé par le framework à toutes les autres parties d'applications qui se sont enregistrées pour savoir quand ce type d'action se déroule et comment
=> exemple : une instance de  modele est gérée par plusieurs disques durs, lorsqu'elle est supprimée, il faudrait que les fichiers associés soient effacés.
=> une fonction de suppression de ces fichier etant créé, il suffit d'indiquer à Django de l'appeller à chaque fois qu'une entrée de modele est supprimée
from django.db.models.signals import post_delete

post_delete.connect(ma_fonction_de_suppression, sender=MonModele)
=> on importe le signal et on utilise la fonctionne connect pour lui lier une fonction.
=> sender permet de restreindre l'envoie de signaux à un model précis
=> chaque type de signal possède ses propres arguments
=> post_delete:
 - sender : le modele concerné
 - instance: instance du modèle supprimée
 - using: alias de la base de données utilisée (utile uniquement en cas de multiple base)
 => la fonction de suppression pourra s'ecrire ainsi:
def ma_fonction_de_suppression(sender, instance, ** kwargs):
=> il n'y a pas de certitude sur les arguments du signal, le kwargs permet de tous les récuperer et de chercher ce qui nous interesse par la clé du dictionnaire
=>  où placer la fonction? généralement models.py vu que les signaux sont souvent liées à des actions sur des modeles
=> il est possible d'utiliser un decorateur
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=MonModele)
def ma_fonction_de_suppression(sender, instance, ** kwargs):
=> les différents types de signaux:
- django.db.models.signals.pre_save : envoyé avant la sauvegarde d'une instance
  - sender / instance / using / raw (boolean, True indique qu'elle sera sauvegardée telle quelle)
- django.db.models.signals.post_save : envoyé après la sauvegarde d'une instance
  - sender / instance / using / raw / created (boolean, True indique que l'enregistrement s'est bien passé)
- django.db.models.signals.pre_delete : envoyé avant la suppression d'une instance
  - sender / instance / using
- django.db.models.signals.post_delete : envoyé après la suppression d'une instance
  - sender / instance / using
- django.core.signals.request_started : envoyé quand django reçoit une nouvelle requete http:
 - sender ( la classe qui a envoyé la requete)
- django.core.signals.request_finished : envoyé quand django termine de répondre à une requete http:
 - sender ( la classe qui a envoyé la requete)
...
=> il est bien sûr possible de créer son propre signal, chaque signal est une instance de django.dispatch.Signal
=> pour crééer un nouveau signal il suffit de crééer une nouvelle instance et lui donner des arguments à transmettre
from django.dispatch import Signal

crepe_finie = Signal(providing_args=["adresse", "prix"])
=> on peut ensuite lier une fonction à ce signal
crepe_finie.connect(faire_livraison)   # Quand crepe_finie est lancé, appeler 'faire_livraison'
=> pour lancer une notification à toutes les fonctions enregistrées, il faut utiliser la methode send() avec l'argument sender
crepe_finie.send(sender=self, adresse=adresse, prix=self.prix)

=> deconnecter une fonction d'un signal, si un argument sender est fourni lors de la connexion, il doit y être aussi lors de la deconnexion
crepe_finie.disconnect(faire_livraison)

## les middlewares
=> a chaque requete, django execute du code middleware, des fonctions executées et enrobant la vue appelée
=> modifier certaines variables/ interrompre le processus de traitement ...
=> un midlleware est une fonction qui retourne une autre fonction qui sera appelée à chque fois que Django reçoit une requete. La fonction principale prend en parametre une méthode , fournie par Django qui va nous permettre de lancer l'appel de la vue demandée par l'utilisateur et ainsi lui renvoyer la réponse

=> ils sont enregistrés dans settings.py, il faut ajouter ceux que l'on a crée à la liste. tous les middlewares sont appelées dans l'ordre de ce fichier. Chaque fonction englobe donc la suivante
def simple_middleware(get_response):

    # Le code ici est appelé une seule fois, pour l'initialisation
    # et la configuration
    def middleware(request):
        # Code qui sera exécuté à chaque requête, et avant
        # le traitement de la réponse

        response = get_response(request)
        # Code qui sera exécuté à chaque requête, une fois la
        # réponse calculée, mais pas encore servie

        return response
    return middleware
=> Il est dès lors possible d'intercepter toute requête, d'en modifier ses paramètres puis de laisser continuer son exécution, ou de même décider de renvoyer une réponse tout à fait différente. De même, il est tout à fait possible de modifier une réponse calculée.
def middleware1(get_response):

    def middleware(request):
        print("J'ouvre le bal de la requête")
        response = get_response(request)
        print("Et je clôture également le show.")
        return response
    return middleware


def middleware2(get_response):
    def middleware(request):
        print("J'englobe également la vue, mais après")
        response = get_response(request)
        print("Compris ?")
        return response
    return middleware


def ma_vue(request):
    print("Enfin, nous arrivons dans la vue !")
    return HttpResponse("Ma réponse")
=> donnera
J'ouvre le bal de la requête
J'englobe également la vue, mais après
Enfin, nous arrivons dans la vue !
Compris ?
Et je clôture également le show.
=> exemple sur l'application stats
=> A l'image de l'objet Q, il existe un objet F qui permet de faire des requetes sql elaborées, gérant par exemple l'opération "+1"
UPDATE stats_page SET nb_visites=nb_visites+1 # Q ferait un select puis un update
=> C'est un outil pratique pour optimiser de simples opérations numériques sur des champs.

=> Avant chaque appel de vue Django appelle la methode process_view qui se charge de determiner si l'url de la page a déjà été appelée (l'url est accessible de partout grace à request.path de l'objet HttpRequest)
=> le middleware inctemente le compteur d'entrée ou en créé un
=> ensuite on verifie si la requete s'est bien passée (instance response), le code HTTP 200 et on modifie le contenu de la réponse (inclut dans response.content)
=>  En pratique, on ne modife jamais la réponse via un middleware, pensez aux template context processors !
