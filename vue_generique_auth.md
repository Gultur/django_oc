Vue :django.contrib.auth.views.login.
Arguments optionnels :
    template_name: le nom du template à utiliser (par défautregistration/login.html).

Contexte du template :
    form: le formulaire à afficher ;
    next: l'URL vers laquelle l'utilisateur sera redirigé après la connexion.

Affiche le formulaire et se charge de vérifier si les données saisies correspondent à un utilisateur. Si c'est le cas, la vue redirige l'utilisateur vers l'URL indiquée danssettings.LOGIN_REDIRECT_URLou vers l'URL passée par le paramètre GETnexts'il y en a un, sinon il affiche le formulaire. Le template doit pouvoir afficher le formulaire et un bouton pour l'envoyer.
Se déconnecter

Vue :django.contrib.auth.views.logout.
Arguments optionnels (un seul à utiliser) :
    next_page: l'URL vers laquelle le visiteur sera redirigé après la déconnexion ;
    template_name: le template à afficher en cas de déconnexion (par défautregistration/logged_out.html) ;
    redirect_field_name: utilise pour la redirection l'URL du paramètre GET passé en argument.

Contexte du template :
    title: chaîne de caractères contenant « Déconnecté ».

Déconnecte l'utilisateur et le redirige.
Se déconnecter puis se connecter

Vue :django.contrib.auth.views.logout_then_login.
Arguments optionnels :
    login_url: l'URL de la page de connexion à utiliser (par défaut utilisesettings.LOGIN_URL).

Contexte du template : aucun.

Déconnecte l'utilisateur puis le redirige vers l'URL contenant la page de connexion.
Changer le mot de passe

Vue :django.contrib.auth.views.password_change.
Arguments optionnels :
    template_name: le nom du template à utiliser (par défautregistration/password_change_form.html) ;
    post_change_redirect: l'URL vers laquelle rediriger l'utilisateur après le changement du mot de passe ;
    password_change_form: pour spécifier un autre formulaire que celui utilisé par défaut.

Contexte du template :
    form: le formulaire à afficher

Affiche un formulaire pour modifier le mot de passe de l'utilisateur, puis le redirige si le changement s'est correctement déroulé. Le template doit contenir ce formulaire et un bouton pour l'envoyer.
Confirmation du changement de mot de passe

Vue :django.contrib.auth.views.password_change_done.
Arguments optionnels :
    template_name: le nom du template à utiliser (par défautregistration/password_change_done.html).

Contexte du template : aucun.

Vous pouvez vous servir de cette vue pour afficher un message de confirmation après le changement de mot de passe. Il suffit de faire pointer la redirection dedjango.contrib.auth.views.password_changesur cette vue.
Demande de réinitialisation du mot de passe

Vue :django.contrib.auth.views.password_reset.
Arguments optionnels :
    template_name: le nom du template à utiliser (par défautregistration/password_reset_form.html) ;
    email_template_name: le nom du template à utiliser pour générer l'e-mail qui sera envoyé à l'utilisateur avec le lien pour réinitialiser le mot de passe (par défautregistration/password_reset_email.html) ;
    html_email_template_name : le nom du template HTML à utiliser pour l'e-mail. Par défaut, l'e-mail n'est envoyé qu'au format texte.
    subject_template_name: le nom du template à utiliser pour générer le sujet de l'e-mail envoyé à l'utilisateur (par défautregistration/password_reset_subject.txt) ;
    password_reset_form: pour spécifier un autre formulaire à utiliser que celui par défaut ;
    post_reset_redirect: l'URL vers laquelle rediriger le visiteur après la demande de réinitialisation ;
    from_email: une adresse e-mail valide depuis laquelle sera envoyé l'e-mail (par défaut, Django utilisesettings.DEFAULT_FROM_EMAIL).

Contexte du template :
    form: le formulaire à afficher.

Contexte de l'e-mail et du sujet :
    user: l'utilisateur concerné par la réinitialisation du mot de passe ;
    email: un alias pouruser.email;
    domain: le domaine du site web à utiliser pour construire l'URL (utiliserequest.get_host()pour obtenir la variable) ;
    protocol:httpouhttps;
    uid: l'ID de l'utilisateur encodé en base 36 ;
    token: letokenunique de la demande de réinitialisation du mot de passe.

La vue affiche un formulaire permettant d'indiquer l'adresse e-mail du compte à récupérer. L'utilisateur recevra alors un e-mail (il est important de configurer l'envoi d'e-mails, référez-vous à l'annexe sur le déploiement en production pour davantage d'informations à ce sujet) avec un lien vers la vue de confirmation de réinitialisation du mot de passe.

Voici un exemple du template pour générer l'e-mail :

Une demande de réinitialisation a été envoyée pour le compte {{ user.username }}. Veuillez suivre le lien ci-dessous :

{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb36=uid token=token %}

Confirmation de demande de réinitialisation du mot de passe

Vue :django.contrib.auth.views.password_reset_done.
Arguments optionnels :
    template_name: le nom du template à utiliser (par défautregistration/password_reset_done.html).

Contexte du template : vide.

Vous pouvez vous servir de cette vue pour afficher un message de confirmation après la demande de réinitalisation du mot de passe. Il suffit de faire pointer la redirection dedjango.contrib.auth.views.password_resetsur cette vue.
Réinitialiser le mot de passe

Vue :django.contrib.auth.views.password_reset_confirm.
Arguments optionnels :

    template_name: le nom du template à utiliser (par défautregistration/password_reset_confirm.html) ;
    set_password_form: pour spécifier un autre formulaire à utiliser que celui par défaut ;
    post_reset_redirect: l'URL vers laquelle sera redirigé l'utilisateur après la réinitialisation.

Contexte du template :
    form: le formulaire à afficher ;
    validlink: booléen, mis àTruesi l'URL actuelle représente bien une demande de réinitialisation valide.

Cette vue affichera le formulaire pour introduire un nouveau mot de passe, et se chargera de la mise à jour de ce dernier.
Confirmation de la réinitialisation du mot de passe

Vue :django.contrib.auth.views.password_reset_complete.
Arguments optionnels :
    template_name: le nom du template à utiliser (par défautregistration/password_reset_complete.html).
Contexte du template : aucun.
Vous pouvez vous servir de cette vue pour afficher un message de confirmation après la réinitialisation du mot de passe. Il suffit de faire pointer la redirection de django.contrib.auth.views.password_reset_confirm sur cette vue.
