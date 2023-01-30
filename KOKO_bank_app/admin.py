from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Koclient,Kosupplier,Kouser,Verified_Invoice,Requested_Invoice,Approved_Invoice,Denied])