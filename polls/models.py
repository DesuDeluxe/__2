import datetime
import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from subprocess import check_output

class Routes:
    def __init__(self,text):
        self.text=text
    def go(self):
        process = check_output(['python2','/home/desu/oop/proj/tutorial/polls/bluetoo/te.py', self.text])
        a=str(process)
        return a

class Route(models.Model):
    count=0
    route_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):              # __unicode__ on Python 2
        return self.route_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def by(self):
        self.count+=1
        return 'you'


class Choice(models.Model):
    route = models.ForeignKey(Route)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    selected=models.IntegerField(default=99999999)
    def __unicode__(self):              # __unicode__ on Python 2
            return self.choice_text
    def go(self):
        rout=Routes(self.choice_text)
        a=rout.go()
        return a
#    def res(self):
  #      self.selected=99999999
#        return self.selected
    def re(self):
        aa=5
        return aa

