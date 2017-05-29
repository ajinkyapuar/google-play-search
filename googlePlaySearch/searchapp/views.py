# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import requests
from bs4 import BeautifulSoup

from .models import  Queries, Results

from django.utils import timezone


def index(request):
    template = loader.get_template('index.html')
    query = request.GET.get('query')
    # print query
    # webRequest = requests.get('https://play.google.com/store/search?q=' + query)
    # if webRequest.status_code == requests.codes.ok:
    #     page = webRequest.text
    #     soup = BeautifulSoup(page)
    #     cards = soup.find_all('div', {"class": "card"})
    #     # count = 1
    #     for card in cards[:10]:
    #         print "********* Begin App Data *********"
    #         # print count
    #         print "AppID: " + card['data-docid']
    #         print "AppName: " + card.find('a', {"class": "title"}).text
    #         print "DeveloperName: " + card.find('a', {"class": "subtitle"}).text
    #         # count+=1
    #         print "********* End App Data *********"

    # queries = Queries.objects.all()


    try:
        queries = Queries.objects.filter(query_text=query)
        # print queries
        if not queries:
            print "****** QUERY NOT FOUND!!! ******"
            q = Queries(query_text=query, pub_date=timezone.now())
            q.save()
            print q.id
            webRequest = requests.get('https://play.google.com/store/search?q=' + query)
            if webRequest.status_code == requests.codes.ok:
                page = webRequest.text
                soup = BeautifulSoup(page)
                cards = soup.find_all('div', {"class": "card"})
                # count = 1
                for card in cards[:10]:
                    print "********* Begin App Data *********"
                    # print count
                    # print "AppID: " + card['data-docid']
                    # print "AppName: " + card.find('a', {"class": "title"}).text
                    # print "DeveloperName: " + card.find('a', {"class": "subtitle"}).text
                    # count+=1
                    print q.id
                    r = Results(query_id_id = q.id, app_id = card['data-docid'], app_name = card.find('a', {"class": "title"}).text, dev_name =  card.find('a', {"class": "subtitle"}).text )
                    r.save()
                    print "********* End App Data *********"

        else:
            print "****** QUERY FOUND!!! ******"
            # queries = Queries.objects.filter(query_text=query)
            # print queries
            # print [q.id for q in Queries.objects.filter(query_text=query)]
            q_id = [q.id for q in queries]
            q_text = [q.query_text for q in queries]
            print q_id[0]
            print q_text[0]
            results = Results.objects.filter(query_id = q_id[0])
            print results
            if not results:
                print "****** RESULTS NOT FOUND!!! ******"
            else:
                print "****** RESULTS FOUND!!! ******"
    except Queries.DoesNotExist:
        print "****** Query doesn't exsist! ******"

    context = {
        # 'app_list': app_list,
    }
    # print context
    return HttpResponse(template.render(context, request))


