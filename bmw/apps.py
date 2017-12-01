'''
Created on May 11, 2017

@author: theo
'''

from django.apps import AppConfig
from django.db.models import signals
 
class BmwConfig(AppConfig):
    name = 'bmw'
    label = 'bmw'
    verbose_name = 'Boeren Meten Water'

    def ready(self):
        # auto create api keys
        from tastypie.models import create_api_key
        signals.post_save.connect(create_api_key, sender='auth.User')
