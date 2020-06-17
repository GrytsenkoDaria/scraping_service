from django.db import models

from .utils import from_cyrillic_to_eng

import jsonfield


def default_urls():
    return {'work': '', 'rabota': '', 'dou': '', 'djinni': ''}


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
            super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    description = models.TextField()
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Vacancies'

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()  # noqa | to support in sqllite3 - in postgres threre is such field in sqllite - no


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
