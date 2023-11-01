from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..omg_app_views.model_views import EmailAPIView
from django.core import mail

class EmailAPIViewTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = '/api/email/'
        self.view = EmailAPIView.as_view()

    def test_send_email_valid_data(self):
        data = {
            'email_title': 'Test Email',
            'email_msg': 'Hello, this is a test email',
            'email': 'dksms1@naver.com'
        }
        request = self.factory.post(self.url, data)
        response = self.view(request)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Email')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')

    def test_send_email_invalid_data(self):
        data = {}
        request = self.factory.post(self.url, data)
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
