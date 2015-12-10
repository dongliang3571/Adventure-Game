from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
class AdventureTests(TestCase):

    #Daniel and his daughter login to the account they created last time they
    #went on an adventure.
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    #They have selected the adventure to help the wizard and start adventure
    #They now see a page showing them information about the adventure. The
    #estimated time to complete, estimated cost, and any items needed to
    #complete
    def test_preadventure_information(self):
        response = self.client.get('/information/')
        advetnureid = response.context('adventure_id')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/information.html')
        self.assertEqual(adventureid , '0000')

    #They have hit accept and have gone on to the actual adventure
    #They see the wizard asking for help and telling them what's happening to
    #his land.
    def test_story_so_far(self):
        response = self.client.get('/story/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coreapp/story.html')

    #After accepting the task from the wizard, they are taken to the map view
    def test_map(self):
        response = self.client.get('/adventure/')
        self.assertEqual(response.status_code, 200)
        self.asssertTemplateUsed(response, 'map/map.html')

    #They click on the first location and are taken to task 1. The Wizard asks
    #them to make a wish at the fountain.
    def test_task1(self):
        response = self.client.get('/adventure/task1/')
        self.assertEqual(response.status_code, 200)
        self.asssertTemplateUsed(response, 'map/taskpage.html')

    #Once they have made their wish, they are sent a scrambled message by the
    #wizard that they need to decode.
    def test_scramble(self):
        response = self.client.get('/adventure/scramble/')
        self.assertEqual(response.status_code, 200)
        self.asssertTemplateUsed(response, 'map/scramble.html')


"""
class MapTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_(self):
"""
