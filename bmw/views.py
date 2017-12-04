'''
Created on Apr 25, 2017

@author: theo
'''
from django.http.response import JsonResponse

from django.views.generic.list import ListView
from django.conf import settings

import logging
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from acacia.data.models import MeetLocatie, ProjectLocatie
from django.views.generic.detail import DetailView

logger = logging.getLogger(__name__)

class StaffRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request,
                'Je het niet de vereiste rechten om de gevraagde bewerking uit te voeren.')
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

def json_locations(request):
    """ return json response with measuring locations """
    result = []
    for p in MeetLocatie.objects.all():
        loc = p.latlon()
        if loc:
            result.append({'id': p.pk, 'name': p.name, 'lon': loc.x, 'lat': loc.y})
    return JsonResponse(result,safe=False)
            
class LocationListView(ListView):
    template_name = 'bmw/location_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['maptype'] = "ROADMAP"
        context['options'] = {
            'center': [53.16371, 6.27530],
            'zoom': 10 }
        
        return context

class ProjectlocatieListView(LocationListView):
    model = ProjectLocatie
    
class MeetlocatieListView(LocationListView):
    model = MeetLocatie
    template_name = 'bmw/meetlocatie_list.html'
        
    def get_context_data(self, **kwargs):
        context = LocationListView.get_context_data(self, **kwargs) 
        return context
    
class MeetlocatieDetailView(DetailView):
    model = MeetLocatie
    template_name = 'bmw/meetlocatie_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(MeetlocatieDetailView, self).get_context_data(**kwargs)
        mloc = self.get_object()
        pos = mloc.latlon()
        context['api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['maptype'] = "ROADMAP"
        context['options'] = {
            'center': [pos.y, pos.x],
            'zoom': 16 }
        return context

    