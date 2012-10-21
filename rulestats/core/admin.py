from django.contrib import admin
from rulestats.core.models import Firewall
from rulestats.core.forms import AdminFirewallCredentialsChangeForm

class FirewallAdmin(admin.ModelAdmin):
    form = AdminFirewallCredentialsChangeForm
    
admin.site.register(Firewall, FirewallAdmin)