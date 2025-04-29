from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile

class ProfileUpdateTest(TestCase):
    def setUp(self):
        # Create test user and profile for Daniel Chen
        self.user = User.objects.create_user(
            username='DanielChen',
            email='daniel.chen@live.uwe.ac.uk',
            password='12345678-.'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Old bio',
            interests='games',
            address='15 Coldharbour Lane, Bristol, BS16 1QY',
            dob='2000-11-03'
        )
