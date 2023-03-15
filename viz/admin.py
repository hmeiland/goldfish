from django.contrib import admin

# Register your models here.
from viz.models import VizNode, VizNodeList

admin.site.register(VizNode)
admin.site.register(VizNodeList)
