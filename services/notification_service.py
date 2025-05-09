# services/notification_service.py

import time
import threading

class NotificationService:
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, user_id: str):
        """Subscribe a user to live notifications."""
        self.subscribers.add(user_id)
        print(f"User {user_id} subscribed.")

    def unsubscribe(self, user_id: str):
        """Unsubscribe a user from live notifications."""
        if user_id in self.subscribers:
            self.subscribers.remove(user_id)
            print(f"User {user_id} unsubscribed.")
        else:
            print(f"User {user_id} was not subscribed.")

    def send_notification(self, user_id: str, message: str):
        """Send notification to a subscribed user."""
        if user_id in self.subscribers:
            print(f"Sending notification to {user_id}: {message}")
        else:
            print(f"User {user_id} is not subscribed, notification not sent.")

    def start_live_updates(self, match_id: str, interval: int = 60):
        """Start live updates by sending notifications at specified intervals."""
        def live_update():
            while True:
                match_status = "Live match update: Status changed"  # Placeholder, integrate actual status
                for subscriber in self.subscribers:
                    self.send_notification(subscriber, match_status)
                time.sleep(interval)

        thread = threading.Thread(target=live_update)
        thread.daemon = True
        thread.start()
