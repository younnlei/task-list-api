import pytest



def test_get_tasks_sorted_asc(client, three_tasks):
    response = client.get("/tasks?sort=asc")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False,
            "goal_id": None
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False,
            "goal_id": None
        },
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False,
            "goal_id": None
        }
    ]


def test_get_tasks_sorted_desc(client, three_tasks):
    response = client.get("/tasks?sort=desc")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False,
            "goal_id": None
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False,
            "goal_id": None
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False,
            "goal_id": None
        }
    ]
