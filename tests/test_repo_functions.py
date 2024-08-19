import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.auth.repo import UsersRepository

from src.auth.models import Users_app

from src.auth.schema import UserCreate


class TestRepo(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = Users_app(id=1, email='nazar@gmail.com', password='12345')
        self.repo = UsersRepository(session=self.session)

    def test_create_user(self):
        user_data = UserCreate(email='nazar@gmail.com', password='12345')
        self.session.add.return_value = None
        self.session.commit.return_value = None

        result = self.repo.create_user(user_data)

        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertEqual(result.email, user_data.email)
        self.assertEqual(result.password, user_data.password)

    def test_get_user_by_email(self):
        self.session.query().filter().first.return_value = self.user

        result = self.repo.get_user_by_email(self.user.email)

        self.session.query().filter().first.assert_called_once()
        self.assertEqual(result.email, self.user.email)

    def test_activate_user(self):
        self.session.query().filter().first.return_value = self.user
        self.session.commit.return_value = None

        user = self.repo.get_user_by_email(self.user.email)
        result = self.repo.activate_user(user)

        self.session.commit.assert_called_once()
        self.assertTrue(result.is_active)

    def test_update_avatar(self):
        self.session.query().filter().first.return_value = self.user
        self.session.commit.return_value = None

        result = self.repo.update_avatar(self.user.email, 'test')

        self.session.commit.assert_called_once()
        self.assertEqual(result.avatar, 'test')

if __name__ == '__main__':
    unittest.main()