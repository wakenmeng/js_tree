# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse

def json_response(func):

    def _wrapper(*args, **kwargs):
        rst = func(*args, **kwargs)
        return HttpResponse(json.dumps(rst), content_type="application/json")

    return _wrapper


