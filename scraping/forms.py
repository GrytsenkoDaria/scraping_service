from django import forms

from .models import City, Language


class SearchForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Місто',
        to_field_name='name',
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Спеціальність',
        to_field_name='name',
    )
