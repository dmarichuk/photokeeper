from django.test import Client, TestCase
from django.urls import reverse
from model_bakery import baker

from users.models import Follow, User


class FollowTestCase(TestCase):

    def setUp(self):
        self.user_1 = baker.make(User, username='author')
        self.user_2 = baker.make(User, username='follower')

    def test_follow(self):

        self.assertEqual(self.user_1.followers.count(), 0)
        self.assertEqual(self.user_2.follows.count(), 0)

        c = Client()
        c.force_login(self.user_2)
        c.get(
            reverse(
                'follow',
                kwargs={
                    'username': self.user_1.username
                }
            )
        )

        self.assertEqual(self.user_1.followers.count(), 1)
        self.assertEqual(self.user_1.follows.count(), 0)
        self.assertEqual(self.user_1.followers.first().follower, self.user_2)
        self.assertEqual(self.user_2.follows.count(), 1)
        self.assertEqual(self.user_2.followers.count(), 0)
        self.assertEqual(self.user_2.follows.first().user, self.user_1)

    def test_unfollow(self):
        follow = baker.make(Follow, user=self.user_1, follower=self.user_2)

        self.assertIsInstance(follow, Follow)
        self.assertEqual(self.user_1.followers.count(), 1)
        self.assertEqual(self.user_2.follows.count(), 1)

        c = Client()
        c.force_login(self.user_2)
        c.get(
            reverse(
                'follow',
                kwargs={
                    'username': self.user_1.username
                }
            )
        )
        self.assertEqual(self.user_1.followers.count(), 0)
        self.assertEqual(self.user_2.follows.count(), 0)

    def test_followers_list(self):

        baker.make(Follow, user=self.user_1, follower=self.user_2)

        c = Client()
        c.force_login(self.user_1)
        response = c.get(
            reverse(
                'followers',
                kwargs={
                    'username': self.user_1.username
                }
            )
        )
        follow = response.context['followers'].first()
        self.assertEqual(follow.follower, self.user_2)

    def test_follows_list(self):

        baker.make(Follow, user=self.user_1, follower=self.user_2)

        c = Client()
        c.force_login(self.user_2)
        response = c.get(
            reverse(
                'follows',
                kwargs={
                    'username': self.user_2.username
                }
            )
        )
        follow = response.context['follows'].first()
        self.assertEqual(follow.user, self.user_1)


class UserTestCase(TestCase):

    def test_user_sign_up(self):
        c = Client()

        response = c.post(
            reverse('sign_up'),
            data={
                'username': 'test_user',
                'email': 'email@test.com',
                'password1': 'test_password',
                'password2': 'test_password',
                },
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='test_user')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'email@test.com')

    def test_user_logout(self):
        c = Client()
        user = baker.make(User)
        c.force_login(user)

        response = c.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))
        self.assertRaisesMessage(Warning, 'You have succesfully logged out!')
