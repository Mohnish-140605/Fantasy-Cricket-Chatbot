# tests/unit/test_notification_service.py

import unittest
from services.notification_service import NotificationService
from unittest.mock import patch
import time 

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        """Setup the NotificationService instance before each test."""
        self.notification_service = NotificationService()

    def test_subscribe(self):
        """Test if users can subscribe to notifications."""
        self.notification_service.subscribe("user123")
        self.assertIn("user123", self.notification_service.subscribers)

    def test_unsubscribe(self):
        """Test if users can unsubscribe from notifications."""
        self.notification_service.subscribe("user123")
        self.notification_service.unsubscribe("user123")
        self.assertNotIn("user123", self.notification_service.subscribers)

    def test_send_notification_to_subscribed_user(self):
        """Test if notifications are sent to subscribed users."""
        self.notification_service.subscribe("user123")
        with patch('builtins.print') as mocked_print:
            self.notification_service.send_notification("user123", "Live match update!")
            mocked_print.assert_called_with("Sending notification to user123: Live match update!")

    def test_send_notification_to_unsubscribed_user(self):
        """Test if notifications are not sent to unsubscribed users."""
        self.notification_service.subscribe("user123")
        self.notification_service.unsubscribe("user123")
        with patch('builtins.print') as mocked_print:
            self.notification_service.send_notification("user123", "This should not be sent.")
            mocked_print.assert_not_called()

    @patch('time.sleep', return_value=None)  # To prevent actual sleep during testing
    def test_live_updates(self, mock_sleep):
        """Test if live updates are triggered correctly."""
        self.notification_service.subscribe("user123")
        with patch('builtins.print') as mocked_print:
            self.notification_service.start_live_updates("MATCH001", interval=1)

            # Simulate a few updates
            for _ in range(3):
                time.sleep(1)  # Allow the mock to trigger live updates
                self.assertTrue(mocked_print.called)
                mocked_print.reset_mock()  # Reset mock call history for next iteration

    def tearDown(self):
        """Clean up after each test."""
        self.notification_service.subscribers.clear()


if __name__ == "__main__":
    unittest.main()
