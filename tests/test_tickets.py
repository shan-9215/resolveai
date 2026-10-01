from conftest import client


def test_create_ticket():
    response = client.post(
        "/tickets",
        json={
            "title": "WiFi Issue",
            "description": "Office WiFi is down"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "WiFi Issue"
    assert data["description"] == "Office WiFi is down"
    assert data["status"] == "open"
    assert data["priority"] == "medium"
    assert "id" in data
    assert "created_at" in data

    ticket_id = data["id"]

    get_response = client.get(f"/tickets/{ticket_id}")

    assert get_response.status_code == 200

    saved_ticket = get_response.json()

    assert saved_ticket["id"] == ticket_id
    assert saved_ticket["title"] == "WiFi Issue"
    assert saved_ticket["description"] == "Office WiFi is down"


def test_get_tickets():
    client.post(
        "/tickets",
        json={
            "title": "WiFi Issue",
            "description": "Office WiFi is down"
        }
    )

    client.post(
        "/tickets",
        json={
            "title": "Account Blocked",
            "description": "User cannot access account"
        }
    )

    response = client.get("/tickets")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "WiFi Issue"
    assert data[1]["title"] == "Account Blocked"


def test_update_ticket_status():
    create_response = client.post(
        "/tickets",
        json={
            "title": "WiFi Issue",
            "description": "Office WiFi is down"
        }
    )

    ticket_id = create_response.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={
            "status": "in_progress"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == ticket_id
    assert data["status"] == "in_progress"


def test_reject_invalid_status():
    create_response = client.post(
        "/tickets",
        json={
            "title": "WiFi Issue",
            "description": "Office WiFi is down"
        }
    )

    ticket_id = create_response.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={
            "status": "banana"
        }
    )

    assert response.status_code == 422

    get_response = client.get(f"/tickets/{ticket_id}")

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "open"


def test_delete_ticket():
    create_response = client.post(
        "/tickets",
        json={
            "title": "WiFi Issue",
            "description": "Office WiFi is down"
        }
    )

    ticket_id = create_response.json()["id"]

    delete_response = client.delete(f"/tickets/{ticket_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Ticket deleted successfully"

    get_response = client.get(f"/tickets/{ticket_id}")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Ticket not found"


def test_ticket_not_found():
    response = client.get("/tickets/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"