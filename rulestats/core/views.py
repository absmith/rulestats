from django.template import Context, loader, RequestContext
from django.shortcuts import get_object_or_404, get_list_or_404, \
                             render_to_response

from django.contrib.auth.models import User

from rulestats.core.models import *

# Create your views here.

#@login_required
def home(request, template='core/index.html'):
    data = {}

    data['firewalls'] = Firewall.objects.all()
    return render_to_response(template, data,
                              context_instance=RequestContext(request))

