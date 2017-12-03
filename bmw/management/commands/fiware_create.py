'''
Created on Dec 01, 2017

@author: theo
'''
from django.core.management.base import BaseCommand
from django.conf import  settings
from bmw.fiware import Orion
from acacia.data.models import MeetLocatie
from django.utils.text import slugify
from bmw.models import OrionLink
import logging

logger = logging.getLogger(__name__)  

class Command(BaseCommand):
    args = ''
    help = 'notifies fiware-orion about timeseries'
    
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
        parser.add_argument('-f','--force',
                action='store_true',
                dest = 'force',
                default = False,
                help = 'force replacement of existing entities')

    def handle(self, *args, **options):
        pk = options.get('pk')
        if pk:
            query = MeetLocatie.objects.filter(pk=pk)
        else:
            query = MeetLocatie.objects.all()
        url = options.get('url')
        orion = Orion(url)
        for loc in query:
            logger.info('Fiware-orion creating entity '+loc.name)
            entity = slugify(loc.name)
            data = {
                'id': entity,
                'type': 'Measurement',
            }
    
            pos = loc.latlon()
            data['location'] = {
                'type': 'geo:Point',
                'value': '{lon},{lat}'.format(lon=pos.x, lat=pos.y),
                'metadata': {
                'coordinateSystem': {
                    'value': 'EPSG4326'
                    }
                }
            }

            data['latitude'] = {
                'value': pos.y,
                'type': 'Number'
            }
            data['longitude'] = {
                'value': pos.x,
                'type': 'Number'
            }

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
                            },
                            'unit': {
                                'value': series.unit
                            }
                        }
                    }
            
            response = orion.create_entity(data)
            if not response.ok:
                if response.status_code == 422:
                    logger.warning('Entity {} already exists'.format(entity))
                    if options.get('force') == True:
                        logger.info('Replacing entity {} ...'.format(entity))
                        #Already exist. delete and try again (http verb PUT is not allowed)
                        orion.delete_entity(entity)
                        response = orion.create_entity(data)
                        try:
                            response.raise_for_status()
                        except Exception as e:
                            logger.error(e)
