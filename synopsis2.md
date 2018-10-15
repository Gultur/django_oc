
# les utilisateurs
## modèle user de base
=> Par defaut l'application gérant les utilisateurs est installée
=> settings.py : 'django.contrib.auth'et'django.contrib.contenttypes'
django.contrib.sessions.middleware.SessionMiddleware ; # supprimée django 1.10
django.contrib.auth.middleware.AuthenticationMiddleware
=> un modèle User : django.contrib.auth.models.User
username: nom d'utilisateur, 30 caractères maximum (lettres, chiffres et les caractères spéciaux _, @, +, . et -) ; __
first_name: prénom, optionnel, 30 caractères maximum ;
last_name: nom de famille, optionnel, 30 caractères maximum ;
email: adresse e-mail ;
password: un hash du mot de passe. Django n'enregistre pas les mots de passe en clair dans la base de données,;
is_staff: booléen, permet d'indiquer si l'utilisateur a accès à l'administration de Django ;
is_active: booléen, par défaut mis àTrue. Si mis àFalse, l'utilisateur est considéré comme désactivé et ne peut plus se connecter. Au lieu de supprimer un utilisateur, il est conseillé de le désactiver afin de ne pas devoir supprimer d'éventuels modèles liés à l'utilisateur (avec une ForeignKey par exemple) ;
is_superuser: booléen, si mis à True, l'utilisateur obtient toutes les permissions
last_login:datetime, date/l'heure à laquelle l'utilisateur s'est connecté la dernière fois ;
date_joined:datetime, r date/l'heure à laquelle l'utilisateur s'est inscrit ;
user_permissions: une relation ManyToMany vers les permissions  ;
groups: une relation ManyToMany vers les groupes.
=> créer un utilisateur :
from django.contrib.auth.models import User
user = User.objects.create_user(nom, email, mot_de_passe)
=> password est un attribut qu'il n'est pas possible d'editer classiquement
=> Tous les mots de passe sont enregistrés selon cette disposition :algorithme$iterations$sel$empreinte
Algorithme : le nom de l'algorithme de la fonction de hachage utilisée pour le mot de passe (icipbkdf2_sha256, la fonction de hachage par défaut de Django). Il est possible de changer d'algorithme par défaut, tout en gardant la validité des anciens mot de passe, de cette manière ;
Itérations : le nombre de fois que l'algorithme va être exécuté afin de ralentir le processus. Si le chiffrement est plus lent, alors cela ralenti le nombre d'essais possible à la seconde via le bruteforce. Rassurez-vous, cette lenteur est invisible à l'oeil nu sur un essai ;
Sel : le sel est une chaîne de caractères insérée dans le mot de passe originel pour rendre son déchiffrage encore plus difficile (ici cRu9mKvGzMzW). Django s'en charge tout seul, inutile de s'y attarder ;
Empreinte : l'empreinte finale, résultat de la combinaison du mot de passe originel et du sel par la fonction de hachage après le nombre d'itérations précisé. Elle représente la majeure partie deuser.password.
=> les methodes pour le mot de passe:
set_password(mot_de_passe): permet de modifier le mot de passe de l'utilisateur par celui donné en argument. Django va hacher ce dernier comme vu précédemment. Cette méthode ne sauvegarde pas l'entrée dans la base de données, il faut faire un.save()par la suite.
check_password(mot_de_passe): vérifie si le mot de passe donné en argument correspond bien à l'empreinte enregistrée dans la base de données. RetourneTruesi les deux mots de passe correspondent, sinonFalse.
set_unusable_password(): permet d'indiquer que l'utilisateur n'a pas de mot de passe défini. Dans ce cas,check_passwordretournera toujoursFalse.
has_usable_password(): retourneTruesi le compte utilisateur a un mot de passe valide,Falsesiset_unusable_passworda été utilisé.
=> on peut étendre, pour ajouter des champs, le model user en créant un model qui sera lié en OneToOneField vers le model User (par exemple créer un model profil pour ajouter un avatar, une signature...)
=> il est possible de créer l'instance profil avec un signal post_save sur le model User
## les vues
=> pour l'enregistrement, faire un formulaire, une vue, un template...
=> Pour la connexion : formulaire avec pseudo/mot de passe, template, une vue
=> forms.PasswordInput permet d'avoir une boite de saisie avec caractères masqués
=> un utilisateur connecté est représenté par le modèle User, un invité par le modele AnonymousUser
=> la variable user dans les templates est ajoutée par un context_processors par defaut
=> dans les vues, c'est toujours accessible par request.user
=> les methodes pour agir sur la connexion : dans le module django.contrib.auth
=> verifier si un utilisateur existe : methode authenticate(username=nom, password=mdp)
=> faire une connexion : login(request, user):
=> pour la deconnexion, la methode logout
=> pour limiter l'accès de certaines pages à des utilisateurs connectés, django fournit un décorateur:
from django.contrib.auth.decorators import login_required

