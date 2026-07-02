import datetime

async def test_full_booking_integration_flow(async_client):
    await async_client.post(
        "/auth/register",
        json={"email": "employee@example.com", "password": "pass", "full_name": "Сотрудник"}
    )
    login_resp = await async_client.post(
        "/auth/login",
        data={"username": "employee@example.com", "password": "pass"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    room_resp = await async_client.post(
        "/rooms/",
        json={"name": "Переговорная Alpha", "description": "Для созвонов"},
        headers=headers
    )
    room_id = room_resp.json()["id"]

    slot_resp = await async_client.post(
        "/rooms/slots",
        json={
            "room_id": room_id,
            "start_time": "10:00:00",
            "end_time": "11:00:00"
        },
        headers=headers
    )
    assert slot_resp.status_code == 201
    slot_id = slot_resp.json()["id"]

    today_str = str(datetime.date.today())
    booking_resp = await async_client.post(
        "/bookings/",
        json={
            "slot_id": slot_id,
            "date": today_str
        },
        headers=headers
    )
    assert booking_resp.status_code == 201
    booking_id = booking_resp.json()["booking_id"]

    fail_booking_resp = await async_client.post(
        "/bookings/",
        json={
            "slot_id": slot_id,
            "date": today_str
        },
        headers=headers
    )
    assert fail_booking_resp.status_code == 400
    assert "уже забронирован" in fail_booking_resp.json()["detail"]
    cancel_resp = await async_client.delete(
        f"/bookings/{booking_id}",
        headers=headers
    )
    
    assert cancel_resp.status_code == 204