# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import requests
from bs4 import BeautifulSoup

from .models import Queries, Results

from django.utils import timezone

import time


def index(request):
    # print("****** REQUEST FOUND ******")
    template = loader.get_template('index.html')
    results = {}
    context = {}
    query = request.GET.get('query')
    if not query:
        return HttpResponse(template.render(context))
    # print(query)
    queries = Queries.objects.filter(query_text=query)
    print(queries)
    if not queries:
        print("****** QUERY NOT FOUND!!! ******")
        q = Queries(query_text=query, pub_date=timezone.now())
        q.save()
        # print(q.id)
        scrapeGooglePlayStore(query, q.id)
        results = Results.objects.filter(query_id=q.id)
    else:
        print("****** QUERY FOUND!!! ******")
        q_id = [q.id for q in queries]
        # print(q_id)
        results = Results.objects.filter(query_id=q_id[0])
        # print(results)
        if not results:
            print("****** RESULTS NOT FOUND!!! ******")
            scrapeGooglePlayStore(query, q_id)
            time.sleep(10)
            results = Results.objects.filter(query_id=q_id[0])
        # else:
        #     print("****** RESULTS FOUND!!! ******")

    # print(results)
    context = {
        'query': query,
        'app_list': results,
    }
    return HttpResponse(template.render(context))


def scrapeGooglePlayStore(query, qId):
    print("****** Scrapping Google Play Store ******")
    webRequest = requests.get('https://play.google.com/store/search?q=' + query)
    if webRequest.status_code == requests.codes.ok:
        page = webRequest.text
        soup = BeautifulSoup(page)
        cards = soup.find_all('div', {"class": "card"})
        # count = 1
        for card in cards[:10]:
            # print("********* Begin App Data *********")
            # # print(count)
            # print("AppID: " + card['data-docid'])
            # print("AppName: " + card.find('a', {"class": "title"}).text)
            # print("DeveloperName: " + card.find('a', {"class": "subtitle"}).text)
            # count+=1
            # print qId
            r = Results(query_id_id=qId, app_id=card['data-docid'],
                        app_name=card.find('a', {"class": "title"}).text,
                        dev_name=card.find('a', {"class": "subtitle"}).text)
            r.save()
            print(r.id)
            # time.sleep(10)

            # print("********* End App Data *********")
    else:
        print("******* Status Code Error ******")

def details(request):
    template = loader.get_template('details.html')
    context = {}
    return HttpResponse(template.render(context))
#################################################################################################################################


# if request.GET:
#     print("****** REQUEST FOUND ******")
#     query = request.GET.get('query')
#     # print query
#     # try:
#     queries = Queries.objects.filter(query_text=query)
#     # print queries
#     if not queries:
#         print("****** QUERY NOT FOUND!!! ******")
#         q = Queries(query_text=query, pub_date=timezone.now())
#         q.save()
#         # print q.id
#         webRequest = requests.get('https://play.google.com/store/search?q=' + query)
#         if webRequest.status_code == requests.codes.ok:
#             page = webRequest.text
#             soup = BeautifulSoup(page)
#             cards = soup.find_all('div', {"class": "card"})
#             # count = 1
#             for card in cards[:10]:
#                 print("********* Begin App Data *********")
#                 # print count
#                 # print "AppID: " + card['data-docid']
#                 # print "AppName: " + card.find('a', {"class": "title"}).text
#                 # print "DeveloperName: " + card.find('a', {"class": "subtitle"}).text
#                 # count+=1
#                 # print q.id
#    #########################
#                 # r = Results(query_id_id=q.id, app_id=card['data-docid'],
#                 #             app_name=card.find('a', {"class": "title"}).text,
#                 #             dev_name=card.find('a', {"class": "subtitle"}).text)
#                 # r.save()
#   #########################
#                 print("********* End App Data *********")
#     else:
#         print("****** QUERY FOUND!!! ******")
#         # queries = Queries.objects.filter(query_text=query)
#         # print queries
#         # print [q.id for q in Queries.objects.filter(query_text=query)]
#         q_id = [q.id for q in queries]
#         # q_text = [q.query_text for q in queries]
#         # print q_id[0]
#         # print q_text[0]
#         results = Results.objects.filter(query_id=q_id[0])
#         # print results
#         if not results:
#             print("****** RESULTS NOT FOUND!!! ******")
#       ####################
#             # webRequest = requests.get('https://play.google.com/store/search?q=' + query)
#             # if webRequest.status_code == requests.codes.ok:
#             #     page = webRequest.text
#             #     soup = BeautifulSoup(page)
#             #     cards = soup.find_all('div', {"class": "card"})
#             #     # count = 1
#             #     for card in cards[:10]:
#             #         print("********* Begin App Data *********")
#             #         # print count
#             #         # print "AppID: " + card['data-docid']
#             #         # print "AppName: " + card.find('a', {"class": "title"}).text
#             #         # print "DeveloperName: " + card.find('a', {"class": "subtitle"}).text
#             #         # count+=1
#             #         # print q.id
#             #         r = Results(query_id_id=q.id, app_id=card['data-docid'],
#             #                     app_name=card.find('a', {"class": "title"}).text,
#             #                     dev_name=card.find('a', {"class": "subtitle"}).text)
#             #         r.save()
#             #         print("********* End App Data *********")
#             #
#        ####################
#
#         else:
#             print("****** RESULTS FOUND!!! ******")
#             # context = {
#             #     'app_list': results,
#             # }
#             # for cr in results:
#             #     print cr
#     context = {
#         'app_list': results,
#     }
#     # except Queries.DoesNotExist:
#     #     print("****** Query doesn't exsist! ******")
#     # print context
#     # return render_to_response('index.html', {'app_list': results})
#     return HttpResponse(template.render(context, request))
# # return render_to_response('index.html', {})
# return HttpResponse(template.render(context, request))
