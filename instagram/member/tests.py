from django.contrib.auth import authenticate
from django.test import TestCase, TransactionTestCase

from .forms import User


class UserModelTest(TransactionTestCase):
    """
    user를 그냥 만들었을 걍우, default값이 잘 들어있는지를
    Test하기
    """
    DUMMY_USERNAME = 'username'
    DUMMY_PASSWORD = 'password'
    DUMMY_AGE = 0

    def test_fields_default_value(self):
        user = User.objects.create_user(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD
        )
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.username, self.DUMMY_USERNAME)
        self.assertEqual(user.img_profile, '')
        self.assertEqual(user.age, self.DUMMY_AGE)
        self.assertEqual(user.following_users.count(), 0)
        # 입력한 username, password로 인증한 user와 위에서 생성한 user가 같은지
        self.assertEqual(user, authenticate(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD
        ))

    def test_follow(self):
        mina, hyeri, yura, sojin = [User.objects.create(
            username=f'{name}',
            age=0  # test에서는 password안만들어도 에러는 안남
        ) for name in ['민아', '혜리', '유라', '소진']]

        # 민아는 모두 팔로우
        mina.follow_toggle(hyeri)
        mina.follow_toggle(yura)
        mina.follow_toggle(sojin)

        # 혜리는 유라 소진만 팔로우
        hyeri.follow_toggle(sojin)
        hyeri.follow_toggle(sojin)

        # 유라는 소진만 팔로우
        yura.follow_toggle(sojin)
        # 소진은 아무도 팔로우하지 않음

        self.assertEqual(mina.following_users.count(), 3)
        self.assertEqual(hyeri.following_users.count(), 2)
        self.assertEqual(yura.following_users.count(), 1)
        self.assertEqual(sojin.following_users.count(), 0)

        self.assertIn(hyeri, mina.following_users.all())
        self.assertIn(yura, mina.following_users.all())
        self.assertIn(sojin, mina.following_users.all())

        self.assertIn(mina, hyeri.followers.all())
        self.assertIn(mina, yura.followers.all())
        self.assertIn(mina, sojin.followers.all())
