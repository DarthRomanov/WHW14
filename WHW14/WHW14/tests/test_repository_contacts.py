import unittest
from unittest.mock import Mock
from WHW14.src.routes.contacts import (
    create_contact,
    get_all_contacts,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    upcoming_birthdays
)
from WHW14.src.database.models import Contact

class TestContactsAPI(unittest.TestCase):
    def test_create_contact(self):
        # Підготовка
        db_session_mock = Mock()
        mock_contact_data = {"first_name": "John", "last_name": "Doe", "email": "john@example.com"}
        db_session_mock.add.return_value = Mock(**mock_contact_data)

        # Виклик функції
        result = create_contact(Mock(**mock_contact_data), db_session_mock)

        # Перевірка
        self.assertEqual(result, Mock(**mock_contact_data))
        db_session_mock.add.assert_called_once()

    def test_get_all_contacts(self):
        # Підготовка
        db_session_mock = Mock()
        mock_contacts = [Mock(id=i) for i in range(1, 6)]
        db_session_mock.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_contacts

        # Виклик функції
        result = get_all_contacts(db=db_session_mock)

        # Перевірка
        self.assertEqual(result, mock_contacts)
        db_session_mock.query.return_value.offset.assert_called_once()
        db_session_mock.query.return_value.limit.assert_called_once()

    # Додайте аналогічно інші тести для інших функцій

if __name__ == "__main__":
    unittest.main()
