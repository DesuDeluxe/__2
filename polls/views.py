
# _*_ coding: utf-8 _*_
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.forms import *

from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.auth import authenticate, login,logout

from .models import Choice, Question,User


def main_page(request):
    template = get_template("polls/main_page.html")
    variables=RequestContext(request)
    output = template.render(variables)
    return HttpResponse(output)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#def go(request, question_id):
#    p = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': p, 'error_message': Question.objects.get(poszla()),   })


def run(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': p,'error_message': "You didn't select a route.",   })
    else:
        selected_choice.go()
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))




def login_page(request):
    if request.method == 'POST':
        form = FormularzLogowania(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            login(request,user)
            template = get_template("polls/main_page.html")
            variables = RequestContext(request,{'user':user})
            output = template.render(variables)
            return HttpResponseRedirect("/")
    else:
        form = FormularzLogowania()
    template = get_template("registration/login.html")
    variables = RequestContext(request,{'form':form})
    output = template.render(variables)
    return HttpResponse(output)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")
 #   return HttpResponseRedirect(reverse('polls:main_page'))

def register_page(request):
    if request.method == 'POST':
        form = FormularzRejestracji(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
              username=form.cleaned_data['username'],
              password=form.cleaned_data['password1'],
              email=form.cleaned_data['email']
            )
            user.save()
            if form.cleaned_data['log_on']:
                user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
                login(request,user)
                template = get_template("polls/main_page.html")
                variables = RequestContext(request,{'user':user})
                output = template.render(variables)
                return HttpResponseRedirect("/")
            else:
                template = get_template("registration/register_success.html")
                variables = RequestContext(request,{'username':form.cleaned_data['username']})
                output = template.render(variables)
                return HttpResponse(output)
    else:
        form = FormularzRejestracji()
    template = get_template("registration/register.html")
    variables = RequestContext(request,{'form':form})
    output = template.render(variables)
    return HttpResponse(output)

#def logout(request):
 #   auth.logout(request)
 #   return HttpResponseRedirect("/account/loggedout/")
