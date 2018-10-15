from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext


def test_i18n(request):

    nb_chats = 2
    couleur = "blanc"
    chaine = _("J'ai un %(animal)s %(col)s.") % {'animal': 'chat', 'col': couleur}
    ip = _("Votre IP est %s" % request.META['REMOTE_ADDR'])
    infos = ungettext(
        "… et selon mes informations, vous avez %(nb)s chat %(col)s !",
        "… et selon mes informations, vous avez %(nb)s chats %(col)ss !",
        nb_chats) % {'nb': nb_chats, 'col': couleur}

    return render(request, 'i18napp/test_i18n.html', locals())
