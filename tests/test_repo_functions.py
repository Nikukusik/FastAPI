import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.auth.repo import UsersRepository
from src.auth.models import Users_app
from src.auth.schema import UserCreate


class TestRepo(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = Users_app(id=1, email='nazar@gmail.com', hashed_password='hashed_password', verification=False)
        self.repo = UsersRepository(session=self.session)

    @patch('src.auth.repo.get_password_hash')
    def test_create_user(self, mock_get_password_hash):
        user_data = UserCreate(email='nazar@gmail.com', password='12345')
        mock_get_password_hash.return_value = 'hashed_password'
        self.session.add.return_value = None
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        result = self.repo.create_user(user_data)

        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        self.assertEqual(result.email, user_data.email)
        self.assertEqual(result.hashed_password, 'hashed_password')

    def test_get_user_by_email(self):
        self.session.execute.return_value.scalar_one_or_none.return_value = self.user

        result = self.repo.get_user_by_email(self.user.email)

        self.session.execute.assert_called_once()
        self.assertEqual(result.email, self.user.email)

    def test_activate_user(self):
        self.session.query().filter().first.return_value = self.user
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        user = self.repo.get_user_by_email(self.user.email)
        result = self.repo.activate_user(user)

        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        self.assertTrue(result.verification)

    def test_update_avatar(self):
        self.session.query().filter().first.return_value = self.user
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        result = self.repo.update_avatar(self.user.email, 'test')

        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        self.assertEqual(result.avatar, 'test')

if __name__ == '__main__':
    unittest.main()