@login_required
def ma_vue(request):
=> l'utilisateur non connecté sera redirigé vers l'adresse de connexion, que l'on defini dans settings.py:
LOGIN_URL = '/connexion/'
=> django redirige avec une adresse possedant un paramètre next, indiquant la page d'où vient l'utilisateur
http://127.0.0.1:8000/authentification/connexion/?next=/authentification/prive/
=> il est possible de recuperer ce paralètre pour faire une redirection
=> on peut renommer ce parametre dans le décorateur , on peut aussi changer la redirection automatique
@login_required(redirect_field_name='rediriger_vers',login_url='/connexion_pour_concours/')
=> django utilise des signaux pour certains evenements utilisateur
user_logged_in : Envoyé quand un utilisateur se connecte, avec request et user en argument ;
user_logged_out : Envoyé quand un utilisateur se déconnecte, avec request et user en argument ;
user_login_failed : Envoyé quand une tentative de connexion a échoué avec credentials en argument, contenant des informations sur la tentative.

## les vues génériques
=> django.contrib.auth fournit des vues génériques pour la connexion / deconnexion / gestion du mot de mot_de_passe
=> Pour utiliser ces vues, il suffit de leur assigner une URL et de passer les  paramètres que l'on désire changer :
# On import les vues de Django, avec un nom spécifique
from django.contrib.auth import views as auth_views
path('connexion', auth_views.login, {'template_name': 'auth/connexion.html'})
=> voir vue_generique_auth.md  pas à jour django 2 : voir la doc
=> les vues génériques de gestion utilisateur cherchent par defaut dans un dossier registration
=> il faut bien sur faire les templates

## les permissions et groupes
=> une permission à la forme nom_application.nom_permission
=> Django crée automatiquement 3 permissions pour chaque modele
=> exemple pour un Article dans le module blog : blog.add_article, blog.change_article, blog.delete_article
=> on peut crééer une permission, un permission dépend d'un model et est décrite dans sa classe Meta
class Article(models.Model):
{ ... }
    class Meta:
        permissions = (
            ("commenter_article", "Commenter un article"),
            ("marquer_article", "Marquer un article comme lu"),
                    )
=> ajouter un permission se fait via un tuple(nom_permission, description_permission)
=> cela necessite un makemigration et un migrate
=> pour tester une permission : user.has_perm("blog.commenter_article") qui renvoit un boolean
=> c'est aussi récupérable grace à un context_processors "perms":
{% if perms.blog.commenter_article %}
=> les permissions sont exploitables par un décorateur:
from django.contrib.auth.decorators import permission_required

@permission_required('blog.commenter_article')
def article_commenter(request, article):
=> il est possible de créer dynamiquement une permission Pour cela, il faut importer le modèlePermission, situé dansdjango.contrib.auth.models. Ce modèle possède les attributs suivants :

    name: le nom de la permission, 50 caractères maximum.

    content_type: uncontent_typepour désigner le modèle concerné.

    codename: le nom de code de la permission.

Donc, si nous souhaitons par exemple créer une permission « commenter un article » spécifique à chaque article, et ce à chaque fois que nous créons un nouvel article, voici comment procéder :

from django.contrib.auth.models import Permission
from blog.models import Article
from django.contrib.contenttypes.models import ContentType

…  # Récupération des données
article.save()
content_type = ContentType.objects.get(app_label='blog', model='Article')
permission = Permission.objects.create(
    codename='commenter_article_{0}'.format(article.id),
    name='Commenter l\'article "{0}"'.format(article.titre),
    content_type=content_type)

=> Une fois que la permission est créée, il est possible de l'assigner à un utilisateur précis de cette façon :
user.user_permissions.add(permission)

Pour rappel,user_permissions est une relation ManyToMany de l'utilisateur vers la table des permissions.

