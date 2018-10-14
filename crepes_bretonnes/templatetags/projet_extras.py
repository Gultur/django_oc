from django import template
register = template.Library()

from random import randint

@register.tag
def random(parser, token):
    """ Tag générant un nombre aléatoire, entre les bornes données en arguments """
    # Séparation des paramètres contenus dans l'objet token. Le premier
    # élément du token est toujours le nom du tag en cours
    try:
        nom_tag, begin, end = token.split_contents()
    except ValueError:
        msg = 'Le tag %s doit prendre exactement deux arguments.' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    # Nous vérifions ensuite que nos deux paramètres sont bien des entiers
    try:
        begin, end = int(begin), int(end)
    except ValueError:
        msg = 'Les arguments du tag %s sont obligatoirement des entiers.' % nom_tag
        raise template.TemplateSyntaxError(msg)

    # Nous vérifions si le premier est inférieur au second
    if begin > end:
        msg = 'L\'argument "begin" doit obligatoirement être inférieur à l\'argument "end" dans le tag %s.' % nom_tag
        raise template.TemplateSyntaxError(msg)
    return RandomNode(begin, end)


class RandomNode(template.Node):
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def render(self, context):
        return str(randint(self.begin, self.end))
