from reporter import Reporter


def test_announcement_send(rc: Reporter) -> None:
    response = rc.announcements.send(
        {
            "title": "test_announcement_send",
            "body": "Hello",
            "send_to": "all",
            "user_activity": "all",
        }
    )

    assert response["success"] is True
    assert "recipients" in response
    assert isinstance(response["recipients"], int)
