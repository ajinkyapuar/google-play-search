# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Queries(models.Model):
    query_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def is_duplicate(self):
        # TODO: check if duplicate query
        return
        # return self.query_text == Quer


class Results(models.Model):
    query_id = models.ForeignKey(Queries, on_delete=models.CASCADE)
    app_id = models.CharField(max_length=200)
    app_name = models.CharField(max_length=200)
    dev_name = models.CharField(max_length=200)
