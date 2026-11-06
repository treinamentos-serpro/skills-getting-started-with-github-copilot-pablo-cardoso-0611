from copy import deepcopy


def test_cancel_removes_only_selected_registration_and_allows_signup_again(
    client, activity_data
):
    email = "michael@mergington.edu"
    url = "/activities/Chess%20Club/signup"
    params = {"email": email}
    activity_data["Art Club"]["participants"].append(email)
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].remove(email)

    response = client.delete(url, params=params)

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Cancelled signup for {email} for Chess Club"
    }
    assert client.get("/activities").json() == expected

    assert client.post(url, params=params).status_code == 200
    expected["Chess Club"]["participants"].append(email)
    assert client.get("/activities").json() == expected


def test_unknown_activity_returns_404_without_changes(client, activity_data):
    before = deepcopy(activity_data)

    response = client.delete(
        "/activities/Unknown/signup", params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activity_data == before


def test_unknown_registration_returns_404_without_changes(client, activity_data):
    before = deepcopy(activity_data)

    response = client.delete(
        "/activities/Chess%20Club/signup", params={"email": "unknown@example.com"}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert activity_data == before


def test_missing_email_returns_422_without_changes(client, activity_data):
    before = deepcopy(activity_data)

    response = client.delete("/activities/Chess%20Club/signup")

    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"] and error["type"] == "missing"
        for error in response.json()["detail"]
    )
    assert activity_data == before


def test_last_participant_and_repeated_cancellation(client, activity_data):
    email = "student+art@example.com"
    url = "/activities/Art%20Club/signup"
    params = {"email": email}
    before = deepcopy(activity_data)

    assert client.post(url, params=params).status_code == 200
    after_signup = client.get("/activities")
    expected = deepcopy(before)
    expected["Art Club"]["participants"].append(email)
    assert after_signup.status_code == 200
    assert after_signup.json() == expected

    response = client.delete(url, params=params)
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Cancelled signup for {email} for Art Club"
    }
    after_cancellation = client.get("/activities")
    assert after_cancellation.status_code == 200
    assert after_cancellation.json() == before

    repeated = client.delete(url, params=params)
    assert repeated.status_code == 404
    assert repeated.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert activity_data == before
