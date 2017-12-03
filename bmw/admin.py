from django.contrib import admin
from bmw.models import OrionLink

@admin.register(OrionLink)
class OrionLinkAdmin(admin.ModelAdmin):
    model = OrionLink
    list_display = ('series','attribute')
    list_filter = ('series__mlocatie',)    
    search_fields = ('attribute', 'series__name','series__mlocatie', )