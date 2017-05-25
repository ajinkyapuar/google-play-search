# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import requests
from bs4 import BeautifulSoup

def index(request):
    template = loader.get_template('index.html')
    query = request.GET.get('query')
    # print query
    webRequest = requests.get('https://play.google.com/store/search?q=' + query)
    if webRequest.status_code == requests.codes.ok:
        page = webRequest.text
        soup = BeautifulSoup(page)
        cards = soup.find_all('div', {"class": "card"})
        # count = 1
        for card in cards[:10]:
            print "********* Begin App Data *********"
            # print count
            print "AppID: " + card['data-docid']
            print "AppName: " + card.find('a', {"class": "title"}).text
            print "DeveloperName: " + card.find('a', {"class": "subtitle"}).text
            # count+=1
            print "********* End App Data *********"
    context = {
        # 'app_list': app_list,
    }
    # print context
    return HttpResponse(template.render(context, request))