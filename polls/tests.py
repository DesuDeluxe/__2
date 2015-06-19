import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Question


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_route(self):
        """
        was_published_recently() should return False for routes whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_route = Question(pub_date=time)
        self.assertEqual(future_route.was_published_recently(), False)

    def test_was_published_recently_with_old_route(self):
        """
        was_published_recently() should return False for routes whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_route = Question(pub_date=time)
        self.assertEqual(old_route.was_published_recently(), False)

    def test_was_published_recently_with_recent_route(self):
        """
        was_published_recently() should return True for routes whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_route = Question(pub_date=time)
        self.assertEqual(recent_route.was_published_recently(), True)

def create_route(route_text, days):
    """
    Creates a route with the given `route_text` published the given
    number of `days` offset to now (negative for routes published
    in the past, positive for routes that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(route_text=route_text,pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_routes(self):
        """
        If no routes exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_route_list'], [])


    def test_index_view_with_a_past_route(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_route(route_text="Past route.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_route_list'],
            ['<Question: Past route.>']
        )

    def test_index_view_with_a_future_route(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_route(route_text="Future route.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_route_list'], [])

    def test_index_view_with_future_route_and_past_route(self):
        """
        Even if both past and future routes exist, only past routes
        should be displayed.
        """
        create_route(route_text="Past route.", days=-30)
        create_route(route_text="Future route.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_route_list'],
            ['<Question: Past route.>']
        )

    def test_index_view_with_two_past_routes(self):
        """
        The routes index page may display multiple routes.
        """
        create_route(route_text="Past route 1.", days=-30)
        create_route(route_text="Past route 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_route_list'],
            ['<Question: Past route 2.>', '<Question: Past route 1.>']
        )

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_route(self):
        """
        The detail view of a route with a pub_date in the future should
        return a 404 not found.
        """
        future_route = create_route(route_text='Future route.',
                                          days=5)
        response = self.client.get(reverse('polls:detail',
                                   args=(future_route.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_route(self):
        """
        The detail view of a route with a pub_date in the past should
        display the route's text.
        """
        past_route = create_route(route_text='Past Question.',
                                        days=-5)
        response = self.client.get(reverse('polls:detail',args=(past_route.id,)))
        self.assertContains(response, past_route.route_text,status_code=200)