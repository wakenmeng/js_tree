# -*- coding: utf-8 -*-

import json

from django.template import RequestContext
#from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from cto_tree.models import CTONode
from corelib.decorators import json_response


def index(request):
    trees = json.dumps(CTONode.get_trees())
    return render_to_response("index.html", locals(), context_instance=RequestContext(request))


@require_POST
@json_response
def create_node(request):
    parent_id = request.POST.get('parent')
    name = request.POST.get('name')
    node = CTONode.create(parent_id, name)
    return node.get_info()


@require_POST
@json_response
def remove_node(request):
    print request.POST
    nid = request.POST.get('id')
    node = CTONode.get(nid)
    node.discard()
    return {}


@require_POST
@json_response
def update_node(request):
    nid = request.POST.get('id')
    name = request.POST.get('name')
    node = CTONode.get(nid)
    node.name = name
    node.save()
    return node.get_info()


@require_POST
@json_response
def income(request):
    nid = request.POST.get('id')
    try:
        amount = int(request.POST.get('amount'))
    except ValueError:
        return {}
    node = CTONode.get(nid)
    node.income(amount)
    return node.get_info()


