from django.test import TestCase
from django.db.utils import IntegrityError

from apps.users.models import User, Profile
from main.tests.utils import SimpleUploadedImage


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password=r'Qwerty123!',
        )

    def test_profile_created_with_user(self):
        profile_created = Profile.objects.filter(user=1).exists()

        self.assertTrue(profile_created)

    def test_field_props(self):
        profile = Profile.objects.get(user=1)
        field = profile._meta.get_field('image')

        self.assertEquals(field.default, 'default_profile_pic.jpg')
        self.assertEquals(field.upload_to, 'profile_pics')

    def test_try_create_profile_without_user(self):
        with self.assertRaisesMessage(
                IntegrityError,
                'NOT NULL constraint failed: users_profile.user_id'):
            Profile.objects.create()

    def test_image_resized(self):
        max_height = 300
        max_width = 300
        big_image = SimpleUploadedImage('big-image.jpg',
                                        height=1024,
                                        width=1024,
                                        color=(255, 0, 0))

        profile = Profile.objects.get(user=1)
        profile.image = big_image
        profile.save()

        self.assertEquals(profile.image.height, max_height)
        self.assertEquals(profile.image.width, max_width)

    def test_cascade_delete_profile(self):
        user1 = User.objects.get(id=1)
        user1.delete()
        profile_deleted = not Profile.objects.filter(user=1).exists()

        self.assertTrue(profile_deleted)
