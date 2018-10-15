from django.shortcuts import (render, get_object_or_404, redirect)
from django.views.generic import (CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage
from .models import MiniURL
from .forms import MiniURLForm


def lister_mini_urls(request, page=1):
    mini_urls = MiniURL.objects.order_by('-nombre_acces')
    paginator = Paginator(mini_urls, 2)

    try:
        minis = paginator.page(page)
    except EmptyPage:
        # on renvoie la dernière pas si la page indiquée n'existe pas
        minis = paginator.page(paginator.num_pages)

    return render(request, 'mini_url/mini_urls.html', {
        'mini_urls': minis
        }  # on pourrait mettre uniquement local() au lieu du dictionnaire
                 )


def creer_mini_url(request):
    form = MiniURLForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(lister_mini_urls)

    return render(request, 'mini_url/creation_mini_url.html', locals())


def acceder_url(request, code):
    mini_url = get_object_or_404(MiniURL, code=code)
    mini_url.nombre_acces += 1
    mini_url.save()
    return redirect(mini_url.url, permanent=True)


class URLCreate(CreateView):
    model = MiniURL
    template_name = 'mini_url/creation_mini_url.html'
    form_class = MiniURLForm
    success_url = reverse_lazy('liste_url')


class URLUpdate(UpdateView):

    model = MiniURL
    template_name = 'mini_url/creation_mini_url.html'
    form_class = MiniURLForm
    success_url = reverse_lazy('liste_url')

    def get_object(self, queryset=None):
        code = self.kwargs.get('code', None)
        return get_object_or_404(MiniURL, code=code)


class URLDelete(DeleteView):

    model = MiniURL
    context_object_name = "mini_url"
    template_name = 'mini_url/supprimer.html'
    success_url = reverse_lazy('liste_url')

    def get_object(self, queryset=None):
        code = self.kwargs.get('code', None)
        return get_object_or_404(MiniURL, code=code)
