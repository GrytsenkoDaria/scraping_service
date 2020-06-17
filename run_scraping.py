# import codecs
import os
import sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django  # noqa
django.setup()

from scraping.parsers import *  # noqa
from scraping.models import Vacancy, City, Language, Error, Url  # noqa

user = get_user_model()

parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),  # noqa
    (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'),  # noqa
    (rabota, 'https://rabota.ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'),  # noqa
    (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python&title_only=True')  # noqa
)


def get_settings():
    qs = user.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data']) for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dict[pair]
        urls.append(tmp)
    return urls

city = City.objects.filter(slug='kyiv').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    job, error = func(url)
    jobs += job
    errors += error

for job in jobs:
    vacancy = Vacancy(**job, city=city, language=language)
    try:
        vacancy.save()
    except DatabaseError:
        pass

if errors:
    error = Error(data=errors).save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close
