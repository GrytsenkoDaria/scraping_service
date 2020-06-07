from django.shortcuts import render

from .models import Vacancy
from .forms import SearchForm


def home(request):
    # print(request.GET)
    form = SearchForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    if city or language:
        f = {}
        if city:
            f['city__name'] = city
        if language:
            f['language__name'] = language

        qs = Vacancy.objects.filter(**f)
    else:
        qs = Vacancy.objects.all()
    return render(request, 'home.html', {'object_list': qs, 'form': form})
