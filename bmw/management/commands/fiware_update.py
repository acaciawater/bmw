'''
Created on Dec 01, 2017

@author: theo
'''
from django.core.management.base import BaseCommand
from django.conf import  settings
from acacia.data.models import MeetLocatie
from bmw.fiware import Orion
from bmw.models import OrionLink
from django.utils.text import slugify

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'notifies fiware-orion'
    
    def add_arguments(self, parser):
        parser.add_argument('-l','--location',
                action='store',
                type = int,
                dest = 'pk',
                default = None,
                help = 'select single single location')
        parser.add_argument('-u','--url',
                action='store',
                dest = 'url',
                default = settings.ORION_URL,
                help = 'url of context broker')

    def handle(self, *args, **options):
        pk = options.get('pk',None)
        if pk:
            query = MeetLocatie.objects.filter(pk=pk)
        else:
            query = MeetLocatie.objects.all()
        url = options.get('url')
        orion = Orion(url)
        for loc in query:
            logger.info('Updating '+loc.name)
            entity = slugify(loc.name)
            
            data = {}
            for series in loc.series_set.all():
                try:
                    link = series.orionlink
                except Exception as e:
                    link = OrionLink.objects.create(series=series,attribute=slugify(series.name))
                    
                last = series.laatste()
                if last and last.value:
                    attr = link.attribute
                    data[attr] = {
                        'value': last.value, 
                        'metadata': {
                            'timestamp': {
                                'value': last.date.isoformat(),
                                'type':'datetime'
                            }
                        }
                    }
            try:
                response = orion.update(entity, data)
                response.raise_for_status()
            except Exception as e:
                logger.error(e)
