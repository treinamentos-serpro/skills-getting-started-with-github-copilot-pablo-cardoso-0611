from copy import deepcopy
from unittest import TestCase

from fastapi.testclient import TestClient

from src.app import activities, app


class CancelSignupTests(TestCase):
    def setUp(self):
        self.original_activities = deepcopy(activities)
        self.client = TestClient(app)
        self.addCleanup(self.restore_activities)
        self.addCleanup(self.client.close)

    def restore_activities(self):
        activities.clear()
        activities.update(self.original_activities)

    def test_cancel_removes_only_selected_registration_and_frees_a_spot(self):
        email = "michael@mergington.edu"
        activity = "Chess Club"
        other_participants = activities[activity]["participants"][1:]
        self.client.post("/activities/Art%20Club/signup", params={"email": email})

        response = self.client.delete(
            "/activities/Chess%20Club/signup", params={"email": email}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        updated = self.client.get("/activities").json()
        self.assertEqual(updated[activity]["participants"], other_participants)
        self.assertIn(email, updated["Art Club"]["participants"])
        self.assertEqual(
            self.client.post(
                "/activities/Chess%20Club/signup", params={"email": email}
            ).status_code,
            200,
        )

    def test_unknown_activity_returns_404_without_changes(self):
        response = self.client.delete(
            "/activities/Unknown/signup", params={"email": "michael@mergington.edu"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Activity not found")
        self.assertEqual(activities, self.original_activities)

    def test_unknown_registration_returns_404_without_changes(self):
        response = self.client.delete(
            "/activities/Chess%20Club/signup", params={"email": "unknown@example.com"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["detail"], "Student is not signed up for this activity"
        )
        self.assertEqual(activities, self.original_activities)

    def test_last_participant_and_repeated_cancellation(self):
        url = "/activities/Art%20Club/signup"
        params = {"email": "student+art@example.com"}
        self.assertEqual(self.client.post(url, params=params).status_code, 200)
        self.assertEqual(self.client.delete(url, params=params).status_code, 200)
        self.assertEqual(self.client.get("/activities").json()["Art Club"]["participants"], [])
        self.assertEqual(self.client.delete(url, params=params).status_code, 404)