## les groupes
Un groupe est un regroupement d'utilisateurs auquel nous pouvons assigner des permissions. Une fois qu'un groupe dispose d'une permission, tous ses utilisateurs en disposent automatiquement aussi. Il s'agit donc d'un modèle,django.contrib.auth.models.Group, qui dispose des champs suivants :
    name: le nom du groupe (80 caractères maximum) ;
    permissions: une relation ManyToMany vers les permissions, comme user_permissions pour les utilisateurs.

Pour ajouter un utilisateur à un groupe, il faut utiliser la relation ManyToMany groups de User:
from django.contrib.auth.models import User, Group
group = Group(name="Les gens géniaux")
group.save()
user = User.objects.get(username="Mathieu")
user.groups.add(group)

Une fois cela fait, l'utilisateur « Mathieu » dispose de toutes les permissions attribuées au groupe « Les gens géniaux ». Il conserve également les permissions qui lui ont été attribué spécifiquement. La méthode user.has_perm('app.nom_perm') vérifie donc si l'utilisateur à cette permission ou s'il appartient à un groupe ayant la permission app.nom_perm.

# les messages / notifications
=> système implémenté dans django, dans settings.py
'django.contrib.messages.middleware.MessageMiddleware', dans MIDDLEWARE
'django.contrib.messages', dans INSTALLED_APPS
'django.contrib.messages.context_processors.messages' dans TEMPLATE_CONTEXT_PROCESSORS (si la variable est absente, c'est par défaut)
=> Les message sont plusieurs niveaux d'"importance"', caractérisée par un entier  :
- DEBUG - 10 : phase de developpement uniquement, DEBUG=True dans settings.py
- INFO - 20 : information pour l'utilisateur
- SUCCESS - 25 : confirmation qu'une action s'est bien déroulée
- WARNING - 30 : pas d'erreur rencontrée, mais possibilité qur'il y en ait rapidement
- ERROR - 40 : une action ne s'est pas déroulée comme prévu
=> chaque niveau à un attribut "tags" associé (en minuscule), utile pour le CSS
=> depuis une vues
from django.contrib import messages
messages.add_message(request, messages.INFO, 'Bonjour visiteur !')
=> il existe des raccourcis pour les niveaux par défaut
messages.debug(request, '%s requêtes SQL ont été exécutées.' % compteur)
messages.info(request, 'Rebonjour !')
messages.success(request, 'Votre article a bien été mis à jour.')
messages.warning(request, 'Votre compte expire dans 3 jours.')
messages.error(request, 'Cette image n\'existe plus.')
=> le context_processers envoie une variable "messages" par défaut, l'affichage est dont simple dans le template
=> "messages" pouvant contenir plusieurs notifications il est necessaire de l'iterer
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
=> pour ajouter un niveau il suffit de creer une constante avec une valeur entière, on peut mettre un nom de tag en argument :
CRITICAL = 50
messages.add_message(request, CRITICAL, 'Une erreur critique est survenue.', extra_tags="fail")
=> on peut spécifier une constante MESSAGE_LEVEL , affecté à un entier, dans le fichiers settings pour définir une valeur minimale des messages à envoyer
=> c'est aussi faisable avec sur une vue en particulier  :
messages.set_level(request, messages.DEBUG)
=> dans le cas d'une application destinée à être incorporé dans des projets, sans être sur que le systeme de emssage soit présent, on peut les faire échouer silencieusement:
messages.info(request, 'Message à but informatif.', fail_silently=True)

# le cache
## systeme de cache
=> django dispose de plusieurs système de cache, sa configuration se faire grace à la constance  CACHES dans le fichier settings.py
- cache dans les fichiers : système enregistrant dans es fichiers sur le serveur, pour chaque valeur dans le cache , django va crééer un fichier et enregistrer le contenu de la donnée, en s'aidant du module pickle:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
=> location doit pointer vers un dossier et non un fichier (chemin absolu)
-  cache dans la mémoire : les données sont enregistrées dans la mémoire vive
'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
'LOCATION': 'cache_crepes'
=> le nom pour LOCATION doit être différent pour chaque projet django tournant sur un même serveur
=> c'est le cache par défaut de django  en développement, il n'est pas performant au nveau de la gestion de mémoire
- cache en base de données : il faut d'abord crééer une table spécifique dans la bases de données :
python manage.py createcachetable [nom_table_cache]
=> et il faut le spécifier dans le settings.py
'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
'LOCATION': 'nom_table_cache',
=> ce système peut être rapide et pratique mais il necessite de dedier un serveur physique pour la base de données
- en utilisant Memcached : c'est un système indépendant de django. Il faut lancer un programme responsable du cache, à qui Django enverra les données / les recuperera
=> ce système est plus efficace bien que necessitant un deploiement, il enregistre aussi en mémoire vive mais de façon plus efficace.
=> Memcached n'existe que sous linux :
(dans un terminal)
apt-get install memcached
memcached -d -m 512 -l 127.0.0.1 -p 11211 / -d demon -m taille maximum Mo -l adresse ip -p port
(dans django)
'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
'LOCATION': '127.0.0.1:11211',
=> location est l'adresse / port sur laquelle tourne memcached
- le cache inexistant : il active juste le système de cache , sans s'en servir
'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
## techniques de mise en cache
- cache par vue :  dès que le rendu d'une vue est calculé il est mis en cache, cela permet de recherche la page dans le cache sans rappeler la vue.
=> cette mise en cache se fait via un décorateur, avec comme paramètre la durée en seconde
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def lire_article(request, id):
    article = Article.objects.get(id=id)
=> chaque url aura sa propre mise en cache, il est possible de spécifier ce cache dans le fichier urls, il est du coup possible de l'affecter à des vues génériques , la vue doit etre sous forme de référence et non de chaine de caractère
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    re_path(r'^article/(\d{1,4})/$', cache_page(60 * 15)(views.lire_article)),
]
- cache dans les templates : en utlisant un tag {% cache %}, il doit être précédemment chargé par un {% load cache %}, ce tag prendre deux arguments au minimum, la durée d'expiration en seconde et le nom de la valeur/clé en cache
{% load cache %}
{% cache 500 carrousel %}
    # mon carrousel
{% endcache %}
=> on peut personnaliser la mise en cache en utilisant une clé dépendant de l'utilisateur, ex {% cache 500 user.username %}
- mise en cache bas niveau : il permet une mise en cache de variables bien récises. on utilise le module django.core.cache , partuculièrement des fonctions de l'objet cache. Objet qui se comporte comme un dictionnaire
from django.core.cache import cache
cache.set('ma_cle', 'Coucou !', 30)
cache.get('ma_cle')
'Coucou !'
=> set(clé, valeur, [durée  / optionnel]) stocke en cache, ecrase si déjè présente
=> get(clé, [valeur par defaut si clé non existante / optionnel])
=> add(clé, valeur) ajoute une clé uniquement si elle est absente
=> set_many, get_many permettent de gerer plusieurs variables
=> delete(cle) supprime du cache
=> clear() vide le cache
=> incr et decr permette d'incrementer ou de decrementer un nombre dans le cache sans passer par get puis set

