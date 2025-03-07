from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestHomePage(TestCase):

    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')

class TestWishList(TestCase):

    fixtures = ['test_places']

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestVisitedPage(TestCase):

    def test_places_visited_page_shows_empty_list_message_for_empty_database(self):
        places_visited_url = reverse('places_visited')
        response = self.client.get(places_visited_url)
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places')

class TestVisitedList(TestCase):

    fixtures = ['test_places']

    def test_places_visited_contains_visited_places(self):
        places_visited_url = reverse('places_visited')
        response = self.client.get(places_visited_url)
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')

class TestAddNewPlace(TestCase):

    def test_add_new_unvisted_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Sydney', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        
        response_places = response.context['places']

        self.assertEqual(1, len(response_places)) # Check only one place.
        sydney_from_response = response_places[0]

        sydney_from_database = Place.objects.get(name='Sydney', visited=False)

        self.assertEqual(sydney_from_database, sydney_from_response)

class TestVisitedPlace(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york_from_database = Place.objects.get(pk=2)
        self.assertTrue(new_york_from_database.visited)

    def test_non_existent_place(self):
        visit_nonexistent_place_url = reverse('place_was_visited', args=(123456, ))
        response = self.client.post(visit_nonexistent_place_url, follow=True)
        self.assertEqual(404, response.status_code)
