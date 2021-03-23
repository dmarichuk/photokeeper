from os import path, remove

from django.test import Client, TestCase
from django.urls import reverse
from model_bakery import baker
from PIL import Image

from albums.models import Album, Comment, Photo, User
from albums.services import add_like, is_fan
from photokeeper.settings import MEDIA_ROOT


class AlbumTestCase(TestCase):

    def setUp(self):

        self.album = baker.make(Album)
        self.user = baker.make(User)

    def test_album_creation(self):
        self.assertTrue(isinstance(self.album, Album))
        self.assertEqual(self.album.__str__(), self.album.title)

    def test_album_get(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(
            reverse(
                'one_album',
                kwargs={
                    'username': self.album.creator.username,
                    'album_id': self.album.id,
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['album'], Album)

    def test_album_post(self):
        c = Client()
        c.force_login(self.user)
        response = c.post(
            reverse(
                'new_album',
                kwargs={
                    'username': self.user.username,
                }
            ),
            data={
                'title': 'test_title',
                'description': 'test_description'
                },
            follow=True
        )
        self.assertRedirects(response, reverse(
            'all_albums',
            kwargs={
                'username': self.user.username,
                }
                )
            )
        self.assertEqual(self.user.albums.count(), 1)
        album = self.user.albums.first()
        self.assertEqual(album.title, 'test_title')

    def test_album_del(self):

        c = Client()
        c.force_login(self.user)
        album = baker.make(
            Album,
            creator=self.user
        )

        self.assertEqual(self.user.albums.count(), 1)

        response = c.get(
            reverse(
                'delete_album',
                kwargs={
                    'username': self.user.username,
                    'album_id': album.id
                }
            ),
            follow=True
        )

        self.assertEqual(self.user.albums.count(), 0)
        self.assertRedirects(
            response,
            reverse(
                'all_albums',
                kwargs={
                    'username': self.user.username,
                    }
                )
            )


class PhotoTestCase(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.album = baker.make(Album, creator=self.user)
        self.image = Image.new('1', (100, 100))
        self.image_path = path.join(MEDIA_ROOT, 'test_img.jpg')
        self.image.save(self.image_path)

    def test_photo_creation(self):
        photo = baker.make(Photo)
        self.assertTrue(isinstance(photo, Photo))
        self.assertEqual(photo.__str__(), 'Photo')

    def test_photo_get(self):
        c = Client()
        c.force_login(self.user)
        photo = baker.make(Photo, album=self.album, creator=self.user)
        response = c.get(
            reverse(
                'get_photo',
                kwargs={
                    'username': self.user.username,
                    'album_id': photo.album.id,
                    'photo_id': photo.id,
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['photo'], Photo)

    def test_photo_post(self):

        image = Image.new('1', (100, 100))
        image_path = path.join(MEDIA_ROOT, 'test_img.jpg')
        image.save(image_path)

        c = Client()
        c.force_login(self.user)
        with open(image_path, 'rb') as im:
            response = c.post(
                reverse(
                    'add_photo',
                    kwargs={
                        'username': self.user.username,
                        'album_id': self.album.id,
                    }
                ),
                data={
                    'photo': im,
                    'description': 'test_description',
                },
                follow=True
            )
        self.assertRedirects(response, reverse(
            'one_album',
            kwargs={
                'username': self.user.username,
                'album_id': self.album.id,
                }
                )
            )
        self.assertEqual(self.album.photos.count(), 1)
        photo = self.album.photos.first()
        self.assertEqual(photo.description, 'test_description')

        remove(self.image_path)
        remove(path.join(MEDIA_ROOT, 'photos/test_img.jpg'))

    def test_photo_del(self):
        c = Client()
        c.force_login(self.user)
        photo = baker.make(
            Photo,
            creator=self.user
        )

        self.assertEqual(self.user.photos.count(), 1)

        response = c.get(
            reverse(
                'delete_photo',
                kwargs={
                    'username': self.user.username,
                    'album_id': photo.album.id,
                    'photo_id': photo.id,
                }
            ),
            follow=True
        )

        self.assertEqual(self.user.photos.count(), 0)
        self.assertRedirects(
            response,
            reverse(
                'one_album',
                kwargs={
                    'username': self.user.username,
                    'album_id': photo.album.id,
                    }
                )
            )


class CommentTestCase(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.photo = baker.make(Photo, creator=self.user)

    def test_comment_creation(self):
        comment = baker.make(Comment)
        self.assertTrue(isinstance(comment, Comment))
        self.assertEqual(
            comment.__str__(),
            'Text: %s, Author %s' % (comment.text, comment.creator)
            )

    def test_comment_post(self):
        c = Client()
        c.force_login(self.user)
        response = c.post(
            reverse(
                'add_comment',
                kwargs={
                    'username': self.user.username,
                    'album_id': self.photo.album.id,
                    'photo_id': self.photo.id,
                }
            ),
            data={
                'text': 'test_text',
                },
            follow=True
        )
        self.assertRedirects(response, reverse(
            'get_photo',
            kwargs={
                'username': self.user.username,
                'album_id': self.photo.album.id,
                'photo_id': self.photo.id,
                }
                )
            )
        self.assertEqual(self.user.comments.count(), 1)
        comment = self.user.comments.first()
        self.assertEqual(comment.text, 'test_text')

    def test_comment_del(self):
        c = Client()
        c.force_login(self.user)
        comment = baker.make(
            Comment,
            creator=self.user,
            photo=self.photo,
        )

        self.assertEqual(self.user.comments.count(), 1)

        response = c.get(
            reverse(
                'delete_comment',
                kwargs={
                    'username': self.user.username,
                    'album_id': self.photo.album.id,
                    'photo_id': self.photo.id,
                    'comment_id': comment.id,
                }
            ),
            follow=True
        )

        self.assertEqual(self.user.comments.count(), 0)
        self.assertRedirects(
            response,
            reverse(
                'get_photo',
                kwargs={
                    'username': self.user.username,
                    'album_id': self.photo.album.id,
                    'photo_id': self.photo.id,
                    }
                )
            )


class LikeTestCase(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.photo = baker.make(Photo)

    def test_add_like(self):
        c = Client()
        c.force_login(self.user)

        self.assertFalse(is_fan(self.photo, self.user))
        self.assertEqual(self.photo.total_likes, 0)

        c.get(
            reverse(
                'like',
                kwargs={
                    'username': self.user.username,
                    'photo_id': self.photo.id,
                }
            ),
        )

        self.assertTemplateUsed('albums/get_photo.html')
        self.assertTrue(is_fan(self.photo, self.user))
        self.assertEqual(self.photo.total_likes, 1)

    def test_rm_like(self):
        c = Client()
        c.force_login(self.user)
        add_like(self.photo, self.user)

        self.assertTrue(is_fan(self.photo, self.user))
        self.assertEqual(self.photo.total_likes, 1)

        c.get(
            reverse(
                'like',
                kwargs={
                    'username': self.user.username,
                    'photo_id': self.photo.id,
                }
            ),
        )

        self.assertTemplateUsed('albums/get_photo.html')
        self.assertFalse(is_fan(self.photo, self.user))
        self.assertEqual(self.photo.total_likes, 0)