# pagination
=> c'est le fait de diviser une liste d'objet en plusieurs pages
=> Django fournit une classe nommée Paginator qui effectue la pagination. Elle se situe dans le module django.core.paginator
=> le paginator commence à 1  et non 0
=> plusieurs exceptions peuvent être renvoyés selon les cas (argument not int, page vide)
=> paramètres optionnels du Paginator
- orphans=int : indique le nombre minimum d'objet à afficher dans la dernière page, si ce n'est pas le cas, ils sont reportés sur la page précédente
- allow_empty_first_page=True/False : permet de lancer une exception si la première page est vide
=> Des methodes de paginator :
- p = Paginator(liste, nombre_element_par_page)
- p.count : nombre d'objets, p.num_pages : nombre de page necessaire, p.page_range : la liste des pages
- page1 = p.page(1) => crée un objet Page
- page1.object_list : contenu de la page, page1.has_next()/has_previous : indique s'il y a une page suivante/precedente
=> pour l'utiliser il suffit d'importer le paginator et de l'initialiser dans une view
from django.core.paginator import Paginator, EmptyPage
paginator = Paginator(minis_list, 5)  # 5 liens par page
try (on recupere les élements de la page)/ except EmptyPage
=> dans le template, il suffit d'utiliser les attribut has_previous/has_next sur la liste d'éléments récupérés
=> elts.number : indique le numéro de page actuelle, previous_page_number/next_page_number : numéro page précendent/suivante

+> il est possible de prévoir un template spécifique pour les paginations et l'include par la suite
{% include "pagination.html" with liste=minis view="liste_url" %}
