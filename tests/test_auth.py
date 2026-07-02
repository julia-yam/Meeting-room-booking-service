async def test_register_user(async_client):
    response = await async_client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "superpassword123",
            "full_name": "Тестовый Пользователь"
        }
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["message"] == "Пользователь успешно зарегистрирован"
    assert "user_id" in data