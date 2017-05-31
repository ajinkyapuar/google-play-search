# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
#
# Create your views here.
from django.http import HttpResponse
from django.template import loader

import requests
from bs4 import BeautifulSoup

from .models import Queries, Results

from django.utils import timezone


def index(request):
    template = loader.get_template('index.html')
    results = {}
    context = {}
    query = request.GET.get('query')
    if not query:
        context = {
            'error': 'Search Term cannot be empty',
        }
        return HttpResponse(template.render(context))
    query = query.lower()
    if len(query.split(" ")) >= 2:
        print("****** Query can contain only one word ******")
        context = {
            'error': 'Search Term should be one word only',
        }
        return HttpResponse(template.render(context))
    queries = Queries.objects.filter(query_text=query)
    if not queries:
        print("****** QUERY NOT FOUND!!! ******")
        q = Queries(query_text=query, pub_date=timezone.now())
        q.save()
        scrapeGooglePlayStore(query, q.id)
        results = Results.objects.filter(query_id=q.id)
    else:
        print("****** QUERY FOUND!!! ******")
        q_id = [q.id for q in queries]
        results = Results.objects.filter(query_id=q_id[0])
        if not results:
            print("****** RESULTS NOT FOUND!!! ******")
            scrapeGooglePlayStore(query, q_id[0])
    context = {
        'query': query,
        'app_list': results,
    }
    return HttpResponse(template.render(context))


def scrapeGooglePlayStore(query, qId):
    print("****** Scrapping Google Play Store ******")
    webRequest = requests.get('https://play.google.com/store/search?q=' + query)
    # print(webRequest.status_code)
    if webRequest.status_code == requests.codes.ok:
        page = webRequest.text
        soup = BeautifulSoup(page)
        cards = soup.find_all('div', {"class": "card"})
        count = 1
        for card in cards:
            if count <= 10:
                if card.find('a', {"class": "subtitle"}) is not None:
                    print("****** Dev Name found ******")
                    r = Results(query_id_id=qId,
                                app_id=card['data-docid'],
                                app_name=card.find('a', {"class": "title"}).text,
                                dev_name=card.find('a', {"class": "subtitle"}).text)
                    r.save()
                    count += 1
            else:
                break
    else:
        print("******* Status Code Error ******")
    print("****** Scrapping Completed! Data Saved to DB ******")


def details(request, pk):
    template = loader.get_template('details.html')
    results = Results.objects.filter(id=pk)
    context = {'details': results}
    return HttpResponse(template.render(context))