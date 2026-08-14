import allure
from helpers.api_client import ApiClient

@allure.feature("Логин пользователя")
class TestUserLogin:
    @allure.title("Вход под существующим пользователем")
    @allure.description("Проверка успешного входа с корректными данными")
    def test_login_existing_user(self, api_client, created_user):
        response = api_client.login_user(email=created_user["email"],password=created_user["password"])
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data["user"]["email"] == created_user["email"]

    @allure.title("Вход с неверным логином и паролем")
    @allure.description("Проверка ошибки при входе с неправильными данными")
    def test_login_with_wrong_credentials(self, api_client):
        response = api_client.login_user(email="wrong_email@test.ru",password="wrong_password")
        
        assert response.status_code == 401
        error_data = response.json()
        assert error_data["success"] is False
        assert "email or password are incorrect" in error_data["message"]