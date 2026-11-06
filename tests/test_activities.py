from copy import deepcopy


def test_root_redirects_to_static_page(client, activity_data):
    before = deepcopy(activity_data)

    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
    assert activity_data == before


def test_list_activities_returns_details_without_changes(client, activity_data):
    before = deepcopy(activity_data)

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == before
    for activity in response.json().values():
        assert set(activity) == {
            "description", "schedule", "max_participants", "participants"
        }
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
        assert all(isinstance(email, str) for email in activity["participants"])
    assert activity_data == before
