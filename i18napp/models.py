from django.db import models
import random
import string
from django.utils.translation import ugettext_lazy as _


class MiniURL(models.Model):
    url = models.URLField(verbose_name=_("URL à réduire"), unique=True)
    code = models.CharField(max_length=6, unique=True)
    date = models.DateTimeField(auto_now_add=True,
                                verbose_name=_("Date d'enregistrement"))
    pseudo = models.CharField(max_length=255, blank=True, null=True)
    nb_acces = models.IntegerField(default=0,
                                   verbose_name=_("Nombre d'accès à l'URL"))

    def __str__(self):
        return "[{0}] {1}".format(self.code, self.url)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.generer(6)
        super(MiniURL, self).save(*args, **kwargs)

    def generer(nb_caracteres):
        caracteres = string.ascii_letters + string.digits
        aleatoire = [random.choice(caracteres) for _ in range(nb_caracteres)]

        self.code = ''.join(aleatoire)

    class Meta:
        verbose_name = _("Mini URL")
        verbose_name_plural = _("Minis URLs")
