from django.contrib import admin
from .models import Categorie, Article, Contact
# import pour la methode affichant une portion du contenu
from django.utils.text import Truncator


class ArticleAdmin(admin.ModelAdmin):

    # liste des champs à afficher dans le tableau
    list_display = ('id','titre', 'auteur', 'date', 'apercu_contenu')
    # liste des champs permettant de filtrer les entrées
    list_filter = ('auteur', 'categorie',)
    # permet de filtrer par date de façon intuitive
    date_hierarchy = 'date'
    # Tri par défaut du tableau
    ordering = ('date', )
    # Configuration du champ de recherche
    search_fields = ('titre', 'contenu')
    # ordre d'apparation des champs d'edition
    # fields = ('titre', 'auteur', 'categorie', 'contenu')

    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
        ('Général', {
            'classes': ['collapse', ],
            'fields': ('titre', 'auteur', 'slug', 'categorie')
        }),
        # Fieldset 2 : contenu de l'article
        ('Contenu de l\'article', {
            'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
            'fields': ('contenu', )
        }),
    )

    prepopulated_fields = {'slug': ('titre', ), }

    def apercu_contenu(self, article):
        """
        Retourne les 40 premiers caractères du contenu de l'article,
        suivi de points de suspension si le texte est plus long.

        On pourrait le coder nous même, mais Django fournit déjà la
        fonction qui le fait pour nous !
        """
        return Truncator(article.contenu).chars(40, truncate='...')

    # En-tête de notre colonne
    apercu_contenu.short_description = 'Aperçu du contenu'


admin.site.register(Categorie)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Contact)
