Quel est l’avantage (toujours vrai) d’une vue générique TemplateView ?
Cela permet d’écrire une vue simple, sans données, directement dans le urls.py    

Quel est le nom du template par défaut dans le cadre d’une ListView ?   
<app>/<model>_list.html __

Quelle est l’utilité de reverse_lazy ?
Cette fonction permet de récupérer l’URL d’une vue à l’exécution plutôt qu’à l’initialisation du code    

Quel est l’inverse de la requête suivante ?
Eleve.objects.exclude(classe="1ere", sexe="H")

Que fait cette requête ?
Elle renvoie le nombre d’élèves dont le nom ne commence pas par "F" et la moyenne globale de ceux-ci  

Combien de tables SQL seront créées avec les modèles suivants ?
3

En reprenant les modèles de la question précédente, laquelle de ces lignes est incorrecte ? On suppose que l’on récupère une entrée de la base à chaque fois sans problème
AdministrationPublique.objects.get(id=1).maires sans problème.

Quel tag permet de charger une librairie de tags et filtres contenue dans blog_extras.py ?   
{% load blog_extras %}

Comment est représenté un filtre avec paramètre ?
Par une fonction avec 2 arguments : valeur et arg

Qu’affichera {{ taux_change }} dans accueil.html ?
Rien du tout

Quelles sont les deux étapes à implémenter pour la réalisation d’un tag ?
La fonction de compilation et le rendu

Qu’est-ce qu’il n’est pas possible de faire avec un signal ?
Incrémenter un compteur à chaque utilisation d’un filtre  

Quand est exécuté un middleware ?
Ça dépend du middleware    

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
