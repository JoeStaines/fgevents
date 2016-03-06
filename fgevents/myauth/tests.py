from django.test import TestCase, Client

from .models import MyUser

# Create your tests here.

def create_user(checkbox):
    """
    Creates a user using the test client going through the post request
    """
    c = Client()
    if checkbox:
        c.post('/auth/register/', {'email': 'example@example.com', 'password1': 'testpass123', 'password2': 'testpass123', 'findplayers': 'check'})
    else:
        c.post('/auth/register/', {'email': 'example@example.com', 'password1': 'testpass123', 'password2': 'testpass123'})

class RegisterMethodTests(TestCase):
    
    def test_user_created(self):
        """
        Check user created to database correctly
        """
        create_user(True)
        queryset = MyUser.objects.filter(email="example@example.com")
        self.assertIsNotNone(queryset.first())
        
    def test_find_players_checked(self):
        """
        Check profile defines a value >0 for find_radius when user chooses to let players find them
        """
        create_user(True)
        queryset = MyUser.objects.filter(email="example@example.com")
        user = queryset.first()
        profile = user.profile
        self.assertGreater(profile.find_radius, 0)
        
    def test_find_players_unchecked(self):
        """
        Check profile defines a value 0 for find_radius when user chooses to not let players find them
        """
        create_user(False)
        queryset = MyUser.objects.filter(email="example@example.com")
        user = queryset.first()
        profile = user.profile
        self.assertEquals(profile.find_radius, 0)