from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from albums.models import Album


User = get_user_model()
class AlbumTest(TestCase):

    def setUp(self):
        
        self.client = Client()

        self.testUser = User.objects.create(username='testUser')
        self.testAlbum = Album.objects.create(title='testTitle', description='testDescription')
    
    def testAlbumCreation(self):

        self.client.force_login(self.testUser)
        
        response = self.client.get(
            reverse('new_album', kwargs={'username': self.testUser.username}))
        
        self.assertEqual(response.status_code, 200)   
        
        response = self.client.post( 
            reverse('new_album', kwargs={'username': self.testUser.username}),
            {'title': 'testTitle', 'description': 'testDescription'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.testUser.albums.count(), 1)
    
    def testAlbumGet(self):

        self.client.force_login(self.testUser)
        self.testAlbum.creator = self.testUser

        response = self.client.get(
            reverse('all_albums', kwargs={'username': self.testUser.username}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'].first, self.testAlbum)


