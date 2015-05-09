from django.contrib import admin

# Register your models here.
from rentv_crm.models import Manager
from rentv_crm.models import Client
from rentv_crm.models import Status

admin.site.register(Manager)
admin.site.register(Client)
admin.site.register(Status)
