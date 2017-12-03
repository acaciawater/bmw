'''
Created on Nov 7, 2017

@author: theo
'''

import requests
import json
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

class NGSI:
    ''' formatters and converters for NGSI '''
    @staticmethod
    def timestamp(arg):
        ''' return dict of timestamp in NGSI format '''
        if isinstance(arg, datetime):
            t = arg
        elif hasattr(arg, 'time'):
            t = arg.time
        elif isinstance(arg,dict):
            t = arg['time']
        else:
            t = arg

        if isinstance(t, datetime):
            return {'type':'DateTime','value': t.isoformat()}
        else:
            raise ValueError('datetime expected')

    @staticmethod
    def measurement(value, typename, timestamp):
        ''' return dict of value/timestamp combination in NGSI format '''
        return {
            'value': value, 
            'type': typename, 
            'timestamp': NGSI.timestamp(timestamp)
        }
    
class Orion:
    ''' Interface to Orion Context Broker '''

    def __init__(self, url, **kwargs):
        self.url = url

    def log_response(self, response):
        ''' send response to log system '''
        if response.ok:
            logger.debug('response = {}'.format(response.status_code))
        else:
            logger.error('response = {}, reason = {}'.format(response.status_code, response.reason))
        return response
                   
    def get(self,path,**kwargs):
        url = self.url+path
        logger.debug('GET {}?{}'.format(url,kwargs))
        return requests.get(url,**kwargs)
            
    def post(self,path,data,headers={'content-type':'application/json'}):
        url = self.url+path
        logger.debug('POST {}?{}'.format(url,data))
        return requests.post(self.url+path,data,headers=headers)

    def put(self,path,data,headers={'content-type':'application/json'}):
        url = self.url+path
        logger.debug('PUT {}?{}'.format(url,data))
        return requests.put(url,data,headers=headers)

    def patch(self,path,data,headers={'content-type':'application/json'}):
        url = self.url+path
        logger.debug('PATCH {}?{}'.format(url,data))
        return requests.patch(url,data,headers=headers)

    def delete(self,path):
        url = self.url+path
        logger.debug('DELETE {}'.format(url))
        return requests.delete(url)

    def create_entity(self, data):
        ''' create new entity '''
        return self.post('entities',json.dumps(data))

    def delete_entity(self, entity_id):
        ''' delete entity '''
        path = 'entities/{id}'.format(id=entity_id)
        return self.delete(path)
    
    def update(self, entity_id, data):
        ''' update some or all attributes of existing entity '''
        path = 'entities/{id}/attrs'.format(id=entity_id)
        return self.patch(path,json.dumps(data))

    def update_attribute(self, entity_id, attribute_name, data):
        ''' update single attribute of existing entity '''
        path = 'entities/{id}/attrs/{att}'.format(id=entity_id,att=attribute_name)
        return self.put(path,json.dumps(data))

    def subscribe(self,data):
        return self.post('subscriptions',json.dumps(data))
