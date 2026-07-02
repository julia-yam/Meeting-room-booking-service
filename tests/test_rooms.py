async def test_create_room_flow(async_client):
    await async_client.post(
        "/auth/register",
        json={
            "email": "admin@example.com",
            "password": "superpassword",
            "full_name": "Администратор"
        }
    )
    
    login_response = await async_client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "superpassword"
        }
    )
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    room_response = await async_client.post(
        "/rooms/",
        json={
            "name": "Тестовая переговорная",
            "description": "Светлая комната с доской"
        },
        headers=headers
    )
    
    assert room_response.status_code == 201
    data = room_response.json()
    assert data["name"] == "Тестовая переговорная"
    assert "id" in data