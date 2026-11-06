from copy import deepcopy


def test_signup_adds_only_selected_registration(client, activity_data):
    email = "student+chess@example.com"
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].append(email)

    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert activity_data == expected
    assert client.get("/activities").json() == expected


def test_duplicate_signup_returns_400_without_changes(client, activity_data):
    email = "student@example.com"
    url = "/activities/Chess%20Club/signup"
    params = {"email": email}
    assert client.post(url, params=params).status_code == 200
    before = deepcopy(activity_data)

    response = client.post(url, params=params)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert activity_data == before
    assert activity_data["Chess Club"]["participants"].count(email) == 1


def test_unknown_activity_returns_404_without_changes(client, activity_data):
    before = deepcopy(activity_data)

    response = client.post(
        "/activities/Unknown/signup", params={"email": "student@example.com"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activity_data == before


def test_missing_email_returns_422_without_changes(client, activity_data):
    before = deepcopy(activity_data)

    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"] and error["type"] == "missing"
        for error in response.json()["detail"]
    )
    assert activity_data == before
