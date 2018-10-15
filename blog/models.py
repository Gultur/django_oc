from django.db import models
from django.utils import timezone
# timezone est l'équivalent de datetime.datetime mais avec support des fuseaux horaires


class Article(models.Model):
    titre = models.CharField(max_length=100)
    # le slug permet d'eviter d'utiliser des id dans les adresses
    slug = models.SlugField(max_length=100)
    auteur = models.CharField(max_length=42)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date de parution")
    # on passe une fonction en argument 'timezone.now' mais sans ()
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)

    class Meta:

        verbose_name = "article"
        ordering = ['date']
        permissions = (
            ("commenter_article", "Commenter un article"),
            ("marquer_article", "Marquer un article comme lu"),
            )

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        """
        return self.titre


class Categorie(models.Model):

    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Moteur(models.Model):
    nom = models.CharField(max_length=25)

    def __str__(self):
        return self.nom


class Voiture(models.Model):
    nom = models.CharField(max_length=25)
    moteur = models.OneToOneField(Moteur, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Vendeur(models.Model):

    nom = models.CharField(max_length=30)
    # le through indique par quel model intermediaire passer
    # cad celui de la table de correspondance / model Offre
    # la relation inverse est desactivee
    produits = models.ManyToManyField(Produit, through='Offre',
                                      related_name='+')
    # le second ManyToManyField est une relation sans modele intermediaire
    produits_sans_prix = models.ManyToManyField(Produit, related_name="vendeurs")
# il faut modifier un related_name pour eviter les conflits
    def __str__(self):
        return self.nom


class Offre(models.Model):
    # ce model remplace la table de correspondance créée automatiquement par la relation ManyToManyField
    # il faut indiquer les ForeignKey

    # on ajoute une information supplémentaire sur cette liaison
    # le prix , un entier
    prix = models.IntegerField()
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} vendu par {1}".format(self.produit, self.vendeur)


class Contact(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    photo = models.ImageField(upload_to="photos/")

    def __str__(self):
        return self.nom
