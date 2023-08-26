import unittest
from unittest.mock import Mock
from WHW14.src.repository.users import get_user_by_email
from WHW14.src.database.models import User

class TestGetUserByEmail(unittest.TestCase):
    def test_get_user_by_email_existing(self):
        # Підготовка
        db_session_mock = Mock()
        mock_user = Mock()
        db_session_mock.query.return_value.filter.return_value.first.return_value = mock_user

        # Виклик функції
        result = get_user_by_email(db_session_mock, "test@example.com")

        # Перевірка
        self.assertEqual(result, mock_user)
        db_session_mock.query.return_value.filter.assert_called_once_with(User.email == "test@example.com")
        db_session_mock.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_user_by_email_non_existing(self):
        # Підготовка
        db_session_mock = Mock()
        db_session_mock.query.return_value.filter.return_value.first.return_value = None

        # Виклик функції
        result = get_user_by_email(db_session_mock, "nonexistent@example.com")

        # Перевірка
        self.assertIsNone(result)
        db_session_mock.query.return_value.filter.assert_called_once_with(User.email == "nonexistent@example.com")
        db_session_mock.query.return_value.filter.return_value.first.assert_called_once_with()

if __name__ == "__main__":
    unittest.main()
