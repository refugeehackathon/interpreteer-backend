from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Offer
from user_management.models import UserProfile, Location

class OfferTests(APITestCase):
    def setUp(self):
        location = Location.objects.create(latitude='52.1', longitude='13.2', zip_code='12345')
        user = UserProfile.objects.create(username='John Doe', email='john@example.com', location=location)
        Offer.objects.create(title='Test', user=user, kind=0)

        location = Location.objects.create(latitude='51.1', longitude='13.2', zip_code='12345')
        user = UserProfile.objects.create(username='Jane Doe', email='jane@example.com', location=location)
        Offer.objects.create(title='Test', user=user, kind=0)

    def test_list(self):
        """
        Ensure we can list the offers.
        """
        url = reverse('offer-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test')

    def test_list_with_point(self):
        """
        Ensure we can list the offers with location query.
        """
        url = reverse('offer-list')
        data = {'point': '51.1,13.2'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['distance'], 0)
        self.assertTrue(response.data[1]['distance'] > 111.19
            and response.data[1]['distance'] < 111.2)

    def test_list_with_point_and_dist(self):
        """
        Ensure we can list the offers with location query.
        """
        url = reverse('offer-list')
        data = {'point': '51.1,13.2', 'dist': '100'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['distance'], 0)
