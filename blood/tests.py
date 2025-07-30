# Django's test framework and client for simulating requests
from django.test import TestCase, Client

# Built-in User model for authentication
from django.contrib.auth.models import User

# Reverse URL resolution for named routes
from django.urls import reverse

# Models under test
from blood.models import Donor, BloodRequest


# -------------------------------
# 🧪 Blood App Test Suite
# -------------------------------
class BloodAppTests(TestCase):
    def setUp(self):
        # Create test client and user
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    # 🔐 Helper to log in test user
    def login_test_user(self):
        response = self.client.post('/accounts/login/', {
            'username': self.username,
            'password': self.password
        }, follow=True)
        return response

    # 🏠 Test homepage loads successfully
    def test_home_page_loads(self):
        self.user.is_staff = True  # Grant staff access if needed
        self.user.save()
        self.login_test_user()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # 🔁 Test login redirects to dashboard
    def test_login_redirects_to_user_dashboard(self):
        self.user.is_staff = True
        self.user.save()
        response = self.login_test_user()

        # Debug: print redirect chain
        print("Redirect chain:", response.redirect_chain)

        # Extract final URL from redirect chain
        final_url = response.redirect_chain[-1][0] if response.redirect_chain else response.request['PATH_INFO']

        # Assert dashboard was hit during redirect
        dashboard_hit = any('/accounts/dashboard/' in url for url, _ in response.redirect_chain)
        self.assertTrue(dashboard_hit, "Dashboard was not hit during login redirect.")

        # Assert user is authenticated
        self.assertEqual(int(self.client.session.get('_auth_user_id')), self.user.id)

        # Optional: assert final redirect is logout (if expected)
        self.assertEqual(final_url, '/accounts/logout/')

    # ✅ Test valid donor creation
    def test_donor_creation_valid(self):
        self.login_test_user()
        response = self.client.post(reverse('register_donor'), {
            'blood_type': 'A+',
            'location': 'Test City',
            'units_donated': 1,
            'available': True,
            'notes': 'Test note'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Donor.objects.filter(user=self.user).exists())

    # ❌ Test invalid donor creation (missing fields)
    def test_donor_creation_invalid(self):
        self.login_test_user()
        response = self.client.post(reverse('register_donor'), {
            'blood_type': '',
            'location': '',
            'units_donated': '',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blood Type: This field is required.')
        self.assertContains(response, 'Location: This field is required.')
        self.assertContains(response, 'Units donated: This field is required.')

    # ✅ Test valid blood request creation
    def test_blood_request_creation_valid(self):
        self.login_test_user()
        response = self.client.post(reverse('request_blood'), {
            'patient_name': 'John Doe',
            'age': 30,
            'blood_type': 'B+',
            'location': 'City Hospital',
            'quantity_needed': 500,
            'contact': '9876543210'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(BloodRequest.objects.filter(user=self.user).exists())

    # ❌ Test invalid blood request (missing fields)
    def test_blood_request_creation_invalid(self):
        self.login_test_user()
        response = self.client.post(reverse('request_blood'), {
            'patient_name': '',
            'age': '',
            'blood_type': '',
            'location': '',
            'quantity_needed': '',
            'contact': ''
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    # 🔐 Test dashboard access requires login
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('user_dashboard'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/dashboard/')

    # 🔐 Test donor registration requires login
    def test_register_donor_requires_login(self):
        response = self.client.get(reverse('register_donor'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/blood/register/')

    # 🔐 Test blood request requires login
    def test_request_blood_requires_login(self):
        response = self.client.get(reverse('request_blood'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/blood/request/')
