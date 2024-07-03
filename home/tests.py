from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from home.models import Contact
from home import views
from datetime import date

class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="Test User",
            phone="1234567890",
            email="test@example.com",
            desc="This is a test description."
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.name, "Test User")
        self.assertEqual(self.contact.phone, "1234567890")
        self.assertEqual(self.contact.email, "test@example.com")
        self.assertEqual(self.contact.desc, "This is a test description.")
        self.assertEqual(self.contact.date, date.today())

    def test_str_method(self):
        self.assertEqual(str(self.contact), "Test User")


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.index_url = reverse('index')
        self.contact_url = reverse('contact')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_index_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.index_url)
        self.assertRedirects(response, self.login_url)

    def test_index_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, self.index_url)

    def test_login_view_post_invalid(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_contact_view_get(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_view_post(self):
        response = self.client.post(self.contact_url, {
            'name': 'Test Name',
            'phone': '1234567890',
            'email': 'test@example.com',
            'desc': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTrue(Contact.objects.filter(email='test@example.com').exists())

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)


class URLTests(TestCase):
    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_contact_url_resolves(self):
        url = reverse('contact')
        self.assertEqual(resolve(url).func, views.contact)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.loginUser)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logoutUser)
