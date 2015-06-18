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

class Question(models.Model):
    count=0
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):              # __unicode__ on Python 2
        return self.question_text

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
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):              # __unicode__ on Python 2
            return self.choice_text
    def go(self):
        route=Routes(self.choice_text)
        a=route.go()
        return a

