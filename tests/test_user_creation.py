import allure
from helpers.api_client import ApiClient

@allure.feature("Создание пользователя")
class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка успешного создания нового пользователя")
    def test_create_unique_user(self, api_client):
        email = api_client.generate_random_email()
        password = api_client.generate_random_string(8)
        name = api_client.generate_random_string(6)
        
        response = api_client.create_user(email=email, password=password, name=name)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data["user"]["email"] == email
        assert data["user"]["name"] == name

    @allure.title("Создание уже зарегистрированного пользователя")
    @allure.description("Проверка ошибки при создании существующего пользователя")
    def test_create_existing_user(self, api_client):
        email = api_client.generate_random_email()
        password = api_client.generate_random_string(8)
        name = api_client.generate_random_string(6)
        
        first_response = api_client.create_user(email=email, password=password, name=name)
        first_data = first_response.json()
        
        second_response = api_client.create_user(email=email, password=password, name=name)
        
        assert second_response.status_code == 403
        error_data = second_response.json()
        assert error_data["success"] is False
        assert error_data["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Проверка ошибки при создании пользователя без email")
    def test_create_user_without_required_field(self, api_client):
        response = api_client.create_user_without_field(missing_field='email')
        
        assert response.status_code == 403
        error_data = response.json()
        assert error_data["success"] is False
        assert error_data["message"] == "Email, password and name are required fields"