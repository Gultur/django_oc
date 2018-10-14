import random
import string
from django.db import models
from django.utils import timezone

# Create your models here.


class MiniURL(models.Model):

    url = models.URLField(unique=True, verbose_name='URL à réduire')
    code = models.CharField(unique=True, max_length=6)
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date de génération")
    pseudo = models.CharField(max_length=20, blank=True, null=True)
    nombre_acces = models.IntegerField(default=0, verbose_name="Nombre d'accès à l'URL")

    def __str__(self):
        return "[{0}] {1}".format(self.code, self.url)

    # on altère la methode save pour inclure la génération de code
    def save(self, *args, **kwargs):
        # self.pk cherche la clé primaire : l'identifiant
        if self.pk is None:
            self.generer(6)

        # ligne indispensable qui appelle la methode save originale (celle du parent)
        super(MiniURL, self).save(*args, **kwargs)

    # il serait possible de mettre cette fonction en dehors du modele
    # on écrirait self.code = generer(6) au moment de l'appel
    # et uniquement return ''.join(aleatoire) dans la fonction
    def generer(self, nb_caracteres):
        caracteres = string.ascii_letters + string.digits
        aleatoire = [random.choice(caracteres) for _ in range(nb_caracteres)]

        self.code = ''.join(aleatoire)

    class Meta:
        verbose_name = "Mini URL"
        verbose_name_plural = "Minis URL"
