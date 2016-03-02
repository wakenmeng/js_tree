# -*- coding: utf-8 -*-

class RESTfulRequestMiddleware(object):

    def process_request(self, request):
        method = request.method
        if method in ['PUT', 'DELETE']:
            request.method = 'POST'
            request._load_post_and_files()
            request.method = method
            setattr(request, request.method, request.POST)

