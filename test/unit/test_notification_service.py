# tests/unit/test_notification_service.py

import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from services.notification_service import NotificationService
from unittest.mock import patch
import time
import threading

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        self.notification_service = NotificationService()

    def test_subscribe(self):
        self.notification_service.subscribe("user123")
        self.assertIn("user123", self.notification_service.subscribers)

    def test_unsubscribe(self):
        self.notification_service.subscribe("user123")
        self.notification_service.unsubscribe("user123")
        self.assertNotIn("user123", self.notification_service.subscribers)

    def test_send_notification_to_subscribed_user(self):
        self.notification_service.subscribe("user123")
        with patch('builtins.print') as mocked_print:
            self.notification_service.send_notification("user123", "Live match update!")
            mocked_print.assert_called_with("Sending notification to user123: Live match update!")

    def test_send_notification_to_unsubscribed_user(self):
        self.notification_service.subscribe("user123")
        self.notification_service.unsubscribe("user123")
        with patch('builtins.print') as mocked_print:
            self.notification_service.send_notification("user123", "This should not be sent.")
            mocked_print.assert_called_with("User user123 is not subscribed, notification not sent.")

    @patch('time.sleep', return_value=None)
    def test_live_updates(self, mock_sleep):
        self.notification_service.subscribe("user123")
        with patch('builtins.print') as mocked_print:
            # Call the helper method directly instead of starting a thread
            self.notification_service.send_live_update_once("MATCH001")
            mocked_print.assert_any_call("Sending notification to user123: Live match update: Status changed")
            # Start live updates in a thread and let it run a few iterations
            thread = threading.Thread(target=self.notification_service.start_live_updates, args=("MATCH001", 1))
            thread.daemon = True
            thread.start()
            time.sleep(0.1)  # Give the thread a moment to run
            # Check that print was called at least once
            self.assertTrue(mocked_print.called)
            # Stop the thread after test (if your implementation allows for stopping)
            # Otherwise, the thread will be killed when the test process exits

    def tearDown(self):
        self.notification_service.subscribers.clear()

if __name__ == "__main__":
    unittest.main()
