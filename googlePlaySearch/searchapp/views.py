# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import requests


def index(request):
    template = loader.get_template('index.html')
    query = request.GET.get('query')
    # print query
    webRequest = requests.get('https://play.google.com/store/search?q=' + query)
    # print webRequest
    if webRequest.status_code == requests.codes.ok:
        print "*** Web Request Successfull ***"
        print webRequest.text
    else:
        print "*** Web Request Not Successfull ***"

    context = {
        # 'latest_question_list': latest_question_list,
    }
    print context
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello! Search App initialized")

    # def searchResults(request):
    #     drname = request.GET.get('searchParam')
    #     print request
    #     print drname
    #     # doctors = Doctor.objects.filter(name__contains=drname)
    #     # clinic = Doctor.objects.filter(clinic__name__contains=drname)
    #     # d = getVariables(request)
    #     # d['doctors'] = doctors
    #     # d['doctors_by_clinic'] = doctors
    #     # return render_to_response('meddy1/doclistings.html',d)
