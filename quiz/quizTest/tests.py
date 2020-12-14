from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.


class TestViews(TestCase):

    #Simple test to ensure that our index views is functioning properly
    def test_index_page(self):
        response = self.client.get(reverse('index', args=('mathematics',)))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizTest/quiz.html')
        self.assertContains(response, 'Quiz Time')
        
