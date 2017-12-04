'''
Created on Dec 1, 2017

@author: theo
'''
from django.db import models
from acacia.data.models import Series
    
class OrionLink(models.Model):
    ''' links series with orion attribute name '''
    series = models.OneToOneField(Series)
    attribute = models.CharField(max_length = 100)

    def __unicode__(self):
        return str(self.series)
    
    
