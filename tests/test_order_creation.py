import allure
from helpers.api_client import ApiClient

@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, api_client, created_user, ingredients_data):
        response = api_client.create_order(ingredients=ingredients_data["valid_ingredients"],token=created_user["token"])
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "order" in data
        assert data["order"]["number"] is not None

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api_client, ingredients_data):
        response = api_client.create_order(ingredients=ingredients_data["valid_ingredients"])

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "order" in data

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, api_client, created_user, ingredients_data):
        response = api_client.create_order(ingredients=ingredients_data["valid_ingredients"],token=created_user["token"])
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "order" in data
        assert len(data["order"]["ingredients"]) > 0

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api_client, created_user):
        response = api_client.create_order(ingredients=[],token=created_user["token"])
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {response.text}")
        
        assert response.status_code == 400
        error_data = response.json()
        assert error_data["success"] is False
        assert error_data["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, api_client, created_user, ingredients_data):
        response = api_client.create_order(ingredients=[ingredients_data["invalid_ingredient_hash"]],token=created_user["token"])
        
        assert response.status_code == 500